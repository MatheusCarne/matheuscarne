#!/usr/bin/env python3
import requests
import json
import os
from datetime import datetime

# Configurações
USERNAME = "Matheus_Carne"  # Substitua pelo seu username
RATING_TYPE = "rapid"        # "rapid", "blitz" ou "bullet"
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "ratings.json")


def get_current_rating():
    """Busca o rating atual da API do Chess.com"""
    url = f"https://api.chess.com/pub/player/{USERNAME}/stats"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) GitHubActionsBot/1.0"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

    try:
        data = resp.json()
    except json.JSONDecodeError:
        print(f"❌ Response was not JSON: {resp.text[:200]!r}")
        return None

    stats_key = f"chess_{RATING_TYPE}"
    node = data.get(stats_key)
    if not node or "last" not in node:
        print(f"❌ '{stats_key}' not found in response; available keys: {list(data.keys())}")
        return None

    rating = node["last"].get("rating")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"✅ API returned rating {rating} for {stats_key} at {timestamp}")
    return {"rating": rating, "timestamp": timestamp}


def load_history():
    """Carrega o histórico de ratings do arquivo JSON"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"⚠️ Failed loading history ({e}), reinitializing.")
            data = {"history": []}
        if not isinstance(data.get("history"), list):
            data["history"] = []
        return data
    return {"history": []}


def save_history(entry):
    """Salva um novo rating no histórico"""
    history = load_history()
    history["history"].append(entry)
    history["history"] = history["history"][-30:]
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)
    print(f"💾 Saved to {HISTORY_FILE}")


if __name__ == "__main__":
    current = get_current_rating()
    if current:
        save_history(current)
        print(current["rating"])
    else:
        hist = load_history().get("history", [])
        fallback = hist[-1]["rating"] if hist else 0
        print(f"⚠️ Using fallback rating: {fallback}")
        print(fallback)
