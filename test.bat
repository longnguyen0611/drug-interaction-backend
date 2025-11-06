::
:: Test Backend API locally
:: Run this script to test the backend before deploying
::

@echo off
echo ========================================
echo Testing Drug Interaction Backend API
echo ========================================
echo.

:: Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

:: Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

:: Start server in background
echo Starting server...
start /B python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000

:: Wait for server to start
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo Server started at http://localhost:8000
echo ========================================
echo.
echo Opening API docs in browser...
start http://localhost:8000/docs
echo.
echo ========================================
echo Test Endpoints:
echo ========================================
echo.

:: Test health check
echo [1] Health Check
curl http://localhost:8000/
echo.
echo.

:: Test get drugs
echo [2] Get All Drugs (first 5)
curl http://localhost:8000/drugs | python -c "import sys, json; data = json.load(sys.stdin); print('\n'.join(data[:5]))"
echo.
echo.

:: Test prediction
echo [3] Test Prediction (Aspirin + Warfarin)
curl -X POST http://localhost:8000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"drug1\": \"Aspirin\", \"drug2\": \"Warfarin\", \"model\": \"graphsage\"}"
echo.
echo.

echo ========================================
echo Tests completed!
echo ========================================
echo.
echo Visit http://localhost:8000/docs for interactive API documentation
echo Press Ctrl+C to stop the server
echo.
pause
