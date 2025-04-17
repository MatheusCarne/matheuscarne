#!/usr/bin/env python3
import asciichartpy as acp
import re
from datetime import datetime
from fetch_ratings import load_history
import os

# Configurações
USERNAME = "Matheus_Carne"
RATING_TYPE = "rapid"       # "blitz", "bullet", etc.
MAX_POINTS = 20              # Número máximo de ratings no gráfico
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "ratings.json")

# Regex para remover códigos ANSI
ANSI_ESCAPE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def generate_chart():
    # Carrega o histórico
    history = load_history().get("history", [])
    if not history:
        return "⚠️ Nenhum dado de rating encontrado. Execute o workflow primeiro."

    # Prepara os dados para o gráfico (últimos MAX_POINTS ratings)
    ratings = [entry["rating"] for entry in history][-MAX_POINTS:]

    # Configurações do gráfico ASCII sem cores ANSI
    config = {
        "height": 15,               # Altura do gráfico
        "format": "{:8.2f} ┤",    # Formato dos valores Y
        "offset": 3                 # Espaçamento lateral
    }

    # Gera o gráfico sem especificar cores (usa padrão sem ANSI)
    chart = acp.plot(ratings, config)
    chart = ANSI_ESCAPE.sub('', chart)  # Remove códigos ANSI

    # Rótulos personalizados
    min_rating = min(ratings)
    max_rating = max(ratings)
    last_update = history[-1]["timestamp"]

    # Monta linhas do gráfico em Markdown
    lines = []
    lines.append(f"# ♟ Chess.com {RATING_TYPE.capitalize()} Rating - @{USERNAME}")
    lines.append("")
    lines.append(f"Última atualização: {last_update}")
    lines.append(f"Rating mínimo: {min_rating}")
    lines.append(f"Rating máximo: {max_rating}")
    lines.append("")
    lines.append("```")
    lines.append(chart)
    lines.append("```")

    return "\n".join(lines)

if __name__ == "__main__":
    # Imprime o gráfico completo
    print(generate_chart())
