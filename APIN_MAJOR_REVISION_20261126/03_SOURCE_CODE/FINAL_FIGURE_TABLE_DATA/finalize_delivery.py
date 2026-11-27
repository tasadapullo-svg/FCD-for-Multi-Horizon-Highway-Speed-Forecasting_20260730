from pathlib import Path
import csv, hashlib, json, re, sys, zipfile
import pandas as pd
import pyogrio

R=Path(r'E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改')
O=R.parent
B=R/'07_FIGURES_TABLES/FINAL_FIGURE_TABLE_DATA'
FIG=B/'01_FIGURE_DATA'; TAB=B/'02_TABLE_DATA'; SUP=B/'03_SUPPLEMENTARY_DATA'; META=B/'05_SOURCE_AND_DATA_DICTIONARY'; MAPPING=B/'06_REVIEWER_MAPPING'; DEL=B/'07_FINAL_DELIVERY'
G=FIG/'Fig01_Study_Area_GIS'
DEL.mkdir(exist_ok=True);MAPPING.mkdir(exist_ok=True)
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def rel(p):return str(p.relative_to(R)).replace('\\','/')
def save(df,p):df.to_csv(p,index=False,encoding='utf-8-sig')
def sheet(name,df,title=None):
 return {'name':name[:31],'title':title or name,'source':'frozen accepted evidence; see source index','headers':list(df.columns),'rows':df.fillna('').values.tolist()}

# Reviewer mapping follows the frozen 31-row matrix; no new scientific adjudication.
reviews=pd.read_csv(R/'04_EXPERIMENTS/FINAL_NONTRAINING_CLOSURE/FINAL_Reviewer_Evidence_Matrix_v2.csv').fillna('')
assert len(reviews)==31 and reviews.comment_id.nunique()==31
def chart_for(row):
 t=' '.join(str(row[k]) for k in ['scientific_issue','manuscript_section','specific_manuscript_change']).lower()
 out=[]
 for tokens,fig,tables in [
  (['signific','wilcoxon','holm','bootstrap','statistic','inferen','block'],['Fig06'],['Table07']),
  (['missing','coverage','eligib','sample','attrition','sparse'],['Fig02'],['Table01','Table05']),
  (['target','horizon','forecast window'],['Fig03'],['Table03']),
  (['feature','leakage','split','protocol','causal'],['Fig03','Fig08'],['Table02','Table04']),
  (['model','baseline','prediction','performance'],['Fig04'],['Table07']),
  (['reliab','spatial','node','road','corridor','map','gis'],['Fig01','Fig05'],['Table01']),
  (['regime','free-flow','free flow','traffic'],['Fig07'],['Table07']),
  (['sensitivity','ablation','fairness','tuning','ridge'],['Fig08'],['Table08']),
  (['runtime','efficien','latency','cost'],['Fig08'],['Table09'])]:
  if any(k in t for k in tokens):out.extend(fig+tables)
 return ', '.join(dict.fromkeys(out))
mapped=pd.DataFrame([{'reviewer_id':r.reviewer_id,'comment_id':r.comment_id,'scientific_issue':r.scientific_issue,'manuscript_section':r.manuscript_section,'related_figure_table':chart_for(r),'actual_final_evidence':r.actual_final_evidence,'final_evidence_paths':r.final_evidence_paths,'evidence_readiness':r.evidence_readiness,'final_adoption_status':r.final_adoption_status,'remaining_author_action':r.remaining_author_action,'mapping_note':'Proposed display mapping; original review/evidence state preserved'} for _,r in reviews.iterrows()])
save(mapped,MAPPING/'Final_31_Reviewer_Figure_Table_Mapping.csv')

figrows=[];panels=[];tables=[];supps=[]
for d in sorted(FIG.iterdir()):
 if not d.is_dir():continue
 i=int(d.name[3:5]); cs=sorted(d.glob('Fig*.csv'))
 figrows.append({'figure':f'Fig{i:02d}','folder':rel(d),'panel_csv_count':len(cs),'xlsx_count':len(list(d.glob('*.xlsx'))),'status':'DATA_PREPARED_AUTHOR_DRAWING_PENDING','caveat':'Historical road length unverified; author review 15 nodes' if i==1 else 'Accepted aggregate sources; see README'})
 for p in cs:
  try:
   x=pd.read_csv(p);panels.append({'figure':f'Fig{i:02d}','file':rel(p),'rows':len(x),'columns':len(x.columns),'sha256':sha(p)})
  except Exception as e:raise RuntimeError(f'CSV unreadable: {p}: {e}')
for d in sorted(TAB.iterdir()):
 if d.is_dir():
  for p in d.glob('Table*.csv'):
   x=pd.read_csv(p);tables.append({'table':p.stem,'file':rel(p),'rows':len(x),'columns':len(x.columns),'xlsx':len(list(d.glob('*.xlsx'))),'tex':len(list(d.glob('*.tex'))),'sha256':sha(p)})
for d in sorted(SUP.iterdir()):
 if d.is_dir():supps.append({'group':d.name,'folder':rel(d),'csv_count':len(list(d.glob('*.csv'))),'xlsx_count':len(list(d.glob('*.xlsx')))})

layers=[]
for gpkg in [G/'Fig01_Pan_Borneo_Study_Area.gpkg',G/'Fig01_Inter_Node_Routes.gpkg']:
 for name,typ in pyogrio.list_layers(gpkg):
  f=pyogrio.read_dataframe(gpkg,layer=name)
  assert f.crs.to_epsg()==4326 and f.geometry.notna().all() and f.geometry.is_valid.all()
  layers.append({'file':rel(gpkg),'layer':name,'feature_count':len(f),'geometry_type':typ,'crs':'EPSG:4326','valid':True,'fields':', '.join(f.columns.drop('geometry')),'sha256':sha(gpkg)})
assert next(x['feature_count'] for x in layers if x['layer']=='Original_Observation_Nodes')==51
assert next(x['feature_count'] for x in layers if x['layer']=='GIS_Review_Candidates_15')==15
for stem in ['Fig01_Original_Observation_Nodes','Fig01_Matched_Road_Nodes_Current_OSM','Fig01_Existing_Road_Network_Current_OSM']:
 p=G/(stem+'.shp')
 if p.exists():
  assert all(p.with_suffix(s).exists() for s in ['.shp','.shx','.dbf','.prj','.cpg'])
  assert len(pyogrio.read_dataframe(p))>0

save(pd.DataFrame(figrows),META/'Final_Figure_Registry.csv')
save(pd.DataFrame(panels),META/'Final_Panel_Registry.csv')
save(pd.DataFrame(tables),META/'Final_Table_Registry.csv')
save(pd.DataFrame(supps),META/'Final_Supplement_Registry.csv')
save(pd.DataFrame(layers),DEL/'Final_GIS_Layer_Validation.csv')
consistency=pd.DataFrame([
 {'check':'8 planned figures','observed':len(figrows),'expected':8,'status':'PASS' if len(figrows)==8 else 'FAIL'},
 {'check':'9 main tables','observed':len(tables),'expected':9,'status':'PASS' if len(tables)==9 else 'FAIL'},
 {'check':'8 supplement groups','observed':len(supps),'expected':8,'status':'PASS' if len(supps)==8 else 'FAIL'},
 {'check':'31 reviewer comments','observed':len(mapped),'expected':31,'status':'PASS' if len(mapped)==31 else 'FAIL'},
 {'check':'51 original GIS nodes','observed':51,'expected':51,'status':'PASS'},
 {'check':'15 GIS review candidates','observed':15,'expected':15,'status':'PASS'},
 {'check':'QGIS project (.qgz)','observed':0,'expected':'QGIS unavailable; GPKG plus loading instructions','status':'DOCUMENTED_UNAVAILABLE'},
 {'check':'E08 external training','observed':0,'expected':'target asset not found','status':'DOCUMENTED_NOT_RUN'},
])
save(consistency,DEL/'Final_Numerical_Consistency_Checks.csv')
sections=mapped.groupby('manuscript_section',dropna=False).agg(review_comments=('comment_id','count'),comment_ids=('comment_id',lambda s:', '.join(s))).reset_index()
save(sections,MAPPING/'Final_Manuscript_Section_Map.csv')
missing=pd.DataFrame([
 {'item':'QGZ project','status':'NOT_GENERATED','reason':'QGIS/PyQGIS unavailable; validated GPKG and loading instructions provided','author_action':'Open GPKG in QGIS and save project locally'},
 {'item':'Historical 130 km highway mainline','status':'UNVERIFIED','reason':'Current OSM path and straight-line length are distinct estimands','author_action':'Review 15 nodes and verify historical corridor before numeric distance claim'},
 {'item':'E08 JB external validation','status':'NOT_RUN_TARGET_ASSET_NOT_FOUND','reason':'Approved 451,008-row historical panel not available in registered path','author_action':'Do not claim external validation'},
 {'item':'Ridge SVD paired common-origin contrasts','status':'NOT_RECOMPUTED','reason':'SVD corrected native metrics available; old Cholesky paired contrasts are not transferable','author_action':'Avoid corrected Ridge paired superiority claim'},
 {'item':'Original baseline training source/configuration','status':'NOT_RECOVERED','reason':'Frozen predictions and accepted original outcomes available; implementation details limited','author_action':'State reproducibility limitation'},
 {'item':'GIS and aggregate data distribution rights','status':'AUTHOR_CONFIRMATION_REQUIRED','reason':'Commercial FCD license not supplied','author_action':'Keep author-local ZIP local; review ZIP contains only aggregates, still check license before external sharing'},
])
save(missing,DEL/'Final_Missing_or_Unavailable.csv')

payload={'workbooks':[
 {'file':'Final_31_Reviewer_Figure_Table_Mapping.xlsx','dir':rel(MAPPING),'sheets':[sheet('Reviewer mapping',mapped),sheet('Section map',sections)]},
 {'file':'APIN_Final_All_Figures_and_Tables_Master.xlsx','dir':rel(B),'sheets':[sheet('Overview',pd.DataFrame([{'planned_figures':8,'tables':9,'supplement_groups':8,'review_comments':31,'gis_nodes':51,'gis_review_nodes':15,'E08_status':'NOT_RUN_TARGET_ASSET_NOT_FOUND'}])),sheet('Figure registry',pd.DataFrame(figrows)),sheet('Panel registry',pd.DataFrame(panels)),sheet('Table registry',pd.DataFrame(tables)),sheet('Supplement registry',pd.DataFrame(supps)),sheet('GIS layers',pd.DataFrame(layers)),sheet('Reviewer mapping',mapped),sheet('Section map',sections),sheet('Numerical changes',consistency),sheet('Missing actions',missing)]}
]}
(R/'03_CODE/FINAL_FIGURE_TABLE_DATA/final_workbook_payload.json').write_text(json.dumps(payload,ensure_ascii=False,default=str),encoding='utf-8')
print(json.dumps({'panels':len(panels),'tables':len(tables),'supplements':len(supps),'gis_layers':len(layers),'review_comments':len(mapped),'workbook_payload':rel(R/'03_CODE/FINAL_FIGURE_TABLE_DATA/final_workbook_payload.json')},ensure_ascii=False))
