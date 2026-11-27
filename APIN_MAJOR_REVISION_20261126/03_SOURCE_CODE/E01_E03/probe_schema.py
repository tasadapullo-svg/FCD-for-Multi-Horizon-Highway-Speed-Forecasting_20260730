from common import *
import zipfile,io
log('schema probe after protocol freeze')
p=BASE/'01_DATA_PIPELINE/folds/fold1/H1/sample_manifest_fold1_H1.parquet';m=pd.read_parquet(p)
print('MANIFEST columns',m.columns.tolist(),'row_id_formats',m.history_row_ids.iloc[0],m.target_row_ids.iloc[0])
folder=p.parent
for file in folder.iterdir():
 print('FILE',file.name,file.stat().st_size)
 if file.suffix=='.npz':
  with np.load(file,allow_pickle=False) as z:
   print('NPZ KEYS',z.files)
   for key in z.files:
    arr=z[key];print(key,arr.shape,arr.dtype)
for name in ['fold_level_model_metrics.csv','model_horizon_summary.csv']:
 df=pd.read_csv(BASE/'04_METRICS'/name);print(name,df.columns.tolist());print(df.head(2).to_string(index=False))
raw=Path('\\\\?\\'+V['raw_archive'])
with zipfile.ZipFile(raw) as z:
 c=pd.read_csv(io.BytesIO(z.read('02_cleaned_records/tomtom_cleaned_records.csv.gz')),compression='gzip')
 print('CLEANED FLAG TYPES',{s:str(c[s].dtype) for s in c if s.startswith('valid')});print('ID uniqueness',{s:bool(c[s].is_unique) for s in ['pd_uuid','flow_uuid']});print('time parse', {s:float(pd.to_datetime(c[s],errors='coerce').notna().mean()) for s in ['event_time','capture_time','pd_create_time','flow_create_time']})
 for s in ['valid_record','valid_coordinates','valid_speed','valid_travel_time','valid_confidence','valid_time']:print('FLAG',s,c[s].value_counts(dropna=False).to_dict())
