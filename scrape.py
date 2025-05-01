# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
#
# def get_matches(url):
#
#     driver = webdriver.Chrome()
#     driver.get(url)
#
#     time.sleep(5)
#
#     partidas = driver.find_element(By.CLASS_NAME, 'match-table')
#     tbodies = partidas.find_elements(By.TAG_NAME, 'tbody')
#
#     jogos = []
#
#     for tbody in tbodies:
#         try:
#             # Data
#             data_element = tbody.find_element(By.CLASS_NAME, 'date-cell').find_element(By.TAG_NAME, 'span')
#             data = data_element.text
#
#             # Times
#             time1 = tbody.find_element(By.CLASS_NAME, 'team-1').text
#             time2 = tbody.find_element(By.CLASS_NAME, 'team-2').text
#
#             # Link para a página do jogo
#             match_link_element = tbody.find_element(By.CLASS_NAME, 'matchpage-button')
#             match_link = match_link_element.get_attribute('href')
#
#
#             jogos.append({
#                 'data': data,
#                 'time1': time1,
#                 'time2': time2,
#                 'link': match_link
#             })
#         except Exception as e:
#             print(f"Erro ao processar uma partida: {e}")
#
#     # # Mostrar os jogos extraídos
#     # for jogo in jogos:
#     #     print(jogo)
#
#     driver.quit()
#     return jogos
#
# # Teste
# url = 'https://www.hltv.org/team/11712/sashi#tab-matchesBox'
# jogos = get_matches(url)
#
# # Exibir resultados
# for jogo in jogos:
#     print(jogo)


#####################

from bs4 import BeautifulSoup
import cloudscraper

def get_matches(url):
    scraper = cloudscraper.create_scraper()
    res = scraper.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    # Encontra a tabela de partidas
    partidas = soup.find('table', class_='match-table')
    tbodies = partidas.find_all('tbody')

    jogos = []

    for tbody in tbodies:
        try:
            # Verifica se há linha da partida
            linha = tbody.find('tr', class_='team-row')
            if not linha:
                continue

            # Data
            date_cell = linha.find('td', class_='date-cell')
            time_tag = date_cell.find('span') if date_cell else None
            data = time_tag.text.strip() if time_tag else "Data não disponível"

            # Times
            team1_tag = linha.find('a', class_='team-name team-1')
            team2_tag = linha.find('a', class_='team-name team-2')
            time1 = team1_tag.text.strip() if team1_tag else "Time 1"
            time2 = team2_tag.text.strip() if team2_tag else "Time 2"

            # Link da partida
            link_tag = linha.find('a', class_='matchpage-button')
            link = 'https://www.hltv.org' + link_tag['href'] if link_tag else "Link não disponível"

            jogos.append({
                'data': data,
                'time1': time1,
                'time2': time2,
                'link': link
            })

        except Exception as e:
            print(f"Erro ao processar uma partida: {e}")
    print(jogos)
    return jogos

# # Teste
# url = 'https://www.hltv.org/team/11712/sashi#tab-matchesBox'
# jogos = get_matches(url)
#
# # Exibir resultados
# for jogo in jogos:
#     print(jogo)
