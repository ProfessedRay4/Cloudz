@echo off

REM Define the repository URL
set "repoURL=https://github.com/ProfessedRay4/Discord-AutoRaid.git"

REM Get the current directory of the batch file
set "localFolder=%~dp0"

REM Check if Git is installed
where git > nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed. Please install Git and try again.
    exit /b 1
)

REM Check if Python is installed
where python > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

REM Check if the local folder exists
if not exist "%localFolder%" (
    echo Local folder does not exist. Cloning the repository...
    git clone "%repoURL%" "%localFolder%"
) else (
    echo Local folder exists.

    REM Check if the requirements file exists
    if not exist "%localFolder%\requirements.txt" (
        echo Installing requirements...
        cd "%localFolder%"
        pip install -r requirements.txt
    ) else (
        echo Requirements already installed.
    )

    REM Check if the remote origin already exists
    cd "%localFolder%"
    git remote -v | findstr /C:"origin" > nul 2>&1
    if %errorlevel% neq 0 (
        echo Setting remote origin...
        git remote add origin "%repoURL%"
    )

    REM Fetch and pull the latest changes from the remote repository
    git fetch origin
    git pull origin main
)

REM Run main.py
echo Running main.py...
python "%localFolder%\main.py"
