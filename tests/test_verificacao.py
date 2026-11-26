"""Testes da trava de verificação única (chamados/verificacao.py)."""

import threading
import unittest

from tests import PASTA_TESTE  # noqa: F401  (garante a pasta temporária antes de importar chamados)
from chamados import verificacao


class TestUmaVerificacaoPorVez(unittest.TestCase):
    def tearDown(self):
        verificacao.concluir_verificacao()

    def test_segunda_verificacao_e_recusada(self):
        self.assertTrue(verificacao.iniciar_verificacao())
        self.assertTrue(verificacao.verificacao_em_andamento())
        self.assertFalse(verificacao.iniciar_verificacao())

    def test_libera_depois_de_concluir(self):
        self.assertTrue(verificacao.iniciar_verificacao())
        verificacao.concluir_verificacao()
        self.assertFalse(verificacao.verificacao_em_andamento())
        self.assertTrue(verificacao.iniciar_verificacao())

    def test_concluir_duas_vezes_nao_da_erro(self):
        verificacao.iniciar_verificacao()
        verificacao.concluir_verificacao()
        verificacao.concluir_verificacao()
        self.assertFalse(verificacao.verificacao_em_andamento())

    def test_recusa_vale_para_outra_thread(self):
        # A verificação roda em segundo plano; o clique seguinte vem da tela (outra thread)
        self.assertTrue(verificacao.iniciar_verificacao())
        resultado = []
        t = threading.Thread(target=lambda: resultado.append(verificacao.iniciar_verificacao()))
        t.start()
        t.join()
        self.assertEqual(resultado, [False])

    def test_mensagem_pedida_na_tarefa(self):
        self.assertEqual(verificacao.MENSAGEM_EM_ANDAMENTO,
                         "Já existe uma verificação em andamento. Finalize-a antes de iniciar uma nova.")


if __name__ == "__main__":
    unittest.main()
