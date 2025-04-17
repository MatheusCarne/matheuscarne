#!/usr/bin/env python3
import asciichartpy as acp
from datetime import datetime
from fetch_ratings import load_history
import os

# Configurações
USERNAME = "Matheus_Carne"
RATING_TYPE = "rapid"
MAX_POINTS = 20

def generate_chart():
    history = load_history().get("history", [])
    
    if not history:
        return "⚠️ Nenhum dado de rating encontrado. Execute o workflow primeiro."
    
    ratings = [entry["rating"] for entry in history][-MAX_POINTS:]
    timestamps = [entry["timestamp"] for entry in history][-MAX_POINTS:]
    
    config = {
        "height": 10,
        "format": "{:8.2f} ┤",
        "offset": 3
        # 👇 NÃO incluir "colors" aqui
    }

    chart = acp.plot(ratings, config)
    
    min_rating = min(ratings)
    max_rating = max(ratings)
    last_update = timestamps[-1] if timestamps else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""\
# ♟ Chess.com {RATING_TYPE.capitalize()} Rating - @{USERNAME}

Última atualização: {last_update}
Rating mínimo: {min_rating}
Rating máximo: {max_rating}

