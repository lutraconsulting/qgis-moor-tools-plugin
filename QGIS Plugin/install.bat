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
mkdir %DEST%\examples
mkdir %DEST%\Templates\Logos
xcopy /y *.py %DEST%
xcopy /y *.png %DEST%
xcopy /y metadata.txt %DEST%
xcopy /y *.ui %DEST%
xcopy /y examples\*.* %DEST%\examples
xcopy /y Templates\*.* %DEST%\Templates
xcopy /y Templates\Logos\*.* %DEST%\Templates\Logos

PAUSE
