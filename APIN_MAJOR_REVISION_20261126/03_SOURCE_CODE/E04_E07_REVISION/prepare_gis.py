from g2_common import *
import zipfile,io,urllib.request,urllib.parse
GIS=ROOT/'02_DATA/02_EXTERNAL_DATA/E07_GIS';GIS.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(RAW_ARCHIVE) as z:nodes=pd.read_csv(io.BytesIO(z.read('03_nodes/nodes.csv')))
nodes['display_id']=nodes.node_id.map(lambda s:'N'+str(int(s[1:])).zfill(2));save(nodes[['node_id','display_id','order_index','latitude','longitude']],GIS/'node_coordinates_local_only.csv')
bounds=[float(nodes.latitude.min()-.02),float(nodes.longitude.min()-.02),float(nodes.latitude.max()+.02),float(nodes.longitude.max()+.02)]
print('BBOX',bounds,flush=True)
query='[out:json][timeout:40];way["highway"~"^(motorway|trunk|primary|secondary|motorway_link|trunk_link|primary_link|secondary_link)$"]('+','.join(map(str,bounds))+');(._;>;);out body;'
attempts=[];p=GIS/'osm_corridor_overpass.json'
if not p.exists():
 for server in ['https://overpass-api.de/api/interpreter','https://overpass.kumi.systems/api/interpreter']:
  try:
   url=server+'?'+urllib.parse.urlencode({'data':query});req=urllib.request.Request(url,headers={'User-Agent':'APIN-Revision-Research/1.0'})
   with urllib.request.urlopen(req,timeout=55) as response:data=response.read()
   parsed=json.loads(data);assert len(parsed.get('elements',[]))>0;p.write_bytes(data);attempts.append({'server':server,'status':'SUCCESS','bytes':len(data)});break
  except Exception as e:attempts.append({'server':server,'status':'FAILED','error':str(e)});log('GIS fetch '+str(e))
dump(GIS/'acquisition_manifest.json',{'at':now(),'bbox_wgs84':bounds,'query':query,'attempts':attempts,'license':'OpenStreetMap ODbL; attribution OpenStreetMap contributors','source':'https://www.openstreetmap.org/copyright','historical_representativeness':'current snapshot not proof of2025-12..2026-02 road state','status':'DOWNLOADED' if p.exists() else 'BLOCKED_EXTERNAL_SERVICE'})
log('E07 targeted road acquisition '+('DOWNLOADED' if p.exists() else 'BLOCKED'))
