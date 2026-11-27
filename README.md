<p align="center">
  <img src="assets/marca_cadari.png" alt="Marca da Cadari Engenharia" width="240">
</p>

# Abertura de Chamados

Programa interno da Cadari para a equipe pedir suporte, fazer a triagem dos pedidos e transformar cada chamado em tarefa no FlowUp.

**Status:** em produção · **Versão:** 2.5.0 · **Python:** 3.12 · [Histórico de versões](CHANGELOG.md)

## Índice

- [Sobre o projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Como usar](#como-usar)
- [Conceitos rápidos](#conceitos-rápidos)
- [Tecnologias](#tecnologias)
- [Instalação para desenvolvimento](#instalação-para-desenvolvimento)
- [Comandos](#comandos)
- [Gerar o executável](#gerar-o-executável)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Onde fica cada coisa](#onde-fica-cada-coisa)
- [Como contribuir](#como-contribuir)
- [Documentação](#documentação)
- [Pessoas desenvolvedoras](#pessoas-desenvolvedoras)
- [Licença](#licença)

## Sobre o projeto

Quando alguém da equipe tem um problema com Revit, Dynamo, AutoCAD, Office, suporte de TI ou outro assunto, abre um chamado por este programa. Quem cuida do suporte vê todos os chamados numa lista, define o responsável, o prazo e o status, e o programa cria e atualiza a tarefa correspondente no quadro CHAMADOS e PROTOCOLOS do FlowUp.

Todos os usuários trabalham sobre os mesmos dados, que ficam numa pasta da rede. O executável só lê e grava nessa pasta e chama a API do FlowUp.

| Entra | Sai |
|---|---|
| Pedido de suporte preenchido na tela (nome, categoria, assunto, tema, descrição e imagem opcional) | Chamado gravado com protocolo (C001, C002...) no banco da rede |
| Responsável, prazo e status definidos na triagem | Tarefa criada ou atualizada no FlowUp, com a descrição do chamado |

## Funcionalidades

- **Novo chamado:** na mesma tela a pessoa preenche o pedido e, se já souber, o responsável, o prazo e o status. O programa devolve o protocolo.
- **Tarefa no FlowUp:** com responsável definido, a tarefa é criada no FlowUp. Sem responsável, o chamado aguarda triagem na aba "Chamados".
- **Acompanhamento:** a aba "Chamados" tem a lista com filtros e o painel de detalhes, com os botões para salvar alterações (atualiza a tarefa) e excluir (apaga o chamado e a tarefa). Os status são os mesmos do quadro do FlowUp.
- **Equipe sincronizada:** a cada abertura, a lista de pessoas é atualizada com os usuários ativos do FlowUp.
- **Verificação do computador:** na abertura e pelo botão "Verificar computador", o programa confere a pasta da rede, a permissão de gravação, o banco e a conexão com o FlowUp, e mostra o que falta quando algo não está certo. Só uma verificação roda por vez.
- **Uma janela por vez:** o programa não abre duas vezes no mesmo computador (abrir de novo traz a janela que já está aberta), e as janelas secundárias (verificação, mensagens, confirmações) bloqueiam a principal até serem fechadas.
- **Tema claro e escuro, e zoom:** a escolha fica salva por pessoa.
- **Ambientes de Testes e Produção:** toda alteração é validada num exe de Testes, com dados e quadro do FlowUp próprios, antes de chegar à equipe ([docs/ambientes.md](docs/ambientes.md)).

## Como usar

Esta seção é para quem só usa o programa. Não precisa instalar Python nem Git.

1. Abra **Abertura de Chamados** pelo atalho da área de trabalho ou pela pasta `Z:\Biblioteca\Padronização\Cadari\Executaveis`.
2. Espere a tela de carregamento terminar. Se aparecer a janela de verificação com algum erro, siga a dica mostrada ao lado do item.
3. Na aba **Novo chamado**, preencha seu nome, a categoria, o assunto, o tema e a descrição. Se quiser, anexe um print pelo botão **Anexar imagem**.
4. Clique em **Registrar chamado** e anote o protocolo que aparece.
5. Para acompanhar, use a aba **Chamados**: filtre pela situação ou pelo nome e clique no chamado para ver os detalhes.

O computador precisa de acesso ao drive Z: e à internet (`https://api.flowup.me`). Se aparecer um erro, abra um chamado de Suporte TI com o print da tela e o relatório do botão **Verificar computador**.

## Conceitos rápidos

Termos que aparecem daqui para baixo, para quem não programa no dia a dia.

| Termo | O que significa aqui |
|---|---|
| Repositório | A pasta do projeto no GitHub, com todo o histórico de alterações. |
| Commit | Um registro de alteração no repositório, com uma mensagem dizendo o que mudou. |
| Branch | Uma cópia de trabalho do código, separada da versão oficial, onde uma tarefa é feita. |
| Pull Request (PR) | O pedido para juntar uma branch ao código oficial, com revisão de outra pessoa. |
| Chave da tarefa | O código da tarefa: `C0xx` quando vem de um chamado, `Sxx` quando é uma tarefa da Sprint. Vai na branch, no commit e no PR. |
| Terminal | A janela de comandos do Windows (Prompt de Comando ou PowerShell). |
| Ambiente virtual (`.venv`) | Uma pasta com o Python e as bibliotecas só deste projeto, para não misturar com outros. |
| Executável (`.exe`) | O programa pronto, que a equipe abre com dois cliques. |
| FlowUp | O sistema de gestão de tarefas da Cadari. O programa conversa com ele pela API (endereço `https://api.flowup.me`). |
| Token | A senha de acesso à API do FlowUp. Fica só no `config.json` da rede, nunca no código. |
| Ambiente | Conjunto de dados, configuração e executável. **Testes** é onde as alterações são validadas; **Produção** é o que a equipe usa. |

## Tecnologias

| Tecnologia | Para que é usada |
|---|---|
| Python 3.12 | Linguagem do programa (o 3.14 ainda não funciona com o PyInstaller neste projeto) |
| CustomTkinter 5.2.2 | Telas |
| tkcalendar 1.6.1 e babel 2.17.0 | Campos de data |
| Pillow 11.3.0 | Imagens (marca, anexos) |
| requests 2.32.5 | Chamadas à API do FlowUp |
| pendulum 3.1.0 | Datas e fuso horário |
| SQLite | Banco de chamados (`chamados.db` na rede) |
| unittest e coverage | Testes automáticos e relatório de cobertura |
| PyInstaller 6.16.0 | Geração do executável |

As versões exatas estão em [requirements.txt](requirements.txt) (programa) e [requirements-dev.txt](requirements-dev.txt) (desenvolvimento).

## Instalação para desenvolvimento

Esta seção é para quem vai alterar o código.

**Pré-requisitos**

| Item | Como conferir |
|---|---|
| Windows 10 ou 11 | |
| Python 3.12, instalado com a opção "Add python.exe to PATH" | no terminal: `py -3.12 --version` |
| Git ou GitHub Desktop | no terminal: `git --version` |
| Acesso ao drive Z: | abrir `Z:\Desenvolvimento\Dados\Chamados` no Explorer |

**Passo a passo**

1. Baixe o repositório. No terminal, dentro da pasta onde você guarda projetos:

   ```bat
   git clone https://github.com/cadariengenhariaa/CadariChamados.git
   cd CadariChamados
   ```

2. Rode os testes. Na primeira vez, o comando cria o ambiente virtual e instala as bibliotecas (leva alguns minutos):

   ```bat
   scripts\testar.bat
   ```

   No final deve aparecer `OK`.

3. A partir do código, o programa usa o **ambiente de Testes** (`Z:\Desenvolvimento\Dados\Chamados_Testes` e o quadro TESTES GERAL do FlowUp), sem mexer nos dados reais. Para usar uma cópia só sua, veja [docs/desenvolvimento.md](docs/desenvolvimento.md#rodar-sem-mexer-nos-dados-reais). Ambientes e fluxo de publicação: [docs/ambientes.md](docs/ambientes.md).

4. Abra o programa a partir do código:

   ```bat
   scripts\executar.bat
   ```

## Comandos

Todos rodam no terminal, a partir da pasta do repositório. Quem tem o `make` instalado pode usar a segunda coluna; o resultado é o mesmo.

| Windows | Com make | O que faz |
|---|---|---|
| `scripts\executar.bat` | `make executar` | Abre o programa a partir do código |
| `scripts\testar.bat` | `make testar` | Roda os testes automáticos |
| `scripts\cobertura.bat` | `make cobertura` | Roda os testes e mostra quanto do código eles cobrem (`docs\gerado\cobertura\index.html`) |
| `scripts\gerar_executavel.bat testes` | `make executavel AMBIENTE=testes` | Gera o executável de Testes em `dist\` |
| `scripts\gerar_executavel.bat producao` | `make executavel AMBIENTE=producao` | Gera o executável de Produção e o `.zip` da versão em `dist\` |
| `scripts\limpar.bat` | `make limpar` | Apaga as pastas geradas (`build\`, `dist\`, `docs\gerado\`) |
| `scripts\diagnosticar_flowup.bat` | `make diagnostico` | Confere o ambiente, a pasta de dados e a integração com o FlowUp, sem alterar nada (Testes, a não ser com `set CHAMADOS_AMBIENTE=producao`) |
| `scripts\atualizar_testes.bat` | `make atualizar-testes` | Copia os dados de Produção para o ambiente de Testes (pede confirmação) |

O diagnóstico aceita `--tarefa 51808` (mostra uma tarefa do FlowUp) e `--gerar-token` (gera um token novo). Detalhes em [docs/manutencao.md](docs/manutencao.md).

## Gerar o executável

Toda versão passa primeiro por Testes e só depois vai para Produção ([docs/ambientes.md](docs/ambientes.md#fluxo-de-publicação-testes--produção)).

1. Confira se a versão em `src\chamados\__init__.py` e a primeira entrada do `CHANGELOG.md` são a mesma.
2. Na `develop`, rode `scripts\gerar_executavel.bat testes`. Sai `dist\Abertura de Chamados (TESTES).exe`; copie para `Z:\Biblioteca\Padronização\Cadari\Executaveis\Testes` e faça o checklist de validação.
3. Validado, na `main` rode `scripts\gerar_executavel.bat producao`. O programa sai em `dist\Abertura de Chamados.exe` (um arquivo único) e o pacote para a Release em `dist\CadariChamados-vX.Y.Z.zip`.
4. Anexe o `.zip` na Release do GitHub e copie o `.exe` para `Z:\Biblioteca\Padronização\Cadari\Executaveis`. Passo a passo da distribuição em [docs/desenvolvimento.md](docs/desenvolvimento.md#distribuir-para-a-equipe).

## Estrutura do repositório

```
CadariChamados/
├── src/
│   └── chamados/                   # código do programa
│       ├── __init__.py             # versão (__version__)
│       ├── __main__.py             # ponto de entrada
│       ├── config.py               # ambiente, pasta de dados, config.json, recursos e log
│       ├── categorias.py           # categorias e assuntos do formulário
│       ├── database.py             # leitura e gravação no banco SQLite
│       ├── equipe.py               # sincronização da lista da equipe com o FlowUp
│       ├── flowup_api.py           # chamadas à API do FlowUp
│       ├── servico.py              # regras da integração (criar, atualizar e excluir tarefas)
│       ├── verificacao.py          # verificação do computador (rede, permissões, FlowUp)
│       ├── instancia.py            # instância única: o programa não abre duas vezes
│       ├── diagnostico_flowup.py   # diagnóstico da integração (scripts\diagnosticar_flowup.bat)
│       ├── atualizar_testes.py     # copia os dados de Produção para Testes (scripts\atualizar_testes.bat)
│       └── interface/              # telas (CustomTkinter)
├── tests/                          # testes automáticos (espelham src/chamados)
├── design/                         # especificação e decisões de design
├── assets/                         # marca, ícone e tela de abertura
├── scripts/                        # comandos do projeto (.bat) e receita do executável (.spec)
├── docs/                           # documentação (gerado/ fica fora do Git)
├── .github/                        # modelo de descrição de Pull Request
├── .gitignore                      # o que o Git nunca deve enviar
├── .gitattributes                  # fim de linha e arquivos binários
├── Makefile                        # os mesmos comandos de scripts/, para quem usa make
├── requirements.txt                # bibliotecas do programa
├── requirements-dev.txt            # bibliotecas de desenvolvimento
├── config.example.json             # modelo do config.json, sem token
├── CHANGELOG.md                    # histórico de versões
└── README.md                       # este arquivo
```

## Onde fica cada coisa

| O quê | Onde | Vai para o GitHub? |
|---|---|---|
| Código, imagens, testes e documentação | este repositório | Sim |
| O que alimenta o programa: `config.json` (token do FlowUp) e lista da equipe (`nomes_equipe.csv`) | Produção: `Z:\Desenvolvimento\Dados\Chamados\entrada`<br>Testes: `Z:\Desenvolvimento\Dados\Chamados_Testes\entrada` | **Não, nunca** |
| O que o programa produz: banco de chamados (`chamados.db`), anexos e logs | Produção: `Z:\Desenvolvimento\Dados\Chamados\saida`<br>Testes: `Z:\Desenvolvimento\Dados\Chamados_Testes\saida` | **Não, nunca** |
| Executável usado pela equipe (Produção) | `Z:\Biblioteca\Padronização\Cadari\Executaveis` (gerado em `dist\`) | Não (vai anexado na Release) |
| Executável de Testes (só TI) | `Z:\Biblioteca\Padronização\Cadari\Executaveis\Testes` | Não |

## Como contribuir

Toda alteração segue o Processo de desenvolvimento do TI Cadari. Cada alteração nasce de uma tarefa, e a chave dessa tarefa acompanha a branch, os commits e o PR, para que qualquer pessoa saiba de onde veio a mudança.

### Chave da tarefa

| Chave | Origem | Formato |
|---|---|---|
| `C0xx` | Chamado aberto neste programa | o protocolo do chamado (C + número) |
| `Sxx` | Tarefa planejada na Sprint | S + número da tarefa na Sprint |

### Passo a passo

1. Descubra a chave da tarefa (`C0xx` ou `Sxx`).
2. Crie a branch a partir da `develop`, com o tipo, a chave e uma descrição curta, sem espaço nem acento:
   - `feature/Sxx-descricao-curta` para funcionalidade nova;
   - `fix/C0xx-descricao-curta` para correção;
   - `refactor/...` para melhoria sem mudar o comportamento.
3. Faça os commits no padrão `[CHAVE] tipo: título no infinitivo` (tabela abaixo).
4. Rode `scripts\testar.bat` e teste pelo código, que usa o ambiente de Testes.
5. Abra o PR para a `develop` (confira a base antes de criar) e peça revisão:
   - **Título:** `[CHAVE] Abertura de Chamados x Nome da tarefa`;
   - **Descrição:** o modelo de `.github/pull_request_template.md` aparece sozinho. Preencha **O que foi feito** (as mudanças, em tópicos curtos), **Como testar** (os passos para quem revisa conferir) e **Tarefa** (a chave).
6. Depois da aprovação, faça o **squash and merge**: os commits da branch viram um só na `develop`.
7. Gere o exe de Testes a partir da `develop`, valide e só então abra o PR da `develop` para a `main` ([docs/ambientes.md](docs/ambientes.md)).

### Tipos de commit

| Tipo | Quando usar | Exemplo |
|---|---|---|
| `feat` | Nova funcionalidade | `[Sxx] feat: criar filtro por responsável` |
| `fix` | Correção de erro | `[C0xx] fix: corrigir data de entrega no FlowUp` |
| `docs` | Documentação | `[Sxx] docs: atualizar README com instalação` |
| `refactor` | Melhoria sem mudar comportamento | `[C0xx] refactor: extrair montagem da tarefa` |
| `test` | Testes automáticos | `[C0xx] test: adicionar testes da lista da equipe` |
| `style` | Formatação, sem mudar lógica | `[Sxx] style: padronizar indentação da interface` |
| `chore` | Configuração e dependências | `[Sxx] chore: atualizar versão do customtkinter` |

O título do commit usa verbo no infinitivo e completa a frase "Este commit vai...".

Regras do projeto:

- Token, senha e caminho de rede não entram no código. Ficam no `config.json` da pasta de dados ou em `src/chamados/config.py`.
- Valide no ambiente de Testes antes de distribuir uma versão nova.
- Se a integração com o FlowUp parar, rode `scripts\diagnosticar_flowup.bat` antes de mexer no código.

## Documentação

| Documento | Conteúdo |
|---|---|
| [docs/arquitetura.md](docs/arquitetura.md) | Organização do código, banco de dados e regras da integração com o FlowUp |
| [docs/configuracao.md](docs/configuracao.md) | `config.json`, token do FlowUp, IDs, lista da equipe e categorias do formulário |
| [docs/ambientes.md](docs/ambientes.md) | Ambientes de Testes e Produção e fluxo de publicação entre eles |
| [docs/desenvolvimento.md](docs/desenvolvimento.md) | Ambiente, testes, geração do executável e distribuição |
| [docs/manutencao.md](docs/manutencao.md) | Diagnóstico, erros comuns, logs, backup e histórico de incidentes |
| [design/decisoes/](design/decisoes/) | Decisões de design, uma por arquivo |
| [CHANGELOG.md](CHANGELOG.md) | O que mudou em cada versão |

## Pessoas desenvolvedoras

| Nome | Função |
|---|---|
| Henrique Viana | Desenvolvimento e manutenção |

## Licença

Uso interno da Cadari Engenharia. Todos os direitos reservados.
