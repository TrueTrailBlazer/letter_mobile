import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
from flask import Flask, jsonify

app = Flask(__name__)
application = app

USER = 'spklf'
YEAR = 2026

# SEU BANCO DE FRASES 
quotes_ahead = [
    "A vida passa muito rápido. Se não parar e olhar em volta, pode perdê-la. — Curtindo a Vida Adoidado",
    "Eu sinto a necessidade... a necessidade de velocidade! — Top Gun",
    "Eu sou a velocidade. — Carros",
    "Ao infinito e além! — Toy Story",
    "Para onde vamos, não precisamos de estradas. — De Volta Para o Futuro",
    "Eu sou o rei do mundo! — Titanic",
    "Eu posso fazer isso o dia todo. — Capitão América",
    "A Força é forte neste aqui. — Star Wars",
    "Eu sou inevitável. — Vingadores: Ultimato",
    "May the odds be ever in your favor. — Jogos Vorazes"
]

quotes_on_track = [
    "Perfeitamente equilibrado, como todas as coisas devem ser. — Vingadores: Guerra Infinita",
    "Um mago nunca se atrasa, Frodo Bolseiro. Ele chega exatamente quando pretende. — O Senhor dos Anéis",
    "Adoro quando um plano dá certo. — Esquadrão Classe A",
    "Tudo o que temos de decidir é o que fazer com o tempo que nos é dado. — O Senhor dos Anéis",
    "Hakuna Matata. Os seus problemas você deve esquecer. — O Rei Leão",
    "Isso vai servir, porco. Isso vai servir. — Babe, O Porquinho Atrapalhado",
    "Mantenha os amigos perto e os inimigos mais perto ainda. — O Poderoso Chefão",
    "A vida é como uma caixa de chocolates. — Forrest Gump"
]

quotes_behind = [
    "Corra, Forrest, corra! — Forrest Gump",
    "Houston, temos um problema. — Apollo 13",
    "Continue a nadar, continue a nadar... — Procurando Nemo",
    "Tick-tock, Clarice. — O Silêncio dos Inocentes",
    "Apertem os cintos, a noite vai ser agitada. — A Malvada",
    "Por que caímos? Para aprendermos a nos levantar. — Batman Begins",
    "Não acabou até que acabe. — Rocky Balboa",
    "Nós estamos no ultimato agora. — Vingadores: Guerra Infinita",
    "Get to the chopper! — Predador",
    "Eu voltarei. — O Exterminador do Futuro",
    "Chegou a hora de acelerar ou morrer. — Velozes e Furiosos"
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

    # Retorna o JSON puro e estruturado
    return jsonify({
        "vistos": watched,
        "dia": target,
        "saldo": saldo_str,
        "restam": restam,
        "projecao": projection,
        "porcentagem": percent,
        "cor": color,
        "mensagem": msg,
        "frase": quote
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
