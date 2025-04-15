import requests
import json

# Pegando os dados históricos de rating (exemplo de resposta JSON do Chess.com)
def get_historical_ratings(Matheus_Carne):
    url = f"https://api.chess.com/pub/player/{matheus_Carne}/games"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Erro ao buscar dados do Chess.com")
    
    data = response.json()
    ratings = {"bullet": [], "blitz": [], "rapid": []}
    
    # Exemplo fictício de como pegar a evolução
    for game in data["games"]:
        ratings["bullet"].append(game["rating"])
    
    return ratings

# Gerar a URL do gráfico
def generate_chart_url(ratings):
    chart_data = {
        "type": "line",
        "data": {
            "labels": ["Jan", "Feb", "Mar"],  # Substituir com as datas reais
            "datasets": [
                {
                    "label": "Bullet",
                    "data": ratings["bullet"],
                    "fill": False,
                    "borderColor": "rgba(75,192,192,1)"
                },
                {
                    "label": "Blitz",
                    "data": ratings["blitz"],
                    "fill": False,
                    "borderColor": "rgba(153,102,255,1)"
                },
                {
                    "label": "Rapid",
                    "data": ratings["rapid"],
                    "fill": False,
                    "borderColor": "rgba(255,159,64,1)"
                }
            ]
        }
    }
    
    chart_url = f"https://quickchart.io/chart?c={json.dumps(chart_data)}"
    return chart_url

# Exemplo de uso
username = "Matheus_Carne"
ratings = get_historical_ratings(username)
chart_url = generate_chart_url(ratings)
print(chart_url)
