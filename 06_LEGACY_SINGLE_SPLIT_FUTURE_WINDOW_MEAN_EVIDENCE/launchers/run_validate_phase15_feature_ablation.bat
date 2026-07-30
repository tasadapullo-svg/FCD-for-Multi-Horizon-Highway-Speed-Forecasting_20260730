@echo off
setlocal
cd /d D:\2026_PD || goto failed
powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\2026_PD\envs\panborneo_fcd\python.exe' -u scripts\validate_phase15_feature_ablation.py; exit $LASTEXITCODE"
if errorlevel 1 goto failed
echo Phase 15 validation passed.
pause
exit /b 0
:failed
echo Phase 15 validation failed. Read reports\phase15_validation_report.md
pause
exit /b 1
