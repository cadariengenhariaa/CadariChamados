"""
Categorias e assuntos do formulário de abertura (também usados no filtro da lista).

No banco continuam nas colunas "software" (categoria) e "ferramenta" (assunto).
Ao alterar, gere o exe de novo e distribua (docs/desenvolvimento.md).
"""

FERRAMENTAS = {
    "Revit": ["Template", "Famílias", "Parâmetros", "Fórmulas", "Lookup table", "Vistas", "Licença", "Exportação",
              "Download de disciplinas complementares", "Plug-ins", "Outros"],
    "Dynamo": ["Pacotes", "Rotinas", "Python", "Erros", "Outros"],
    "AutoCAD": ["CTB", "Layer", "Exportação", "Comandos", "Licença", "Outros"],
    "Office": ["Macros", "Fórmulas", "Validação de dados", "Mala direta", "Licença", "Outros"],
    "Suporte TI": ["Programas internos", "Sugestão de automação", "Instalação e atualização", "Acesso e permissões",
                   "Rede e VPN", "FlowUp", "Computador e periféricos", "E-mail e comunicação", "Licenças", "Outros"],
    "Outros": ["Outros"],
}
