@echo off
echo By default this script installs for the current user.
echo To install for all users, edit this script and set DEST accordingly
echo ""
echo Press ENTER to continue or CTRL+C to abort.
PAUSE

SET NAME=moor-tools

rem Install for current user
SET DEST=%HOMEPATH%\.qgis2\python\plugins\%NAME%

rem Install for all users (required script to be run as Administrator)
rem SET DEST=C:\Program Files (x86)\Quantum GIS Lisboa\apps\qgis\python\plugins\%NAME%

mkdir %DEST%
xcopy /e /y *.py %DEST%
xcopy /e /y *.png %DEST%
xcopy /e /y metadata.txt %DEST%
xcopy /e /y *.ui %DEST%
xcopy /e /y help %DEST%
xcopy /e /y examples %DEST%
xcopy /e /y i18n %DEST%
