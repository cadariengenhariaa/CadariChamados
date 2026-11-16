# 0001. Adotar o padrão de repositórios da Cadari

**Data:** novembro de 2026 · **Situação:** aceita

## Contexto

A reorganização da versão 2.3.0 ficou pela metade: módulos duplicados na raiz e em `chamados/`, `main.py` e `Bugs.py` juntos, `matriz/` e `assets/` com as mesmas imagens, testes em `testes/`, diagnóstico em `ferramentas/` e a receita do executável na raiz, com espaço no nome. Cada pessoa precisava lembrar comandos diferentes para testar e gerar o executável.

## Decisão

Seguir o Padrão de repositórios da Cadari Engenharia (versão 1.1):

- código em `src/chamados/`, com a versão só em `src/chamados/__init__.py` (`__version__`);
- ponto de entrada em `src/chamados/__main__.py` (`python -m chamados`);
- testes em `tests/`, um arquivo por módulo do núcleo;
- diagnóstico do FlowUp dentro do pacote (`chamados.diagnostico_flowup`), chamado por `scripts\diagnosticar_flowup.bat`;
- comandos em `scripts\` (`executar`, `testar`, `cobertura`, `gerar_executavel`, `limpar`) e `Makefile` na raiz;
- receita do executável em `scripts\abertura_de_chamados.spec`, chamada por `gerar_executavel.bat`;
- `.gitignore`, `.gitattributes` e modelo de PR padrão.

## Consequências

- O executável continua sendo um `.exe` único com tela de abertura (`--onefile` pelo `.spec`). É a exceção prevista no padrão: quando o build precisa de `.spec`, ele fica em `scripts\` e o `.bat` o chama.
- O nome de exibição continua "Abertura de Chamados" na janela e no executável; o pacote Python continua `chamados`.
- O comportamento do programa não muda.
