"""Testes de chamados.atualizar_testes: cópia dos dados de Produção para Testes."""

import os
import shutil
import sqlite3
import tempfile
import unittest

from tests import PASTA_TESTE  # noqa: F401  (pasta temporária antes de importar chamados)
from chamados import atualizar_testes


class TestAtualizarTestes(unittest.TestCase):
    def setUp(self):
        self.raiz = tempfile.mkdtemp(prefix="chamados_ambientes_")
        self.producao = os.path.join(self.raiz, "producao")
        self.testes = os.path.join(self.raiz, "testes")
        for pasta in (self.producao, self.testes):
            os.makedirs(os.path.join(pasta, "entrada"))
            os.makedirs(os.path.join(pasta, "saida"))
        os.makedirs(os.path.join(self.producao, "saida", "anexos"))
        with open(os.path.join(self.producao, "saida", "anexos", "C001_print.png"), "wb") as f:
            f.write(b"png")
        with open(os.path.join(self.producao, "entrada", "nomes_equipe.csv"), "w", encoding="utf-8") as f:
            f.write("Id,Name,Email\n10,Renata,\n")
        with open(os.path.join(self.testes, "entrada", "config.json"), "w", encoding="utf-8") as f:
            f.write('{"ambiente": "testes"}')
        conn = sqlite3.connect(os.path.join(self.producao, "saida", "chamados.db"))
        conn.execute("CREATE TABLE chamados (protocolo TEXT, flowup_task_id INTEGER)")
        conn.executemany("INSERT INTO chamados VALUES (?, ?)", [("C001", 51808), ("C002", None)])
        conn.commit()
        conn.close()

    def tearDown(self):
        shutil.rmtree(self.raiz, ignore_errors=True)

    def test_copia_banco_sem_vinculo_com_flowup(self):
        atualizar_testes.atualizar(self.producao, self.testes)
        conn = sqlite3.connect(os.path.join(self.testes, "saida", "chamados.db"))
        linhas = conn.execute("SELECT protocolo, flowup_task_id FROM chamados ORDER BY protocolo").fetchall()
        conn.close()
        self.assertEqual(linhas, [("C001", None), ("C002", None)])

    def test_producao_continua_igual(self):
        atualizar_testes.atualizar(self.producao, self.testes)
        conn = sqlite3.connect(os.path.join(self.producao, "saida", "chamados.db"))
        self.assertEqual(conn.execute("SELECT flowup_task_id FROM chamados WHERE protocolo='C001'").fetchone()[0],
                         51808)
        conn.close()

    def test_copia_anexos_e_equipe_e_preserva_config_de_testes(self):
        atualizar_testes.atualizar(self.producao, self.testes)
        self.assertTrue(os.path.isfile(os.path.join(self.testes, "saida", "anexos", "C001_print.png")))
        self.assertTrue(os.path.isfile(os.path.join(self.testes, "entrada", "nomes_equipe.csv")))
        with open(os.path.join(self.testes, "entrada", "config.json"), encoding="utf-8") as f:
            self.assertIn("testes", f.read())

    def test_recusa_mesma_pasta(self):
        with self.assertRaises(ValueError):
            atualizar_testes.atualizar(self.producao, self.producao)

    def test_recusa_sem_banco_de_producao(self):
        os.remove(os.path.join(self.producao, "saida", "chamados.db"))
        with self.assertRaises(FileNotFoundError):
            atualizar_testes.atualizar(self.producao, self.testes)


if __name__ == "__main__":
    unittest.main()
