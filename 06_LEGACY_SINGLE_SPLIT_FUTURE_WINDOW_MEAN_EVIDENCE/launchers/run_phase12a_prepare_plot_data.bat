@echo off
setlocal

cd /d D:\2026_PD
if errorlevel 1 goto failed

if not exist outputs\logs mkdir outputs\logs
if not exist outputs\plot_data mkdir outputs\plot_data

powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\2026_PD\envs\panborneo_fcd\python.exe' -u scripts\phase12a_prepare_plot_data.py 2>&1 | Tee-Object -FilePath outputs\logs\phase12a_prepare_plot_data_console.log; exit $LASTEXITCODE"
if errorlevel 1 goto failed

echo Phase 12A plot data preparation completed. Console log: outputs\logs\phase12a_prepare_plot_data_console.log
pause
exit /b 0

:failed
echo Phase 12A plot data preparation failed. Check outputs\logs\phase12a_prepare_plot_data_console.log if it was created.
pause
exit /b 1
