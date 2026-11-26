"""
Instância única do programa: impede que o Controle de Chamados seja aberto duas vezes.

Usa um mutex com nome do Windows, que o próprio sistema libera quando o processo
termina (inclusive se o programa travar ou for fechado pelo Gerenciador de Tarefas).
Cada ambiente tem o seu mutex, então o exe de Testes e o de Produção podem ficar
abertos ao mesmo tempo, mas nenhum deles duas vezes.

Fora do Windows (testes em Linux/WSL) a trava não se aplica e o programa sempre abre.
"""

import ctypes
import sys

ERRO_JA_EXISTE = 183  # ERROR_ALREADY_EXISTS
PREFIXO_TITULO = "Controle de Chamados"  # começo do título da janela principal (app.py)
MARCA_TESTES = "[TESTES]"  # fim do título da janela principal no ambiente de Testes


def nome_mutex(ambiente):
    """Nome do mutex no espaço da sessão do usuário ("Local\\"), um por ambiente."""
    return f"Local\\CadariControleDeChamados_{ambiente}"


class InstanciaUnica:
    """
    Trava de instância única. Use adquirir() na abertura; o mutex fica preso ao
    objeto e é liberado em liberar() ou quando o processo termina.
    """

    def __init__(self, ambiente):
        self.nome = nome_mutex(ambiente)
        self._handle = None

    def adquirir(self):
        """True se esta é a única instância aberta; False se o programa já está aberto."""
        if sys.platform != "win32":
            return True
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateMutexW.restype = ctypes.c_void_p
        handle = kernel32.CreateMutexW(None, False, self.nome)
        erro = ctypes.get_last_error()
        if not handle:
            return True  # sem conseguir criar a trava, não impede o uso do programa
        if erro == ERRO_JA_EXISTE:
            kernel32.CloseHandle(ctypes.c_void_p(handle))
            return False
        self._handle = handle
        return True

    def liberar(self):
        if self._handle and sys.platform == "win32":
            ctypes.WinDLL("kernel32").CloseHandle(ctypes.c_void_p(self._handle))
        self._handle = None


def e_janela_do_programa(titulo, em_testes):
    """True se o título é o da janela principal do programa no ambiente indicado."""
    return titulo.startswith(PREFIXO_TITULO) and (MARCA_TESTES in titulo) == bool(em_testes)


def trazer_janela_para_frente(em_testes):
    """
    Restaura e traz para frente a janela principal já aberta do mesmo ambiente.
    Retorna True se encontrou a janela.
    """
    if sys.platform != "win32":
        return False
    user32 = ctypes.windll.user32
    encontradas = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def conferir(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        tamanho = user32.GetWindowTextLengthW(hwnd)
        if tamanho:
            texto = ctypes.create_unicode_buffer(tamanho + 1)
            user32.GetWindowTextW(hwnd, texto, tamanho + 1)
            if e_janela_do_programa(texto.value, em_testes):
                encontradas.append(hwnd)
                return False
        return True

    user32.EnumWindows(conferir, 0)
    if not encontradas:
        return False
    hwnd = encontradas[0]
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, 9)  # SW_RESTORE
    user32.SetForegroundWindow(hwnd)
    return True
