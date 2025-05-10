import telebot
from telebot import types
import time
import settings
from scrape import get_matches
import json
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()


api_key = settings.api_key
bot = telebot.TeleBot(api_key)
logs_thread_id = 70 # TOPICO QUE VAI MANDAR OS LOGS

def iniciar_bot():
    #comandos do menu
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Abrir Menu de Opcoes")
    ])

    #so responder comandos no pv
    @bot.message_handler(['start'],chat_types=['private'])
    def start(msg:telebot.types.Message):
        # foto do professor
        fallen = open('fallen.png', 'rb')

        markup = types.InlineKeyboardMarkup()
        botao_grupo = types.InlineKeyboardButton('Grupo', callback_data='botao_grupo')
        botao_sobre = types.InlineKeyboardButton('Sobre',callback_data='botao_sobre')

        caption = (
            "fala galera, fallenzao aqui\n\n"
            "Quer trocar uma ideia com a galera? Clica em 👉 Grupo pra entrar no chat da FURIA! 🔥\n\n"
            "E se quiser saber quem foi o dev que fez essa parada aqui, clica em 👉 Sobre! 😂\n\n"
            "Tamo junto, GLHF! 🎯"
        )

        markup.add(botao_grupo,botao_sobre)
        bot.send_photo(msg.chat.id,fallen,caption=caption,reply_markup=markup)

        #match case do markup
    @bot.callback_query_handler()
    def callback_response(call:types.CallbackQuery):
        match call.data:
            case 'botao_grupo':
                link_grupo = 'Acesse em: t.me/TorcedoresFuria'
                bot.send_message(call.message.chat.id,link_grupo)
                #deletar msg anterior
                bot.delete_message(call.message.chat.id, call.message.id)
            case 'botao_sobre':
                text = 'Bot da furia que vai te adicionar no grupo principal\n\nMade by: github.com/Joaopedrobs7'
                bot.send_message(call.message.chat.id,text)
                #deletar msg anterior
                bot.delete_message(call.message.chat.id,call.message.id)

    #pega resto das msgs
    @bot.message_handler()
    def getall(msg: types.Message):
        print(f"Msg: {msg.text} Chat ID: {msg.chat.id} thread_id:{msg.message_thread_id}")
        if msg.text == 'bao?':
            bot.send_message(chat_id=msg.chat.id, text='bao')

    bot.infinity_polling()


def criar_topicos(url,chat_id,time_in_seconds):
    while True:
        print('Procurando Jogos...')
        jogos = get_matches(url)
        print('Procurando Jogos Para remover...')
        check_active_games(jogos)
        jogos = search_new_games(jogos)


        if jogos:
            for row in jogos:
                if row['time2'] != 'Time 2': #Verificar tbd

                    if len(row['data']) == 5: #Tratar jogos que tem apenas o horario
                        row['data'] = datetime.today().strftime('%d/%m/%Y')

                    topic_name = f"{row['time1']} x {row['time2']} {row['data']}"
                    game_info = f"Para mais informacoes acesse: {row['link']}"
                    topic = bot.create_forum_topic(chat_id=chat_id, name=topic_name)
                    #salvando thread id para cada topico para posteriormente deletar
                    row['thread_id'] = topic.message_thread_id
                    bot.send_message(chat_id=chat_id, message_thread_id=topic.message_thread_id, text=game_info)
                    #criar log
                    log = f"topico criado: {topic_name}"
                    bot.send_message(chat_id=chat_id,message_thread_id=logs_thread_id,text=log)
                    print(topic_name)
            save_jogos(jogos)
        else:
            print("Nenhum Jogo a ser adicionado")
            log = "Nenhum Jogo a ser adicionado"
            bot.send_message(chat_id=chat_id, message_thread_id=logs_thread_id, text=log)

        #espera 24h para checar dnv
        time.sleep(time_in_seconds)

def search_new_games(jogos):
    # aqui eu abro o json e pego os links existentes
    with open('jogos.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        link_existentes = {j['link'] for j in data['jogos']}  # pega os links do json

    jogos_novos = []
    # aqui eu procuro por jogos nao adicionados nos topicos
    for row in jogos:
        if row['link'] in link_existentes:
            print(f"Link duplicado: {row['link']}")
        else:
            print(f"novo link encontrado: {row['link']}")
            jogos_novos.append(row)
    return jogos_novos

def save_jogos(jogos_novos):
    #salvando no json
    with open('jogos.json','r',encoding='utf-8') as file:
        data = json.load(file)

    with open('jogos.json', 'w', encoding='utf-8') as file:
        data['jogos'].extend(jogos_novos)
        json.dump(data, file, indent=4, ensure_ascii=False, )



def check_active_games(jogos):
    with open('jogos.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    #se os jogos do data nao estiverem em jogos a partida ja ocorreu
    links_achados = {j['link'] for j in jogos}
    jogos_ativos = []
    removidos = 0

    for row in data['jogos']:
        if row['link'] not in links_achados:
            delete_topic(row)
            removidos+=1
        else:
            jogos_ativos.append(row)

    # salva no json
    data['jogos'] = jogos_ativos
    if data['jogos']:
        with open('jogos.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    if removidos == 0:
        print("Nenhum Jogo a ser removido")
        bot.send_message(chat_id=settings.chat_id,message_thread_id=logs_thread_id,text="Nenhum Jogo a ser removido")


def delete_topic(row):
    row_thread_id = row['thread_id']
    bot.delete_forum_topic(chat_id=settings.chat_id, message_thread_id=row_thread_id)
    log = f"Thread Deletado {row['time1']} x {row['time2']} {row['data']}"
    bot.send_message(chat_id=settings.chat_id, message_thread_id=logs_thread_id, text=log)




