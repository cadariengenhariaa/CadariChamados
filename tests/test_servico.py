"""Testes de chamados.servico: montagem da tarefa enviada ao FlowUp."""

import unittest
from unittest import mock

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

    def test_urgencia_vira_priority_no_payload(self):
        chamado = {"protocolo": "C101", "tema": "T", "nome_solicitante": "Ana", "responsavel": "Beto",
                   "urgencia": "Urgente"}
        p = servico.montar_payload(chamado, {"Ana": 1, "Beto": 2}, config.carregar_config_flowup())
        self.assertEqual(p["Priority"], 3)

    def test_chamado_antigo_sem_urgencia_nao_manda_priority(self):
        chamado = {"protocolo": "C102", "tema": "T", "nome_solicitante": "Ana", "responsavel": "Beto"}
        p = servico.montar_payload(chamado, {"Ana": 1, "Beto": 2}, config.carregar_config_flowup())
        self.assertNotIn("Priority", p)

    def test_tarefa_em_testes_tem_marca_no_comeco_do_titulo(self):
        chamado = {"protocolo": "C103", "tema": "Revit travando", "nome_solicitante": "Ana", "responsavel": "Beto"}
        p = servico.montar_payload(chamado, {"Ana": 1, "Beto": 2}, config.carregar_config_flowup())
        self.assertEqual(p["Title"], "[TESTE] Chamado C103 - Revit travando")

    def test_tema_ja_marcado_nao_repete_a_marca(self):
        chamado = {"protocolo": "C104", "tema": "[TESTE] Revit travando"}
        self.assertEqual(servico.titulo_tarefa(chamado), "[TESTE] Chamado C104 - Revit travando")

    def test_tarefa_em_producao_sem_marca(self):
        with mock.patch.object(config, "EM_TESTES", False):
            self.assertEqual(servico.titulo_tarefa({"protocolo": "C105", "tema": "Revit travando"}),
                             "Chamado C105 - Revit travando")

    def test_responsavel_fora_da_lista(self):
        with self.assertRaises(servico.ErroIntegracao):
            servico.montar_payload({"responsavel": "Fulano"}, {}, config.carregar_config_flowup())

if __name__ == "__main__":
    unittest.main()
