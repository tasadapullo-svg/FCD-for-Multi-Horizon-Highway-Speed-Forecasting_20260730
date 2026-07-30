@echo off
setlocal
cd /d D:\2026_PD || goto failed
powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\2026_PD\envs\panborneo_fcd\python.exe' -u scripts\validate_phase13_full_outputs.py; exit $LASTEXITCODE"
if errorlevel 1 goto failed
echo Phase 13A full validation passed.
pause
exit /b 0
:failed
echo Phase 13A full validation failed. Read reports\phase13A_full_validation_report.md
pause
exit /b 1
