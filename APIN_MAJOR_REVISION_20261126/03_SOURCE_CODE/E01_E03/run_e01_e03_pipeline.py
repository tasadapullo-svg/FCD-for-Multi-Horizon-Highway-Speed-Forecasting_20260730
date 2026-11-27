"""Default verifies the accepted cache. Never repeats accepted E01--E03 automatically."""
from common import *
def main():
 lockpath=CTL/'G1_Accepted_Result_Lock.json'
 if not lockpath.exists():raise SystemExit('No accepted lock. Run prepare_shared -> E01 -> E02 -> E03 -> validation -> deliverables explicitly; do not silently overwrite existing results.')
 lock=json.loads(lockpath.read_text(encoding='utf-8'));changes=[]
 if PROTOCOL_SHA!=lock['protocol_sha256']:changes.append('protocol changed')
 for entry in lock['analysis_code']:
  p=Path(entry['path'])
  if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:changes.append('analysis code: '+str(p))
 for entry in lock['source_signatures']:
  p=Path('\\\\?\\'+entry['path'])
  if not p.exists():changes.append('input missing: '+entry['path']);continue
  stat=p.stat()
  if stat.st_size!=entry['size_bytes'] or stat.st_mtime_ns!=entry['mtime_ns']:changes.append('input signature changed: '+entry['path'])
 for entry in lock['accepted_result_hashes']:
  p=Path(entry['path'])
  if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:changes.append('accepted result changed: '+str(p))
 if changes:
  jwrite(LOG/'targeted_change_detection.json',{'at':now(),'changes':changes,'action':'do not automatically repeat; diagnose exact affected scientific task'});raise SystemExit('\n'.join(changes))
 print('REUSED_PASS: accepted E01–E03 inputs, protocol, analysis code and aggregate outputs unchanged; no calculations rerun.')
if __name__=='__main__':main()
