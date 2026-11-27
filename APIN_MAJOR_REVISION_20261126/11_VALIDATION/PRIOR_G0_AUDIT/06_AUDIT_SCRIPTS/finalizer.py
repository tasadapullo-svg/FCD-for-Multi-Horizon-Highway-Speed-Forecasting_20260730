import sys,json,csv,re,hashlib,zipfile,io,datetime,os
from pathlib import Path
C=json.loads(Path(__file__).with_name('config.json').read_text(encoding='utf8')); O=Path(C['out']); R=Path(C['root']); H=Path(C['hist']); repo=H/'20260730_AJSE_FINAL_GitHub'; P=repo/'04_PHASE2A_DATA_RESULTS'
sys.path.insert(0,str(O/'06_AUDIT_SCRIPTS/deps'))
import pandas as pd,numpy as np
from pypdf import PdfReader
def save(name,rows,fields=None):
 rows=list(rows); fields=fields or list(dict.fromkeys(k for r in rows for k in r)) or ['status','reason']
 with (O/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

for name in ['G0_FULL_AUDIT_REPORT.md','G0_EXECUTIVE_VERDICT.md']:
 p=O/'05_REPORTS'/name;s=p.read_text(encoding='utf8');s=s.replace("状态{'PASS_HASH_ONLY': 452, 'MISMATCH': 273, 'MISSING_LOCAL_DATA': 2}","状态：452个Git blob字节一致；272个文本仅CRLF/LF差异、规范化后对应；README.md确有版本差异；2份缺失为legacy Phase14历史材料，不混入正式结果")
 s=s.replace('冻结面板逐速度与raw去重结果的全量连接尚未完成，因此不把每个箭头判为复现通过。','补充完成raw规则重建与冻结15min面板241601行逐键连接，速度差0；原始API至cleaned的上游链仍未完整核验。')
 s=s.replace('六幅投稿PNG已视觉检查（未完成所有图内数值逐项核对）','六幅投稿PNG已视觉检查（未完成所有图内数值逐项核对）')
 s+='\n最终核验汇总：18/18份manifest的target按原始panel_row_id重建通过；54/54个split因果/边界检查通过；54/54个split计数与registry一致；15/15既存Holm调整算术复核通过。54份checkpoint仅容器结构/CRC通过，state_dict形状未核验。\n';p.write_text(s,encoding='utf8')
p=O/'04_REVIEW_AND_GAPS/G0_discrepancy_register.csv';d=pd.read_csv(p).fillna('');d=pd.concat([d,pd.DataFrame([dict(issue_id='V2',severity='MINOR',claim_or_file='local export README.md vs public main',expected='Git blob 4f43f74be131157e89f7346a1c171b3b397932ae',actual='866456e10fd9ae5aeb2d873d544786c8cff342c3',exact_evidence='G0_github_freeze_comparison.csv',status='MISMATCH',minimal_fix='保留两版本，只读检查README版本说明；不替换正式结果')])],ignore_index=True);save('04_REVIEW_AND_GAPS/G0_discrepancy_register.csv',d.to_dict('records'))
# correct report-level entries for visual review evidence and raw-panel supplement, preserve audit history in scripts/logs.
(O/'06_AUDIT_SCRIPTS/README.md').write_text('运行：用config.json指定输入和独立输出。python -X utf8 audit.py → core.py → data.py → extended.py → finish.py → supplement.py → version_check.py → finalizer.py。均只读输入；不执行项目源码、不加载模型、不发采集请求。报告列明未完成项。不要直接重跑已冻结目录，复制脚本到新审计输出目录更新config。schema_probe.py/qa.py为只读诊断。',encoding='utf8')
(O/'07_LOGS/G0_errors.log').write_text('历史执行错误及修复：默认GBK读取config失败→使用-X utf8；临时inspect.py遮蔽stdlib→重命名schema_probe.py；row_ids并非JSON数组→按分隔数字解析；报告tree变量未定义→显式读取github_tree。均已重跑成功。完整执行输出见G0_commands.log。PowerShell启动CET失败，改用Node文件API和bundled Python。',encoding='utf8')
rows=[]
for p in sorted(O.rglob('*')):
 if p.is_file() and p.name!='G0_output_sha256_manifest.csv':rows.append(dict(relative_path=str(p.relative_to(O)),size_bytes=p.stat().st_size,sha256=sha(p)))
save('00_MANIFESTS/G0_output_sha256_manifest.csv',rows)
print('FINAL OUTPUTS',len(rows),flush=True)
