"""Integrate accepted G1/G2 aggregate CSVs; no bootstrap, predictions or training."""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
E03 = ROOT / '04_EXPERIMENTS/E03_STATISTICAL_INFERENCE'
G2 = ROOT / '04_EXPERIMENTS/G2_E04_E07_ACCEPTANCE'
OUT = ROOT / '04_EXPERIMENTS/FINAL_TARGETED_CHECKS'
OUT.mkdir(parents=True, exist_ok=True)
g1_3 = pd.read_csv(E03 / 'E03_08_Holm_Adjusted_Comparisons.csv')
g1_7 = pd.read_csv(E03 / 'E03_07_Block_Length_Sensitivity.csv')
g2 = pd.read_csv(G2 / 'G2_Key_Comparisons_Actual.csv')
assert len(g1_3) == len(g1_7) == 15 and len(g2) == 4

def holm(group):
    ordered = group.sort_values(['raw_p', 'comparison']).copy()
    adjusted = np.maximum.accumulate(np.minimum(1, (len(group)-np.arange(len(group)))*ordered.raw_p.to_numpy()))
    ordered['holm_adjusted_p'] = adjusted
    return ordered.sort_index()

g1_7 = pd.concat([holm(group) for _, group in g1_7.groupby('horizon')]).sort_values(['horizon','comparison'])
g1_7['family_size'] = 5
g1_7['significant_holm_0_05'] = g1_7.holm_adjusted_p < 0.05
g1_3 = g1_3.sort_values(['horizon','comparison'])
assert np.allclose(g1_3.effect.to_numpy(), g1_7.effect.to_numpy(), atol=1e-9)
assert set(zip(g1_3.horizon,g1_3.comparison)) == set(zip(g1_7.horizon,g1_7.comparison))

g1 = g1_3[['horizon','comparison','effect','CI_low','CI_high','raw_p','holm_adjusted_p','dates']].copy()
g1.insert(0,'family','G1_5_PER_HORIZON')
g1['block_days'] = 3
g1['role'] = 'PRIMARY'
g1['significant_holm_0_05'] = g1.holm_adjusted_p < .05
sens = g1_7[['horizon','comparison','effect','CI_low','CI_high','raw_p','holm_adjusted_p','dates','significant_holm_0_05']].copy()
sens.insert(0,'family','G1_5_PER_HORIZON')
sens['block_days'] = 7
sens['role'] = 'SENSITIVITY_FROM_ACCEPTED_RAW_P'
sens['source_file'] = 'E03_07_Block_Length_Sensitivity.csv'
g1['source_file'] = 'E03_08_Holm_Adjusted_Comparisons.csv'

g2rows = pd.DataFrame({
    'family':'G2_4_KEY_COMPARISONS','horizon':[1,6,1,1],
    'comparison':g2.comparison_id,'effect':g2.day_mean_MAE_delta_alt_minus_ref,
    'CI_low':g2.block3_CI_low,'CI_high':g2.block3_CI_high,
    'raw_p':g2.block3_p_two_sided,'holm_adjusted_p':g2.holm_adjusted_p,
    'dates':g2.test_days,'block_days':3,'role':'PRIMARY',
    'significant_holm_0_05':g2.holm_adjusted_p < .05,
    'source_file':'G2_Key_Comparisons_Actual.csv'})
g2sens = g2rows.copy()
g2sens[['CI_low','CI_high','raw_p']] = g2[['block7_CI_low','block7_CI_high','block7_p_descriptive']].to_numpy()
g2sens['holm_adjusted_p'] = np.nan
g2sens['significant_holm_0_05'] = np.nan
g2sens['block_days'] = 7
g2sens['role'] = 'DESCRIPTIVE_SENSITIVITY_NO_NEW_FORMAL_FAMILY'

primary = pd.concat([g1,g2rows],ignore_index=True)
primary.to_csv(OUT/'Final_Statistical_Inference.csv',index=False,encoding='utf-8-sig')
pd.concat([g1,sens,g2rows,g2sens],ignore_index=True).to_csv(OUT/'Final_Statistical_Sensitivity_3d_7d.csv',index=False,encoding='utf-8-sig')

claims = [
 ('C01','XGBoost vs Ridge obtains significant day-macro evidence at H1 and H3','STATISTICALLY_SUPPORTED','G1 3-day Holm; H6 is not included','E03_08_Holm_Adjusted_Comparisons.csv'),
 ('C02','GRU vs Ridge obtains significant day-macro evidence at H1, H3 and H6','STATISTICALLY_SUPPORTED','Same corridor; retrospective 41 test dates','E03_08_Holm_Adjusted_Comparisons.csv'),
 ('C03','XGBoost is stably superior to SeasonalHA across all horizons','NOT_SUPPORTED','All three G1 primary confidence intervals span zero','E03_08_Holm_Adjusted_Comparisons.csv'),
 ('C04','GATE-FCD supports transparent data auditing and a common evaluation contract','DESCRIPTIVELY_SUPPORTED','Protocol and denominators audited; not an accuracy superiority claim','G1_06_Acceptance_Report_CN.md'),
 ('C05','GATE-FCD guarantees lower forecasting MAE','NOT_SUPPORTED','G2 ablations and key tests do not establish a universal improvement','G2_Key_Comparisons_Actual.csv'),
 ('C06','Stricter sample eligibility always improves forecasting','NOT_SUPPORTED','3/4 and strict H6 comparisons do not show universal improvement; 4/4 lacks validation support','G2_Actual_Common_Origin_Contrasts.csv'),
 ('C07','Current outcomes validate true road-speed accuracy','NOT_SUPPORTED','Target is provider-returned speed without synchronous independent truth','G1_06_Acceptance_Report_CN.md'),
 ('C08','Current outcomes establish generalisation to another corridor','NOT_SUPPORTED','Single commercial FCD corridor; E08 not run','G2_07_Acceptance_Report_CN.md'),
 ('C09','Current outcomes establish reliable live production availability','NOT_SUPPORTED','Original API arrival latency unavailable','G2_01_Source_and_Implementation_Report_CN.md'),
 ('C10','4/4 completeness yields a six-fold model comparison at H6','NOT_ESTIMABLE','All H6 validation folds empty','E04_Threshold4_Sample_Support.csv'),
 ('C11','G2 key paired changes are significant after four-test Holm correction','NOT_SUPPORTED','All four G2 adjusted p values exceed 0.05','G2_Key_Comparisons_Actual.csv'),
]
pd.DataFrame(claims,columns=['claim_id','proposed_claim','support_status','scope_or_limitation','evidence_file']).to_csv(OUT/'Final_Scientific_Claims_Registry.csv',index=False,encoding='utf-8-sig')
summary = {'g1_primary_significant':int(g1.significant_holm_0_05.sum()),
           'g1_7d_sensitivity_significant':int(sens.significant_holm_0_05.sum()),
           'g1_primary_significant_7d_preserved':bool(set(zip(g1[g1.significant_holm_0_05].horizon,g1[g1.significant_holm_0_05].comparison)).issubset(set(zip(sens[sens.significant_holm_0_05].horizon,sens[sens.significant_holm_0_05].comparison)))),
           'g2_primary_significant':int(g2rows.significant_holm_0_05.sum()),
           'sources':['E03_08_Holm_Adjusted_Comparisons.csv','E03_07_Block_Length_Sensitivity.csv','G2_Key_Comparisons_Actual.csv']}
(OUT/'Final_Statistics_Receipt.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary))
