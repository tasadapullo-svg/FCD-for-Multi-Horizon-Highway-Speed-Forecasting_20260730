"""One bounded GIS reconciliation from existing node coordinates and current OSM snapshot."""
from pathlib import Path
from collections import Counter
import json,math
import pandas as pd,networkx as nx,geopandas as gpd
from shapely.geometry import Point,LineString
from shapely.strtree import STRtree
from pyproj import Transformer,Geod

ROOT=Path(__file__).resolve().parents[2]
GIS=ROOT/'02_DATA/02_EXTERNAL_DATA/E07_GIS'
OUT=ROOT/'04_EXPERIMENTS/FINAL_TARGETED_CHECKS'
OUT.mkdir(parents=True,exist_ok=True)
source=json.loads((GIS/'osm_corridor_overpass.json').read_text(encoding='utf-8'))
acq=json.loads((GIS/'acquisition_manifest.json').read_text(encoding='utf-8'))
coords=pd.read_csv(GIS/'node_coordinates_local_only.csv').sort_values('order_index')
assert len(coords)==51 and coords.node_id.is_unique
elements=source['elements']
verts={e['id']:(e['lon'],e['lat']) for e in elements if e['type']=='node'}
ways={e['id']:e for e in elements if e['type']=='way' and 'highway' in e.get('tags',{})}
to_m=Transformer.from_crs('EPSG:4326','EPSG:32649',always_xy=True)
to_ll=Transformer.from_crs('EPSG:32649','EPSG:4326',always_xy=True)
geod=Geod(ellps='WGS84')
xy={k:to_m.transform(*v) for k,v in verts.items()}
graph=nx.Graph();segs=[];seg_meta=[];road_features=[]
for wid,way in ways.items():
    ids=way['nodes'];tags=way.get('tags',{})
    valid=[v for v in ids if v in verts]
    if len(valid)>=2:
        road_features.append({'osm_way_id':wid,'name':tags.get('name',''),'ref':tags.get('ref',''),'highway':tags.get('highway',''),'oneway_tag':tags.get('oneway',''),
                              'geometry':LineString([verts[v] for v in valid])})
    for u,v in zip(ids,ids[1:]):
        if u not in xy or v not in xy or u==v:continue
        geom=LineString([xy[u],xy[v]]);length=geom.length
        if length<=0:continue
        graph.add_edge(u,v,weight=length,way_id=wid)
        segs.append(geom);seg_meta.append((u,v,wid))
tree=STRtree(segs)
rows=[];matching_features=[]
for raw in coords.itertuples(index=False):
    original=Point(*to_m.transform(raw.longitude,raw.latitude))
    j=int(tree.nearest(original));segment=segs[j];u,v,wid=seg_meta[j]
    snapped=segment.interpolate(segment.project(original))
    nearest_anchor=min([u,v],key=lambda z:original.distance(Point(*xy[z])))
    lon,lat=to_ll.transform(snapped.x,snapped.y)
    tags=ways[wid].get('tags',{})
    nearby=tree.query(original.buffer(50.0))
    alternative_ways={seg_meta[int(k)][2] for k in nearby if seg_meta[int(k)][2]!=wid and segs[int(k)].distance(original)<=50.0}
    offset=float(original.distance(snapped))
    flags=[]
    if offset>30:flags.append('OFFSET_GT_30M')
    if tags.get('highway','').endswith('_link'):flags.append('LINK_ROAD_MATCH')
    if not tags.get('name') and not tags.get('ref'):flags.append('ROAD_NAME_REF_MISSING')
    rows.append({'node_id':raw.node_id,'display_id':raw.display_id,'order_index':int(raw.order_index),'original_latitude':raw.latitude,'original_longitude':raw.longitude,
                 'matched_latitude':lat,'matched_longitude':lon,'matched_osm_way_id':wid,'matched_road_name':tags.get('name',''),'matched_road_ref':tags.get('ref',''),
                 'highway_class':tags.get('highway',''),'oneway_osm_tag':tags.get('oneway',''),'lateral_offset_m':offset,
                 'other_osm_ways_within_50m':len(alternative_ways),'parallel_road_verified':False,'nearest_anchor_osm_node_id':nearest_anchor,
                 'match_basis':'Nearest eligible current-OSM line segment; anchor is closest segment endpoint, not exact snap point',
                 'confidence':'LOW_REVIEW' if flags else 'PROVISIONAL_CURRENT_OSM',
                 'manual_review_reason':'|'.join(flags)})
    matching_features.append({'node_id':raw.node_id,'geometry':Point(lon,lat)})
match=pd.DataFrame(rows)
pair_rows=[];edge_use=Counter();route_features=[];straight_sum=0.0;graph_sum=0.0
for a,b in zip(rows,rows[1:]):
    _,_,straight=geod.inv(a['original_longitude'],a['original_latitude'],b['original_longitude'],b['original_latitude'])
    straight=float(straight);straight_sum+=straight
    u=a['nearest_anchor_osm_node_id'];v=b['nearest_anchor_osm_node_id']
    connected=nx.has_path(graph,u,v)
    path=nx.shortest_path(graph,u,v,weight='weight') if connected else []
    length=sum(graph.edges[x,y]['weight'] for x,y in zip(path,path[1:])) if connected else math.nan
    if connected:graph_sum+=length
    ratio=length/straight if connected and straight>0 else math.nan
    flags=[]
    if not connected:flags.append('DISCONNECTED')
    if ratio>2:flags.append('ROAD_TO_STRAIGHT_GT_2')
    if length>8000:flags.append('ROAD_PATH_GT_8KM')
    pair_rows.append({'from_node':a['node_id'],'to_node':b['node_id'],'order_from':a['order_index'],'order_to':b['order_index'],
                      'straight_geodesic_m':straight,'current_osm_undirected_shortest_path_m':length,'road_to_straight_ratio':ratio,
                      'cumulative_straight_m':straight_sum,'cumulative_road_graph_m':graph_sum if connected else math.nan,
                      'connected_current_graph':connected,'historical_connection_verified':False,'direction_verified':False,'review_flags':'|'.join(flags)})
    for x,y in zip(path,path[1:]):
        key=tuple(sorted((x,y)));edge_use[key]+=1
        route_features.append({'from_node':a['node_id'],'to_node':b['node_id'],'osm_way_id':graph.edges[x,y]['way_id'],
                               'geometry':LineString([verts[x],verts[y]])})
pairs=pd.DataFrame(pair_rows)
for row in rows:
    adjacent=pairs[(pairs.from_node==row['node_id']) | (pairs.to_node==row['node_id'])]
    extra='|'.join(x for x in adjacent.review_flags if isinstance(x,str) and x)
    if extra:
        row['manual_review_reason']='|'.join(x for x in [row['manual_review_reason'],extra] if x)
        row['confidence']='LOW_REVIEW'
match=pd.DataFrame(rows)
unique_length=sum(graph.edges[u,v]['weight'] for u,v in edge_use)
repeated_length=sum(graph.edges[u,v]['weight']*(count-1) for (u,v),count in edge_use.items())
max_repeat=max(edge_use.values()) if edge_use else 0
match.to_csv(OUT/'GIS_Final_Node_Matching.csv',index=False,encoding='utf-8-sig')
pairs.to_csv(OUT/'GIS_Final_Inter_Node_Distance.csv',index=False,encoding='utf-8-sig')
adj=pairs[['from_node','to_node','connected_current_graph','historical_connection_verified','direction_verified','current_osm_undirected_shortest_path_m','review_flags']].copy()
adj['adjacency_scope']='Adjacent by supplied node index; current OSM undirected connectivity only, not validated traffic-neighbor relation'
adj.to_csv(OUT/'GIS_Adjacency_Evidence.csv',index=False,encoding='utf-8-sig')
reconciliation=pd.DataFrame([
 {'measure':'Original manuscript approximate corridor length','km':130.0,'status':'UNVERIFIED_APPROXIMATE_CLAIM','basis':'Original manuscript; no dated centreline, endpoints or GIS measurement recovered'},
 {'measure':'Sum of adjacent-node WGS84 straight geodesics','km':straight_sum/1000,'status':'VERIFIED_FROM_51_COORDINATES','basis':'Original node coordinate sequence; not road mileage'},
 {'measure':'Sum of adjacent-node current OSM graph shortest paths','km':graph_sum/1000,'status':'CURRENT_OSM_ANCHOR_PROXY_ONLY','basis':'Undirected graph, each node anchored to nearest segment endpoint; can detour or repeat edges'},
 {'measure':'Unique current OSM graph edge length in selected paths','km':unique_length/1000,'status':'CURRENT_OSM_PROXY_ONLY','basis':'Deduplicated selected path edges; not necessarily original research mainline'},
 {'measure':'Repeated selected graph edge length','km':repeated_length/1000,'status':'DIAGNOSTIC_ONLY','basis':f'Maximum per-edge path reuse {max_repeat} times'},
 {'measure':'Historically verified mainline corridor length','km':math.nan,'status':'HISTORICAL_CORRIDOR_LENGTH_NOT_VERIFIED','basis':'No dated matched mainline/endpoint record or directed topology evidence'}])
reconciliation.to_csv(OUT/'GIS_Corridor_Length_Reconciliation.csv',index=False,encoding='utf-8-sig')

gpkg=OUT/'GIS_Final_Plot_Data_Local_Only.gpkg'
assert gpkg.resolve().is_relative_to(ROOT.resolve())
if gpkg.exists():gpkg.unlink()
for i,(layer,frame) in enumerate([
    ('nodes_original',gpd.GeoDataFrame(coords.copy(),geometry=gpd.points_from_xy(coords.longitude,coords.latitude),crs='EPSG:4326')),
    ('nodes_matched_current_osm',gpd.GeoDataFrame(match.merge(pd.DataFrame(matching_features),on='node_id'),geometry='geometry',crs='EPSG:4326')),
    ('road_centerlines_current_osm',gpd.GeoDataFrame(road_features,geometry='geometry',crs='EPSG:4326')),
    ('selected_undirected_paths',gpd.GeoDataFrame(route_features,geometry='geometry',crs='EPSG:4326'))]):
    frame.to_file(gpkg,layer=layer,driver='GPKG',engine='pyogrio',mode='w' if i==0 else 'a')

summary={'source_at':acq['at'],'nodes':len(match),'offset_median_m':float(match.lateral_offset_m.median()),'offset_max_m':float(match.lateral_offset_m.max()),
         'nodes_manual_review':int((match.confidence=='LOW_REVIEW').sum()),'pairs_connected':int(pairs.connected_current_graph.sum()),
         'pairs_flagged_detour':int(pairs.review_flags.str.contains('ROAD_TO_STRAIGHT_GT_2').sum()),'straight_km':straight_sum/1000,
         'current_osm_graph_km':graph_sum/1000,'unique_graph_edge_km':unique_length/1000,'repeated_edge_km':repeated_length/1000,
         'max_edge_reuse':max_repeat,'historical_corridor_length_status':'HISTORICAL_CORRIDOR_LENGTH_NOT_VERIFIED','gpkg_local_only':str(gpkg.relative_to(ROOT)).replace('\\','/')}
(OUT/'GIS_Final_Summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary))
