import os
import telebot
from os import system as sys
from time import sleep as sl
import datetime

token = '5155515281:AAFl3Qix7TcUQ7d7mp8TKVbTqgBfkYr8n40'
tokenP = '5378272351:AAHgM3veBoTOvuYrrxtPBh6XGqqLwXk9Gz8'
# chat = '-1001799501522' #VIP
chatFree = ''  # FREE
# chatFree = '5065618545'  # PRIVADOFREE
chat = '5065618545'  # PRIVADO
# chat = '-681686624'  # testes
# chat = '-1001663194828'  # FREE 24h
#chat = '-1001610191274'  # Vip Double 24h
chatpatinhasvip = ''
chatpatinhasfree = ''
# chatFree = '-681686624'
chatErro = '5065618545'
# chat = '-1001689222723'

bot = telebot.TeleBot(token)
botp = telebot.TeleBot(tokenP)

bot.send_message(chat, "ola")
