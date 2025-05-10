import os
from dotenv import load_dotenv
load_dotenv()


api_key = os.getenv('API_KEY') #api_key do seu bot do telegram
chat_id = -1002271878708  # Id do chat que o bot vai gerenciar
url = 'https://www.hltv.org/team/8297/furia#tab-matchesBox'  # Url do time para fazer scraping
time_in_seconds = 28800  # Tempo em Segundos para checar por novos jogos