@echo off
setlocal EnableDelayedExpansion
echo Starting Windows Pets...

:: 1. Check if 'py' launcher is installed and working
py -c "import encodings" >nul 2>&1
if !errorlevel! == 0 (
    echo Using Python Launcher ^(py^)
    py -m pip install PyQt6 --quiet
    py "%~dp0main.py"
    goto :end
)

:: 2. Check if 'python' is in PATH and working
python -c "import encodings" >nul 2>&1
if !errorlevel! == 0 (
    echo Using python from PATH
    python -m pip install PyQt6 --quiet
    python "%~dp0main.py"
    goto :end
)

:: 3. Check common local app data install locations
for %%V in (313 312 311 310) do (
    if exist "%LOCALAPPDATA%\Programs\Python\Python%%V\python.exe" (
        "%LOCALAPPDATA%\Programs\Python\Python%%V\python.exe" -c "import encodings" >nul 2>&1
        if !errorlevel! == 0 (
            echo Found Python %%V
            "%LOCALAPPDATA%\Programs\Python\Python%%V\python.exe" -m pip install PyQt6 --quiet
            "%LOCALAPPDATA%\Programs\Python\Python%%V\python.exe" "%~dp0main.py"
            goto :end
        )
    )
)

echo ERROR: No working Python installation found. 
echo Please download and install Python from https://www.python.org/downloads/
pause

:end
