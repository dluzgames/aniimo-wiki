@echo off
title Aniimo Wiki - Servidor Local Offline
cd /d "%~dp0"
echo ============================================================
echo      ANIIMO WIKI - SERVIDOR LOCAL OFFLINE
echo ============================================================
echo.
echo Iniciando servidor em http://localhost:8080...
start http://localhost:8080/
python serve.py
pause
