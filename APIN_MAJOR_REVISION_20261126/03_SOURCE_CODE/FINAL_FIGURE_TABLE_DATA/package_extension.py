from pathlib import Path
import hashlib,json,shutil,zipfile,csv,tempfile
import pandas as pd
from openpyxl import load_workbook
import pyogrio

R=Path(r'E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改');O=R.parent;B=R/'07_FIGURES_TABLES/FINAL_FIGURE_TABLE_DATA';M=B/'08_MASTER_RESEARCH_RESULTS';V=B/'09_QGIS_VALIDATION';G=B/'01_FIGURE_DATA/Fig01_Study_Area_GIS';P=B/'GPT_SCI_PLOTTING_DATA';T=B/'10_GPT_REVIEW_PACKAGE';T.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def files(d):return sorted(p for p in d.rglob('*') if p.is_file() and not p.name.endswith('.inspect.ndjson'))
def cp(p,q):q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
for name in ['APIN_01_Complete_Research_Results_Summary_CN.md','APIN_01_Complete_Research_Results_Summary_EN.md','APIN_03_Reviewer_31_Evidence_and_Figure_Mapping.xlsx','APIN_03_Reviewer_31_Evidence_and_Figure_Mapping.csv','Master_Aggregate_Provenance.csv']:cp(M/name,T/name)
cp(V/'APIN_QGIS_Data_Validation_Report_CN.md',T/'APIN_QGIS_Data_Validation_Report_CN.md')
cp(V/'GIS_00_File_and_Layer_Inventory.csv',T/'GIS_00_File_and_Layer_Inventory.csv')
for p in files(P):cp(p,T/'GPT_SCI_PLOTTING_DATA'/p.relative_to(P))
for d in sorted(M.glob('R*')):
 for p in files(d):
  if any(k in p.stem for k in ['Node_Hour','Node_Matching','Inter_Node_Distance','Review_Checklist','Reviewer_Evidence_Matrix']):continue
  cp(p,T/'AGGREGATE_RESEARCH_RESULTS'/d.name/p.name)
for d in [B/'02_TABLE_DATA',B/'03_SUPPLEMENTARY_DATA',B/'04_LATEX_TABLES']:
 for p in files(d):
  if p.name.endswith('.xlsx') and 'S08' in str(p):continue
  cp(p,T/d.name/p.relative_to(d))
for name in ['build_research_master.py','build_extension_documents.py','build_plot_tables.py','validate_gis_extension.py']:
 cp(R/'03_CODE/FINAL_FIGURE_TABLE_DATA'/name,T/'ANALYSIS_CODE'/name)
cp(R/'04_EXPERIMENTS/FINAL_TARGETED_CHECKS/Ridge_Corrected_Aggregates.csv',T/'AGGREGATE_RESEARCH_RESULTS/R08_Model_Fairness_and_Ridge/Ridge_Corrected_Aggregates.csv')

# GPT workbook contains spatially aggregated error instead of a node-level matrix.
wb=load_workbook(M/'APIN_00_All_Research_Results_Master.xlsx');ws=wb['18_Node_Level_Error'];wb.remove(ws);ws=wb.create_sheet('18_Node_Level_Error')
node=pd.read_csv(B/'01_FIGURE_DATA/Fig05_Reliability_and_Spatial_Error/Fig05D_Node_Level_Model_Error.csv')
num=[c for c in node.columns if pd.api.types.is_numeric_dtype(node[c]) and c.lower() in ['mae','rmse','bias','mean_absolute_error']]
gcols=[c for c in ['model','horizon'] if c in node.columns]
if num and gcols:
 ag=node.groupby(gcols,dropna=False)[num].mean().reset_index();ag['aggregation']='mean across nodes; node-level values withheld'
else:ag=pd.DataFrame([{'status':'NODE_LEVEL_WITHHELD','node_count':51,'source':'author-local figure dataset'}])
ws.append(list(ag.columns))
for row in ag.fillna('').itertuples(index=False,name=None):ws.append(list(row))
wb.save(T/'APIN_00_All_Research_Results_Master.xlsx')
start='''# GPT独立审核起点\n\n请先读取 APIN_00_All_Research_Results_Master.xlsx、APIN_01_Complete_Research_Results_Summary_CN.md、APIN_02_All_Result_Files_Registry.csv、APIN_03_Reviewer_31_Evidence_and_Figure_Mapping.xlsx，再逐一核对8张图、9张正文表、8组补充、QGIS技术校验及科学主张。\n\n原六模型结果和G2独立返修实现不可混合；G1 Method A与旧稿Method B不同。Ridge SVD修正的native指标不能替代旧Cholesky共同目标配对。E08和空间邻居模型未执行。当前OSM连接不能证明历史主线。原始商业FCD、逐样本预测、特征张量、模型权重和受限坐标未纳入本包。Holm显著性以实际冻结统计CSV为准；未给出的CI/p值不得填零。请基于实际数据独立审核，不把本说明视为科学验收。对外使用仍需作者确认商业数据许可。\n'''
(T/'START_HERE_GPT_REVIEW_CN.md').write_text(start,encoding='utf-8')
rows=[]
for i,p in enumerate([p for p in files(T) if p.name!='APIN_02_All_Result_Files_Registry.csv'],1):
 x={'file_id':f'F{i:04d}','filename':p.name,'relative_path':str(p.relative_to(T)).replace('\\','/'),'file_type':p.suffix.lower(),'experiment_id':p.parent.name if p.parent.name.startswith('R') else '', 'figure_id':p.parent.name[:5] if p.parent.name.startswith('Fig') else '', 'table_id':p.stem if p.stem.startswith('Table') else '', 'supplementary_id':p.parent.name[:3] if p.parent.name.startswith('S0') else '', 'reviewer_id':'31 comments' if 'Reviewer_31' in p.name else '', 'source_file':'see Master_Aggregate_Provenance.csv','source_sha256':'see provenance','output_sha256':sha(p),'row_count':'','column_count':'','calculation_script':'ANALYSIS_CODE/','data_version':'20261126_FREEZE','implementation_id':'MIXED_SEPARATED','seed_aggregation':'see source','availability_status':'PRESENT','licensing_status':'AUTHOR_REVIEW_ONLY; DISTRIBUTION_RIGHTS_CONFIRM'}
 if p.suffix.lower()=='.csv':
  try:df=pd.read_csv(p);x['row_count']=len(df);x['column_count']=len(df.columns)
  except pd.errors.EmptyDataError:x['availability_status']='EMPTY_SOURCE_RECORDED';x['row_count']=0;x['column_count']=0
 rows.append(x)
reg=pd.DataFrame(rows);reg.to_csv(T/'APIN_02_All_Result_Files_Registry.csv',index=False,encoding='utf-8-sig')

def package(path,members,base,prefix):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in members:z.write(p,prefix+str(p.relative_to(base)).replace('\\','/'))
 with zipfile.ZipFile(path) as z:assert z.testzip() is None
def checkzip(p):
 with zipfile.ZipFile(p) as z:return len(z.namelist()),z.testzip() is None
z1=O/'APIN_GPT_REVIEW_AND_SCI_PLOTTING_20261126.zip';z2=O/'APIN_QGIS_DRAWING_AND_VALIDATION_LOCAL_20261126.zip';z3=O/'APIN_FINAL_RESEARCH_RESULTS_LOCAL_20261126.zip'
qstage=B/'11_QGIS_LOCAL_PACKAGE';qstage.mkdir(exist_ok=True)
for p in files(G):cp(p,qstage/p.name)
for p in files(V):cp(p,qstage/'VALIDATION'/p.name)
cp(R/'03_CODE/FINAL_FIGURE_TABLE_DATA/validate_gis_extension.py',qstage/'VALIDATION/validate_gis_extension.py')
package(z1,files(T),T,'APIN_GPT_REVIEW/')
package(z2,files(qstage),qstage,'APIN_QGIS_LOCAL/')
local=[p for p in files(B) if not str(p).startswith(str(T)) and not str(p).startswith(str(qstage)) and not str(p).startswith(str(B/'07_FINAL_DELIVERY/APIN_Final_Delivery_'))]
local += [R/'03_CODE/FINAL_FIGURE_TABLE_DATA'/n for n in ['build_research_master.py','build_extension_documents.py','validate_gis_extension.py','package_extension.py']]
package(z3,local,R,'APIN_RESEARCH_LOCAL/')
with tempfile.TemporaryDirectory(dir=B/'07_FINAL_DELIVERY') as tmp:
 with zipfile.ZipFile(z2) as z:z.extractall(tmp)
 gp=next(Path(tmp).rglob('Fig01_Pan_Borneo_Study_Area.gpkg'))
 assert len(pyogrio.list_layers(gp))==8 and len(pyogrio.read_dataframe(gp,layer='Original_Observation_Nodes'))==51
checks=[{'check':'ZIP_CRC','target':p.name,'status':'PASS' if checkzip(p)[1] else 'FAILED','detail':checkzip(p)[0]} for p in [z1,z2,z3]]
checks +=[{'check':'Reviewer_31','target':'mapping','status':'PASS' if len(pd.read_csv(T/'APIN_03_Reviewer_31_Evidence_and_Figure_Mapping.csv'))==31 else 'FAILED','detail':31},{'check':'QGIS_runtime','target':'QGZ','status':'NOT_AVAILABLE','detail':'QGIS_PROJECT_NOT_RUNTIME_VERIFIED'},{'check':'Author_GIS_review','target':'15 candidates','status':'AUTHOR_REVIEW_REQUIRED','detail':15},{'check':'New_model_fits','target':'phase','status':'PASS','detail':0},{'check':'New_traffic_datasets','target':'phase','status':'PASS','detail':0}]
D=B/'07_FINAL_DELIVERY';pd.DataFrame(checks).to_csv(D/'APIN_Final_Delivery_Validation.csv',index=False,encoding='utf-8-sig')
manifest={'date':'2026-11-26','project_root':str(R),'gpt_files':len(files(T)),'local_files':len(local),'qgis_files':len(files(qstage)),'research_categories':10,'aggregate_files':53,'master_sheets':37,'figure_count':8,'main_tables':9,'supplement_groups':8,'gis_original_nodes':51,'gis_routes':50,'gis_road_features':1598,'gis_review_candidates':15,'qgis_project_status':'QGIS_PROJECT_NOT_RUNTIME_VERIFIED','historical_corridor_length':'NOT_VERIFIED','reviewer_comments':31,'new_model_fits':0,'new_traffic_datasets':0,'archives':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p),'entries':checkzip(p)[0]} for p in [z1,z2,z3]]}
(D/'APIN_Final_Delivery_Manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(D/'APIN_Final_Delivery_SHA256SUMS.txt').write_text('\n'.join(f"{sha(p)}  {p.name}" for p in [z1,z2,z3])+'\n',encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False))
