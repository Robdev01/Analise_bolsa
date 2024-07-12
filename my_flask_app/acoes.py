import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import io
import base64



API_KEY = 'SUJX70BTEQR47160'  # Substitua pela sua chave de API da Alpha Vantage
BASE_URL = 'https://www.alphavantage.co/query'

def obter_dados_historicos(symbol):
    params = {
        'function': 'TIME_SERIES_MONTHLY',
        'symbol': symbol,
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    dados = response.json()
    return dados


def avaliar_acao(symbol, data):
    if 'Monthly Time Series' not in data:
        return "Erro: Dados da série temporal não encontrados.", None

    dados_mensais = data['Monthly Time Series']
    df = pd.DataFrame.from_dict(dados_mensais, orient='index')
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)

    ano_atual = datetime.datetime.now().year
    anos_recentes = df[df.index.year >= ano_atual - 10]['4. close']

    preco_medio = anos_recentes.mean()
    taxa_crescimento = (anos_recentes.iloc[0] - anos_recentes.iloc[-1]) / anos_recentes.iloc[-1]

    if taxa_crescimento > 0.1 and preco_medio > anos_recentes.iloc[-1]:
        recomendacao = "Ação vale a pena comprar"
    else:
        recomendacao = "Ação não vale a pena comprar"

    # Criar o gráfico
    img = io.BytesIO()
    plt.figure(figsize=(10, 6))
    plt.plot(anos_recentes.index, anos_recentes.values, marker='o')
    plt.title(f'Preço de Fechamento da Ação {symbol}')
    plt.xlabel('Data')
    plt.ylabel('Preço de Fechamento')
    plt.grid(True)
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return recomendacao, plot_url