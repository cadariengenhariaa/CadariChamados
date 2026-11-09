@echo off
chcp 65001 >nul
rem Roda os testes automaticos de tests\.
setlocal
cd /d "%~dp0.."
call scripts\_ambiente.bat || exit /b 1
"%PY%" -m unittest discover -s tests -t . -v
