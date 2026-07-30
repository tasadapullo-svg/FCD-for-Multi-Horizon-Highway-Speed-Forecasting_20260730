@echo off
setlocal

cd /d D:\2026_PD
if errorlevel 1 goto failed

if not exist outputs\logs mkdir outputs\logs
if not exist outputs\checkpoints mkdir outputs\checkpoints

powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\2026_PD\envs\panborneo_fcd\python.exe' -u scripts\phase5_controlled_deep_training.py --config configs\phase5_controlled_deep_training.yaml 2>&1 | Tee-Object -FilePath outputs\logs\phase5_controlled_deep_training_console.log; exit $LASTEXITCODE"
if errorlevel 1 goto failed

echo Phase 5 controlled deep training completed. Console log: outputs\logs\phase5_controlled_deep_training_console.log
pause
exit /b 0

:failed
echo Phase 5 controlled deep training failed. Check outputs\logs\phase5_controlled_deep_training_console.log if it was created.
pause
exit /b 1
