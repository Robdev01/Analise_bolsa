from flask import Flask, render_template, request
from acoes import obter_dados_historicos, avaliar_acao  # Importando as funções necessárias

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    avaliacao = None
    url_grafico = None
    
    if request.method == 'POST':
        simbolo = request.form['symbol'].upper()
        
        # Garantindo que o símbolo da ação termine com '.SA' para a API da Alpha Vantage
        if not simbolo.endswith('.SA'):
            simbolo += '.SA'
        
        dados_acao = obter_dados_historicos(simbolo)
        
        # Verificando se ocorreu algum erro na obtenção dos dados
        if "Error Message" in dados_acao or "Note" in dados_acao:
            avaliacao = "Erro ao obter os dados da ação. Verifique o símbolo e tente novamente."
        else:
            avaliacao, url_grafico = avaliar_acao(simbolo, dados_acao)
    
    return render_template('index.html', avaliacao=avaliacao, url_grafico=url_grafico)

if __name__ == '__main__':
    app.run(debug=True)
