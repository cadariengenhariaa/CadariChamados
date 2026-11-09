@echo off
chcp 65001 >nul
rem Diagnostico da integracao com o FlowUp (somente leitura). Aceita os mesmos
rem argumentos do modulo: --tarefa 51808  ou  --gerar-token
setlocal
cd /d "%~dp0.."
call scripts\_ambiente.bat || exit /b 1
"%PY%" -m chamados.diagnostico_flowup %*
