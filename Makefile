# Comandos do projeto Abertura de Chamados.
#
# No Windows, cada alvo chama o .bat equivalente de scripts\, que é a
# referência. Em Linux ou WSL, os comandos rodam direto com o .venv.
#
#   make executar      abre o programa a partir do código
#   make testar        roda os testes automáticos
#   make cobertura     testes + relatório em docs/gerado/cobertura
#   make executavel    gera o executável e o .zip da versão em dist/
#   make limpar        apaga build/, dist/, docs/gerado/ e caches
#   make diagnostico   diagnóstico da integração com o FlowUp (somente leitura)
#
# Argumentos extras: make executar ARGS="--opcao"  ou  make diagnostico ARGS="--tarefa 51808"

ARGS ?=

.PHONY: all executar testar cobertura executavel limpar diagnostico

all: testar

ifeq ($(OS),Windows_NT)

SHELL := cmd.exe
.SHELLFLAGS := /c

executar:
	scripts\executar.bat $(ARGS)
testar:
	scripts\testar.bat
cobertura:
	scripts\cobertura.bat
executavel:
	scripts\gerar_executavel.bat
limpar:
	scripts\limpar.bat
diagnostico:
	scripts\diagnosticar_flowup.bat $(ARGS)

else

PY     := .venv/bin/python
NOME   := Abertura de Chamados
VERSAO  = $(shell PYTHONPATH=src $(PY) -c "import chamados; print(chamados.__version__)")
export PYTHONPATH := src

$(PY): requirements.txt requirements-dev.txt
	python3 -m venv .venv
	$(PY) -m pip install --disable-pip-version-check -q -r requirements-dev.txt
	@touch $(PY)

executar: $(PY)
	$(PY) -m chamados $(ARGS)

testar: $(PY)
	$(PY) -m unittest discover -s tests -t . -v

cobertura: $(PY)
	$(PY) -m coverage run --source=src -m unittest discover -s tests -t .
	$(PY) -m coverage report
	$(PY) -m coverage html -d docs/gerado/cobertura
	@echo "Relatório em docs/gerado/cobertura/index.html"

executavel: $(PY)
	$(PY) -m PyInstaller --noconfirm --clean --distpath dist --workpath build scripts/abertura_de_chamados.spec
	cd dist && zip -q "FormularioBugs-v$(VERSAO).zip" "$(NOME)"
	@echo "Pronto: dist/$(NOME) e dist/FormularioBugs-v$(VERSAO).zip"

diagnostico: $(PY)
	$(PY) -m chamados.diagnostico_flowup $(ARGS)

limpar:
	rm -rf build dist docs/gerado .coverage
	find src tests -name __pycache__ -type d -prune -exec rm -rf {} +

endif
