@echo off
chcp 65001 >nul
rem Roda os testes e gera o relatorio de cobertura em docs\gerado\cobertura.
setlocal
cd /d "%~dp0.."
call scripts\_ambiente.bat || exit /b 1
"%PY%" -m coverage run --source=src -m unittest discover -s tests -t .
"%PY%" -m coverage report
"%PY%" -m coverage html -d docs\gerado\cobertura
echo Relatorio em docs\gerado\cobertura\index.html
