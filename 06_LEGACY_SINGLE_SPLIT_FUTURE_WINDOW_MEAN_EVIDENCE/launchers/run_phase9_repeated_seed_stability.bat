@echo off
setlocal

cd /d D:\2026_PD
if errorlevel 1 goto failed

if not exist outputs\logs mkdir outputs\logs
if not exist outputs\checkpoints mkdir outputs\checkpoints

powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\2026_PD\envs\panborneo_fcd\python.exe' -u scripts\phase9_repeated_seed_stability.py --config configs\phase9_repeated_seed_stability.yaml 2>&1 | Tee-Object -FilePath outputs\logs\phase9_repeated_seed_stability_console.log; exit $LASTEXITCODE"
if errorlevel 1 goto failed

echo Phase 9 repeated-seed stability completed. Console log: outputs\logs\phase9_repeated_seed_stability_console.log
pause
exit /b 0

:failed
echo Phase 9 repeated-seed stability failed. Check outputs\logs\phase9_repeated_seed_stability_console.log if it was created.
pause
exit /b 1
