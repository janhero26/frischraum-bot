# 🥗Frischraum Bot

A Discord bot that displays the daily menu of the Frischraum cafeteria at the University of Bayreuth.

## Features
- 🍽️ `/frischraum` - Shows today's menu with prices
- 📅 `/frischraum [tag]` - Menu for a specific day via dropdown
- 🐱 `/frischkitty` - Random cat image
- ℹ️ `/frischhelp` - Shows all commands

## ⚙️Requirements
- Python 3.11+
- [discord.py](https://discordpy.readthedocs.io/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [requests](https://requests.readthedocs.io/)

## Setup
1. Clone the repository
```bash
   git clone https://github.com/janhero26/frischraum-bot
   cd frischraum-bot
```

2. Install dependencies
```bash
   pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Discord bot token:
```
   DISCORD_TOKEN=your_token_here
```
   You can get your token from the [Discord Developer Portal](https://discord.com/developers/applications).

4. Invite the bot to your server via the Discord Developer Portal:
   - Go to **OAuth2 -> URL Generator**
   - Under **Scopes**, select `bot` and `applications.commands`
   - Under **Bot Permissions**, select `Administrator`
   - Open the generated URL in your browser and add the bot to your server

5. Run the bot
```bash
   python bot.py
```

## Notes
- Menu data is scraped from [imensa.de](https://www.imensa.de/bayreuth/frischraum/index.html)
- The Frischraum is closed on weekends, which the bot handles automatically