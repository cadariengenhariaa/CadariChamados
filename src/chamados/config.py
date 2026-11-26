"""
Configuração central do Sistema de Chamados.

Tudo o que depende do ambiente fica neste módulo ou no arquivo config.json
da pasta de dados: local da rede, token do FlowUp, IDs do FlowUp e log.
Nenhum outro módulo deve ter caminho de rede ou senha escrito no código.

Detalhes de cada campo: docs/configuracao.md
"""

import copy
import getpass
import json
import logging
import os
import sys
import tempfile
from datetime import datetime

from chamados import __version__

VERSAO = __version__  # a versão fica só em chamados/__init__.py

# Raiz do repositório (src/chamados/config.py -> três níveis acima). No exe, o
# PyInstaller descompacta os recursos em sys._MEIPASS.
PASTA_BASE = getattr(sys, "_MEIPASS", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


# ---------------------------------------------------------------------------
# Ambientes (Testes e Produção)
# ---------------------------------------------------------------------------
# Cada ambiente tem a própria pasta de dados (banco, anexos, logs, config.json) e,
# pelo config.json, o próprio quadro no FlowUp. Fluxo de publicação: docs/ambientes.md
#   exe            o ambiente é gravado na hora de gerar o exe
#                  (scripts\gerar_executavel.bat testes|producao) e não muda depois.
#   código-fonte   variável CHAMADOS_AMBIENTE; sem ela, Testes. Assim, rodar o
#                  código nunca grava na produção por engano.
AMBIENTES = {
    "producao": {"nome": "Produção", "pasta_dados": r"Z:\Desenvolvimento\Dados\Chamados"},
    "testes": {"nome": "Testes", "pasta_dados": r"Z:\Desenvolvimento\Dados\Chamados_Testes"},
}
AMBIENTE_PADRAO_CODIGO = "testes"
ARQUIVO_AMBIENTE_EXE = "ambiente.txt"  # criado pelo .spec dentro do exe
QUADRO_PRODUCAO = 2271  # quadro CHAMADOS e PROTOCOLOS: o ambiente de Testes nunca pode usar


def _ambiente_do_exe():
    """Ambiente gravado no exe, ou None quando o programa roda pelo código."""
    if not getattr(sys, "frozen", False):
        return None
    try:
        with open(os.path.join(PASTA_BASE, ARQUIVO_AMBIENTE_EXE), "r", encoding="utf-8") as f:
            return f.read().strip().lower()
    except OSError:
        return "producao"  # exe gerado antes da 2.4.0 (sem o arquivo) só existia em produção


def escolher_ambiente():
    """Nome do ambiente em uso ("producao" ou "testes"). Valor desconhecido vira Testes, o lado seguro."""
    nome = _ambiente_do_exe() or (os.environ.get("CHAMADOS_AMBIENTE") or AMBIENTE_PADRAO_CODIGO).strip().lower()
    return nome if nome in AMBIENTES else "testes"


AMBIENTE = escolher_ambiente()
NOME_AMBIENTE = AMBIENTES[AMBIENTE]["nome"]
EM_TESTES = AMBIENTE == "testes"

MARCA_TESTE = "[TESTE]"  # vai no título dos chamados e das tarefas criados no ambiente de Testes


def marcar_teste(titulo, em_testes=None):
    """
    Põe "[TESTE] " no começo do título quando o programa está no ambiente de Testes.
    Não repete a marca se ela já estiver lá. Em Produção, devolve o título como veio.
    """
    if not (EM_TESTES if em_testes is None else em_testes):
        return titulo
    texto = str(titulo or "").strip()
    if texto.upper().startswith(MARCA_TESTE):
        return texto
    return f"{MARCA_TESTE} {texto}".strip()

# ---------------------------------------------------------------------------
# Pasta de dados compartilhada
# ---------------------------------------------------------------------------
# Cada programa tem uma pasta própria dentro de Z:\Desenvolvimento\Dados e, dentro
# dela, os dados ficam separados em duas subpastas:
#   entrada\  o que alimenta o programa (config.json, nomes_equipe.csv)
#   saida\    o que o programa produz (chamados.db, anexos\, logs\)
# Fica na rede e NUNCA vai para o GitHub. A pasta vem do ambiente; para testar
# com uma cópia local, defina a variável CHAMADOS_PASTA_DADOS (ver docs/desenvolvimento.md).
PASTA_DADOS_PADRAO = AMBIENTES[AMBIENTE]["pasta_dados"]
PASTA_DADOS = os.environ.get("CHAMADOS_PASTA_DADOS") or PASTA_DADOS_PADRAO

PASTA_ENTRADA = os.path.join(PASTA_DADOS, "entrada")
PASTA_SAIDA = os.path.join(PASTA_DADOS, "saida")

ARQUIVO_CONFIG = os.path.join(PASTA_ENTRADA, "config.json")
ARQUIVO_EQUIPE = os.path.join(PASTA_ENTRADA, "nomes_equipe.csv")
ARQUIVO_BANCO = os.path.join(PASTA_SAIDA, "chamados.db")
PASTA_ANEXOS = os.path.join(PASTA_SAIDA, "anexos")
PASTA_LOGS = os.path.join(PASTA_SAIDA, "logs")


def resource_path(relative_path):
    """Local de um arquivo a partir da raiz do projeto (ex.: assets/icone.ico), no código ou no exe."""
    return os.path.join(PASTA_BASE, relative_path)


def recurso(*partes):
    """Local de um arquivo da pasta assets/, no código ou no exe (ex.: recurso("icone.ico"))."""
    return os.path.join(PASTA_BASE, "assets", *partes)


def resolver_caminho_dados(caminho):
    """Converte um caminho relativo salvo no banco (ex.: anexos/C001_print.png) em caminho absoluto dentro de saida."""
    if not caminho:
        return caminho
    if os.path.isabs(caminho):
        return caminho
    return os.path.join(PASTA_SAIDA, caminho)


# ---------------------------------------------------------------------------
# FlowUp
# ---------------------------------------------------------------------------
# Valores padrão. O config.json da pasta de dados pode sobrescrever qualquer
# um deles; o token só existe lá (ou na variável CHAMADOS_FLOWUP_TOKEN).
FLOWUP_PADRAO = {
    "url_base": "https://api.flowup.me",
    "versao_api": "v1",
    "token": "",
    "projeto_id": 151,
    "quadro_id": 2271,
    "tag": {"Id": 286, "Name": "Chamados", "Color": "#ff4500", "Active": True},
    "seguidores_fixos": [10],
    # Urgência do chamado -> valor do campo Priority da tarefa no FlowUp (a API aceita 0 a 3).
    # A ordem daqui é a ordem da lista na tela. Confira os nomes no FlowUp e ajuste no config.json.
    "prioridades": {"Baixa": 0, "Média": 1, "Alta": 2, "Urgente": 3},
    # Status do quadro (os mesmos nomes do FlowUp). Ao abrir, o programa lê a lista atual do
    # quadro no FlowUp; estes valores só valem se o FlowUp não responder.
    "status": {
        "Novas": 11583,
        "Em andamento": 11585,
        "Pendência Interna": 11677,
        "Finalizadas": 11584,
    },
    "status_final": "Finalizadas",
    "timeout_segundos": 30,
}


URGENCIA_PADRAO = "Média"  # urgência escolhida ao abrir um chamado novo


def carregar_config_flowup():
    """
    Lê a seção "flowup" do config.json e completa com os valores padrão.

    Nunca lança exceção: se o arquivo não existir ou estiver inválido, devolve
    os padrões (sem token) e registra o problema no log. Quem chama decide o
    que fazer quando o token está vazio.
    """
    cfg = copy.deepcopy(FLOWUP_PADRAO)
    try:
        with open(ARQUIVO_CONFIG, "r", encoding="utf-8-sig") as f:
            dados = json.load(f)
        secao = dados.get("flowup", {}) if isinstance(dados, dict) else {}
        for chave, valor in secao.items():
            if chave == "status" and isinstance(valor, dict):
                cfg["status"].update(valor)
            elif chave == "prioridades" and isinstance(valor, dict) and valor:
                cfg["prioridades"] = valor  # substitui a lista inteira (nomes e ordem)
            else:
                cfg[chave] = valor
    except FileNotFoundError:
        logging.warning("config.json não encontrado em %s. Integração com o FlowUp desativada.", ARQUIVO_CONFIG)
    except (OSError, ValueError) as e:
        logging.error("Não foi possível ler %s: %s", ARQUIVO_CONFIG, e)

    token_ambiente = os.environ.get("CHAMADOS_FLOWUP_TOKEN")
    if token_ambiente:
        cfg["token"] = token_ambiente
    cfg["token"] = (cfg.get("token") or "").strip()
    return cfg


def ambiente_do_config():
    """
    Ambiente declarado no campo "ambiente" do config.json.

    Sem o campo, vale "producao" (o config.json de produção é anterior aos ambientes).
    Devolve None se o config.json não existir ou não puder ser lido.
    """
    try:
        with open(ARQUIVO_CONFIG, "r", encoding="utf-8-sig") as f:
            dados = json.load(f)
    except (OSError, ValueError):
        return None
    if not isinstance(dados, dict):
        return None
    return str(dados.get("ambiente") or "producao").strip().lower()


def _mesma_pasta(a, b):
    return os.path.normcase(os.path.normpath(a)) == os.path.normcase(os.path.normpath(b))


def conferir_ambiente():
    """
    Confere se a pasta de dados e o config.json combinam com o ambiente do programa.

    Devolve None quando está tudo certo, ou um texto explicando o problema. Com problema,
    o programa não abre: é a trava que impede o exe de Testes de gravar nos dados reais
    (e o de Produção de usar os dados de teste).
    """
    pasta_producao = AMBIENTES["producao"]["pasta_dados"]
    if EM_TESTES and _mesma_pasta(PASTA_DADOS, pasta_producao):
        return (f"O programa de Testes está apontando para a pasta de dados de Produção ({pasta_producao}). "
                "Confira a variável CHAMADOS_PASTA_DADOS.")
    declarado = ambiente_do_config()
    if declarado is not None and declarado != AMBIENTE:
        nome_declarado = AMBIENTES.get(declarado, {}).get("nome", declarado)
        return (f"Este programa é do ambiente {NOME_AMBIENTE}, mas o config.json da pasta de dados "
                f"({ARQUIVO_CONFIG}) é do ambiente {nome_declarado}. Use o executável do ambiente certo "
                "ou corrija o campo \"ambiente\" do config.json.")
    if EM_TESTES:
        cfg = carregar_config_flowup()
        if cfg.get("token") and int(cfg.get("quadro_id") or 0) == QUADRO_PRODUCAO:
            return (f"O config.json de Testes aponta para o quadro de Produção do FlowUp ({QUADRO_PRODUCAO}). "
                    "Troque o quadro_id pelo quadro de testes (docs/ambientes.md) ou deixe o token vazio.")
    return None


# ---------------------------------------------------------------------------
# Log
# ---------------------------------------------------------------------------
def usuario_atual():
    try:
        return getpass.getuser()
    except Exception:
        return "desconhecido"


def configurar_log():
    """
    Grava o log em <pasta de dados>/logs/AAAA-MM_<usuario>.log.
    Se a rede não estiver acessível, usa a pasta temporária do Windows.
    Devolve o arquivo de log em uso.
    """
    nome = f"{datetime.now():%Y-%m}_{usuario_atual()}.log"
    arquivo = None
    # Só usa a pasta da rede se ela já existir (o log não deve criar a pasta de dados)
    pastas = [PASTA_LOGS] if os.path.isdir(PASTA_DADOS) else []
    for pasta in pastas + [os.path.join(tempfile.gettempdir(), "chamados_logs")]:
        try:
            os.makedirs(pasta, exist_ok=True)
            arquivo = os.path.join(pasta, nome)
            handler = logging.FileHandler(arquivo, encoding="utf-8", delay=True)
            break
        except OSError:
            arquivo = None
            continue
    handlers = [logging.StreamHandler()]
    if arquivo:
        handlers.insert(0, handler)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(module)s] %(message)s",
        handlers=handlers,
        force=True,
    )
    return arquivo
