@echo off
setlocal
cd /d D:\2026_PD || goto failed
if not exist logs mkdir logs
powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\2026_PD\envs\panborneo_fcd\python.exe' -u scripts\phase16_robustness.py --config configs\phase16_robustness.yaml --mode smoke 2>&1 | Tee-Object -FilePath logs\phase16_robustness_smoke_console.log; exit $LASTEXITCODE"
if errorlevel 1 goto failed
echo Phase 16 smoke completed.
pause
exit /b 0
:failed
echo Phase 16 smoke failed. Check logs\phase16_robustness_smoke_console.log
pause
exit /b 1
