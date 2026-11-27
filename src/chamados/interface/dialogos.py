"""
Janelas secundárias do programa: todas modais e com a identidade visual da Cadari.

- JanelaModal: base de toda janela que abre por cima da principal. Enquanto ela está
  aberta, a janela de baixo fica bloqueada (não recebe clique nem teclado) e só volta
  quando ela é fechada. Uma janela aberta por cima de outra bloqueia a de baixo da mesma forma.
- Dialogo / mensagem / perguntar: caixas de mensagem no lugar das
  caixas padrão do Windows, com topo azul, check dourado, linha dourada e rodapé diagonal.
"""

import os
import sys
import tkinter as tk
from tkinter import font as tkfont

import customtkinter

from chamados.config import resource_path
from chamados.interface import tema

_ABERTAS = []  # janelas modais abertas, da mais antiga para a mais nova


def janela_do_topo(padrao):
    """A janela que deve ser dona de uma nova janela modal: a última modal aberta ou a padrão."""
    abertas = [j for j in _ABERTAS if j.winfo_exists()]
    return abertas[-1] if abertas else padrao


def _bloquear(janela, bloquear):
    """No Windows, desabilita de fato a janela de baixo (clique nela faz a modal piscar)."""
    if sys.platform == "win32" and janela is not None:
        try:
            janela.attributes("-disabled", bloquear)
        except tk.TclError:
            pass


class JanelaModal(customtkinter.CTkToplevel):
    """Janela secundária modal, centralizada sobre a dona, com fundo e ícone da Cadari."""

    def __init__(self, master, titulo):
        self.dono = janela_do_topo(master)
        super().__init__(self.dono)
        self.title(titulo)
        self.configure(fg_color=tema.COR["fundo"])
        if self.dono.winfo_viewable():
            self.transient(self.dono)  # com a dona escondida, a janela também ficaria escondida
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind("<Escape>", lambda e: self.destroy())
        # O CustomTkinter troca o ícone das janelas secundárias logo depois de abrir; repõe o da Cadari.
        self.after(250, self._icone)

    def _icone(self):
        try:
            self.iconbitmap(resource_path(os.path.join("assets", "icone.ico")))
        except Exception:
            pass

    def centralizar(self, largura=None, altura=None):
        """Centraliza sobre a dona. Largura e altura em pixels de desenho (o CustomTkinter aplica a escala)."""
        if largura and altura:
            self.geometry(f"{largura}x{altura}")
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        if w <= 1:
            w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        if self.dono.winfo_viewable():
            x = self.dono.winfo_rootx() + (self.dono.winfo_width() - w) // 2
            y = self.dono.winfo_rooty() + (self.dono.winfo_height() - h) // 2
        else:
            x, y = (self.winfo_screenwidth() - w) // 2, (self.winfo_screenheight() - h) // 2
        tk.Toplevel.wm_geometry(self, f"+{max(0, x)}+{max(0, y)}")

    def ativar(self):
        """
        Bloqueia a dona, mostra por cima, prende o mouse e o teclado nesta janela e foca nela.
        Chamada só no fim da montagem: se algo falhar antes, a janela de baixo não fica travada.
        """
        _ABERTAS.append(self)
        _bloquear(self.dono, True)
        self.lift()
        self.focus_force()
        try:
            self.wait_visibility()
            self.grab_set()
        except tk.TclError:
            pass

    def destroy(self):
        if self in _ABERTAS:
            _ABERTAS.remove(self)
            _bloquear(self.dono, False)
            try:
                self.grab_release()
            except tk.TclError:
                pass
            anterior = janela_do_topo(None)
            try:
                if anterior is not None:
                    anterior.grab_set()
                self.dono.lift()
                self.dono.focus_force()
            except tk.TclError:
                pass
        super().destroy()


class Cabecalho(tk.Canvas):
    """Topo azul das janelas secundárias: check dourado e título em branco, caixa alta e negrito."""

    ALTURA = 56

    def __init__(self, pai, texto):
        super().__init__(pai, height=self.ALTURA, highlightthickness=0, bd=0)
        self.texto = texto
        self.bind("<Configure>", lambda e: self.desenhar())

    def desenhar(self):
        self.delete("all")
        h = round(self.ALTURA * tema.fator())
        self.configure(bg=tema.cor("topo"), height=h)
        check = round(h * 0.46)
        x = round(24 * tema.fator())
        tema.desenhar_check(self, x, (h - check) / 2, check)
        self.create_text(x + round(1.3 * check), h // 2 + 1, text=self.texto.upper(), anchor="w",
                         font=tema.fonte_tk(13, "bold"), fill=tema.BRANCO)


class Dialogo(JanelaModal):
    """
    Caixa de mensagem modal. Espera ser fechada e guarda em .resposta o texto do botão clicado
    (None se fechada pelo X ou Esc).
    """

    def __init__(self, master, titulo, texto, botoes=("OK",), principal=0, perigo=None):
        super().__init__(master, titulo)
        self.resposta = None
        self.resizable(False, False)
        Cabecalho(self, titulo).pack(fill="x")
        customtkinter.CTkFrame(self, height=3, fg_color=tema.DOURADO, corner_radius=0).pack(fill="x")
        tema.rotulo(self, texto, 11, "texto", wraplength=440).pack(anchor="w", fill="x", padx=28, pady=(22, 20))

        acoes = customtkinter.CTkFrame(self, fg_color="transparent")
        acoes.pack(fill="x", padx=28, pady=(0, 22))
        for i, nome in reversed(list(enumerate(botoes))):  # alinhados à direita, na ordem pedida
            tipo = "perigo" if nome == perigo else ("primario" if i == principal else "secundario")
            b = tema.botao(acoes, nome, lambda n=nome: self._responder(n), tipo=tipo,
                           width=max(110, tkfont.Font(font=tema.fonte_tk(11, "bold")).measure(nome) + 40))
            b.pack(side="right", padx=(10, 0))
            if i == principal:
                self.bind("<Return>", lambda e, n=nome: self._responder(n))
        tema.Rodape(self, altura=22).pack(fill="x", side="bottom")

        self.centralizar()
        self.ativar()
        self.bell()
        self.wait_window()

    def _responder(self, nome):
        self.resposta = nome
        self.destroy()


def _raiz(master):
    """A janela principal (ou a raiz do Tk) para abrir a caixa por cima."""
    return master if master is not None else tk._default_root


def mensagem(titulo, texto, master=None):
    """Mensagem com o botão OK (erros, avisos e informações). Espera a pessoa fechar."""
    Dialogo(_raiz(master), titulo, texto)


def perguntar(titulo, texto, sim="Sim", nao="Cancelar", master=None, perigo=False):
    """Pergunta de confirmação. True só se a pessoa clicar no botão de confirmar."""
    d = Dialogo(_raiz(master), titulo, texto, botoes=(sim, nao), principal=1 if perigo else 0,
                perigo=sim if perigo else None)
    return d.resposta == sim


def mensagem_sem_janela(titulo, texto):
    """
    Caixa de mensagem quando a janela principal ainda não existe (ex.: programa já aberto).
    Cria uma raiz escondida só para mostrar a caixa e a fecha em seguida.
    """
    pref = tema.ler_preferencias()
    customtkinter.set_appearance_mode("Dark" if pref.get("tema") == "escuro" else "Light")
    raiz = customtkinter.CTk()
    raiz.withdraw()
    try:
        Dialogo(raiz, titulo, texto)
    finally:
        raiz.destroy()
