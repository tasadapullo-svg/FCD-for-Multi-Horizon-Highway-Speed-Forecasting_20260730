@echo off
setlocal

cd /d D:\2026_PD
if errorlevel 1 goto failed

if not exist outputs\logs mkdir outputs\logs
if not exist outputs\checkpoints mkdir outputs\checkpoints

powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\2026_PD\envs\panborneo_fcd\python.exe' -u scripts\phase4_deep_smoke_test.py --config configs\phase4_deep_smoke_test.yaml 2>&1 | Tee-Object -FilePath outputs\logs\phase4_deep_smoke_test_console.log"
if errorlevel 1 goto failed

echo Phase 4 deep learning smoke test completed. Console log: outputs\logs\phase4_deep_smoke_test_console.log
pause
exit /b 0

:failed
echo Phase 4 deep learning smoke test failed. Check outputs\logs\phase4_deep_smoke_test_console.log if it was created.
pause
exit /b 1
