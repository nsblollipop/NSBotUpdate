@echo off
taskkill /F /IM NSLaunch.exe
echo Downloading update...
set "version=%~1"

if not defined version (
    echo No version provided. Exiting...
    exit /b
)

curl -L -o NSBotUpdate.zip "https://github.com/nsblollipop/NSBotUpdate/releases/download/%version%/NSBotUpdate.zip"

IF EXIST NSBotUpdate.zip (
    echo NSBotUpdate.zip has been downloaded.
) ELSE (
    echo Failed to download NSBotUpdate.zip.
    exit /b
)

if %errorlevel% neq 0 (
    echo Error downloading update.
    pause
    exit /b
)

setlocal
set "batch_dir=%~dp0"
set "exclude_files=NSBotUpdate.zip update.bat"

echo Deleting files and folders...

for /F "delims=" %%f in ('dir /B /A-D "%batch_dir%" ^| findstr /V /I "%exclude_files%"') do (
    del /F /Q "%batch_dir%\%%f"
)

for /D %%d in ("%batch_dir%*") do (
    if /I not "%%~nxd"=="%exclude_files%" (
        rd /S /Q "%%~d"
    )
)

set "batch_dir=%~dp0"
set "zip_file=%batch_dir%NSBotUpdate.zip"
set "extract_dir=%batch_dir%"

echo Extracting files...

powershell -Command "Expand-Archive -Path '%zip_file%' -DestinationPath '%extract_dir%'"

set "zip_file=%~dp0NSBotUpdate.zip"

if exist "%zip_file%" (
    del /f /q "%zip_file%"
    echo NSBotUpdate.zip has been deleted.
) else (
    echo NSBotUpdate.zip does not exist.
)

echo Update completed.
start NSLaunch.exe
exit /b
