@echo off
setlocal EnableDelayedExpansion

set "namesFile=names.txt"
set "progressFile=progress.txt"

if exist "%progressFile%" (
    set /p progress=<"%progressFile%"
) else (
    set "progress=0"
)

for /f "skip=%progress% tokens=* delims=" %%a in (%namesFile%) do (
    set /a progress+=1

    set "name=%%a"
    set "name=!name:~0,-1!"

    for /f "tokens=1,* delims=," %%b in ("!name!") do (
        set "lastName=%%b"
        set "firstName=%%c"
    )

    set "firstName=!firstName:~1!"
    set "searchUrl=https://www.facebook.com/search/top/?q=!firstName!%2!lastName!"

    start "" "!searchUrl!"

    echo !progress!>"%progressFile%"

    echo Searching for: !name!...
    echo Press Enter to continue to the next name...
    pause >nul
)

del "%progressFile%"

endlocal
