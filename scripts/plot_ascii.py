import asciichartpy as acp
from datetime import datetime
from fetch_ratings import load_history
import os

# Configurações
USERNAME = "Matheus_Carne"  # Substitua pelo seu username
RATING_TYPE = "rapid"       # "blitz", "bullet", etc.
MAX_POINTS = 20             # Número máximo de ratings no gráfico

def generate_chart():
    # Carrega o histórico
    history = load_history().get("history", [])
    
    if not history:
        return "⚠️ Nenhum dado de rating encontrado. Execute o workflow primeiro."
    
    # Prepara os dados para o gráfico (últimos MAX_POINTS ratings)
    ratings = [entry["rating"] for entry in history][-MAX_POINTS:]
    timestamps = [entry["timestamp"] for entry in history][-MAX_POINTS:]
    
    # Configurações do gráfico ASCII
    config = {
        "height": 15,                          # Altura do gráfico
        "format": "{:8.2f} ┤",                 # Formato dos valores Y
        "offset": 3                            # Espaçamento lateral
    }
    
    # Gera o gráfico
    chart = acp.plot(ratings, config)
    
    # Adiciona rótulos personalizados
    min_rating = min(ratings)
    max_rating = max(ratings)
    last_update = timestamps[-1] if timestamps else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""
Última atualização: {last_update}
Rating mínimo: {min_rating}
Rating máximo: {max_rating}

{chart}
"""
    
if __name__ == "__main__":
    print(generate_chart())
