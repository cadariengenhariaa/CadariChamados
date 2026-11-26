# 0003. Ambientes de Testes e Produção

**Data:** novembro de 2026 · **Situação:** aceita · **Tarefa:** S01 (Chamados x Definição de ambientes)

## Contexto

Havia um único ambiente: a pasta `Z:\Desenvolvimento\Dados\Chamados` e o quadro CHAMADOS e PROTOCOLOS do FlowUp. Para testar, cada pessoa montava uma cópia local e apontava a variável `CHAMADOS_PASTA_DADOS` para ela. Isso só funcionava a partir do código, não permitia testar a integração sem criar tarefas no quadro real e não deixava claro, na tela, qual ambiente estava aberto. Rodar o código sem a variável gravava direto nos dados reais.

## Decisão

- Dois ambientes, cada um com pasta de dados, `config.json` e quadro do FlowUp próprios: Testes (`Z:\Desenvolvimento\Dados\Chamados_Testes`, quadro 2815 TESTES GERAL) e Produção (sem mudança).
- O ambiente do exe é gravado na geração (`gerar_executavel.bat testes|producao`, arquivo `ambiente.txt` dentro do exe). Não há chave para trocar depois: são dois executáveis com nomes diferentes.
- O código-fonte usa Testes por padrão; Produção só com `CHAMADOS_AMBIENTE=producao`.
- O `config.json` declara o ambiente (`"ambiente"`). Sem o campo, vale Produção, para o arquivo atual e os exes antigos continuarem funcionando sem mudança.
- Trava na abertura: o programa não abre se o ambiente do exe, a pasta e o `config.json` não combinarem, nem se Testes estiver com o quadro de Produção.
- Faixa laranja e `[TESTES]` no título no ambiente de Testes.
- Dados de Testes atualizados a partir de Produção por `scripts\atualizar_testes.bat`, apagando os vínculos com as tarefas do FlowUp na cópia. Nunca no sentido contrário.
- `develop` alimenta Testes; `main` alimenta Produção.

## Alternativas descartadas

- **Um exe só, com chave na tela ou no `config.json` para trocar de ambiente:** fácil de esquecer na posição errada, e um exe de Produção poderia abrir dados de teste.
- **Continuar só com a variável `CHAMADOS_PASTA_DADOS`:** não resolve o FlowUp nem quem testa pelo exe, e o padrão continuaria sendo Produção.
- **Quadro de testes dentro do projeto SETOR DE QUALIDADE:** o quadro TESTES GERAL do projeto Desenvolvimento já existe e serve para os testes dos programas internos.

## Consequências

- Versão 2.4.0. Produção não muda de pasta nem de configuração: a equipe só troca o exe quando a versão for distribuída.
- Quem gera o exe precisa informar o ambiente (`gerar_executavel.bat` sem argumento recusa).
- Quem roda o código passa a cair em Testes. Para o diagnóstico de Produção, `set CHAMADOS_AMBIENTE=producao`.
- Os protocolos de Testes seguem a numeração da cópia e podem repetir números de Produção; em Testes eles não têm valor.
- Fluxo e checklist em `docs/ambientes.md`.
