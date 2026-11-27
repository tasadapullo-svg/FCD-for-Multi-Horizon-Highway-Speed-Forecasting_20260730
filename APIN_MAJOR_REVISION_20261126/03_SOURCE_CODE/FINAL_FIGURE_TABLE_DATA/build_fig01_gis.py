"""Prepare author-local QGIS layers from frozen coordinates and current OSM snapshot."""
from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd,geopandas as gpd,pyogrio
from shapely.geometry import LineString,MultiLineString,box
from pyproj import Geod
R=Path(__file__).resolve().parents[2]
G=R/'07_FIGURES_TABLES/FINAL_FIGURE_TABLE_DATA/01_FIGURE_DATA/Fig01_Study_Area_GIS';G.mkdir(parents=True,exist_ok=True)
S=R/'04_EXPERIMENTS/FINAL_TARGETED_CHECKS'
src=S/'GIS_Final_Plot_Data_Local_Only.gpkg';assert src.exists()
nodes=pyogrio.read_dataframe(src,layer='nodes_original')
matched=pyogrio.read_dataframe(src,layer='nodes_matched_current_osm')
roads=pyogrio.read_dataframe(src,layer='road_centerlines_current_osm')
pieces=pyogrio.read_dataframe(src,layer='selected_undirected_paths')
dist=pd.read_csv(S/'GIS_Final_Inter_Node_Distance.csv')
assert len(nodes)==len(matched)==51 and nodes.node_id.is_unique and matched.node_id.is_unique
assert len(dist)==50 and set(nodes.node_id)==set(matched.node_id)
assert all(x.crs.to_epsg()==4326 and x.geometry.notna().all() and x.geometry.is_valid.all() for x in [nodes,matched,roads,pieces])
geod=Geod(ellps='WGS84')
obs=nodes.rename(columns={'node_id':'node_id_original','display_id':'node_id_display','order_index':'node_order'}).copy()
obs['road_name']=obs.node_id_original.map(matched.set_index('node_id').matched_road_name)
obs['data_source']='Pan Borneo TomTom FCD author-local';obs['observation_period']='2025-12-08 to 2026-02-28'
obs['coordinate_crs']='EPSG:4326';obs['match_status']='ORIGINAL_OBSERVATION_LOCATION'
mat=matched.rename(columns={'matched_osm_way_id':'osm_way_id','matched_road_name':'road_name','lateral_offset_m':'matching_distance_m','manual_review_reason':'review_reason'}).copy()
flag=mat.review_reason.fillna('').astype(str).str.strip().ne('')
mat['review_status']=np.where(flag,'AUTHOR_GIS_REVIEW_REQUIRED','NO_SCREENING_FLAG')
review=mat[flag].copy();assert len(review)==15
road=roads.rename(columns={'name':'road_name','highway':'highway_class','oneway_tag':'oneway'}).copy()
road['geometry_length_m']=[geod.geometry_length(x) for x in road.geometry]
road['data_snapshot_date']='2026-11-25';road['source']='OpenStreetMap contributors; ODbL; current snapshot'
route_rows=[]
edge_counts=pieces.assign(key=pieces.geometry.map(lambda x:hashlib.sha256(x.wkb).hexdigest())).groupby('key').size().to_dict()
for (a,b),part in pieces.groupby(['from_node','to_node'],sort=False):
 d=dist[(dist.from_node==a)&(dist.to_node==b)];assert len(d)==1
 d=d.iloc[0];keys=[hashlib.sha256(x.wkb).hexdigest() for x in part.geometry]
 route_rows.append({'from_node':a,'to_node':b,'route_length_m':d.current_osm_undirected_shortest_path_m,'straight_line_distance_m':d.straight_geodesic_m,'detour_ratio':d.road_to_straight_ratio,'repeated_edge_flag':any(edge_counts[k]>1 for k in keys),'route_status':'CURRENT_OSM_UNDIRECTED_DIAGNOSTIC_REVIEW' if pd.notna(d.review_flags) else 'CURRENT_OSM_UNDIRECTED_DIAGNOSTIC','direction_status':'HISTORICAL_DIRECTION_NOT_VERIFIED','geometry':MultiLineString(list(part.geometry))})
routes=gpd.GeoDataFrame(route_rows,geometry='geometry',crs='EPSG:4326')
assert len(routes)==50 and routes.geometry.is_valid.all()
seen=set();selected=[]
for x in pieces.itertuples(index=False):
 key=hashlib.sha256(x.geometry.wkb).hexdigest()
 if key in seen:continue
 seen.add(key);selected.append({'osm_way_id':x.osm_way_id,'segment_status':'CANDIDATE_CURRENT_OSM_NOT_HISTORICAL_VERIFIED','manual_review':'AUTHOR_GIS_REVIEW_REQUIRED','geometry':x.geometry})
cand=gpd.GeoDataFrame(selected,geometry='geometry',crs='EPSG:4326')
disp=gpd.GeoDataFrame([{'node_id':x.node_id,'displacement_m':x.matching_distance_m,'review_status':x.review_status,'diagnostic_type':'MATCH_DISPLACEMENT_NOT_ROAD','geometry':LineString([nodes.set_index('node_id').loc[x.node_id].geometry,x.geometry])} for x in mat.itertuples(index=False)],geometry='geometry',crs='EPSG:4326')
bounds=nodes.total_bounds;pad=.05
extent=gpd.GeoDataFrame([{'feature_type':'GENERATED_STUDY_EXTENT_NOT_ADMINISTRATIVE_BOUNDARY','source':'Bounding box of 51 original nodes plus 0.05 degree margin','geometry':box(bounds[0]-pad,bounds[1]-pad,bounds[2]+pad,bounds[3]+pad)}],geometry='geometry',crs='EPSG:4326')
layers=[('Original_Observation_Nodes',obs),('Matched_Road_Nodes_Current_OSM',mat),('GIS_Review_Candidates_15',review),('Existing_Road_Network_Current_OSM',road),('Candidate_Study_Corridor_Current_OSM',cand),('Inter_Node_Diagnostic_Routes',routes),('Node_Matching_Displacement_Not_Road',disp),('Generated_Study_Extent_Not_Admin',extent)]
gpkg=G/'Fig01_Pan_Borneo_Study_Area.gpkg'
if gpkg.exists():gpkg.unlink()
for i,(name,df) in enumerate(layers):pyogrio.write_dataframe(df,gpkg,layer=name,driver='GPKG',append=i>0)
routepkg=G/'Fig01_Inter_Node_Routes.gpkg'
if routepkg.exists():routepkg.unlink()
pyogrio.write_dataframe(routes,routepkg,layer='Inter_Node_Diagnostic_Routes',driver='GPKG')
obs.drop(columns='geometry').to_csv(G/'Fig01_Observation_Nodes.csv',index=False,encoding='utf-8-sig')
obs.to_file(G/'Fig01_Observation_Nodes.geojson',driver='GeoJSON',engine='pyogrio')
mat.to_file(G/'Fig01_Matched_Nodes.geojson',driver='GeoJSON',engine='pyogrio')
road.to_file(G/'Fig01_Road_Centreline.geojson',driver='GeoJSON',engine='pyogrio')
obs[['node_id_original','node_id_display','node_order','geometry']].rename(columns={'node_id_original':'node_id','node_id_display':'display_id','node_order':'node_order'}).to_file(G/'Fig01_Observation_Nodes.shp',driver='ESRI Shapefile',encoding='UTF-8',engine='pyogrio')
road[['osm_way_id','road_name','highway_class','oneway','geometry']].rename(columns={'osm_way_id':'way_id','road_name':'road_name','highway_class':'road_class'}).to_file(G/'Fig01_Road_Centreline.shp',driver='ESRI Shapefile',encoding='UTF-8',engine='pyogrio')
pd.DataFrame([{'shapefile':'Fig01_Observation_Nodes.shp','field':'node_id','full_field':'node_id_original'},{'shapefile':'Fig01_Observation_Nodes.shp','field':'display_id','full_field':'node_id_display'},{'shapefile':'Fig01_Observation_Nodes.shp','field':'node_order','full_field':'node_order'},{'shapefile':'Fig01_Road_Centreline.shp','field':'way_id','full_field':'osm_way_id'},{'shapefile':'Fig01_Road_Centreline.shp','field':'road_name','full_field':'road_name'},{'shapefile':'Fig01_Road_Centreline.shp','field':'road_class','full_field':'highway_class'}]).to_csv(G/'Shapefile_Field_Name_Map.csv',index=False)
review.drop(columns='geometry').to_csv(G/'Fig01_GIS_Review_15_Nodes.csv',index=False,encoding='utf-8-sig')
dist.to_csv(G/'Fig01_Inter_Node_Distance_Diagnostic.csv',index=False)
pd.read_csv(S/'GIS_Corridor_Length_Reconciliation.csv').to_csv(G/'Fig01_Corridor_Length_Reconciliation.csv',index=False)
validation=[]
for name,_ in layers:
 df=pyogrio.read_dataframe(gpkg,layer=name)
 validation.append({'layer':name,'feature_count':len(df),'geometry_types':'|'.join(sorted(df.geom_type.unique())),'crs':str(df.crs),'null_geometries':int(df.geometry.isna().sum()),'invalid_geometries':int((~df.geometry.is_valid).sum()),'fields':'|'.join(df.columns.drop('geometry')),'status':'PASS' if len(df)>0 and df.crs.to_epsg()==4326 and df.geometry.notna().all() and df.geometry.is_valid.all() else 'FAIL'})
assert all(x['status']=='PASS' for x in validation)
pd.DataFrame(validation).to_csv(G/'Fig01_GIS_Layer_Validation.csv',index=False)
for stem in ['Fig01_Observation_Nodes','Fig01_Road_Centreline']:
 assert all((G/f'{stem}.{ext}').exists() for ext in ['shp','shx','dbf','prj','cpg'])
(G/'GIS_Source_Manifest.json').write_text(json.dumps({'input_gpkg':str(src),'input_gpkg_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'snapshot':'2026-11-25','crs':'EPSG:4326','distance_method':'WGS84 geodesic for reported metric lengths','license':'© OpenStreetMap contributors; ODbL','historical_length':'HISTORICAL_CORRIDOR_LENGTH_NOT_VERIFIED','qgz_status':'NOT_GENERATED_NO_QGIS_OR_PYQGIS','administrative_boundaries':'NOT_AVAILABLE; study extent is generated rectangle','layers':validation},ensure_ascii=False,indent=2),encoding='utf-8')
(G/'QGIS_Drawing_Instructions_CN.md').write_text('# QGIS Fig.1加载说明\n\n本机未安装QGIS/PyQGIS，故不生成无效QGZ。解压本目录后，在QGIS中以GeoPackage添加Fig01_Pan_Borneo_Study_Area.gpkg的全部8层。建议底部Generated_Study_Extent_Not_Admin，其上Existing_Road_Network_Current_OSM，再Candidate_Study_Corridor_Current_OSM；点层Original_Observation_Nodes与Matched_Road_Nodes_Current_OSM分开显示；GIS_Review_Candidates_15、Inter_Node_Diagnostic_Routes和Node_Matching_Displacement_Not_Road仅供复核。全部EPSG:4326；距离使用WGS84测地计算，不直接用经纬度平面长度。以review_status筛选15节点，优先N007、N015–N016、N037–N038。当前OSM候选线不能视作历史确认主线。历史约130km未验证；137.395km、156.274km、112.264km是不同口径，不能替换原历史主线长度。没有可用的真实行政边界，仅提供明确标记的生成研究范围框。道路数据署名© OpenStreetMap contributors/ODbL。\n',encoding='utf-8')
print('GIS',[(n,len(d)) for n,d in layers])
