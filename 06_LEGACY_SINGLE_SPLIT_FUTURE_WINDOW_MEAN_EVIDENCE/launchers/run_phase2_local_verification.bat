@echo off
setlocal

cd /d "%~dp0"

echo [Phase 2 Verification] Inspecting output files and streaming window counts...
python scripts\verify_phase2_outputs.py --tables-dir outputs\tables --chunksize 500000
if errorlevel 1 goto failed

echo.
echo [Phase 2 Verification] Checking leakage and chronological split boundaries...
python scripts\check_phase2_leakage.py --window-index outputs\tables\window_index_all.csv --split-summary outputs\tables\train_val_test_split_summary.csv --chunksize 500000
if errorlevel 1 goto failed

echo.
echo [Phase 2 Verification] Summarizing feasible horizon-history combinations...
python scripts\summarize_phase2_feasible_horizons.py --feasibility outputs\tables\window_feasibility_by_horizon.csv --missingness outputs\tables\window_missingness_summary.csv --target-summary outputs\tables\target_variable_summary.csv --min-valid-ratio 0.80
if errorlevel 1 goto failed

echo.
echo Phase 2 local verification completed successfully.
exit /b 0

:failed
echo.
echo Phase 2 local verification failed. Check the messages above.
exit /b 1
