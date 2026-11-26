# -*- mode: python ; coding: utf-8 -*-
#
# Receita de compilação do "Abertura de Chamados.exe" (PyInstaller, arquivo único).
#
# Não rode este arquivo direto: use scripts\gerar_executavel.bat, que prepara o
# ambiente, chama este .spec e gera o .zip da versão para a Release.
#
# O executável sai em dist\Abertura de Chamados.exe (Produção) ou
# dist\Abertura de Chamados (TESTES).exe (Testes).
# Não apague este arquivo: ele é a fonte da compilação (ver docs/desenvolvimento.md).

import os

PASTA_PROJETO = os.path.dirname(SPECPATH)  # SPECPATH é a pasta scripts\ (definida pelo PyInstaller)
PASTA_SRC = os.path.join(PASTA_PROJETO, 'src')
ICONE = os.path.join(PASTA_PROJETO, 'assets', 'icone.ico')
TELA_ABERTURA = os.path.join(PASTA_PROJETO, 'assets', 'tela_abertura.png')

# Ambiente do exe (Testes ou Produção). Vem do gerar_executavel.bat pela variável
# CHAMADOS_AMBIENTE e é gravado em ambiente.txt dentro do exe (lido por config.py).
AMBIENTE = os.environ.get('CHAMADOS_AMBIENTE', '').strip().lower()
if AMBIENTE not in ('testes', 'producao'):
    raise SystemExit('Defina o ambiente: scripts\\gerar_executavel.bat testes  ou  producao')
PASTA_BUILD = os.path.join(PASTA_PROJETO, 'build')
os.makedirs(PASTA_BUILD, exist_ok=True)
ARQUIVO_AMBIENTE = os.path.join(PASTA_BUILD, 'ambiente.txt')
with open(ARQUIVO_AMBIENTE, 'w', encoding='utf-8') as f:
    f.write(AMBIENTE)
NOME_EXE = 'Abertura de Chamados' + (' (TESTES)' if AMBIENTE == 'testes' else '')

a = Analysis(
    [os.path.join(PASTA_SRC, 'chamados', '__main__.py')],
    pathex=[PASTA_SRC],
    binaries=[],
    datas=[(os.path.join(PASTA_PROJETO, 'assets'), 'assets'), (ARQUIVO_AMBIENTE, '.')],
    # babel.numbers: exigido pelo tkcalendar.
    # PIL._tkinter_finder: só faz falta se compilar fora do Windows; no Windows não atrapalha.
    hiddenimports=['babel.numbers', 'PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
# Tela de abertura do PyInstaller: exige Tcl/Tk "threaded", que o Python 3.14 (Tcl/Tk 9) não tem.
# Nesse caso o exe sai sem ela e o programa mostra só a própria tela de carregamento.
import sys
extras_splash = []
if sys.version_info < (3, 14):
    splash = Splash(
        TELA_ABERTURA,
        binaries=a.binaries,
        datas=a.datas,
        text_pos=None,
        text_size=12,
        minify_script=True,
        always_on_top=True,
    )
    extras_splash = [splash, splash.binaries]

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    *extras_splash,
    [],
    name=NOME_EXE,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[ICONE],
)
