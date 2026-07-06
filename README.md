# 🥗Frischraum Bot

A Discord bot that displays the daily menu of the Frischraum cafeteria at the University of Bayreuth.

## Features
- 🍽️ `/frischraum` - Shows today's menu with prices
- 📅 `/frischraum [tag]` - Menu for a specific day via dropdown
- 🐱 `/frischkitty` - Random cat image
- ℹ️ `/frischhelp` - Shows all commands

## Usage

The bot is already hosted and running. You can invite it directly to your Discord server:

**[Add to your server](https://discord.com/oauth2/authorize?client_id=1515751115918934077&permissions=2147502080&integration_type=0&scope=bot+applications.commands)**

If you want to host it yourself or modify it, follow the setup instructions below.

## Requirements
- Python 3.11+
- [discord.py](https://discordpy.readthedocs.io/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [requests](https://requests.readthedocs.io/)
- [pytz](https://pypi.org/project/pytz/)

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

3. Create a .env file in the project root and add your Discord bot token:
   DISCORD_TOKEN=your_token_here

   You can get your token from the [Discord Developer Portal](https://discord.com/developers/applications).

4. Invite the bot to your server via the Discord Developer Portal:
   - Go to **OAuth2 -> URL Generator**
   - Under **Scopes**, select `bot` and `applications.commands`
   - Under **Bot Permissions**, select `Send Messages`, `Embed Links` and `Use Slash Commands`
   - Open the generated URL in your browser and add the bot to your server

5. Run the bot
```bash
   python bot.py
```

## Notes
- Closed on Sundays — the bot handles this automatically
- Scraped from the public Studierendenwerk Oberfranken menu via imensa.de