"""
Ponto de entrada do Controle de Chamados da Cadari.

    python -m chamados              (a partir do código, com src no PYTHONPATH: scripts\\executar.bat)
    Abertura de Chamados.exe        (executável gerado por scripts\\gerar_executavel.bat)

Visão geral: README.md e docs/arquitetura.md
"""

import logging
import sys
import traceback

from chamados.config import NOME_AMBIENTE, PASTA_DADOS, VERSAO, conferir_ambiente, configurar_log, usuario_atual


def _registrar_erro_fatal(exc_type, exc, tb):
    logging.critical("Erro fatal:\n%s", "".join(traceback.format_exception(exc_type, exc, tb)))


def _fechar_tela_do_pyinstaller():
    """
    Fecha logo a tela de abertura do PyInstaller. Ela fica sempre por cima; se algo falhar
    durante a abertura, a mensagem de erro do Windows ficaria escondida atrás dela.
    """
    try:
        import pyi_splash
        pyi_splash.close()
    except Exception:
        pass


def main() -> int:
    """Configura o log e abre a janela principal. Retorna o código de saída do processo."""
    _fechar_tela_do_pyinstaller()
    arquivo_log = configurar_log()
    sys.excepthook = _registrar_erro_fatal
    logging.info("Controle de Chamados v%s (ambiente %s) iniciado por %s. Pasta de dados: %s. Log: %s",
                 VERSAO, NOME_AMBIENTE, usuario_atual(), PASTA_DADOS, arquivo_log)
    problema = conferir_ambiente()
    if problema:
        # Trava dos ambientes: não abre a janela para não gravar dados no ambiente errado
        logging.critical("Ambiente incorreto: %s", problema)
        _mostrar_erro(f"O Controle de Chamados não pode abrir.\n\n{problema}\n\nLog: {arquivo_log}")
        return 1
    try:
        from chamados.interface.app import App
        App().mainloop()
    except Exception:
        # Erro antes da janela abrir: registra e mostra, em vez de sumir sem aviso
        logging.critical("Falha ao abrir o programa:\n%s", traceback.format_exc())
        _mostrar_erro("O Controle de Chamados não conseguiu abrir.\n\n"
                      f"{traceback.format_exc(limit=1)}\nLog: {arquivo_log}")
        raise
    return 0


def _mostrar_erro(texto):
    """Caixa de erro do Windows, que aparece mesmo sem a janela do programa."""
    import ctypes
    try:
        ctypes.windll.user32.MessageBoxW(0, texto, "Controle de Chamados", 0x10)
    except Exception:
        pass


if __name__ == "__main__":
    sys.exit(main())
