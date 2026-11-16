# 0002. Centralizar os dados em Z:\Desenvolvimento\Dados

**Data:** novembro de 2026 · **Situação:** aceita

## Contexto

Os dados do Chamados ficavam em `Processos BIM\Formulário de bugs\Banco de dados`, junto do executável, e misturavam o que o programa lê (token do FlowUp, lista da equipe) com o que ele grava (banco, anexos, logs). O executável precisa ser acessível a toda a equipe, mas a pasta do projeto não.

## Decisão

- Dados de todos os programas internos em `Z:\Desenvolvimento\Dados\<Programa>`; o do Chamados é `Z:\Desenvolvimento\Dados\Chamados`.
- Dentro de cada pasta de programa, `entrada\` guarda o que alimenta o programa e `saida\` o que ele produz.
- Executável publicado em `Z:\Biblioteca\Padronização\Cadari\Executaveis`. O programa não depende do lugar do exe: a pasta de dados é um caminho fixo em `config.py`.
- No banco, o caminho do anexo continua relativo (`anexos\...`), agora a partir de `saida\`.

## Consequências

- Versão 2.3.2. O exe 2.3.x procura o caminho antigo e para de funcionar; todos precisam do exe novo.
- Quem usa o programa precisa de leitura em `entrada` e leitura e gravação em `saida`.
