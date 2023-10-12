
"""Esse robô realizara a coleta do site 'https://blaze-1.com/pt/games/double',
fará uma analise a partir de padrões pré selecionados, logo após enviara uma menssagem de alerta
no canal/grupo do telegram indicando a cor que devera ser relizada a entra, por fim indicará se foi vitoria ou não!
"""
try:
    from os import system as sys
    import requests
    import time
    import json
    import telebot
except:
    print("------- INSTALANDO DEPENDÊNCIAS -------")
    sys("pip install requests==2.20.1")
    sys("pip install telebot==0.0.4")


def wait(max_attempts=20, retry_delay=1.5):
    for _ in range(max_attempts):
        try:
            response = requests.get(url + "/current")
            response_data = response.json()

            if response.status_code == 200:
                status = response_data.get("status")

                if status != "rolling":
                    return response_data
            time.sleep(retry_delay)

        except requests.exceptions.RequestException as e:
            time.sleep(retry_delay)

    print("Limite de tentativas atingido. Não foi possível aguardar um resultado.")
    return None

def wait_rolling(max_attempts=20, retry_delay=1.5):
    wait()
    for _ in range(max_attempts):
        try:
            response = requests.get(url + "/current")
            response_data = response.json()

            if response.status_code == 200:
                status = response_data.get("status")

                if status == "rolling":
                    return response_data
            time.sleep(retry_delay)

        except requests.exceptions.RequestException as e:
            time.sleep(retry_delay)

    print("Limite de tentativas atingido. Não foi possível aguardar um resultado.")
    return None

def initial_colors():
    wait()

def last_color(last_result):
    if last_result["color"] == 2:
        return "black"
    elif last_result["color"] == 1:
        return "red"
    else:
        return "white"

def list_results(list, last_color, max_result=10):
    list.append(last_color)
    if len(list) > max_result:
        list.pop(0)
    return list

def verific_pattern(results, black, red):
    for pattern in black:
        size_pattern = len(results) - len(pattern)
        if results[size_pattern:] == pattern:
            return "black"
    
    for pattern in red:
        size_pattern = len(results) - len(pattern)
        if results[size_pattern:] == pattern:
            return "red"
        
def send_signal(color, last_number, last_color):
    if last_color == "red":
        emoji = "🔴"
    elif last_color == "black":
        emoji = "⚫"
    else:
        emoji = "⚪"

    if color == "red":
        msg = f"""👑 SINAL DO PATINHAS 👑

ENTRAR NO 🔴 APÓS -> {last_number} {emoji}

⚪PROTEGENDO O BRANCO⚪
🐓 ATE G2 🐓"""
        bot.send_message(chat, msg)
        if bot_free:
            bot.send_message(chat_free, msg)

    if color == "black":
        msg = f"""👑 SINAL DO PATINHAS 👑

ENTRAR NO ⚫ APÓS -> {last_number} {emoji}

⚪PROTEGENDO O BRANCO⚪
🐓 ATE G2 🐓"""
        
        bot.send_message(chat, msg)
        if bot_free:
            bot.send_message(chat_free, msg)

def verific_win(color, signal, gale):
    msg_win = """✅✅ PAGAAAAA, WIN DO BRABO ✅✅

🤑 FAZ O PIX 🤑"""
    msg_branco = """✅⚪✅ 14X PAGO, PREPARA O PIX ✅⚪✅

⚪⚪ BRANQUINHO PAGO COM SUCESSO! ⚪⚪"""
    msg_loss = """❎❎ CALMAAA, PLATAFORMA LEVOU ❎❎

🤑 VAMO RECUPERAR 🤑"""
    if color == signal:
        bot.send_message(chat, msg_win)
        return True
    
    elif color == "white":
        bot.send_message(chat, msg_branco)
        return True
    
    elif gale >= 2:
        bot.send_message(chat, msg_loss)
        return True


url = "https://blaze.com/api/roulette_games"
list = []

with open('patterns.json', 'r') as arquivo_json:
    dados = json.load(arquivo_json)

black_paterns = dados['black']
red_paterns = dados['red']

bot = telebot.TeleBot("6060820498:AAFQJy1ol0TZdIegzFfbrneMIVPM5Iumu4o")
chat = "5065618545"
chat_free = "5065618545"
bot_free = False
signal = False


bot.send_message(chat, "BOT ON")
print("BOT ON")
while True:
    if signal:
        send_signal(signal, last_result["roll"], last_cor)
        for gale in range(2):
            last_result = wait_rolling()
            last_cor = last_color(last_result)
            results = list_results(list, last_cor)
            if verific_win(last_cor, signal, gale):
                break
        signal = False
    last_result = wait_rolling()
    last_cor = last_color(last_result)
    results = list_results(list, last_cor)
    signal = verific_pattern(results, black_paterns, red_paterns)
    time.sleep(1)
