@echo off
setlocal enabledelayedexpansion

if "%1"=="" (
    echo Please provide the input file path as the first argument.
    exit /b
)

set "input_file=%1"
set "output_file=names.txt"

if exist "%output_file%" del "%output_file%"

for /f "tokens=*" %%a in (%input_file%) do (
    set "entry=%%a"
    
    REM Split each entry into name and other details
    for /f "tokens=1,* delims=," %%b in ("!entry!") do (
        set "name=%%b"
        set "details=%%c"
        
        REM Format the name (remove the prefix)
        set "formatted_name=!name:* =!"

        REM Append the formatted entry to the output file
        echo !formatted_name!,!details!>>"%output_file%"
    )
)

echo Formatted data has been written to %output_file%
exit /b
