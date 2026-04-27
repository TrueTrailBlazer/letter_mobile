import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
from flask import Flask, render_template_string

app = Flask(__name__)
application = app  # Linha mágica necessária para o PythonAnywhere

USER = 'spklf'
YEAR = 2026

# BANCO DE FRASES DE FILMES ORIGINAL
quotes_ahead = [
    "A vida passa muito rápido. Se não parar e olhar em volta, pode perdê-la. <strong>— Curtindo a Vida Adoidado</strong>",
    "Eu sinto a necessidade... a necessidade de velocidade! <strong>— Top Gun</strong>",
    "Eu sou a velocidade. <strong>— Carros</strong>",
    "Ao infinito e além! <strong>— Toy Story</strong>",
    "Para onde vamos, não precisamos de estradas. <strong>— De Volta Para o Futuro</strong>",
    "Eu sou o rei do mundo! <strong>— Titanic</strong>",
    "Eu posso fazer isso o dia todo. <strong>— Capitão América</strong>",
    "A Força é forte neste aqui. <strong>— Star Wars</strong>",
    "Eu sou inevitável. <strong>— Vingadores: Ultimato</strong>",
    "May the odds be ever in your favor. <strong>— Jogos Vorazes</strong>"
]

quotes_on_track = [
    "Perfeitamente equilibrado, como todas as coisas devem ser. <strong>— Vingadores: Guerra Infinita</strong>",
    "Um mago nunca se atrasa, Frodo Bolseiro. Ele chega exatamente quando pretende. <strong>— O Senhor dos Anéis</strong>",
    "Adoro quando um plano dá certo. <strong>— Esquadrão Classe A</strong>",
    "Tudo o que temos de decidir é o que fazer com o tempo que nos é dado. <strong>— O Senhor dos Anéis</strong>",
    "Hakuna Matata. Os seus problemas você deve esquecer. <strong>— O Rei Leão</strong>",
    "Isso vai servir, porco. Isso vai servir. <strong>— Babe, O Porquinho Atrapalhado</strong>",
    "Mantenha os amigos perto e os inimigos mais perto ainda. <strong>— O Poderoso Chefão</strong>",
    "A vida é como uma caixa de chocolates. <strong>— Forrest Gump</strong>"
]

quotes_behind = [
    "Corra, Forrest, corra! <strong>— Forrest Gump</strong>",
    "Houston, temos um problema. <strong>— Apollo 13</strong>",
    "Continue a nadar, continue a nadar... <strong>— Procurando Nemo</strong>",
    "Tick-tock, Clarice. <strong>— O Silêncio dos Inocentes</strong>",
    "Apertem os cintos, a noite vai ser agitada. <strong>— A Malvada</strong>",
    "Por que caímos? Para aprendermos a nos levantar. <strong>— Batman Begins</strong>",
    "Não acabou até que acabe. <strong>— Rocky Balboa</strong>",
    "Nós estamos no ultimato agora. <strong>— Vingadores: Guerra Infinita</strong>",
    "Get to the chopper! <strong>— Predador</strong>",
    "Eu voltarei. <strong>— O Exterminador do Futuro</strong>",
    "Chegou a hora de acelerar ou morrer. <strong>— Velozes e Furiosos</strong>"
]

def get_day_of_year():
    now = datetime.now()
    start = datetime(YEAR, 1, 1)
    return (now - start).days + 1

def fetch_watched_count():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        url = f"https://letterboxd.com/{USER}/"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tenta extrair da estatística do ano na página de perfil
        stat_link = soup.select_one(f'a[href="/{USER}/films/diary/for/{YEAR}/"] .value')
        if not stat_link:
            stat_link = soup.select_one(f'a[href="/{USER}/diary/for/{YEAR}/"] .value')
            
        if stat_link:
            return int(stat_link.text.replace(',', ''))
    except:
        pass
    return 0 

@app.route('/meta')
def get_meta_widget():
    watched = fetch_watched_count()
    target = get_day_of_year()
    
    saldo = watched - target
    percent = round((watched / 365) * 100, 1)
    projection = round((watched / target) * 365) if target > 0 else 0
    restam = 365 - watched

    if saldo > 0:
        color = "#00e054"
        msg = f"Com folga de {saldo} filme(s)"
        quote = random.choice(quotes_ahead)
        saldo_str = f"+{saldo}"
    elif saldo == 0:
        color = "#40bcf4"
        msg = "Meta cravada no dia"
        quote = random.choice(quotes_on_track)
        saldo_str = str(saldo)
    else:
        color = "#ff4e00"
        msg = f"Faltando {abs(saldo)} filme(s) hoje"
        quote = random.choice(quotes_behind)
        saldo_str = str(saldo)

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #14181c; font-family: "Graphik-Semibold-Web", sans-serif; margin: 0; padding: 15px; color: #fff; }
            .section-heading { font-size: 14px; text-transform: uppercase; color: #9ab; border-bottom: 1px solid #2c3440; padding-bottom: 8px; margin-bottom: 15px; font-weight: bold; }
            .meta-stats-row { display: flex; justify-content: space-between; text-align: center; margin-bottom: 15px; border-bottom: 1px solid #2c3440; padding-bottom: 15px; }
            .meta-stat-item { display: flex; flex-direction: column; }
            .meta-stat-val { font-size: 21px; font-weight: 700; color: #fff; line-height: 1; margin-bottom: 4px; }
            .meta-stat-lbl { font-size: 10px; color: #89a; text-transform: uppercase; letter-spacing: 0.05em; }
            .meta-bar-bg { background: #2c3440; height: 4px; border-radius: 2px; overflow: hidden; margin-top: 5px; margin-bottom: 15px; }
            .meta-bar-fill { background: linear-gradient(90deg, #40bcf4 0%, #00e054 100%); height: 100%; width: {{ percent }}%; transition: width 0.5s ease; }
            .meta-msg-box { display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 12px; color: #9ab; background: #242b34; padding: 12px 10px; border-radius: 3px; text-align: center; }
            .meta-msg-main { display: flex; align-items: center; font-weight: bold; margin-bottom: 6px; }
            .meta-msg-dot { width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; background: {{ color }}; box-shadow: 0 0 5px {{ color }}; }
            .meta-quote { font-size: 10px; font-style: italic; color: #678; line-height: 1.3; }
            .meta-quote strong { font-weight: normal; color: #89a; }
        </style>
    </head>
    <body>
        <h2 class="section-heading">
            Meta 365 Filmes
            <span style="float: right; color: #678; font-weight: normal;">DIA {{ target }}/365</span>
        </h2>

        <div class="meta-stats-row">
            <div class="meta-stat-item"><span class="meta-stat-val">{{ watched }}</span><span class="meta-stat-lbl">Vistos</span></div>
            <div class="meta-stat-item"><span class="meta-stat-val" style="color:{{ color }}">{{ saldo_str }}</span><span class="meta-stat-lbl">Saldo</span></div>
            <div class="meta-stat-item"><span class="meta-stat-val">{{ restam }}</span><span class="meta-stat-lbl">Restam</span></div>
            <div class="meta-stat-item"><span class="meta-stat-val" style="color:#40bcf4">{{ projection }}</span><span class="meta-stat-lbl">Projeção</span></div>
        </div>

        <div style="display:flex; justify-content:space-between; font-size:11px; color:#89a; text-transform:uppercase; letter-spacing:0.05em;">
            <span>Progresso Anual</span><span style="color:#40bcf4; font-weight:bold">{{ percent }}%</span>
        </div>
        <div class="meta-bar-bg"><div class="meta-bar-fill"></div></div>

        <div class="meta-msg-box">
            <div class="meta-msg-main">
                <div class="meta-msg-dot"></div>
                <span style="color: #fff">{{ msg }}</span>
            </div>
            <div class="meta-quote">"{{ quote|safe }}"</div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_template, 
                                  target=target, watched=watched, saldo_str=saldo_str, 
                                  restam=restam, projection=projection, percent=percent, 
                                  color=color, msg=msg, quote=quote)

if __name__ == '__main__':
    app.run()
