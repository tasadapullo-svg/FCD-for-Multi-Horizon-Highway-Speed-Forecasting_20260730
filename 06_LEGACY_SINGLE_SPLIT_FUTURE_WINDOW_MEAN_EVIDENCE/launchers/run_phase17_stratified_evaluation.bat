@echo off
setlocal
cd /d D:\2026_PD || goto failed
powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\2026_PD\envs\panborneo_fcd\python.exe' -u scripts\phase17_stratified_evaluation.py --config configs\phase17_stratified_evaluation.yaml; exit $LASTEXITCODE"
if errorlevel 1 goto failed
echo Phase 17 completed.
pause
exit /b 0
:failed
echo Phase 17 failed. Check reports or console output.
pause
exit /b 1
