@echo off
setlocal
cd /d D:\2026_PD || goto failed
if not exist logs mkdir logs
powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\2026_PD\envs\panborneo_fcd\python.exe' -u scripts\phase15_feature_ablation.py --config configs\phase15_feature_ablation.yaml --mode full 2>&1 | Tee-Object -FilePath logs\phase15_feature_ablation_full_console.log; exit $LASTEXITCODE"
if errorlevel 1 goto failed
echo Phase 15 full completed.
pause
exit /b 0
:failed
echo Phase 15 full failed. Check logs\phase15_feature_ablation_full_console.log
pause
exit /b 1
