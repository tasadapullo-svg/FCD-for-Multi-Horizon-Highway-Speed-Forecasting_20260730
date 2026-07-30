@echo off
setlocal
cd /d D:\2026_PD || goto failed
powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\2026_PD\envs\panborneo_fcd\python.exe' -u scripts\phase14_final_statistical_tests.py --config configs\phase14_final_statistical_tests.yaml; exit $LASTEXITCODE"
if errorlevel 1 goto failed
echo Phase 14 statistics completed.
pause
exit /b 0
:failed
echo Phase 14 statistics failed. Check reports or console output.
pause
exit /b 1
