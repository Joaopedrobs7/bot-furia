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


