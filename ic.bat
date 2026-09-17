@echo off

g++ src\main.cc src\model\nanowire.cpp -o src\nanowire

if %errorlevel% neq 0 exit /b %errorlevel%

@REM .\src\nanowire "0 0.3 0.6 1" "12.56 6.28 3.14 9.42" "1.2 0.7 1.3 0.8"

@REM .\src\nanowire "0 0.6 0.63 0.86 1" "7.2 7.7 8 6.8 7.4" "1.1 0.9 1.01 0.99 1" "3 -1 0 0" "3 0 0 0" "2 -1 0 0"

@REM .\src\nanowire "0 0.625 0.666 0.833 1" "7.54 7.54 7.54 7.54 7.54" "1 1 1 1 1" "3 -1 0 0" "3 0 0 0" "2 -1 0 0"

@REM .\src\nanowire "0 0.25 0.5 0.75 1" "5.02 5.02 5.02 5.02 5.02" "1 1 1 1 1" "0 2 0 0"

@REM .\src\nanowire "0 0.5 1" "2 2 2" "1 1 1" "1 0" "0 0" "1 1" "2 0" "3 1" "4 2"

@REM .\src\nanowire "0 0.45 1" "6 7 5" "1.01 1.12 0.87" "3 0" "4 1" "2 -1"

.\src\nanowire "0 0.3 0.6 1" "12.56 6.28 3.14 9.42" "1.2 0.7 1.3 0.8"
@REM .\src\nanowire "0 0.333 0.666 1" "2.5 2.5 2.5 2.5" "1 1 1 1" "0 0 0" "1 1 1" "-1 -1 -1" "0 1 0" "0 -1 0" "1 0 0" "-1 0 0" "0 0 1" "0 0 -1"

@REM .\src\nanowire "0 0.25 0.5 0.75 1" "3.14 3.14 3.14 3.14 3.14" "1 1 1 1 1"

:: The first string is the # of wires and their locations. For instance, "0 0.5 1" represents 3 evenly spaced out nanowires. 

:: The second string is the critical phases associated with each nanowire. E.g. "12 12 12"

:: The third string is the critical currents associated with each nanowire. E.g "1 1 1"

:: Any corresponding strings after the first 2 strings are interpreted to be user inputted vortex states. For more information, 
:: read the README.md

if %errorlevel% neq 0 exit /b %errorlevel%

@REM python src\scripts\CP_VN.py

@REM python src\scripts\plot_ic.py 

python src\scripts\4_nanowire_VSR.py

@REM python src\scripts\5_nanowire_VSR.py

@REM python src\scripts\icb.py