@echo off
chcp 65001 >nul
rem Prepara o ambiente virtual .venv na raiz do projeto. Usado pelos outros comandos.
rem Define PY (python do .venv) e PYTHONPATH (pasta src).
if exist ".venv\Scripts\python.exe" goto instalar
where py >nul 2>&1
if errorlevel 1 (
    echo Python nao encontrado. Instale o Python 3.12 e rode o comando de novo.
    exit /b 1
)
echo Criando o ambiente virtual .venv...
py -3.12 -m venv .venv
if errorlevel 1 exit /b 1
:instalar
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -q -r requirements-dev.txt
if errorlevel 1 exit /b 1
set "PY=%CD%\.venv\Scripts\python.exe"
set "PYTHONPATH=%CD%\src"
exit /b 0
