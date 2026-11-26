from g2_common import *
import torch,sklearn,xgboost,psutil,subprocess
torch.set_num_threads(2)
env={'python':sys.version,'torch':torch.__version__,'sklearn':sklearn.__version__,'xgboost':xgboost.__version__,'numpy':np.__version__,'pandas':pd.__version__,'CPU':platform.processor(),'logical_cores':psutil.cpu_count(),'physical_cores':psutil.cpu_count(logical=False),'RAM_bytes':psutil.virtual_memory().total,'torch_threads':torch.get_num_threads(),'GPU_used':False,'reason':'existing NVIDIA driver457.56 CUDA11.1; new CPU-only wheel; no driver changes','platform':platform.platform()}
print(json.dumps(env,ensure_ascii=False,indent=2));dump(LOG/'environment.json',env)
p=BASE/'03_FORMAL_PREDICTIONS/checkpoints/GRU_F1_H1_S42.pt'
try:
 z=torch.load(p,map_location='cpu',weights_only=True);print('CHECKPOINT_TYPE',type(z));print('KEYS',list(z)[:40])
 for k,val in z.items():
  if isinstance(val,dict):print('DICT',k,[(s,tuple(a.shape) if hasattr(a,'shape') else type(a).__name__) for s,a in list(val.items())[:12]])
  elif hasattr(val,'shape'):print('TENSOR',k,tuple(val.shape))
  else:print('META',k,str(val)[:1200])
except Exception as e:print('SAFE_CHECKPOINT_READ_LIMITATION',type(e).__name__,str(e)[:1600])
