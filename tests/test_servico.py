"""Testes de chamados.servico: montagem da tarefa enviada ao FlowUp."""

import unittest

from chamados import config, servico


class TestServico(unittest.TestCase):
    def test_payload_leva_descricao_html(self):
        chamado = {"protocolo": "C100", "tema": "T", "nome_solicitante": "Ana", "responsavel": "Beto",
                   "software": "Revit", "ferramenta": "Famílias", "descricao": "linha 1\n<b>x</b>",
                   "observacoes": "urgente", "status": "Em andamento", "data_entrega": "2026-10-20"}
        p = servico.montar_payload(chamado, {"Ana": 1, "Beto": 2}, config.carregar_config_flowup())
        self.assertIn("linha 1<br>&lt;b&gt;x&lt;/b&gt;", p["Description"])
        self.assertIn("urgente", p["Description"])
        self.assertEqual((p["UserId"], p["StatusId"], p["FollowerUsers"]), (2, 11585, [1, 10]))
        self.assertEqual(p["StartDate"], "2026-10-20T08:00:00")

    def test_responsavel_fora_da_lista(self):
        with self.assertRaises(servico.ErroIntegracao):
            servico.montar_payload({"responsavel": "Fulano"}, {}, config.carregar_config_flowup())

if __name__ == "__main__":
    unittest.main()
