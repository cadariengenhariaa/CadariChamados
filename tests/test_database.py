"""Testes de chamados.database, com banco SQLite em pasta temporária."""

import os
import unittest

from tests.apoio import PASTA_TESTE
from chamados import config, database


class TestBanco(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        database.criar_tabela()

    def test_fluxo_basico_e_chamado_sem_tarefa(self):
        protocolo = database.registrar_chamado_db("Fulano", "Revit", "Famílias", "Teste", "desc", os.path.join("anexos", "x.png"))
        self.assertRegex(protocolo, r"^C\d{3,}$")

        # Designado e sem tarefa: aparece na lista de pendências
        self.assertTrue(database.atualizar_chamado_db(protocolo, "A", "B", "2026-10-20", "Visto", "obs", "teste"))
        pendentes = [c["protocolo"] for c in database.buscar_chamados_designados_sem_tarefa()]
        self.assertIn(protocolo, pendentes)

        # Salvar sem caminho de imagem mantém o anexo gravado
        chamado = database.buscar_chamado_por_protocolo(protocolo)
        self.assertEqual(chamado["caminho_imagem"], os.path.join("anexos", "x.png"))
        self.assertEqual(chamado["data_entrega"], "2026-10-20")

        database.salvar_flowup_id_db(protocolo, 4242)
        pendentes = [c["protocolo"] for c in database.buscar_chamados_designados_sem_tarefa()]
        self.assertNotIn(protocolo, pendentes)

    def test_caminho_relativo_de_anexo_aponta_para_a_pasta_de_dados(self):
        caminho = config.resolver_caminho_dados(os.path.join("anexos", "C001_print.png"))
        self.assertEqual(caminho, os.path.join(PASTA_TESTE, "anexos", "C001_print.png"))

if __name__ == "__main__":
    unittest.main()
