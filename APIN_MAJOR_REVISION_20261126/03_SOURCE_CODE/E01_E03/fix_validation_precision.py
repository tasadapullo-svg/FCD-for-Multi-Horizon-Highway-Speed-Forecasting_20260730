from common import *
import shutil
for name in ['G1_Validation_Receipt.json','G1_Validation_Checks.csv']:
 p=G1/name;backup=LOG/('before_csv_precision_fix_'+name)
 if not backup.exists():shutil.copyfile(p,backup)
hol=pd.read_csv(E03/'E03_08_Holm_Adjusted_Comparisons.csv');assert hol.raw_p.between(1/10001-5e-13,1+5e-13).all() and hol.CI_low.le(hol.CI_high).all()
p=G1/'G1_Validation_Checks.csv';x=pd.read_csv(p);x.loc[x.check_id=='BOOTSTRAP_P_FINITE',['status','detail']]=['PASS','finite correction verified; min p serialization rounds12significant digits, allowed absolute tolerance5e-13'];save(x,p)
r=json.loads((G1/'G1_Validation_Receipt.json').read_text(encoding='utf-8'));r['checks']=x.to_dict('records');r['overall_status']='CONDITIONAL_PASS' if not x.status.eq('BLOCKED').any() else 'BLOCKED';r['targeted_fix']='CSV raw_p12-digit rounding vs exact1/10001 lower-bound; no statistical values changed, no analyses rerun';r['targeted_fix_at']=now();jwrite(G1/'G1_Validation_Receipt.json',r)
with (LOG/'implementation_fixes.md').open('a',encoding='utf-8') as f:f.write('\nG1验收p值下界检查：CSV12有效位存储的0.000099990001较精确1/10001低约3e-17，导致机械下界误报。仅将验收数值序列化容差设为5e-13，定向复核该项；保存原验收记录，不更改p值/CI/协议或重跑分析。\n')
log('targeted CSV precision acceptance fix; G1 '+r['overall_status'])
