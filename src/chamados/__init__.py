"""
Controle de Chamados da Cadari.

Núcleo (sem interface):
    config.py ........ versão, pasta de dados, config.json e log
    categorias.py .... categorias e assuntos que aparecem no formulário
    database.py ...... banco SQLite dos chamados
    equipe.py ........ lista da equipe sincronizada com o FlowUp
    flowup_api.py .... chamadas HTTP à API do FlowUp
    servico.py ....... regras da integração (criar, atualizar e excluir tarefas)
    verificacao.py ... verificação do computador
    diagnostico_flowup.py ... diagnóstico da integração (python -m chamados.diagnostico_flowup)

Interface (CustomTkinter): pasta interface/.
Ponto de entrada: __main__.py (python -m chamados).
Visão geral: docs/arquitetura.md
"""

__version__ = "2.3.1"
