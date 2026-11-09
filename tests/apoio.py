"""Funções de apoio usadas por mais de um arquivo de teste."""

import json
from unittest import mock

from tests import PASTA_TESTE  # noqa: F401  (garante a pasta temporária antes de importar chamados)
from chamados import config


def resposta_falsa(status, corpo="", location=None):
    """Simula uma resposta do requests com o código HTTP, o corpo e o redirecionamento pedidos."""
    r = mock.Mock()
    r.status_code = status
    r.ok = status < 400
    r.is_redirect = 300 <= status < 400 and location is not None
    r.headers = {"Location": location} if location else {}
    r.text = corpo if isinstance(corpo, str) else json.dumps(corpo)
    r.json = (lambda: corpo) if not isinstance(corpo, str) else mock.Mock(side_effect=ValueError)
    return r


def gravar_config(token="token-de-teste", **extra):
    """Grava um config.json na pasta de dados temporária, com a seção flowup indicada."""
    dados = {"flowup": {"token": token, **extra}}
    with open(config.ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False)
