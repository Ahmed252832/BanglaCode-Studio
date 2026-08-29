@echo off
title BanglaCode IDE
python gui.py
if errorlevel 1 (
    echo.
    echo Could not start BanglaCode IDE.
    echo Make sure Python is installed and added to PATH.
    pause
)
