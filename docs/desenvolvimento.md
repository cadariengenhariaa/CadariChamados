# Desenvolvimento e distribuição

Passo a passo para preparar o computador, testar uma alteração, gerar o executável e entregar a versão nova para a equipe.

## Pré-requisitos

| Item | Como conferir |
|---|---|
| Windows 10 ou 11 | |
| Python 3.12, instalado com a opção "Add python.exe to PATH" | no terminal: `py -3.12 --version` |
| Git ou GitHub Desktop | no terminal: `git --version` |
| Acesso ao drive Z: (dados reais e distribuição do exe) | abrir `Z:\Biblioteca\Padronização\Cadari\Processos BIM\Formulário de bugs` no Explorer |

O Python 3.14 ainda não funciona com o PyInstaller neste projeto (a tela de abertura exige Tcl/Tk "threaded"). Use o 3.12.

## Preparar o ambiente

```bat
git clone https://github.com/cadariengenhariaa/FormularioBugs.git
cd FormularioBugs
scripts\testar.bat
```

Na primeira vez, qualquer comando de `scripts\` cria o ambiente virtual `.venv` (uma pasta com o Python e as bibliotecas só deste projeto) e instala o que está em `requirements-dev.txt`. Leva alguns minutos. No final deve aparecer `OK`.

O `.venv` é de cada computador e não vai para o GitHub. Se der problema, apague a pasta `.venv` e rode o comando de novo.

## Rodar sem mexer nos dados reais

O programa usa a pasta de dados do Z: por padrão. Para testar, crie uma cópia e aponte para ela:

1. Crie `C:\temp\chamados_teste`.
2. Copie para lá `chamados.db` e `nomes_equipe.csv` da pasta `Banco de dados` do Z:.
3. Copie também o `config.example.json` do repositório, renomeando para `config.json`, e deixe o token vazio. Assim a integração fica desligada e nenhum teste cria tarefa de verdade no FlowUp. Se precisar testar a integração, use o token real, mas saiba que as tarefas serão criadas no quadro de produção (apague-as depois) ou peça um quadro de testes e troque o `quadro_id`.
4. No Prompt de Comando, na pasta do repositório:

```bat
set CHAMADOS_PASTA_DADOS=C:\temp\chamados_teste
scripts\executar.bat
```

No PowerShell, troque a linha do `set` por `$env:CHAMADOS_PASTA_DADOS = "C:\temp\chamados_teste"`.

## Testes

```bat
scripts\testar.bat
```

Os testes ficam em `tests\`, um arquivo por módulo do núcleo (`test_config.py`, `test_database.py`, `test_equipe.py`, `test_flowup_api.py`, `test_servico.py`). Usam uma pasta temporária e simulam a API: não acessam a rede, o Z: nem o FlowUp. A pasta temporária é definida em `tests\__init__.py`, antes de o pacote `chamados` ser importado.

Para ver quanto do código os testes cobrem: `scripts\cobertura.bat` (relatório em `docs\gerado\cobertura\index.html`).

Antes de distribuir, faça também o teste manual com a cópia dos dados:

- [ ] abrir um chamado com imagem;
- [ ] designar esse chamado (com a integração desligada aparece o aviso de token ausente, o que é esperado);
- [ ] ver a lista, filtrar e exportar CSV;
- [ ] finalizar e excluir um chamado de teste;
- [ ] `scripts\diagnosticar_flowup.bat` sem erros na pasta real (ele é somente leitura).

## Gerar o executável

1. Aumente `__version__` em `src\chamados\__init__.py` e registre as mudanças no topo do `CHANGELOG.md`. Os dois números precisam ser iguais.
2. Na pasta do projeto:

```bat
scripts\gerar_executavel.bat
```

3. O resultado é `dist\Abertura de Chamados.exe` (cerca de 35 MB) e `dist\FormularioBugs-vX.Y.Z.zip`, o pacote para anexar na Release do GitHub. As pastas `build\` e `dist\` são temporárias e não vão para o GitHub.

O `.bat` usa a receita `scripts\abertura_de_chamados.spec`, que gera um `.exe` único com o pacote `chamados`, a pasta `assets` (imagens), o ícone, a tela de abertura e a importação oculta exigida pelo tkcalendar. Use sempre o `.bat`, em vez de montar o comando do PyInstaller à mão.

## Distribuir para a equipe

O exe não se atualiza sozinho. Cada pessoa roda uma cópia, então a versão nova precisa chegar a todos:

1. Guarde o exe anterior com a versão no nome (por exemplo `Abertura de Chamados 2.3.0.exe`) para poder voltar atrás.
2. Copie o exe novo para o local oficial na rede, na raiz de `Formulário de bugs`, ao lado da pasta `Banco de dados`.
3. Substitua as cópias das áreas de trabalho (ou troque por um atalho para o exe da rede).
4. Confira a versão na barra de título. O log de cada pessoa (`Banco de dados\logs`) registra a versão aberta, o que ajuda a achar quem ainda usa exe antigo.

Para voltar atrás, distribua o exe anterior. O banco é o mesmo para todas as versões 2.x.

## Fluxo de alteração

Segue o Processo de desenvolvimento do TI Cadari (detalhes no [README](../README.md#como-contribuir)):

1. Ticket no Jira em **Desenvolvimento**.
2. Branch a partir da `develop`: `feature/CHAVE-NN-descricao-curta`, `fix/...` ou `refactor/...`.
3. Commits no padrão `[CHAVE-NN] tipo: título no infinitivo`.
4. `scripts\testar.bat` passando e teste manual com a cópia dos dados.
5. PR para a `develop`, revisão de outra pessoa e **squash and merge**.
6. Para distribuir: PR da `develop` para a `main`, tag `vX.Y.Z`, Release no GitHub com o `.zip` anexado e cópia do exe na rede.

Antes de cada commit, confira o `git status`: a lista não pode ter `chamados.db`, `config.json`, `nomes_equipe.csv` nem nada dentro de `Banco de dados`. O `.gitignore` já bloqueia esses arquivos.

Se o token chegar a ser enviado ao GitHub por engano, apagar o arquivo depois não basta (ele fica no histórico). Troque o token (ver [configuracao.md](configuracao.md#quando-trocar-o-token)).
