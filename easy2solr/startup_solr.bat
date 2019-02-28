@echo off
if "%OS%" == "Windows_NT" setlocal
rem ---------------------------------------------------------------------------
rem  ensy start solr7 by yogurt_lei
rem ---------------------------------------------------------------------------

set PORT=8984
set "CMD_LINE_ARGS=start -p %PORT% -m 1g -Dsolr.allow.unsafe.resourceloading=true"
set CURRENT_DIR=%cd%

if not "%SOLR7_HOME%" == "" goto gotHome
set SOLR7_HOME=%CURRENT_DIR%
if exist "%SOLR7_HOME%\bin\solr.cmd" goto okHome
cd ..
set SOLR7_HOME=%cd%
cd %CURRENT_DIR%

:gotHome
if exist "%SOLR7_HOME%\bin\solr.cmd" goto okHome
echo The SOLR7_HOME environment variable is not defined correctly
goto end
:okHome

set EXECUTABLE=%SOLR7_HOME%\bin\solr

rem Check that target executable exists
if exist "%EXECUTABLE%" goto okExec
echo Cannot find %EXECUTABLE%
echo This file is needed to run this program
goto end
:okExec

call %EXECUTABLE% %CMD_LINE_ARGS%

start "C:\Program Files ^(x86^)\Google\Chrome\Application\chrome.exe" http://localhost:%PORT%

call tail -f "%SOLR7_HOME%\server\logs\solr.log"

:end
