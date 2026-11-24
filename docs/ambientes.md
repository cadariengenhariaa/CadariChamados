# Ambientes: Testes e Produção

O programa tem dois ambientes. Toda alteração é desenvolvida e validada em **Testes** antes de chegar à equipe em **Produção**. Cada ambiente tem os próprios dados e a própria configuração, então nada do que se faz em Testes chega aos chamados reais.

## O que muda de um ambiente para o outro

| | Testes | Produção |
|---|---|---|
| Quem usa | TI (quem desenvolve e valida) | Toda a equipe |
| Pasta de dados | `Z:\Desenvolvimento\Dados\Chamados_Testes` | `Z:\Desenvolvimento\Dados\Chamados` |
| Banco, anexos e logs | `Chamados_Testes\saida\` | `Chamados\saida\` |
| `config.json` | `Chamados_Testes\entrada\`, com `"ambiente": "testes"` | `Chamados\entrada\` (sem o campo, vale Produção) |
| Quadro do FlowUp | 2815 TESTES GERAL (projeto 1273 Desenvolvimento) | 2271 CHAMADOS e PROTOCOLOS (projeto 151 SETOR DE QUALIDADE) |
| Seguidores fixos das tarefas | nenhum (ninguém é notificado) | Renata (10) |
| Executável | `Abertura de Chamados (TESTES).exe` | `Abertura de Chamados.exe` |
| Onde fica o exe | `Z:\Biblioteca\Padronização\Cadari\Executaveis\Testes` | `Z:\Biblioteca\Padronização\Cadari\Executaveis` |
| Branch de origem | `develop` | `main` |
| Como reconhecer na tela | faixa laranja "AMBIENTE DE TESTES" e `[TESTES]` no título | sem faixa |

O token do FlowUp é o mesmo nos dois `config.json` (é uma só instância do FlowUp). O que separa as tarefas é o quadro.

## Como o programa sabe em qual ambiente está

- **Executável:** o ambiente é gravado dentro do exe na hora de gerar (`scripts\gerar_executavel.bat testes` ou `producao`) e não muda depois. O exe de Testes só abre os dados de Testes; o de Produção, só os de Produção.
- **Código-fonte** (`scripts\executar.bat`, `scripts\diagnosticar_flowup.bat`): usa **Testes** por padrão. Para rodar contra Produção é preciso pedir de propósito:

  ```bat
  set CHAMADOS_AMBIENTE=producao
  scripts\diagnosticar_flowup.bat
  ```

  No PowerShell: `$env:CHAMADOS_AMBIENTE = "producao"`. Feche o terminal (ou rode `set CHAMADOS_AMBIENTE=`) quando terminar.

A variável `CHAMADOS_PASTA_DADOS` continua valendo para usar uma cópia local (ver [desenvolvimento.md](desenvolvimento.md#rodar-sem-mexer-nos-dados-reais)).

### Trava contra o ambiente errado

Ao abrir, o programa confere o ambiente (`conferir_ambiente()` em `src/chamados/config.py`). Se algo não combinar, ele mostra o motivo e **não abre**:

| Situação | Por que bloqueia |
|---|---|
| Programa de Testes apontando para a pasta de Produção | gravaria chamados de teste nos dados reais |
| Campo `ambiente` do `config.json` diferente do ambiente do programa | exe ou pasta trocados |
| `config.json` de Testes com token e `quadro_id` 2271 | criaria tarefas de teste no quadro real |

A mesma conferência aparece como item "Ambiente" na janela **Verificar computador** e no diagnóstico (`scripts\diagnosticar_flowup.bat`).

## Atualizar os dados de Testes

Para validar com dados parecidos com os reais, copie os dados de Produção para Testes:

```bat
scripts\atualizar_testes.bat
```

O script pede confirmação e então:

- copia `chamados.db`, `anexos\` e `nomes_equipe.csv` de Produção para Testes (Produção só é lida);
- **apaga, na cópia, o vínculo de cada chamado com a tarefa do FlowUp** (`flowup_task_id`). As tarefas vinculadas são do quadro de Produção; sem isso, salvar um chamado antigo em Testes alteraria a tarefa real. Ao salvar um chamado com responsável em Testes, o programa cria uma tarefa nova no quadro TESTES GERAL;
- não mexe no `config.json` de Testes nem nos logs.

A cópia vai **sempre** de Produção para Testes. Nunca copie dados de Testes para Produção.

## Fluxo de publicação (Testes → Produção)

| Etapa | O que fazer | Git | Ambiente |
|---|---|---|---|
| 1. Desenvolver | Branch a partir da `develop`, código e testes automáticos (`scripts\testar.bat`) | `feature/...`, `fix/...` | Código-fonte (Testes por padrão) ou cópia local |
| 2. Revisar | PR para a `develop`, revisão e **squash and merge** | `develop` | |
| 3. Publicar em Testes | Na `develop` atualizada: `scripts\gerar_executavel.bat testes` e copiar `dist\Abertura de Chamados (TESTES).exe` para `Executaveis\Testes` | `develop` | **Testes** |
| 4. Validar | Rodar o checklist abaixo com o exe de Testes. Achou problema: volta para a etapa 1 | | **Testes** |
| 5. Publicar em Produção | PR da `develop` para a `main`, tag `vX.Y.Z`, `scripts\gerar_executavel.bat producao`, Release com o `.zip` e cópia do exe para `Executaveis` ([desenvolvimento.md](desenvolvimento.md#distribuir-para-a-equipe)) | `main` | **Produção** |
| 6. Conferir | `set CHAMADOS_AMBIENTE=producao` e `scripts\diagnosticar_flowup.bat` sem erros; versão certa na barra de título | | **Produção** |

Voltar atrás em Produção: distribuir o exe anterior (guardado com a versão no nome).

### Checklist de validação em Testes

Antes de pedir o PR para a `main`, com o exe de Testes:

- [ ] a faixa "AMBIENTE DE TESTES" aparece e a versão no título é a nova;
- [ ] **Verificar computador** sem ERRO;
- [ ] abrir um chamado com imagem;
- [ ] designar o chamado e conferir a tarefa criada no quadro TESTES GERAL do FlowUp;
- [ ] alterar status e urgência e conferir a tarefa atualizada (a urgência vira a prioridade da tarefa);
- [ ] filtrar a lista e exportar CSV;
- [ ] finalizar e excluir o chamado de teste (a tarefa some do quadro);
- [ ] o que a alteração mudou, testado do jeito que a equipe vai usar.

Anote no PR para a `main` quem validou e quando.

### Mudança no banco de dados

Quando a versão nova altera a estrutura do banco (coluna nova, por exemplo), a alteração acontece sozinha na primeira abertura. Por isso:

1. Rode `scripts\atualizar_testes.bat` para ter uma cópia recente dos dados reais.
2. Abra o exe de Testes: é nessa abertura que a alteração é aplicada na cópia. Confira se os chamados antigos continuam aparecendo.
3. Só depois publique em Produção. A primeira pessoa que abrir o exe novo aplica a alteração no banco real; faça uma cópia de `Chamados\saida\chamados.db` antes de distribuir.

## Criar o ambiente de Testes do zero

Se a pasta de Testes for perdida:

1. Crie `Z:\Desenvolvimento\Dados\Chamados_Testes` com as subpastas `entrada` e `saida`.
2. Copie o `config.json` de Produção para `entrada` e altere: `"ambiente": "testes"` (no topo do arquivo, fora de `"flowup"`), `projeto_id` 1273, `quadro_id` 2815, `seguidores_fixos` `[]` e os IDs de `status` do quadro TESTES GERAL (Novas 14512, Em andamento 14513, Pendência Interna 14518, Finalizadas 14514).
3. Rode `scripts\atualizar_testes.bat`.
4. Rode `scripts\diagnosticar_flowup.bat` (sem `CHAMADOS_AMBIENTE`): todos os itens devem dar OK.
