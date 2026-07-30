@echo off
setlocal

cd /d D:\2026_PD
if errorlevel 1 goto failed

if not exist outputs\logs mkdir outputs\logs
if not exist outputs\checkpoints mkdir outputs\checkpoints

powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\2026_PD\envs\panborneo_fcd\python.exe' -u scripts\phase9b_five_seed_extension.py --config configs\phase9b_five_seed_extension.yaml 2>&1 | Tee-Object -FilePath outputs\logs\phase9b_five_seed_extension_console.log; exit $LASTEXITCODE"
if errorlevel 1 goto failed

echo Phase 9B five-seed extension completed. Console log: outputs\logs\phase9b_five_seed_extension_console.log
pause
exit /b 0

:failed
echo Phase 9B five-seed extension failed. Check outputs\logs\phase9b_five_seed_extension_console.log if it was created.
pause
exit /b 1
