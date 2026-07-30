@echo off
setlocal
cd /d D:\2026_PD || goto failed
powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\2026_PD\envs\panborneo_fcd\python.exe' -u scripts\validate_phase16_robustness.py; exit $LASTEXITCODE"
if errorlevel 1 goto failed
echo Phase 16 validation passed.
pause
exit /b 0
:failed
echo Phase 16 validation failed. Read reports\phase16_validation_report.md
pause
exit /b 1
