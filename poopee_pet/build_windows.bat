@echo off
setlocal EnableDelayedExpansion
title Poopee Desktop Pet - Windows Build

echo ================================================
echo  Poopee Desktop Pet - Build Script
echo ================================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.11+ from python.org
    pause & exit /b 1
)
python --version

:: Install / upgrade dependencies
echo.
echo [1/4] Installing Python dependencies...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [ERROR] pip install failed.
    pause & exit /b 1
)
pip install pyinstaller -q
echo      Done.

:: Clean previous build
echo.
echo [2/4] Cleaning previous build...
if exist "dist\PoopeePet" rmdir /s /q "dist\PoopeePet"
if exist "build\PoopeePet"  rmdir /s /q "build\PoopeePet"
echo      Done.

:: Build with PyInstaller
echo.
echo [3/4] Building with PyInstaller...
pyinstaller poopee_pet.spec --noconfirm
if errorlevel 1 (
    echo [ERROR] PyInstaller build failed.
    pause & exit /b 1
)
echo      Done.

:: Copy .env.example next to exe (optional)
echo.
echo [4/4] Finalising...
copy /y ".env.example" "dist\PoopeePet\.env.example" >nul

echo.
echo ================================================
echo  Build complete!
echo  Executable: dist\PoopeePet\PoopeePet.exe
echo ================================================
echo.
echo To run the app now, press any key.
pause >nul
start "" "dist\PoopeePet\PoopeePet.exe"
