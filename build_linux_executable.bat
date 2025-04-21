@echo off
echo Building Linux executable using Docker...

REM Create output directory
mkdir release 2>nul

REM Build the Docker image
docker build -t csubatch-builder -f Dockerfile.build .

REM Run the container to build the executable
docker run --rm -v "%cd%\release:/output" csubatch-builder

echo.
echo ====================================================
echo Build completed!
echo Your Linux executable package is in the release directory:
echo %cd%\release\CSUbatch-linux.tar.gz
echo ====================================================
echo.
echo You can distribute this file to Linux users. They can extract it with:
echo   tar -xzf CSUbatch-linux.tar.gz
echo.
echo And run it with:
echo   ./CSUbatch
echo.
pause 