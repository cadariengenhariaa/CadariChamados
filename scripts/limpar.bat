@echo off
chcp 65001 >nul
rem Apaga build\, dist\, docs\gerado\ e os __pycache__ do projeto.
setlocal
cd /d "%~dp0.."
for %%p in (build dist docs\gerado) do if exist "%%p" rd /s /q "%%p"
for /d /r src %%d in (__pycache__) do if exist "%%d" rd /s /q "%%d"
for /d /r tests %%d in (__pycache__) do if exist "%%d" rd /s /q "%%d"
if exist .coverage del /q .coverage
echo Limpo.
