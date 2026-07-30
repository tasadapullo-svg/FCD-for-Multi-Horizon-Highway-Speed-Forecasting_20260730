@echo off
setlocal

cd /d D:\2026_PD
if errorlevel 1 goto failed

if not exist outputs\logs mkdir outputs\logs

powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\2026_PD\envs\panborneo_fcd\python.exe' -u scripts\phase8_robustness_diagnosis.py --config configs\phase8_robustness_diagnosis.yaml 2>&1 | Tee-Object -FilePath outputs\logs\phase8_robustness_diagnosis_console.log; exit $LASTEXITCODE"
if errorlevel 1 goto failed

echo Phase 8 robustness diagnosis completed. Console log: outputs\logs\phase8_robustness_diagnosis_console.log
pause
exit /b 0

:failed
echo Phase 8 robustness diagnosis failed. Check outputs\logs\phase8_robustness_diagnosis_console.log if it was created.
pause
exit /b 1
