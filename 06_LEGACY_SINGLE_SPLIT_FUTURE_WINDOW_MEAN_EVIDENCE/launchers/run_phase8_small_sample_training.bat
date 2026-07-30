@echo off
setlocal

cd /d D:\2026_PD
if errorlevel 1 goto failed

if not exist logs mkdir logs
if not exist outputs\logs mkdir outputs\logs
if not exist outputs\tables mkdir outputs\tables
if not exist outputs\checkpoints mkdir outputs\checkpoints

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set TS=%%i
set LOGFILE=logs\phase8_small_sample_training_%TS%.log

powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\2026_PD\envs\panborneo_fcd\python.exe' -u scripts\phase8_small_sample_training.py --config configs\phase8_small_sample_training.yaml 2>&1 | Tee-Object -FilePath '%LOGFILE%'; exit $LASTEXITCODE"
if errorlevel 1 goto failed

echo Phase 8 small-sample training completed.
echo Log: %LOGFILE%
echo Output CSV: outputs\tables\phase8_small_sample_metrics.csv
pause
exit /b 0

:failed
echo Phase 8 small-sample training failed. Check the timestamped log under logs\ if it was created.
pause
exit /b 1
