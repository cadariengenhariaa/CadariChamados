"""Testes de chamados.flowup_api, com a API simulada (sem rede)."""

import os
import unittest
from unittest import mock

from tests.apoio import gravar_config, resposta_falsa
from chamados import config, flowup_api


class TestFlowupApi(unittest.TestCase):
    def setUp(self):
        gravar_config()

    def tearDown(self):
        os.remove(config.ARQUIVO_CONFIG)

    def test_cria_tarefa_no_endereco_novo(self):
        with mock.patch.object(flowup_api.requests, "request", return_value=resposta_falsa(200, {"taskId": 123})) as req:
            ok, resposta = flowup_api.criar_task_flowup({"Title": "x"})
        self.assertTrue(ok)
        self.assertEqual(flowup_api.extrair_task_id(resposta), 123)
        metodo, url = req.call_args[0]
        self.assertEqual((metodo, url), ("POST", "https://api.flowup.me/v1/Task/Create"))
        self.assertFalse(req.call_args[1]["allow_redirects"])
        self.assertEqual(req.call_args[1]["headers"]["Authorization"], "Bearer token-de-teste")

    def test_redirecionamento_vira_mensagem_clara(self):
        falsa = resposta_falsa(302, "<html>", location="/Error/NotFound")
        with mock.patch.object(flowup_api.requests, "request", return_value=falsa):
            ok, msg = flowup_api.criar_task_flowup({})
        self.assertFalse(ok)
        self.assertIn("redirecionamento", msg)

    def test_token_recusado(self):
        with mock.patch.object(flowup_api.requests, "request", return_value=resposta_falsa(401, "Acesso negado.")):
            ok, msg = flowup_api.atualizar_task_flowup({"Id": 1})
        self.assertFalse(ok)
        self.assertIn("401", msg)

    def test_sem_token_nao_chama_a_api(self):
        gravar_config(token="")
        with mock.patch.object(flowup_api.requests, "request") as req:
            ok, msg = flowup_api.criar_task_flowup({})
        self.assertFalse(ok)
        req.assert_not_called()

    def test_extrair_task_id_formatos(self):
        casos = [({"taskId": 5}, 5), ({"TaskId": 6}, 6), ({"Id": 7}, 7), ({"Result": {"Id": 8}}, 8),
                 ("9", 9), (10, 10), ("<html>", None), ({"Id": 0}, None), (True, None), (None, None)]
        for entrada, esperado in casos:
            self.assertEqual(flowup_api.extrair_task_id(entrada), esperado, entrada)

if __name__ == "__main__":
    unittest.main()
