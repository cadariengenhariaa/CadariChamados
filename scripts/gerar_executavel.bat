@echo off
chcp 65001 >nul
rem Gera o executavel em dist\ com o PyInstaller e o .zip da versao para a Release.
rem Uso:  scripts\gerar_executavel.bat testes     exe do ambiente de Testes
rem       scripts\gerar_executavel.bat producao   exe do ambiente de Producao
rem O ambiente fica gravado dentro do exe (ver docs\ambientes.md).
rem Este projeto gera um .exe unico, com tela de abertura: por isso usa a receita
rem scripts\abertura_de_chamados.spec em vez das opcoes direto na linha de comando.
setlocal
cd /d "%~dp0.."

set "CHAMADOS_AMBIENTE=%~1"
if /i "%CHAMADOS_AMBIENTE%"=="testes" goto ambiente_ok
if /i "%CHAMADOS_AMBIENTE%"=="producao" goto ambiente_ok
echo Informe o ambiente do executavel:
echo   scripts\gerar_executavel.bat testes
echo   scripts\gerar_executavel.bat producao
exit /b 1
:ambiente_ok

call scripts\_ambiente.bat || exit /b 1

if not exist build mkdir build
"%PY%" -c "import chamados; print(chamados.__version__)" > build\versao.txt || exit /b 1
set /p VERSAO=<build\versao.txt
echo Gerando Abertura de Chamados versao %VERSAO% - ambiente %CHAMADOS_AMBIENTE%...

"%PY%" -m PyInstaller --noconfirm --clean --distpath dist --workpath build scripts\abertura_de_chamados.spec
if errorlevel 1 (
    echo A geracao do executavel falhou. Veja as mensagens acima.
    exit /b 1
)

if /i "%CHAMADOS_AMBIENTE%"=="testes" (
    echo.
    echo Pronto:
    echo   dist\Abertura de Chamados ^(TESTES^).exe   ^(copiar para Executaveis\Testes na rede^)
    exit /b 0
)

powershell -NoProfile -Command "Compress-Archive -Path 'dist\Abertura de Chamados.exe' -DestinationPath 'dist\CadariChamados-v%VERSAO%.zip' -Force"
if errorlevel 1 exit /b 1

echo.
echo Pronto:
echo   dist\Abertura de Chamados.exe          (copiar para a rede)
echo   dist\CadariChamados-v%VERSAO%.zip       (anexar na Release do GitHub)
