import time
from threading import Thread
from telegram import iniciar_bot
from telegram import criar_topicos



chat_id = -1002271878708
url = 'https://www.hltv.org/team/11712/sashi#tab-matchesBox'

#iniciar o bot do pv. Deve ficar rodando 24h
Thread(target=iniciar_bot).start()

time.sleep(2)# tempo pra ligar o bot deboas
Thread(target=criar_topicos,args=(url,chat_id)).start()


# PARA ACHAR O ID DO CHAT  = -1002271878708
# @bot.message_handler()
# def handle_message(message):
#     print(f"Msg: {message.text} \nChat ID: {message.chat.id}")
#     if message.text == 'bao?':
#         bot.send_message(chat_id=chat_id, text='bao')


#todo
#implementar um json que guarda a data do jogo e o thread-id, assim quando ja tiver acontecido o game eu deleto



