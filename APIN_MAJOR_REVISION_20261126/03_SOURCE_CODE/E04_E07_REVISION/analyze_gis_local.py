"""Local, read-only OSM corridor topology diagnostic; no inferred road direction."""
from pathlib import Path
import json,networkx as nx,pandas as pd
from shapely.geometry import Point,LineString
from shapely.strtree import STRtree
from pyproj import Transformer
from g2_common import ROOT,now
GIS=ROOT/'02_DATA/02_EXTERNAL_DATA/E07_GIS';OUT=ROOT/'04_EXPERIMENTS/E07_SPATIAL_OPERATIONAL';OUT.mkdir(exist_ok=True)
a=json.loads((GIS/'osm_corridor_overpass.json').read_text(encoding='utf-8'));elements=a['elements'];verts={e['id']:(e['lon'],e['lat']) for e in elements if e['type']=='node'};ways=[e for e in elements if e['type']=='way' and 'highway' in e.get('tags',{})];tr=Transformer.from_crs('EPSG:4326','EPSG:32649',always_xy=True);xy={k:tr.transform(*v) for k,v in verts.items()};G=nx.Graph();segments=[];edge_ids=[]
for w in ways:
 ids=w['nodes']
 for u,v in zip(ids,ids[1:]):
  if u not in xy or v not in xy or u==v:continue
  seg=LineString([xy[u],xy[v]]);length=seg.length
  if length<=0:continue
  G.add_edge(u,v,weight=length,way_id=w['id']);segments.append(seg);edge_ids.append((u,v,w['id']))
tree=STRtree(segments);nodes=pd.read_csv(GIS/'node_coordinates_local_only.csv');rows=[]
for row in nodes.itertuples():
 point=Point(*tr.transform(row.longitude,row.latitude));j=int(tree.nearest(point));seg=segments[j];u,v,way=edge_ids[j];anchor=min([u,v],key=lambda t:point.distance(Point(*xy[t])));rows.append({'node_id':row.node_id,'display_id':row.display_id,'order_index':row.order_index,'latitude':row.latitude,'longitude':row.longitude,'nearest_way_id':way,'snap_offset_m':float(point.distance(seg)),'anchor_osm_node_id':anchor,'component':None})
components={node:i for i,comp in enumerate(nx.connected_components(G)) for node in comp}
for row in rows:row['component']=components[row['anchor_osm_node_id']]
pairs=[];cumulative=0.0
for a,b in zip(rows,rows[1:]):
 connected=a['component']==b['component'];distance=float(nx.shortest_path_length(G,a['anchor_osm_node_id'],b['anchor_osm_node_id'],weight='weight')) if connected else None
 if distance is not None:cumulative+=distance
 pairs.append({'from_node':a['node_id'],'to_node':b['node_id'],'road_graph_distance_m':distance,'topology_connected':connected,'cumulative_connected_distance_m':cumulative if connected else None})
junctions=[node for node,degree in G.degree() if degree>=3]
junction_rows=[]
if junctions:
 distances,paths=nx.multi_source_dijkstra(G,junctions,weight='weight')
 for row in rows:
  anchor=row['anchor_osm_node_id'];path=paths.get(anchor)
  junction_rows.append({'node_id':row['node_id'],'nearest_graph_junction_osm_id':path[0] if path else None,'road_distance_to_junction_m':distances.get(anchor),'junction_definition':'OSM graph degree >=3; candidate only, major status unverified'})
pd.DataFrame(rows).to_csv(OUT/'E07_Node_Road_Match_Local.csv',index=False,encoding='utf-8-sig');pd.DataFrame(pairs).to_csv(OUT/'E07_Adjacent_Road_Distances_Local.csv',index=False,encoding='utf-8-sig');summary={'at':now(),'source':'local OSM current snapshot; not historical road proof','osm_vertices':len(verts),'road_ways':len(ways),'road_segments':len(segments),'graph_components':nx.number_connected_components(G),'nodes_matched':len(rows),'max_lateral_offset_m':max(x['snap_offset_m'] for x in rows),'median_lateral_offset_m':pd.Series([x['snap_offset_m'] for x in rows]).median(),'adjacent_pairs_connected':sum(x['topology_connected'] for x in pairs),'adjacent_pairs_total':len(pairs),'direction_validated':False,'status':'DIAGNOSTIC_ONLY_REQUIRES_MANUAL_ROAD_REVIEW'};(OUT/'E07_GIS_Diagnostic.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(summary,ensure_ascii=False))
pd.DataFrame(junction_rows).to_csv(OUT/'E07_Node_Junction_Candidates_Local.csv',index=False,encoding='utf-8-sig')
