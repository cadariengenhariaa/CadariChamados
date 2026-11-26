@echo off
chcp 65001 >nul
rem Copia os dados de Producao para o ambiente de Testes (banco, anexos e lista da equipe).
rem Producao so e lida. O config.json de Testes nao e alterado. Ver docs\ambientes.md.
setlocal
cd /d "%~dp0.."
call scripts\_ambiente.bat || exit /b 1
"%PY%" -m chamados.atualizar_testes %*
