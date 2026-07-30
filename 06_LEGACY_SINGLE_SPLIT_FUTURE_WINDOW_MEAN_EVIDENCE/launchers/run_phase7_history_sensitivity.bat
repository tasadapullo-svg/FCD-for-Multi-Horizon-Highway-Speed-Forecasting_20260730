@echo off
setlocal

cd /d D:\2026_PD
if errorlevel 1 goto failed

if not exist outputs\logs mkdir outputs\logs
if not exist outputs\checkpoints mkdir outputs\checkpoints

powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\2026_PD\envs\panborneo_fcd\python.exe' -u scripts\phase7_history_sensitivity.py --config configs\phase7_history_sensitivity.yaml 2>&1 | Tee-Object -FilePath outputs\logs\phase7_history_sensitivity_console.log; exit $LASTEXITCODE"
if errorlevel 1 goto failed

echo Phase 7 history-length sensitivity completed. Console log: outputs\logs\phase7_history_sensitivity_console.log
pause
exit /b 0

:failed
echo Phase 7 history-length sensitivity failed. Check outputs\logs\phase7_history_sensitivity_console.log if it was created.
pause
exit /b 1
