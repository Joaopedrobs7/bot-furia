import time
import os
from threading import Thread
from telegram import iniciar_bot
from telegram import criar_topicos
import settings


#iniciar o bot do pv. Deve ficar rodando 24h
Thread(target=iniciar_bot).start()

#iniciar o bot que gerencia os topicos do grupo
time.sleep(5)# tempo pra ligar o bot deboas
Thread(target=criar_topicos,args=(settings.url,settings.chat_id,settings.time_in_seconds)).start()

#todo
#implementar um json que guarda a data do jogo e o thread-id, assim quando ja tiver acontecido o game eu deleto



