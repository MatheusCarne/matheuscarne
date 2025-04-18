#!/usr/bin/env python3
import json
import os
from datetime import datetime
import asciichartpy

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "ratings.json")

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)
    return [entry["rating"] for entry in data.get("history", [])]

def get_last_timestamp():
    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)
    if not data["history"]:
        return None
    return data["history"][-1]["timestamp"]

def generate_chart():
    ratings = load_history()
    if not ratings:
        return "No data available."

    chart = asciichartpy.plot(
        ratings,
        {
            "height": 20,
            "format": lambda x: f"{x:7.2f}",
        }
    )

    last_update = get_last_timestamp()
    min_rating = min(ratings)
    max_rating = max(ratings)

    output = (
        "```\n"
        "# ♟︎ Chess.com Ratings Chart #\n\n"
        "Rapid Rating\n"
        f"{chart}\n\n"
        f"Chart last updated - {last_update}\n"
        "```"
    )
    return output

if __name__ == "__main__":
    print(generate_chart())
