"""Read-only contract diagnostic, no fitting/training/inference."""
from g2_common import *
ready=next(p for p in DER.glob('*/ready.json') if load(p).get('condition')=='base' and load(p).get('fold')==1 and load(p).get('horizon')==1)
meta=load(ready);shared=Path(meta['shared_features']);hist=np.load(ready.parent/'history_indices.npy',mmap_mode='r');scaled=np.load(shared/'scaled.npy',mmap_mode='r');old=np.load(BASE/'01_DATA_PIPELINE/folds/fold1/H1/X_sequence.npy',mmap_mode='r')
new_manifest=pd.read_parquet(ready.parent/'manifest.parquet');old_manifest=pd.read_parquet(BASE/'01_DATA_PIPELINE/folds/fold1/H1/sample_manifest_fold1_H1.parquet');order=pd.MultiIndex.from_frame(old_manifest[['node_id','forecast_origin']]).get_indexer(pd.MultiIndex.from_frame(new_manifest[['node_id','forecast_origin']]));assert (order>=0).all()
diff=np.max(np.abs(scaled[hist]-old[order]),axis=(0,1));rows=[{'feature':f,'max_abs_scaled_diff':float(d)} for f,d in zip(FEATURES,diff)];save(pd.DataFrame(rows),GATE/'feature_contract_diagnostic.csv');print(pd.DataFrame(rows).to_string(index=False))
