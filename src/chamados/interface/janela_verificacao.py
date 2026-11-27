"""
Janela com o resultado da verificação do computador (botão "Verificar computador").

É modal: enquanto está aberta, a janela principal fica bloqueada. A verificação só é
dada como concluída quando esta janela é fechada; até lá, um novo pedido é recusado.
"""

import customtkinter

from chamados import verificacao
from chamados.interface import tema
from chamados.interface.dialogos import JanelaModal


class JanelaVerificacao(JanelaModal):
    CORES = {verificacao.OK: ("#2E7D4F", "#7DC383"), verificacao.AVISO: ("#9A6B00", "#F2CF5B"),
             verificacao.ERRO: ("#8E2B2B", "#E08A84")}

    def __init__(self, master, itens):
        super().__init__(master, "Verificação do computador")
        self.itens = itens
        titulo = tema.TituloSecao(self, "Verificação do computador")
        titulo.pack(anchor="w", padx=24, pady=(20, 8))
        erros = sum(1 for i in itens if i.situacao == verificacao.ERRO)
        avisos = sum(1 for i in itens if i.situacao == verificacao.AVISO)
        resumo = ("Tudo certo: este computador tem o que o programa precisa." if not erros and not avisos else
                  f"{erros} erro(s) e {avisos} aviso(s). Erros impedem o uso; avisos limitam a integração com o FlowUp.")
        tema.rotulo(self, resumo, 11, "texto", wraplength=660).pack(anchor="w", padx=24)
        tema.Rodape(self, altura=22).pack(fill="x", side="bottom")  # antes da lista, para não ser espremido
        lista = customtkinter.CTkScrollableFrame(self, fg_color=tema.COR["painel"], corner_radius=0)
        lista.pack(fill="both", expand=True, padx=24, pady=12)
        lista.grid_columnconfigure(1, weight=1)
        for linha, it in enumerate(itens):
            customtkinter.CTkLabel(lista, text=it.situacao, width=64, text_color=self.CORES[it.situacao],
                                   font=tema.fonte(11, "bold"), anchor="w").grid(row=linha, column=0, sticky="nw",
                                                                                 padx=(12, 6), pady=6)
            texto = f"{it.nome}\n{it.detalhe}" + (f"\nO que fazer: {it.dica}" if it.dica else "")
            tema.rotulo(lista, texto, 10, "texto", wraplength=540).grid(row=linha, column=1, sticky="w", pady=6)
        acoes = customtkinter.CTkFrame(self, fg_color="transparent")
        acoes.pack(fill="x", padx=24, pady=(0, 18))
        tema.botao(acoes, "Copiar relatório", self.copiar, width=170).pack(side="left")
        tema.botao(acoes, "Fechar", self.destroy, tipo="secundario", width=100).pack(side="left", padx=10)
        self.copiado = tema.rotulo(acoes, "", 9)
        self.copiado.pack(side="left", padx=8)
        self.centralizar(720, 540)
        self.ativar()

    def destroy(self):
        verificacao.concluir_verificacao()
        super().destroy()

    def copiar(self):
        self.clipboard_clear()
        self.clipboard_append(verificacao.relatorio_texto(self.itens))
        self.copiado.configure(text="Relatório copiado. Cole no chamado de Suporte TI.")
