@echo off
title BanglaCode Studio
python gui.py
if errorlevel 1 (
  echo.
  echo BanglaCode Studio could not start.
  echo Make sure Python is installed and added to PATH.
  pause
)
