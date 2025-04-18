#!/usr/bin/env python3
import json
import os
from datetime import datetime
import asciichartpy
import time

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
    timestamp = data["history"][-1]["timestamp"]
    # Garantir formato correto (string -> datetime -> struct_time)
    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return time.strftime("%a %b %d %H:%M:%S EDT %Y", dt.timetuple())

def generate_chart():
    ratings = load_history()
    if not ratings:
        return "No data available."

    config = {
        "height": 20,
        "format": lambda x: f"{x:7.2f}"
    }

    chart = asciichartpy.plot(ratings, config)

    output = (
        "```\n"
        "# ♟︎ Chess.com Ratings Chart #\n\n"
        "Rapid Rating\n"
        f"{chart}\n\n"
        f"Chart last updated - {get_last_timestamp()}\n"
        "```"
    )
    return output

if __name__ == "__main__":
    print(generate_chart())
