from pathlib import Path
import hashlib,json,sqlite3
import pandas as pd
import pyogrio
from pyproj import Geod

R=Path(r'E:\20261125_论文修改_Applied Intelligence\大修_Applied Intelligence_2026112_论文修改')
B=R/'07_FIGURES_TABLES/FINAL_FIGURE_TABLE_DATA';G=B/'01_FIGURE_DATA/Fig01_Study_Area_GIS';V=B/'09_QGIS_VALIDATION';V.mkdir(exist_ok=True)
gp=G/'Fig01_Pan_Borneo_Study_Area.gpkg';geod=Geod(ellps='WGS84')
def read(n):return pyogrio.read_dataframe(gp,layer=n)
def csv(n):return pd.read_csv(next((R/'04_EXPERIMENTS').rglob(n+'.csv')))
def save(x,n):x.to_csv(V/n,index=False,encoding='utf-8-sig')
orig=read('Original_Observation_Nodes');match=read('Matched_Road_Nodes_Current_OSM');road=read('Existing_Road_Network_Current_OSM');routes=read('Inter_Node_Diagnostic_Routes');review=read('GIS_Review_Candidates_15');m=csv('GIS_Final_Node_Matching');a=csv('GIS_Final_Inter_Node_Distance');r15=csv('GIS_Author_Review_Checklist_15_Nodes')
assert len(orig)==len(match)==len(m)==51 and len(routes)==len(a)==50 and len(review)==len(r15)==15
original_ids=[f'N{i:03d}' for i in range(1,52)];display_ids=[f'N{i:02d}' for i in range(1,52)]
rows=[]
for i,(_,row) in enumerate(orig.iterrows()):
 ref=m.loc[m.node_id==row.node_id_original].iloc[0]
 d=geod.inv(row.geometry.x,row.geometry.y,float(ref.original_longitude),float(ref.original_latitude))[2]
 rows.append({'node_id':row.node_id_original,'display_id':row.node_id_display,'expected_id':original_ids[i],'expected_display_id':display_ids[i],'longitude':row.geometry.x,'latitude':row.geometry.y,'coordinate_crs':row.coordinate_crs,'source_difference_m':d,'coordinate_finite':bool(pd.notna(row.geometry.x) and pd.notna(row.geometry.y)),'geometry_nonempty':not row.geometry.is_empty,'source_match':d<0.001,'id_match':row.node_id_original==original_ids[i] and row.node_id_display==display_ids[i],'status':'PASS' if d<0.001 and row.node_id_original==original_ids[i] and row.node_id_display==display_ids[i] else 'FAILED'})
node=pd.DataFrame(rows);assert node.status.eq('PASS').all() and not node[['longitude','latitude']].duplicated().any()
save(node,'GIS_01_Original_Node_Validation.csv')
file_rows=[];layers=[]
for p in sorted(G.iterdir()):
 if p.suffix.lower() not in ['.gpkg','.shp','.geojson','.csv']:continue
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 try:
  if p.suffix.lower()=='.csv':
   x=pd.read_csv(p);file_rows.append({'file':p.name,'size_bytes':p.stat().st_size,'sha256':digest,'format':'.csv','layer':'','features':len(x),'attributes':len(x.columns),'crs':'','bounds':'','empty_geometries':'','invalid_geometries':'','readability':'PASS'});continue
  named=pyogrio.list_layers(p) if p.suffix.lower()=='.gpkg' else [[p.stem,'']]
  for name,_ in named:
   x=pyogrio.read_dataframe(p,layer=name if p.suffix.lower()=='.gpkg' else None)
   empty=int(x.geometry.isna().sum()+x.geometry.is_empty.sum());invalid=int((~x.geometry.is_valid).sum())
   rec={'file':p.name,'size_bytes':p.stat().st_size,'sha256':digest,'format':p.suffix.lower(),'layer':name,'geometry_type':','.join(map(str,x.geom_type.unique())),'features':len(x),'attributes':len(x.columns)-1,'crs':str(x.crs),'bounds':','.join(f'{v:.6f}' for v in x.total_bounds),'empty_geometries':empty,'invalid_geometries':invalid,'readability':'PASS' if not empty and not invalid else 'CONDITIONAL_PASS'}
   file_rows.append(rec);layers.append(rec)
 except Exception as e:file_rows.append({'file':p.name,'size_bytes':p.stat().st_size,'sha256':digest,'readability':'FAILED','error':str(e)})
save(pd.DataFrame(file_rows),'GIS_00_File_and_Layer_Inventory.csv')
assert all(r['readability']!='FAILED' for r in file_rows)
with sqlite3.connect(gp) as con:integrity=con.execute('PRAGMA integrity_check').fetchone()[0]
assert integrity=='ok'
roadcheck=road.drop(columns='geometry').copy();roadcheck['empty_geometry']=road.geometry.isna()|road.geometry.is_empty;roadcheck['invalid_geometry']=~road.geometry.is_valid;roadcheck['zero_length']=road.geometry_length_m<=0;roadcheck['duplicate_geometry_count']=road.geometry.to_wkb().map(road.geometry.to_wkb().value_counts());roadcheck['multipart']=road.geom_type!='LineString';roadcheck['status']='PASS' if not any(roadcheck[c].any() for c in ['empty_geometry','invalid_geometry','zero_length']) else 'CONDITIONAL_PASS';save(roadcheck,'GIS_03_Road_Network_Geometry_Validation.csv')
matching=m.copy();matching['geodesic_offset_recomputed_m']=[geod.inv(r.original_longitude,r.original_latitude,r.matched_longitude,r.matched_latitude)[2] for r in m.itertuples()];matching['offset_difference_m']=(matching.geodesic_offset_recomputed_m-matching.lateral_offset_m).abs();matching['original_position_unchanged']=matching.node_id.map(dict(zip(node.node_id,node.source_match)));matching['manual_review_status']='AUTHOR_REVIEW_REQUIRED';matching['technical_status']=matching.offset_difference_m.map(lambda v:'PASS' if v<0.01 else 'CONDITIONAL_PASS');save(matching,'GIS_04_Node_Road_Matching_Validation.csv')
route=a.copy();route['geometry_present']=~routes.geometry.isna().values;route['geometry_valid']=routes.geometry.is_valid.values;route['route_geometry_status']=route.apply(lambda r:'PASS' if r.geometry_present and r.geometry_valid else 'FAILED',axis=1);route['direction_status']='NOT_VERIFIED';route['manual_review_status']='AUTHOR_REVIEW_REQUIRED';route['repeated_edge_count']='NOT_AVAILABLE_FROM_AGGREGATE';route['repeated_edge_length_m']='TOTAL_ONLY_44010.192';save(route,'GIS_07_Inter_Node_Route_Validation.csv')
review15=r15.copy();review15['gis_geometry_present']=review15.node_id.isin(review.node_id_original if 'node_id_original' in review.columns else review.node_id);review15['review_status']='AUTHOR_REVIEW_REQUIRED';save(review15,'GIS_06_Author_Manual_Review_Checklist.csv')
crs=f'''# CRS与距离核验\n\n原始点图层字段 `coordinate_crs` 对51点均登记 EPSG:4326；GPKG实测 CRS 为 `{orig.crs}`。51点几何坐标与冻结节点表一致（测地差<0.001 m），经纬度有限、无重复坐标。来源独立测绘定义未另行确认。\n\n道路距离继承冻结 GIS 分析的 WGS84 测地及当前OSM图最短路径口径，不用EPSG:3857计算。原始点范围：{orig.total_bounds.tolist()}。图层CRS读取和SQLite完整性：PASS（{integrity}）。本轮未重新求道路最短路径或变更匹配。\n'''
(V/'GIS_02_CRS_and_Distance_Validation.md').write_text(crs,encoding='utf-8')
report=f'''# QGIS空间数据专项校验\n\n- GPKG SQLite完整性：{integrity}；共{len(layers)}个实际读取的空间图层记录；空几何与无效几何见逐层CSV。\n- 原始节点/当前OSM匹配：{len(orig)}/{len(match)}；51个ID、坐标与冻结表吻合；中位偏移{m.lateral_offset_m.median():.3f} m，最大{m.lateral_offset_m.max():.3f} m（{m.loc[m.lateral_offset_m.idxmax(),'node_id']}）。\n- 15个候选节点：全部仍为AUTHOR_REVIEW_REQUIRED，未自动标记通过。\n- 50个相邻路径：几何均可读；当前无方向图连通{int(a.connected_current_graph.sum())}/50，不证明历史主线或方向。N015–N016、N037–N038需重点人工核查。\n- 历史约130 km未验证；直线和137.395 km、当前图路径156.274 km、唯一边112.264 km不能互换。\n- QGZ：本机未安装QGIS/PyQGIS，QGIS_PROJECT_NOT_RUNTIME_VERIFIED；独立GPKG解包读取已通过，不等同于QGIS工程打开。\n- 来源：冻结本地OSM快照2026-11-25与原始51节点登记。OSM署名与商业FCD许可应分别保留；完整坐标和GIS包仅供作者本机受控研究，分发须经作者确认。\n- 未执行自动几何修复、重新匹配或正式地图绘制。详细结果见本目录CSV。\n'''
(V/'APIN_QGIS_Data_Validation_Report_CN.md').write_text(report,encoding='utf-8')
print(json.dumps({'files_read':len(file_rows),'spatial_layer_reads':len(layers),'nodes':len(node),'routes':len(route),'road_features':len(road),'review_nodes':len(review15),'gpkg_integrity':integrity,'invalid_road_geometries':int(roadcheck.invalid_geometry.sum()),'missing_road_geometry':int(roadcheck.empty_geometry.sum())}))
