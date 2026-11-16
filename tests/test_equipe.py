"""Testes de chamados.equipe: mescla com o FlowUp e leitura e gravação do CSV."""

import os
import unittest

from tests.apoio import PASTA_TESTE
from chamados import equipe


class TestEquipe(unittest.TestCase):
    def test_mescla_com_flowup(self):
        atuais = [{"Id": 31, "Name": "Paulo", "Email": ""}, {"Id": 65, "Name": "Joao Gabriel Rodrigues", "Email": ""},
                  {"Id": 42, "Name": "Paloma", "Email": ""}]
        flowup = [{"Id": 31, "Name": "Lucas Gomes"}, {"Id": 65, "Name": "João Gabriel"}, {"Id": 80, "Name": "Nova  Pessoa"}]
        nova, alteracoes = equipe.mesclar(atuais, flowup)
        nomes = {p["Id"]: p["Name"] for p in nova}
        self.assertEqual(nomes, {31: "Lucas Gomes", 65: "Joao Gabriel Rodrigues", 80: "Nova Pessoa"})
        self.assertEqual(len(alteracoes), 3)  # 31 trocado, 80 incluído, 42 removido

    def test_grava_e_le_csv(self):
        arquivo = os.path.join(PASTA_TESTE, "equipe_teste.csv")
        equipe.gravar_csv([{"Id": 3, "Name": "Simone", "Email": "s@x"}], arquivo)
        self.assertEqual(equipe.ler_csv(arquivo), [{"Id": 3, "Name": "Simone", "Email": "s@x"}])

if __name__ == "__main__":
    unittest.main()
