"""Testes da instância única (chamados/instancia.py)."""

import sys
import unittest
import uuid

from tests import PASTA_TESTE  # noqa: F401  (garante a pasta temporária antes de importar chamados)
from chamados import instancia


class TestNomeMutex(unittest.TestCase):
    def test_um_mutex_por_ambiente(self):
        self.assertNotEqual(instancia.nome_mutex("testes"), instancia.nome_mutex("producao"))
        self.assertTrue(instancia.nome_mutex("producao").startswith("Local\\"))


class TestJanelaDoPrograma(unittest.TestCase):
    def test_reconhece_a_janela_do_ambiente(self):
        self.assertTrue(instancia.e_janela_do_programa("Controle de Chamados (v2.5.0)", em_testes=False))
        self.assertTrue(instancia.e_janela_do_programa("Controle de Chamados (v2.5.0)  [TESTES]", em_testes=True))

    def test_nao_confunde_ambientes_nem_outras_janelas(self):
        self.assertFalse(instancia.e_janela_do_programa("Controle de Chamados (v2.5.0)  [TESTES]", em_testes=False))
        self.assertFalse(instancia.e_janela_do_programa("Controle de Chamados (v2.5.0)", em_testes=True))
        self.assertFalse(instancia.e_janela_do_programa("Verificação do computador", em_testes=False))


@unittest.skipUnless(sys.platform == "win32", "o mutex com nome só existe no Windows")
class TestInstanciaUnica(unittest.TestCase):
    def setUp(self):
        # Nome único por teste, para não esbarrar no programa aberto na mesma máquina
        self.ambiente = f"teste_{uuid.uuid4().hex}"

    def test_segunda_abertura_e_recusada(self):
        primeira = instancia.InstanciaUnica(self.ambiente)
        segunda = instancia.InstanciaUnica(self.ambiente)
        try:
            self.assertTrue(primeira.adquirir())
            self.assertFalse(segunda.adquirir())
        finally:
            primeira.liberar()
            segunda.liberar()

    def test_abre_de_novo_depois_de_fechar(self):
        primeira = instancia.InstanciaUnica(self.ambiente)
        self.assertTrue(primeira.adquirir())
        primeira.liberar()
        segunda = instancia.InstanciaUnica(self.ambiente)
        try:
            self.assertTrue(segunda.adquirir())
        finally:
            segunda.liberar()

    def test_ambientes_diferentes_abrem_juntos(self):
        testes = instancia.InstanciaUnica(self.ambiente + "_testes")
        producao = instancia.InstanciaUnica(self.ambiente + "_producao")
        try:
            self.assertTrue(testes.adquirir())
            self.assertTrue(producao.adquirir())
        finally:
            testes.liberar()
            producao.liberar()


if __name__ == "__main__":
    unittest.main()
