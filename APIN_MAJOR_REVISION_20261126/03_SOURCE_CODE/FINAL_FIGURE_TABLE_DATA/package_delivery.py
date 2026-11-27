from pathlib import Path
import csv, hashlib, json, zipfile
import pandas as pd
import pyogrio

R=Path(r'E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改')
O=R.parent;B=R/'07_FIGURES_TABLES/FINAL_FIGURE_TABLE_DATA';G=B/'01_FIGURE_DATA/Fig01_Study_Area_GIS';D=B/'07_FINAL_DELIVERY'
def rel(p):return str(p.relative_to(R)).replace('\\','/')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def files(folder):return sorted(p for p in folder.rglob('*') if p.is_file() and not p.name.endswith('.inspect.ndjson'))

fig=pd.read_csv(B/'05_SOURCE_AND_DATA_DICTIONARY/Final_Figure_Registry.csv')
panels=pd.read_csv(B/'05_SOURCE_AND_DATA_DICTIONARY/Final_Panel_Registry.csv')
tables=pd.read_csv(B/'05_SOURCE_AND_DATA_DICTIONARY/Final_Table_Registry.csv')
layers=pd.read_csv(D/'Final_GIS_Layer_Validation.csv')
mapping=pd.read_csv(B/'06_REVIEWER_MAPPING/Final_31_Reviewer_Figure_Table_Mapping.csv')
assert len(fig)==8 and len(tables)==9 and len(mapping)==31
workbooks=list(B.rglob('*.xlsx'))
for p in workbooks:
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None and 'xl/workbook.xml' in z.namelist(),p
for p in B.rglob('*.csv'):
 pd.read_csv(p)
for p in B.rglob('*.gpkg'):
 for name,typ in pyogrio.list_layers(p):
  df=pyogrio.read_dataframe(p,layer=name)
  assert df.crs.to_epsg()==4326 and df.geometry.notna().all() and df.geometry.is_valid.all(),(p,name)

source_files=[
 '04_EXPERIMENTS/FINAL_NONTRAINING_CLOSURE/FINAL_Reviewer_Evidence_Matrix_v2.csv',
 '04_EXPERIMENTS/FINAL_NONTRAINING_CLOSURE/Final_Unified_Inference_Benchmark.csv',
 '04_EXPERIMENTS/G2_E04_E07_ACCEPTANCE/G2_02_Experiment_Run_Registry.csv',
 '04_EXPERIMENTS/E03_STATISTICAL_INFERENCE/E03_03_Original_vs_Recomputed_Table7.csv',
 '07_FIGURES_TABLES/FINAL_FIGURE_TABLE_DATA/05_SOURCE_AND_DATA_DICTIONARY/Final_Figure_Table_Data_Provenance.csv',
]
source=[{'path':x,'exists':(R/x).exists(),'sha256':sha(R/x) if (R/x).exists() else None} for x in source_files]
inventory=[{'path':rel(p),'size_bytes':p.stat().st_size,'sha256':sha(p),'kind':p.suffix.lower()} for p in files(B) if p.name not in {'Final_Figure_Table_Execution_Manifest.json','Final_Delivery_ZIP_Checks.json'}]
manifest={'project_root':str(R),'output_root':str(O),'date_local':'2026-11-26','historical_evidence_reused':True,'actual_new_model_fits':0,'actual_new_traffic_datasets':0,'figures':8,'panel_csv_files':len(panels),'tables':9,'supplementary_groups':8,'workbooks':len(workbooks),'reviewer_comments':31,'gis_layers':len(layers),'qgz_status':'UNAVAILABLE_QGIS_NOT_INSTALLED_GPKG_VALIDATED','historical_130km_status':'UNVERIFIED','e08_status':'NOT_RUN_TARGET_ASSET_NOT_FOUND','data_rights':'AUTHOR_LOCAL_CONTROLLED; EXTERNAL_DISTRIBUTION_REQUIRES_AUTHOR_LICENSE_CHECK','source_files':source,'generated_files':inventory}
(D/'Final_Figure_Table_Execution_Manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

fig_lines=[]
for _,r in fig.iterrows():fig_lines.append(f"- {r['figure']}: {r['panel_csv_count']} 个CSV，{r['xlsx_count']} 个工作簿；{r['folder']}")
table_lines=[]
for _,r in tables.iterrows():table_lines.append(f"- {r['table']}: {r['rows']} 行、{r['columns']} 列；CSV、XLSX、LaTeX")
report=f'''# Applied Intelligence 最终图表数据准备报告（2026-11-26）

## 范围与结果

- PROJECT_ROOT：`{R}`；交付 ZIP 位于 `{O}`。
- 复用已验收 G0/G1/G2/Prompt 04–05 证据；本阶段新增模型拟合 **0** 次，新增交通数据集 **0** 个。
- 正文规划图 **8** 张，数据目录 **8** 个，面板/辅助 CSV **{len(panels)}** 个；正文表 **9** 张，补充材料 **8** 组，Excel 工作簿 **{len(workbooks)}** 个；审稿意见映射 **31/31**。
- 数据已具备作者开始正式绘图的条件；正式图件、正文 `main.tex` 和审稿回复尚未制作。

## 每张图的数据

{chr(10).join(fig_lines)}

Fig.1 提供原始观测点、当前 OSM 匹配点、15 个复核候选点、真实道路中心线、候选走廊线、50 条节点间诊断路线、匹配位移线及生成的示意范围面。GPKG **{len(layers)}** 个可读取图层（含独立路线 GPKG 的重复路线层），EPSG:4326，几何非空且有效。原始节点 51 个，人工复核节点 15 个。当前 OSM 路径不是历史 130 km 主线；历史里程未获证实，不能直接放入图轴或正文。当前机器未安装 QGIS/PyQGIS，因此没有生成 QGZ；见 Fig.1 目录的 `QGIS_Drawing_Instructions_CN.md`，作者可直接导入已验证 GPKG、保存自己的 QGIS 工程。行政边界真实图层未证实；生成范围面明确标为非行政边界。

Fig.2–Fig.8 的 CSV/XLSX 包含可复用的聚合绘图数据、面板说明及字段字典。原稿 Fig.1–Fig.6 仅做编号映射；Fig.7–Fig.8 为建议新增。图中数值及统计口径以本次 CSV、来源索引和既有冻结验收记录为准。

## 每张正文表的数据

{chr(10).join(table_lines)}

表格源 CSV 保留全精度，XLSX 和 TeX 由同一内存数据框导出；抽取与导出代码在 `03_CODE/FINAL_FIGURE_TABLE_DATA`。Table 8 中旧 Ridge Cholesky 的逐样本共同目标对比不能代替 SVD 修正的对应配对结果，绘图/写作时不得据此作修正后 Ridge 的配对优势结论。

## 重要修正与限制

- G1 主结果采用 Method A 每样本三种子集成，按折宏平均；旧图中 Method B 或单种子数值不能混入。
- G2 为独立复现与修订实验，与原冻结模型实现分列。Ridge 数值修正后 native 指标已独立列出；其旧 Cholesky 配对对比仍需避免误用。
- Holm 校正结果从冻结的已验收统计证据整理，描述性误差线与多重比较置信结论分开。
- E08 因指定 451,008 行 JB 目标资产未找到而未运行；没有外部验证结果。
- GIS 15 个候选节点等待作者在 QGIS 逐点复核；当前 OSM 几何、直线距离和历史主线长度是不同量。
- 商业 FCD 与受限制坐标仅供作者本地受控研究。作者本地绘图 ZIP 和独立 QGIS ZIP 不默认允许公开；对外验收 ZIP 仅含聚合数据和必要证据，外发仍由作者核对许可。

## 验证与作者后续动作

本机逐一读取全部输出 CSV、XLSX ZIP 结构和每个 GPKG 图层，核对 8 图、9 表、8 组补充、31 条评论、51 原始节点和 15 个 GIS 复核节点。Shapefile 伴随文件齐全。详见 `Final_Numerical_Consistency_Checks.csv`、`Final_GIS_Layer_Validation.csv` 与清单 JSON。

作者下一步：在 QGIS 复核 15 个节点、决定研究区域与历史里程表述；用本地数据包绘制 Fig.1–Fig.8 并检查各图标题/图例；核准商业数据分发许可；图件确认后再更新论文正文和 31 条回复。
'''
(B/'Final_Figure_Table_Data_Preparation_Report_CN.md').write_text(report,encoding='utf-8')

# Author-local full package. Independent GIS archive keeps relative paths in one root.
date='20261126'
zips={
 'local':O/f'APIN_FINAL_FIGURE_TABLE_PLOT_DATA_LOCAL_{date}.zip',
 'gis':O/f'APIN_FIG01_QGIS_DRAWING_DATA_LOCAL_{date}.zip',
 'review':O/f'APIN_FINAL_FIGURE_TABLE_DATA_REVIEW_{date}.zip'}
local=[p for p in files(B) if p.name!='Final_Delivery_ZIP_Checks.json']
gis=files(G)
review=[]
for p in local:
 x=rel(p).lower();name=p.name.lower()
 if '/fig01_' in x or x.endswith('.gpkg') or x.endswith('.geojson') or x.endswith('.shp') or x.endswith('.shx') or x.endswith('.dbf') or x.endswith('.prj') or x.endswith('.cpg'):continue
 if '/fig02_' in x and (name.endswith('.xlsx') or 'node_' in name or name=='data_dictionary.csv'):continue
 if '/fig03_' in x and (name.endswith('.xlsx') or 'nodes' in name or name=='data_dictionary.csv'):continue
 if '/fig05_' in x and (name.endswith('.xlsx') or 'node_' in name or name=='data_dictionary.csv'):continue
 if name=='apin_final_all_figures_and_tables_master.xlsx':continue
 if '/03_supplementary_data/' in x and name.endswith('.xlsx') and 's08' in x:continue
 if name.endswith('.inspect.ndjson'):continue
 if p.suffix.lower() in ['.csv','.xlsx','.tex','.md','.json']:
  review.append(p)
def package(path,members,prefix,base=R):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in members:z.write(p,prefix+str(p.relative_to(base)).replace('\\','/'))
 with zipfile.ZipFile(path) as z:assert z.testzip() is None and len(z.namelist())==len(members)
package(zips['local'],local,'FINAL_FIGURE_TABLE_DATA/')
package(zips['gis'],gis,'FIG01_QGIS_DRAWING_DATA/',G)
package(zips['review'],review,'FINAL_FIGURE_TABLE_DATA_REVIEW/')

# Independent extraction test inside the authorized project; no extra persistent copy.
import tempfile
with tempfile.TemporaryDirectory(dir=D,prefix='gis_extract_check_') as tmp:
 with zipfile.ZipFile(zips['gis']) as z:z.extractall(tmp)
 gp=next(Path(tmp).rglob('Fig01_Pan_Borneo_Study_Area.gpkg'))
 assert len(pyogrio.list_layers(gp))==8
 assert len(pyogrio.read_dataframe(gp,layer='Original_Observation_Nodes'))==51
 assert len(pyogrio.read_dataframe(gp,layer='GIS_Review_Candidates_15'))==15

summary={'zip':[{'kind':k,'absolute_path':str(p),'size_bytes':p.stat().st_size,'sha256':sha(p),'entries':len(zipfile.ZipFile(p).namelist())} for k,p in zips.items()],'figures':8,'panel_csv':len(panels),'tables':9,'supplements':8,'workbooks':len(workbooks),'reviewer_comments':31,'gis_layers':len(layers),'gis_standalone_extract_test':'PASS','new_model_fits':0,'new_traffic_datasets':0}
(D/'Final_Delivery_ZIP_Checks.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
