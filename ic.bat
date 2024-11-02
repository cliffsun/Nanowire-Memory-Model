@echo off

g++ src\main.cc src\model\nanowire.cpp -o src\nanowire

if %errorlevel% neq 0 exit /b %errorlevel%

.\src\nanowire "0 0.5 1" "12.56 12.56 12.56"

:: The first string is the # of wires and their locations. For instance, "0 0.5 1" represents 3 evenly spaced out nanowires. 

:: The second string is the critical phases associated with each nanowire. 

:: Any corresponding strings after the first 2 strings are interpreted to be user inputted vortex states. For more information, 
:: read the README.md

if %errorlevel% neq 0 exit /b %errorlevel%

python src\plot.py