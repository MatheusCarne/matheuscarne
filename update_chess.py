import requests

USERNAME = "SEU_USUARIO_CHESS"  # Substitua aqui
README_PATH = "README.md"

def get_ratings(username):
    url = f"https://api.chess.com/pub/player/{username}/stats"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Erro ao buscar dados do Chess.com")
    data = response.json()
    return {
        "bullet": data["chess_bullet"]["last"]["rating"],
        "blitz": data["chess_blitz"]["last"]["rating"],
        "rapid": data["chess_rapid"]["last"]["rating"],
    }

def update_readme(ratings):
    with open(README_PATH, "r", encoding="utf-8") as file:
        content = file.read()

    new_section = f"""
### ♟️ Meu rating no Chess.com
- Bullet: {ratings['bullet']}
- Blitz: {ratings['blitz']}
- Rapid: {ratings['rapid']}
""".strip()

    start = "<!--chess-start-->"
    end = "<!--chess-end-->"
    updated = f"{start}\n{new_section}\n{end}"
    
    if start in content and end in content:
        content = content.split(start)[0] + updated + content.split(end)[1]
    else:
        content += f"\n\n{updated}"

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(content)

if __name__ == "__main__":
    ratings = get_ratings(USERNAME)
    update_readme(ratings)
