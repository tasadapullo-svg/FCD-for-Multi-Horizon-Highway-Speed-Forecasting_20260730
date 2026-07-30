@echo off
setlocal
cd /d D:\2026_PD || goto failed
if not exist logs mkdir logs
powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\2026_PD\envs\panborneo_fcd\python.exe' -u scripts\phase13_strong_baselines.py --config configs\phase13_strong_baselines.yaml --mode smoke 2>&1 | Tee-Object -FilePath logs\phase13_strong_baselines_smoke_console.log; exit $LASTEXITCODE"
if errorlevel 1 goto failed
echo Phase 13 smoke run completed.
pause
exit /b 0
:failed
echo Phase 13 smoke run failed. Check logs\phase13_strong_baselines_smoke_console.log
pause
exit /b 1
