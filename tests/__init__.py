"""
Testes automáticos do Controle de Chamados. Não acessam a rede, o drive Z: nem o FlowUp.

Rodar na pasta do projeto:
    scripts\\testar.bat

Este arquivo é importado antes de qualquer teste: aponta a pasta de dados para uma
pasta temporária ANTES de o pacote chamados ser importado (config lê a variável na importação).
"""

import os
import tempfile

PASTA_TESTE = tempfile.mkdtemp(prefix="chamados_teste_")
os.environ["CHAMADOS_PASTA_DADOS"] = PASTA_TESTE
os.environ.pop("CHAMADOS_FLOWUP_TOKEN", None)
