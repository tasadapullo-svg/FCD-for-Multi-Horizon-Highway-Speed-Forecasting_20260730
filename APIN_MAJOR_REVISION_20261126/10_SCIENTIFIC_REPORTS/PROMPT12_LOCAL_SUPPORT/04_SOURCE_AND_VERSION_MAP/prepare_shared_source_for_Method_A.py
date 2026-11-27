from common import *
import zipfile,io,platform,importlib.metadata
def main():
 start=now();log('prepare_shared START; original assets read-only; new protocol '+PROTOCOL_SHA)
 inputs=[];audit={};outputs=[]
 raw=Path('\\\\?\\'+V['raw_archive']);inputs.append(raw)
 with zipfile.ZipFile(raw) as z:
  cleaned=pd.read_csv(io.BytesIO(z.read('02_cleaned_records/tomtom_cleaned_records.csv.gz')),compression='gzip')
  nodes=pd.read_csv(io.BytesIO(z.read('03_nodes/nodes.csv')))
  with zipfile.ZipFile(io.BytesIO(z.read('00_raw_original/output_tomtom_data完整数据(4).zip'))) as zz:
   rawframes=[]
   for name in zz.namelist():
    if name.endswith('.csv'):
     frame=pd.read_csv(io.BytesIO(zz.read(name)));frame['source_archive_file']=name;rawframes.append(frame)
   original=pd.concat(rawframes,ignore_index=True)
 audit['raw_csv_count']=len(rawframes);audit['raw_original_rows']=len(original);audit['cleaned_rows']=len(cleaned)
 # Link by immutable return identifiers + speed/confidence; preserve duplicates via occurrence.
 ident=['pd_uuid','point_uuid','flow_uuid','current_speed','free_flow_speed','current_travel_time','free_flow_travel_time','confidence','road_closure']
 for f in [original,cleaned]:f['occurrence']=f.groupby(ident,dropna=False,sort=False).cumcount()
 mapped=original.merge(cleaned[ident+['occurrence','node_id','event_time']],on=ident+['occurrence'],how='left',validate='one_to_one',indicator=True)
 audit['raw_cleaned_identifier_match']=mapped['_merge'].value_counts().to_dict();audit['raw_cleaned_missing_mapping']=int(mapped.node_id.isna().sum())
 assert len(original)==len(cleaned) and mapped.node_id.notna().all(),'raw return mapping unresolved: do not invent timestamps'
 audit['upstream_caveat']='mapped original IDs/values to cleaned corrected event_time one-to-one; date correction program and request failure logs not recovered'
 del rawframes,original
 for c in ['event_time','capture_time','pd_create_time','flow_create_time']:cleaned[c]=pd.to_datetime(cleaned[c],errors='coerce')
 cleaned['quarter_hour']=cleaned.event_time.dt.floor('15min');cleaned['hour']=cleaned.event_time.dt.floor('h')
 quality=(np.isfinite(cleaned.current_speed)&(cleaned.current_speed>0)&(cleaned.current_speed<=130)&np.isfinite(cleaned.current_travel_time)&(cleaned.current_travel_time>0)&np.isfinite(cleaned.confidence)&cleaned.confidence.between(.8,1)&(cleaned.road_closure==0))
 for c in ['valid_record','valid_coordinates','valid_speed','valid_travel_time','valid_confidence','valid_time']:quality&=cleaned[c].fillna(False)
 quality&=cleaned.event_time.notna()&cleaned.pd_latitude.between(-90,90)&cleaned.pd_longitude.between(-180,180)
 cleaned['quality_pass']=quality
 cleaned['in_grid']=cleaned.quarter_hour.between(GRID_START,GRID_END+pd.Timedelta(minutes=45))&cleaned.node_id.isin(NODES)
 cleaned['confidence_bin']=confbin(cleaned.confidence);cleaned['ratio']=np.where(np.isfinite(cleaned.free_flow_speed)&(cleaned.free_flow_speed>0),cleaned.current_speed/cleaned.free_flow_speed,np.nan)
 cleaned['known_time']=cleaned[['event_time','capture_time','pd_create_time','flow_create_time']].max(axis=1)
 cols=['node_id','event_time','quarter_hour','hour','current_speed','free_flow_speed','current_travel_time','free_flow_travel_time','confidence','road_closure','quality_pass','in_grid','confidence_bin','ratio','known_time']
 save(cleaned[cols],DER/'observation_analysis.parquet');outputs.append(DER/'observation_analysis.parquet')
 in_grid=cleaned[cleaned.in_grid]
 slots=in_grid.groupby(['node_id','quarter_hour'],observed=True).agg(returned_rows=('quality_pass','size'),quality_rows=('quality_pass','sum')).reset_index()
 slots['slot_class']=np.where(slots.quality_rows>0,'HAS_QUALITY_RETURN','ONLY_INELIGIBLE_RETURN')
 save(slots,DER/'returned_slot_index.parquet');outputs.append(DER/'returned_slot_index.parquet')
 good=cleaned[cleaned.quality_pass];quarter=good.groupby(['node_id','quarter_hour'],observed=True).agg(speed_15min=('current_speed','mean'),freeflow_15min=('free_flow_speed','mean'),confidence_15min=('confidence','mean'),returned_quality_rows=('quality_pass','size')).reset_index();quarter['hour']=quarter.quarter_hour.dt.floor('h')
 save(quarter,DER/'quality_deduplicated_15min.parquet');outputs.append(DER/'quality_deduplicated_15min.parquet')
 orig15=BASE/'01_DATA_PIPELINE/panels/deduplicated_15min_observations.parquet';hp=BASE/'01_DATA_PIPELINE/panels/hourly_panel_all_thresholds.parquet';inputs.extend([orig15,hp]);fifteen=pd.read_parquet(orig15);hourly=pd.read_parquet(hp).sort_values('panel_row_id').reset_index(drop=True)
 assert not fifteen.duplicated(['node_id','quarter_hour']).any();assert not hourly.duplicated(['node_id','hour']).any();assert np.array_equal(hourly.panel_row_id,np.arange(len(hourly)))
 qgrid=quarter[quarter.quarter_hour.between(GRID_START,GRID_END+pd.Timedelta(minutes=45))]
 compare=qgrid.merge(fifteen,on=['node_id','quarter_hour'],validate='one_to_one',suffixes=('_new','_old'),how='outer',indicator=True)
 audit['dedup_15_comparison']={'both':int((compare['_merge']=='both').sum()),'unmatched':int((compare['_merge']!='both').sum()),'max_abs_speed_diff':float((compare.speed_15min_new-compare.speed_15min_old).abs().max())};assert audit['dedup_15_comparison']['unmatched']==0
 assert audit['dedup_15_comparison']['max_abs_speed_diff']<1e-9
 aggregate=qgrid.groupby(['node_id','hour'],observed=True).agg(quarter_count=('speed_15min','size'),hourly_freeflow=('freeflow_15min','mean'),hourly_speed_rebuilt=('speed_15min','mean'),hourly_confidence_rebuilt=('confidence_15min','mean')).reset_index()
 hourly=hourly.merge(aggregate,on=['node_id','hour'],how='left',validate='one_to_one').sort_values('panel_row_id').reset_index(drop=True)
 assert np.array_equal(hourly.valid_quarters, hourly.quarter_count.fillna(0).astype(int));audit['hour_speed_diff']=float((hourly.hourly_speed_unthresholded-hourly.hourly_speed_rebuilt).abs().max());assert audit['hour_speed_diff']<1e-9
 hourly['date']=hourly.hour.dt.normalize();hourly['hour_of_day']=hourly.hour.dt.hour;hourly['weekend']=hourly.hour.dt.dayofweek>=5
 for t in range(1,5):hourly[f'eligible_{t}']=hourly.valid_quarters>=t
 # Causal reliability on original grid; history end includes origin.
 hourly['observed']=hourly.observed_speed.notna();hourly['coverage_rebuilt']=hourly.groupby('node_id',sort=False)['observed'].transform(lambda s:s.rolling(24,min_periods=1).mean())
 def maxrun(a):
  best=run=0
  for val in a:
   run=0 if val else run+1;best=max(best,run)
  return best
 hourly['gap_rebuilt']=hourly.groupby('node_id',sort=False)['observed'].transform(lambda s:s.rolling(24,min_periods=1).apply(maxrun,raw=True))
 ages=np.empty(len(hourly),dtype=int)
 for node,x in hourly.groupby('node_id',sort=False):
  age=168
  for i,val in zip(x.index,x.observed):age=0 if val else min(age+1,168);ages[i]=age
 hourly['age_rebuilt']=ages;hourly['observable_history_speed']=hourly.groupby('node_id',sort=False).observed_speed.transform(lambda s:s.rolling(24,min_periods=1).mean())
 hourly['observable_history_confidence']=hourly.groupby('node_id',sort=False).hourly_confidence.transform(lambda s:s.rolling(24,min_periods=1).mean())
 hourly['hourly_ratio']=hourly.hourly_speed_unthresholded/hourly.hourly_freeflow
 hourly['observable_history_ratio']=hourly.groupby('node_id',sort=False).hourly_ratio.transform(lambda s:s.rolling(24,min_periods=1).mean())
 save(hourly,DER/'hourly_analysis.parquet');outputs.append(DER/'hourly_analysis.parquet')
 log('observations mapped; hourly panel reconstructed; now read manifests and recover original feature units')
 manifests=[];feature_audit=[]
 for fold in range(1,7):
  params_path=BASE/f'01_DATA_PIPELINE/folds/fold{fold}/fold_train_parameters.json';params=json.loads(params_path.read_text(encoding='utf-8'));inputs.append(params_path)
  filled=hourly.groupby('node_id',sort=False).observed_speed.ffill();filled=filled.fillna(hourly.node_id.map(params['node_medians'])).fillna(params['corridor_median'])
  volatility=filled.groupby(hourly.node_id,sort=False).transform(lambda s:s.rolling(24,min_periods=1).std(ddof=0).fillna(0)).to_numpy()
  for H in HS:
   d=BASE/f'01_DATA_PIPELINE/folds/fold{fold}/H{H}';mp=d/f'sample_manifest_fold{fold}_H{H}.parquet';m=pd.read_parquet(mp);inputs.append(mp)
   assert m.sample_id.is_unique and (m.fold==fold).all() and (m.horizon==H).all()
   origin=hourly.set_index(['node_id','hour']).panel_row_id.reindex(pd.MultiIndex.from_frame(m[['node_id','forecast_origin']])).to_numpy();assert np.isfinite(origin).all();origin=origin.astype(int);m['origin_row_id']=origin
   seq=np.load(d/'X_sequence.npy',mmap_mode='r',allow_pickle=False);assert seq.shape==(len(m),24,13)
   # Order is frozen in config. Restore stored scaled final-row features to physical units.
   restored={}
   for col,j in [('history_coverage_ratio',4),('max_gap_24h',6),('hours_since_last_observation',3),('volatility_24h',7)]:
    s=params['scaler'][col];restored[col]=seq[:,-1,j].astype(float)*s['scale']+s['mean']
   covdiff=float(np.max(np.abs(restored['history_coverage_ratio']-m.history_coverage_ratio)))
   gapdiff=float(np.max(np.abs(restored['max_gap_24h']-m.max_gap_24h)))
   feature_audit.append(dict(fold=fold,horizon=H,coverage_restore_max_diff=covdiff,gap_restore_max_diff=gapdiff,volatility_rebuild_max_diff=float(np.max(np.abs(restored['volatility_24h']-volatility[origin]))),coverage_rebuild_max_diff=float(np.max(np.abs(hourly.coverage_rebuilt.to_numpy()[origin]-m.history_coverage_ratio))),gap_rebuild_max_diff=float(np.max(np.abs(hourly.gap_rebuilt.to_numpy()[origin]-m.max_gap_24h)))))
   assert covdiff<1e-5 and gapdiff<1e-4,'feature standardization mapping not confirmed'
   m['volatility_24h_restored']=np.maximum(restored['volatility_24h'],0);m['hours_since_last_observation_restored']=np.clip(np.rint(restored['hours_since_last_observation']),0,168)
   # target_row_ids must enumerate the full future window; reconstruct each valid position.
   ids=np.array([[int(s) for s in text.split(';')] for text in m.target_row_ids],dtype=int);assert ids.shape==(len(m),H)
   sp=hourly.observed_speed.to_numpy()[ids];ff=hourly.hourly_freeflow.to_numpy()[ids];valid=np.isfinite(sp);cnt=valid.sum(axis=1)
   assert np.array_equal(cnt,m.target_observed_count.to_numpy());target=np.nansum(sp,axis=1)/cnt;assert np.max(np.abs(target-m.target.to_numpy()))<1e-8
   m['target_count_rebuilt']=cnt;m['target_freeflow']=np.where((~valid|np.isfinite(ff)).all(axis=1),np.nansum(np.where(valid,ff,np.nan),axis=1)/cnt,np.nan)
   m['target_ratio']=m.target/m.target_freeflow;m['traffic_regime']=regime(m.target_ratio)
   m['h6_group']=np.where(H!=6,'NA',np.where(cnt==6,'COMPLETE_6_OF_6',np.where(cnt==5,'PARTIAL_5_OF_6','INVALID_TARGET')))
   m['missing_position']=np.where(H==6,np.sum((~valid)*np.arange(1,H+1),axis=1),0)
   m['cov_bin']=covbin(m.history_coverage_ratio);m['gap_bin']=gapbin(m.max_gap_24h);m['age_bin']=agebin(m.hours_since_last_observation_restored)
   # Training-sample quantiles, no test-error-driven choices; cutpoint duplicates merged.
   trainvals=m.loc[m.split=='train','volatility_24h_restored'];cuts=np.unique(trainvals.quantile([1/3,2/3]).to_numpy());m['vol_bin']=pd.cut(m.volatility_24h_restored,[-np.inf,*cuts,np.inf],labels=False,right=True).map(lambda k:f'V{k+1}')
   feature_audit[-1]['training_volatility_cutpoints_kmh']=';'.join(map(str,cuts))
   # Conservative lagged free-flow baseline based solely on earlier known returns.
   outff=np.full(len(m),np.nan);method=np.full(len(m),'MISSING',dtype=object);knownage=np.full(len(m),np.nan)
   for node,idx in m.groupby('node_id',sort=False).groups.items():
    hist=cleaned[(cleaned.node_id==node)&np.isfinite(cleaned.free_flow_speed)&(cleaned.free_flow_speed>0)].copy()
    hist['availability_bound']=pd.concat([hist.known_time,hist.event_time+pd.Timedelta(hours=1)],axis=1).max(axis=1)
    hist=hist.sort_values(['availability_bound','event_time']).drop_duplicates('availability_bound',keep='last')
    origins=m.loc[idx,'forecast_origin'].to_numpy(dtype='datetime64[ns]');bounds=hist.availability_bound.to_numpy(dtype='datetime64[ns]');pos=np.searchsorted(bounds,origins,side='right')-1;has=pos>=0;idxarr=np.asarray(idx)
    if has.any():outff[idxarr[has]]=hist.free_flow_speed.to_numpy()[pos[has]];method[idxarr[has]]='LAGGED_KNOWN_RETURN';knownage[idxarr[has]]=(origins[has]-hist.event_time.to_numpy(dtype='datetime64[ns]')[pos[has]])/np.timedelta64(1,'h')
    train_start,train_end=FOLDS[fold]['train'];histtrain=hist[(hist.event_time>=train_start)&(hist.event_time<train_end)&(hist.availability_bound<=train_end)]
    fallback=np.median(histtrain.free_flow_speed) if len(histtrain) else np.nan
    no=idxarr[~has];allowed=m.loc[no,'forecast_origin']>=train_end
    if np.isfinite(fallback):outff[no[allowed]]=fallback;method[no[allowed]]='FOLD_TRAIN_NODE_MEDIAN'
   corridor=cleaned[(cleaned.event_time>=FOLDS[fold]['train'][0])&(cleaned.event_time<FOLDS[fold]['train'][1])&(cleaned.known_time<=FOLDS[fold]['train'][1])&np.isfinite(cleaned.free_flow_speed)&(cleaned.free_flow_speed>0)].free_flow_speed.median()
   missing=~np.isfinite(outff)&(m.forecast_origin>=FOLDS[fold]['train'][1]).to_numpy();outff[missing]=corridor;method[missing]='FOLD_TRAIN_CORRIDOR_MEDIAN'
   m['freeflow_baseline_pred']=outff;m['freeflow_baseline_source']=method;m['freeflow_return_age_hours']=knownage
   m['analysis_date']=m.forecast_origin.dt.normalize();manifests.append(m)
  log(f'fold {fold} manifests/features/causal freeflow prepared')
 manifests=pd.concat(manifests,ignore_index=True);save(manifests,DER/'target_completeness_and_reliability.parquet');outputs.append(DER/'target_completeness_and_reliability.parquet');save(pd.DataFrame(feature_audit),DER/'feature_recovery_audit.csv');outputs.append(DER/'feature_recovery_audit.csv')
 del cleaned,quarter,compare
 aligned=[];seedmetrics=[];alignment=[]
 for fold in range(1,7):
  for H in HS:
   reference=manifests[(manifests.fold==fold)&(manifests.horizon==H)&(manifests.split=='test')].sort_values('sample_id')
   for model in MODELS:
    frames=[]
    for seed in (SEEDS if model in ['XGBoost','GRU'] else [42]):
     p=BASE/f'03_FORMAL_PREDICTIONS/predictions/{model}_F{fold}_H{H}_S{seed}.parquet';f=pd.read_parquet(p).sort_values('sample_id').reset_index(drop=True);inputs.append(p)
     keys=['sample_id','node_id','forecast_origin','fold','horizon'];assert f[keys].reset_index(drop=True).equals(reference[keys].reset_index(drop=True));assert np.array_equal(f.y_true,reference.target);assert np.isfinite(f.y_pred).all() and f.sample_id.is_unique;assert (f.model==model).all() and (f.seed==seed).all()
     seedmetrics.append(dict(model=model,fold=fold,horizon=H,seed=seed,**metrics(f)));frames.append(f.y_pred.to_numpy())
    arr=np.stack(frames);df=reference[['fold','horizon','sample_id','node_id','forecast_origin','spatial_block','target']].copy().reset_index(drop=True).rename(columns={'target':'y_true'});df['model']=model;df['y_pred']=arr.mean(axis=0);df['signed_error']=df.y_pred-df.y_true;df['absolute_error']=df.signed_error.abs();df['squared_error']=df.signed_error**2
    aligned.append(df);alignment.append(dict(fold=fold,horizon=H,model=model,seeds=';'.join(map(str,SEEDS if len(frames)==3 else [42])),n=len(df),key_match=True,truth_match=True,predictions_finite=True))
  log(f'fold {fold} predictions aligned, seeds explicitly identified')
 aligned=pd.concat(aligned,ignore_index=True);save(aligned,DER/'aligned_predictions.parquet');outputs.append(DER/'aligned_predictions.parquet');save(pd.DataFrame(seedmetrics),DER/'seed_metrics.csv');outputs.append(DER/'seed_metrics.csv');save(pd.DataFrame(alignment),DER/'prediction_alignment_checks.csv');outputs.append(DER/'prediction_alignment_checks.csv')
 paired=aligned.pivot(index=['fold','horizon','sample_id','node_id','forecast_origin','spatial_block','y_true'],columns='model',values='absolute_error').reset_index();paired.columns.name=None
 assert paired[MODELS].notna().all().all()
 for a,b in PAIRS+[('XGBoost','Persistence'),('Persistence','SeasonalHA')]:paired[a+'_minus_'+b]=paired[a]-paired[b]
 save(paired,DER/'paired_loss.parquet');outputs.append(DER/'paired_loss.parquet')
 reliability=aligned.merge(manifests[manifests.split=='test'].drop(columns=['split','target','spatial_block']),on=['fold','horizon','sample_id','node_id','forecast_origin'],validate='many_to_one')
 save(reliability,DER/'reliability_conditioned_predictions.parquet');outputs.append(DER/'reliability_conditioned_predictions.parquet')
 jwrite(DER/'shared_preparation_audit.json',audit)
 env={}
 for name in ['numpy','pandas','pyarrow','scipy','openpyxl','matplotlib']:
  try:env[name]=importlib.metadata.version(name)
  except importlib.metadata.PackageNotFoundError:env[name]='NOT_INSTALLED_OR_METADATA_UNAVAILABLE'
 jwrite(LOG/'environment.json',{'python':sys.version,'platform':platform.platform(),'packages':env,'protocol_sha256':PROTOCOL_SHA,'started_at':start,'ended_at':now(),'input_paths':[norm(p) for p in inputs]})
 stamp('prepare_shared',inputs,outputs,{'audit':audit,'aligned_rows':len(aligned),'paired_rows':len(paired),'manifests_rows':len(manifests)});log(f'prepare_shared DONE paired={len(paired)}, prediction_rows={len(aligned)}')
if __name__=='__main__':
 if '--resume-receipt-only' in sys.argv:
  outputs=[DER/n for n in ['observation_analysis.parquet','returned_slot_index.parquet','quality_deduplicated_15min.parquet','hourly_analysis.parquet','target_completeness_and_reliability.parquet','aligned_predictions.parquet','paired_loss.parquet','reliability_conditioned_predictions.parquet','feature_recovery_audit.csv','seed_metrics.csv','prediction_alignment_checks.csv']]
  assert all(p.exists() for p in outputs)
  env={}
  for name in ['numpy','pandas','pyarrow','scipy','openpyxl','matplotlib']:
   try:env[name]=importlib.metadata.version(name)
   except importlib.metadata.PackageNotFoundError:env[name]='NOT_INSTALLED_OR_METADATA_UNAVAILABLE'
  jwrite(LOG/'environment.json',{'python':sys.version,'platform':platform.platform(),'packages':env,'protocol_sha256':PROTOCOL_SHA,'receipt_recovered_at':now()})
  stamp('prepare_shared',[BASE],outputs,{'resume':'all data outputs were saved before environment metadata lookup error; no computation repeated','audit':json.loads((DER/'shared_preparation_audit.json').read_text(encoding='utf-8'))});log('prepare_shared receipt recovered without recalculation')
 else:main()
