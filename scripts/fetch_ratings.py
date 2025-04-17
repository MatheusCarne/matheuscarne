import requests
import json
import os
from datetime import datetime

# Configurações
USERNAME = "Matheus_Carne"  # 👈 Substitua pelo seu username
RATING_TYPE = "rapid"       # Pode ser "blitz" ou "bullet"
HISTORY_FILE = "scripts/ratings.json"  # Arquivo para armazenar histórico

def get_current_rating():
    """Busca o rating atual da API do Chess.com"""
    try:
        url = f"https://api.chess.com/pub/player/{USERNAME}/stats"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Lança erro se status != 200
        
        data = response.json()
        rating = data["stats"][RATING_TYPE]["last"]["rating"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            "rating": rating,
            "timestamp": timestamp
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Erro na API: {e}")
        return None
    except KeyError:
        print("Dados de rating não encontrados na resposta")
        return None

def load_history():
    """Carrega o histórico de ratings do arquivo JSON"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {"history": []}

def save_history(new_entry):
    """Salva um novo rating no histórico"""
    history_data = load_history()
    history_data["history"].append(new_entry)
    
    # Mantém apenas os últimos 30 registros (opcional)
    if len(history_data["history"]) > 30:
        history_data["history"] = history_data["history"][-30:]
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history_data, f, indent=2)

if __name__ == "__main__":
    # Pega o rating atual
    current = get_current_rating()
    
    if current:
        # Atualiza o histórico
        save_history(current)
        
        # Retorna apenas o valor do rating para uso no plot_ascii.py
        print(current["rating"])
    else:
        # Fallback: usa o último rating conhecido
        history = load_history()
        if history["history"]:
            print(history["history"][-1]["rating"])
        else:
            print(0)  # Valor padrão se não houver dados
