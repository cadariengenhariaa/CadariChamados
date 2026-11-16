"""Testes de chamados.config: pasta de dados, config.json e token."""

import os
import unittest
from unittest import mock

from tests.apoio import PASTA_TESTE, gravar_config
from chamados import config


class TestRecursos(unittest.TestCase):
    def test_recurso_aponta_para_assets_na_raiz_do_projeto(self):
        self.assertTrue(os.path.isfile(config.recurso("icone.ico")))
        self.assertTrue(os.path.isfile(config.resource_path(os.path.join("assets", "marca_negativa.png"))))

    def test_versao_vem_do_pacote(self):
        import chamados
        self.assertEqual(config.VERSAO, chamados.__version__)


class TestConfig(unittest.TestCase):
    def tearDown(self):
        if os.path.exists(config.ARQUIVO_CONFIG):
            os.remove(config.ARQUIVO_CONFIG)

    def test_pasta_de_dados_vem_da_variavel_de_ambiente(self):
        self.assertEqual(config.PASTA_DADOS, PASTA_TESTE)

    def test_dados_separados_em_entrada_e_saida(self):
        entrada = os.path.join(PASTA_TESTE, "entrada")
        saida = os.path.join(PASTA_TESTE, "saida")
        self.assertEqual(os.path.dirname(config.ARQUIVO_CONFIG), entrada)
        self.assertEqual(os.path.dirname(config.ARQUIVO_EQUIPE), entrada)
        self.assertEqual(os.path.dirname(config.ARQUIVO_BANCO), saida)
        self.assertEqual(os.path.dirname(config.PASTA_ANEXOS), saida)
        self.assertEqual(os.path.dirname(config.PASTA_LOGS), saida)

    def test_sem_config_json_usa_padroes_sem_token(self):
        cfg = config.carregar_config_flowup()
        self.assertEqual(cfg["token"], "")
        self.assertEqual(cfg["quadro_id"], 2271)

    def test_prioridades_padrao_e_substituicao_pelo_config_json(self):
        self.assertEqual(list(config.carregar_config_flowup()["prioridades"]), ["Baixa", "Média", "Alta", "Urgente"])
        gravar_config(prioridades={"Normal": 0, "Crítica": 3})
        self.assertEqual(config.carregar_config_flowup()["prioridades"], {"Normal": 0, "Crítica": 3})

    def test_config_json_sobrescreve_e_completa_status(self):
        gravar_config(quadro_id=999, status={"Visto": 1})
        cfg = config.carregar_config_flowup()
        self.assertEqual(cfg["token"], "token-de-teste")
        self.assertEqual(cfg["quadro_id"], 999)
        self.assertEqual(cfg["status"]["Visto"], 1)
        self.assertEqual(cfg["status"]["Em andamento"], 11585)  # veio do padrão

    def test_variavel_de_ambiente_tem_prioridade_no_token(self):
        gravar_config(token="do-arquivo")
        with mock.patch.dict(os.environ, {"CHAMADOS_FLOWUP_TOKEN": "da-variavel"}):
            self.assertEqual(config.carregar_config_flowup()["token"], "da-variavel")

    def test_status_padrao_existem_no_quadro_documentado(self):
        ids_do_quadro = {11583, 11585, 11677, 11584}
        self.assertTrue(set(config.FLOWUP_PADRAO["status"].values()) <= ids_do_quadro)

if __name__ == "__main__":
    unittest.main()
