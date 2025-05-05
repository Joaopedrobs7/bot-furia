# 🔔 HLTV Telegram Bot – FURIA Tracker

Um bot em Python que monitora a página da HLTV de um time (ex: FURIA) e envia alertas para um grupo no Telegram sempre que uma nova partida for detectada. Ideal para manter torcedores atualizados com os próximos confrontos do time.

---

## 🚀 Funcionalidades

- Verifica periodicamente a página de partidas do time na HLTV.
- Detecta novas partidas automaticamente.
- Envia mensagens para um grupo ou canal no Telegram.
- 100% automatizado e personalizável.

---

## ⚙️ Configuração

### 1. Clonar o repositório

```bash
git clone https://github.com/Joaopedrobs7/bot-furia.git
cd bot-furia /
```
### 2. Configurar o `settings.py`

No arquivo `settings.py`, edite as seguintes variáveis de acordo com seu bot e grupo do Telegram:

```python
# settings.py

# Chave da API do seu bot do Telegram (obtenha no BotFather)
api_key = "SEU_TOKEN_DO_BOT"

# ID do grupo onde os tópicos serão criados
chat_id = -1001234567890

# URL da página HLTV do time a ser monitorado
url = "https://www.hltv.org/team/8297/furia#tab-matchesBox"

# Tempo de intervalo entre verificações (em segundos)
time_in_seconds = 86400  # 24 horas
```
### 3. Instalar as dependências

Certifique-se de ter o `pip` instalado e execute o comando abaixo para instalar todas as dependências necessárias:

```bash
pip install -r requirements.txt
```
### 4. Executar o bot

Após configurar e instalar as dependências, execute o bot com:

```bash
python main.py
```
---

## 🗂️ Estrutura do Projeto

O projeto é dividido em vários arquivos, cada um com uma função específica. Abaixo está uma breve explicação de cada um:

### 1. `scrape.py`

Este arquivo é responsável por **extrair as informações das próximas partidas** do time escolhido diretamente da página do HLTV. Utilizando a biblioteca `BeautifulSoup`, ele faz o web scraping da tabela de partidas e coleta os dados como:

- Data do jogo
- Times que irão jogar
- Link da página do jogo

Essas informações são então retornadas para serem utilizadas na criação de tópicos no Telegram.

### 2. `telegram.py`

Aqui ficam definidos **os handlers do bot e a checagem de duplicidade de tópicos**. O arquivo contém:

- Configuração do bot com o `python-telegram-bot`.
- Definição de comandos e interações (como o comando `/start` e botões de interação).
- Verificação de partidas duplicadas, evitando que o bot crie tópicos repetidos no grupo.
- Criação de tópicos no Telegram sobre as próximas partidas e o envio de mensagens com detalhes dos jogos.

### 3. `main.py`

Este é o arquivo que **executa o bot**. Quando o bot é iniciado, este script:

- Inicia o bot que responde a mensagens privadas (`iniciar_bot`).
- Inicia o bot que verifica e cria os tópicos sobre os jogos no grupo de Telegram, utilizando o intervalo de tempo configurado em `settings.py`.
- Ele mantém os dois processos rodando simultaneamente para garantir que o bot fique ativo o tempo todo.

### 4. `settings.py`

Aqui ficam as **configurações do bot**, como:

- `api_key`: A chave da API do Telegram, que você obtém ao criar o bot no BotFather.
- `chat_id`: O ID do grupo ou canal no Telegram onde os tópicos serão criados.
- `url`: O link para a página de partidas do time escolhido na HLTV.
- `time_in_seconds`: O intervalo de tempo em segundos para que o bot verifique a página e busque novas partidas.

### 5. `jogos.json`

Este arquivo é utilizado para **armazenar as informações sobre os tópicos já criados**. Quando o bot encontra uma nova partida, ele cria um tópico no Telegram e registra o link do jogo e o `thread_id` do tópico no arquivo `jogos.json`. Isso permite que o bot identifique partidas duplicadas ao verificar os jogos passados e evita criar tópicos repetidos.

```json
{
  "jogos": [
    {
      "data": "2025-05-05",
      "time1": "FURIA",
      "time2": "Team X",
      "link": "https://www.hltv.org/matches/123456",
      "thread_id": 987654
    }
  ]
}



