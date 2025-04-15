import requests
import json

# Pegando os dados históricos de rating do Chess.com
def get_historical_ratings(username):
    url = f"https://api.chess.com/pub/player/{username}/rating"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Erro ao buscar dados do Chess.com: {response.text}")
    
    data = response.json()
    # Ajuste o tratamento dos dados de acordo com a estrutura da resposta
    ratings = {
        "bullet": [data.get('bullet', {}).get('rating', 0)],
        "blitz": [data.get('blitz', {}).get('rating', 0)],
        "rapid": [data.get('rapid', {}).get('rating', 0)],
    }
    return ratings


# Gerar a URL do gráfico para o QuickChart
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
username = "Matheus_Carne"  # Coloque o seu nome de usuário do Chess.com
ratings = get_historical_ratings(username)
chart_url = generate_chart_url(ratings)
print(chart_url)
