@echo off
setlocal

call conda activate D:\2026_PD\envs\panborneo_fcd
if errorlevel 1 goto failed

cd /d D:\2026_PD
if errorlevel 1 goto failed

if not exist outputs\logs mkdir outputs\logs

python scripts\phase3_run_baselines.py --config configs\phase3_baselines.yaml > outputs\logs\phase3_baseline_console.log 2>&1
if errorlevel 1 goto failed

echo Phase 3 baseline run completed. Console log: outputs\logs\phase3_baseline_console.log
pause
exit /b 0

:failed
echo Phase 3 baseline run failed. Check outputs\logs\phase3_baseline_console.log if it was created.
pause
exit /b 1
