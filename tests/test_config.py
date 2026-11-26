"""Testes de chamados.config: ambiente, pasta de dados, config.json e token."""

import json
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


class TestEscolhaDoAmbiente(unittest.TestCase):
    def test_testes_roda_como_ambiente_de_testes(self):
        self.assertEqual(config.AMBIENTE, "testes")
        self.assertTrue(config.EM_TESTES)

    def test_codigo_sem_variavel_usa_testes(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CHAMADOS_AMBIENTE", None)
            self.assertEqual(config.escolher_ambiente(), "testes")

    def test_codigo_com_variavel_producao(self):
        with mock.patch.dict(os.environ, {"CHAMADOS_AMBIENTE": "Producao"}):
            self.assertEqual(config.escolher_ambiente(), "producao")

    def test_valor_desconhecido_vira_testes(self):
        with mock.patch.dict(os.environ, {"CHAMADOS_AMBIENTE": "homologacao"}):
            self.assertEqual(config.escolher_ambiente(), "testes")

    def test_exe_usa_ambiente_gravado_e_ignora_variavel(self):
        pasta = os.path.join(PASTA_TESTE, "exe_falso")
        os.makedirs(pasta, exist_ok=True)
        with open(os.path.join(pasta, config.ARQUIVO_AMBIENTE_EXE), "w", encoding="utf-8") as f:
            f.write("producao\n")
        with mock.patch.object(config.sys, "frozen", True, create=True), \
                mock.patch.object(config, "PASTA_BASE", pasta), \
                mock.patch.dict(os.environ, {"CHAMADOS_AMBIENTE": "testes"}):
            self.assertEqual(config.escolher_ambiente(), "producao")

    def test_exe_antigo_sem_arquivo_e_producao(self):
        with mock.patch.object(config.sys, "frozen", True, create=True), \
                mock.patch.object(config, "PASTA_BASE", os.path.join(PASTA_TESTE, "nao_existe")):
            self.assertEqual(config.escolher_ambiente(), "producao")

    def test_ambientes_tem_pastas_diferentes(self):
        self.assertNotEqual(config.AMBIENTES["testes"]["pasta_dados"], config.AMBIENTES["producao"]["pasta_dados"])


class TestTravaDoAmbiente(unittest.TestCase):
    def gravar(self, dados):
        with open(config.ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
            json.dump(dados, f)

    def tearDown(self):
        if os.path.exists(config.ARQUIVO_CONFIG):
            os.remove(config.ARQUIVO_CONFIG)

    def test_sem_config_json_nao_bloqueia(self):
        self.assertIsNone(config.conferir_ambiente())

    def test_config_de_testes_com_quadro_de_testes_libera(self):
        self.gravar({"ambiente": "testes", "flowup": {"token": "t", "quadro_id": 2815}})
        self.assertIsNone(config.conferir_ambiente())

    def test_config_sem_campo_ambiente_e_producao_e_bloqueia_testes(self):
        self.gravar({"flowup": {"token": "t"}})
        self.assertEqual(config.ambiente_do_config(), "producao")
        self.assertIn("Produção", config.conferir_ambiente())

    def test_testes_com_quadro_de_producao_bloqueia(self):
        self.gravar({"ambiente": "testes", "flowup": {"token": "t", "quadro_id": config.QUADRO_PRODUCAO}})
        self.assertIn(str(config.QUADRO_PRODUCAO), config.conferir_ambiente())

    def test_testes_com_quadro_de_producao_sem_token_libera(self):
        self.gravar({"ambiente": "testes", "flowup": {"token": "", "quadro_id": config.QUADRO_PRODUCAO}})
        self.assertIsNone(config.conferir_ambiente())

    def test_testes_apontando_para_pasta_de_producao_bloqueia(self):
        with mock.patch.object(config, "PASTA_DADOS", config.AMBIENTES["producao"]["pasta_dados"]):
            self.assertIn("pasta de dados de Produção", config.conferir_ambiente())

    def test_producao_com_config_de_testes_bloqueia(self):
        self.gravar({"ambiente": "testes", "flowup": {"token": "t", "quadro_id": 2815}})
        with mock.patch.multiple(config, AMBIENTE="producao", NOME_AMBIENTE="Produção", EM_TESTES=False):
            self.assertIn("ambiente Testes", config.conferir_ambiente())

if __name__ == "__main__":
    unittest.main()
