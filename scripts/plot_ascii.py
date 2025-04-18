#!/usr/bin/env python3
import asciichartpy as acp
from datetime import datetime
from fetch_ratings import load_history

# Configurações
USERNAME = "Matheus_Carne"  # Seu username do Chess.com
RATING_TYPE = "rapid"       # Tipo de partida
MAX_POINTS = 20             # Máximo de pontos no gráfico

def generate_chart():
    # Carrega o histórico
    history = load_history().get("history", [])
    
    if not history:
        return "⚠️ Nenhum dado de rating encontrado. Execute o workflow primeiro."
    
    # Últimos MAX_POINTS
    ratings = [entry["rating"] for entry in history][-MAX_POINTS:]
    timestamps = [entry["timestamp"] for entry in history][-MAX_POINTS:]
    
    # Configurações do gráfico ASCII
    config = {
        "height": 15,
        "format": "{:8.2f} ┤",
        "offset": 3
    }

    chart = acp.plot(ratings, config)

    # Converte timestamp para data legível
    try:
        last_update = datetime.strptime(timestamps[-1], "%Y-%m-%d %H:%M:%S")
    except:
        last_update = datetime.now()

    ultima_data = last_update.strftime("%Y-%m-%d %H:%M:%S")
    min_rating = min(ratings)
    max_rating = max(ratings)

    # Retorna tudo dentro de um bloco de código para manter formatação no README
    return f"""```
♟ Chess.com {RATING_TYPE.capitalize()} Rating - @{USERNAME}
Última atualização: {ultima_data}
Rating mínimo: {min_rating}
Rating máximo: {max_rating}

{chart}
```"""

if __name__ == "__main__":
    print(generate_chart())
