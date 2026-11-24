"""
Atualiza os dados do ambiente de Testes com uma cópia dos dados de Produção.

Copia, sempre no sentido Produção -> Testes:
    saida\\chamados.db         banco (cópia consistente, pela API de backup do SQLite)
    saida\\anexos\\            imagens anexadas
    entrada\\nomes_equipe.csv  lista da equipe

Não copia o config.json (o de Testes aponta para o quadro de testes do FlowUp) nem os logs.
Na cópia do banco, o vínculo com as tarefas do FlowUp (flowup_task_id) é apagado: as tarefas
ligadas são do quadro de Produção, e salvar um chamado em Testes não pode alterá-las.

Uso, na pasta do projeto:
    scripts\\atualizar_testes.bat

O .bat equivale a "python -m chamados.atualizar_testes", com src no PYTHONPATH.
Detalhes: docs/ambientes.md
"""

import argparse
import os
import shutil
import sqlite3
import sys

from chamados.config import AMBIENTES


def _subpastas(pasta):
    return os.path.join(pasta, "entrada"), os.path.join(pasta, "saida")


def copiar_banco(origem, destino):
    """Copia o banco com a API de backup do SQLite e apaga os vínculos com o FlowUp. Devolve o total de chamados."""
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    if os.path.exists(destino):
        os.remove(destino)
    fonte = sqlite3.connect(f"file:{origem}?mode=ro", uri=True, timeout=10)
    alvo = sqlite3.connect(destino)
    try:
        fonte.backup(alvo)
        colunas = [linha[1] for linha in alvo.execute("PRAGMA table_info(chamados)")]
        if "flowup_task_id" in colunas:
            alvo.execute("UPDATE chamados SET flowup_task_id = NULL")
        alvo.commit()
        return alvo.execute("SELECT COUNT(*) FROM chamados").fetchone()[0]
    finally:
        alvo.close()
        fonte.close()


def atualizar(pasta_producao, pasta_testes):
    """Copia os dados de Produção para Testes. Devolve as linhas do resumo."""
    if os.path.normcase(os.path.abspath(pasta_producao)) == os.path.normcase(os.path.abspath(pasta_testes)):
        raise ValueError("A pasta de Testes é a mesma de Produção.")
    entrada_prod, saida_prod = _subpastas(pasta_producao)
    entrada_test, saida_test = _subpastas(pasta_testes)
    banco_prod = os.path.join(saida_prod, "chamados.db")
    if not os.path.isfile(banco_prod):
        raise FileNotFoundError(f"Banco de Produção não encontrado: {banco_prod}")
    if not os.path.isdir(pasta_testes):
        raise FileNotFoundError(f"Pasta de Testes não encontrada: {pasta_testes}")

    resumo = []
    total = copiar_banco(banco_prod, os.path.join(saida_test, "chamados.db"))
    resumo.append(f"chamados.db: {total} chamados copiados, vínculos com o FlowUp apagados")

    anexos_prod, anexos_test = os.path.join(saida_prod, "anexos"), os.path.join(saida_test, "anexos")
    if os.path.isdir(anexos_prod):
        if os.path.isdir(anexos_test):
            shutil.rmtree(anexos_test)
        shutil.copytree(anexos_prod, anexos_test)
        resumo.append(f"anexos: {len(os.listdir(anexos_test))} arquivos copiados")

    equipe_prod = os.path.join(entrada_prod, "nomes_equipe.csv")
    if os.path.isfile(equipe_prod):
        os.makedirs(entrada_test, exist_ok=True)
        shutil.copy2(equipe_prod, os.path.join(entrada_test, "nomes_equipe.csv"))
        resumo.append("nomes_equipe.csv copiado")
    return resumo


def main(argv=None):
    parser = argparse.ArgumentParser(description="Copia os dados de Produção para o ambiente de Testes.")
    parser.add_argument("--sim", action="store_true", help="não pede confirmação")
    args = parser.parse_args(argv)

    producao = AMBIENTES["producao"]["pasta_dados"]
    testes = AMBIENTES["testes"]["pasta_dados"]
    print(f"Produção: {producao}\nTestes:   {testes}\n")
    print("Os dados de Testes (banco, anexos e lista da equipe) serão SUBSTITUÍDOS pelos de Produção.")
    print("O config.json de Testes não é alterado. Produção só é lida.")
    if not args.sim and input("Continuar? (s/n) ").strip().lower() != "s":
        print("Nada foi alterado.")
        return 1
    try:
        for linha in atualizar(producao, testes):
            print(f"[ OK ] {linha}")
    except (OSError, ValueError, sqlite3.Error) as e:
        print(f"[ERRO] {e}")
        return 1
    print("\nPronto. Feche e abra o programa de Testes para ver os dados novos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
