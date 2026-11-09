@echo off
chcp 65001 >nul
rem Roda o programa a partir do codigo.
setlocal
cd /d "%~dp0.."
call scripts\_ambiente.bat || exit /b 1
"%PY%" -m chamados %*
