#!/usr/bin/env python3
import requests
import json
import os
from datetime import datetime

# Configurações
USERNAME = "Matheus_Carne"                   # Seu username
RATING_TYPE = "rapid"                        # "rapid", "blitz" ou "bullet"
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "ratings.json")

def get_current_rating():
    """Busca o rating atual da API do Chess.com"""
    url = f"https://api.chess.com/pub/player/{USERNAME}/stats"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
                      "GitHubActionsBot/1.0"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        stats_key = f"chess_{RATING_TYPE}"
        if stats_key not in data["stats"] or "last" not in data["stats"][stats_key]:
            print(f"❌ Chave '{stats_key}' não encontrada na resposta da API")
            return None

        rating = data["stats"][stats_key]["last"]["rating"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"✅ API retornou rating {rating} para {stats_key} em {timestamp}")
        return {"rating": rating, "timestamp": timestamp}

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na API: {e}")
        return None

def load_history():
    """Carrega o histórico de ratings do arquivo JSON"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                data = json.load(f)
                if "history" not in data:
                    data["history"] = []
                return data
            except json.JSONDecodeError:
                print(f"⚠️ {HISTORY_FILE} vazio ou corrompido; reinicializando.")
                return {"history": []}
    return {"history": []}

def save_history(new_entry):
    """Salva um novo rating no histórico"""
    history_data = load_history()
    history_data["history"].append(new_entry)
    # Mantém somente os 30 últimos registros
    history_data["history"] = history_data["history"][-30:]
    with open(HISTORY_FILE, "w") as f:
        json.dump(history_data, f, indent=2)
    print(f"💾 Novo rating salvo em {HISTORY_FILE}")

if __name__ == "__main__":
    current = get_current_rating()
    if current:
        save_history(current)
        print(current["rating"])
    else:
        hist = load_history().get("history", [])
        fallback = hist[-1]["rating"] if hist else 0
        print(f"⚠️ Usando fallback: {fallback}")
        print(fallback)
