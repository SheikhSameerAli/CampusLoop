@echo off
cd /d "%~dp0"
if exist build\classes rmdir /S /Q build\classes
mkdir build\classes
javac --release 17 -encoding UTF-8 -d build\classes src\campusloop\*.java
if errorlevel 1 goto fail
xcopy /E /I /Y web build\classes\web >nul
jar --create --file campusloop.jar --main-class campusloop.App -C build\classes .
if errorlevel 1 goto fail
echo Built campusloop.jar
pause
exit /b 0
:fail
echo Build failed. Install JDK 17 or later and check PATH.
pause
exit /b 1
