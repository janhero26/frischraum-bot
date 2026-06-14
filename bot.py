import discord
from discord import app_commands
from discord.ext import commands
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

GESCHLOSSEN = [6]  # Nur Sonntag

WOCHENTAG_NAMEN = {
    0: 'Montag', 1: 'Dienstag', 2: 'Mittwoch',
    3: 'Donnerstag', 4: 'Freitag', 5: 'Samstag', 6: 'Sonntag'
}

def get_speiseplan(tag_slug):
    url = f'https://www.imensa.de/bayreuth/frischraum/{tag_slug}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    gerichte = {}
    aktuelle_kategorie = None

    for element in soup.select('h3, .aw-meal'):
        if element.name == 'h3':
            aktuelle_kategorie = element.text.strip()
            gerichte[aktuelle_kategorie] = []
        elif aktuelle_kategorie:
            name_el = element.select_one('.aw-meal-description')
            preis_el = element.select_one('.aw-meal-price')
            datum_el = element.select_one('.aw-meal-badge')
            if name_el:
                name = name_el.text.strip()
                preis = preis_el.text.strip() if preis_el else ''
                datum = datum_el.text.strip() if datum_el else ''
                gerichte[aktuelle_kategorie].append((name, preis, datum))

    return gerichte

def format_speiseplan_embed(gerichte, tag_name):
    embed = discord.Embed(
        title=f'🍽️ Frischraum – {tag_name}',
        color=discord.Color.green()
    )
    for kategorie, eintraege in gerichte.items():
        if eintraege:
            value = ''
            for name, preis, datum in eintraege:
                zeile = f'• {name}'
                if preis:
                    zeile += f' — {preis}'
                if datum:
                    zeile += f' *(zuletzt: {datum})*'
                value += zeile + '\n'
            embed.add_field(name=kategorie, value=value, inline=False)

    embed.set_footer(text='📍 Universitätsstraße 30 · ⏰ Mo–Sa geöffnet')
    return embed

@bot.event
async def on_ready():
    print(f'{bot.user} ist online!')
    await bot.change_presence(activity=discord.Game(name='/frischhelp'))
    try:
        synced = await bot.tree.sync()
        print(f'{len(synced)} Slash Commands synchronisiert!')
    except Exception as e:
        print(f'Fehler beim Sync: {e}')

@bot.tree.command(name='frischraum', description='Zeigt den Speiseplan des Frischraums')
@app_commands.describe(tag='Welcher Tag? (leer = heute)')
@app_commands.choices(tag=[
    app_commands.Choice(name='Heute',      value='heute'),
    app_commands.Choice(name='Morgen',     value='morgen'),
    app_commands.Choice(name='Montag',     value='montag'),
    app_commands.Choice(name='Dienstag',   value='dienstag'),
    app_commands.Choice(name='Mittwoch',   value='mittwoch'),
    app_commands.Choice(name='Donnerstag', value='donnerstag'),
    app_commands.Choice(name='Freitag',    value='freitag'),
    app_commands.Choice(name='Samstag', value='samstag'),
])
async def frischraum(interaction: discord.Interaction, tag: str = 'heute'):
    heute = datetime.now().weekday()
    slugs = ['montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag', 'samstag']

    if tag == 'morgen':
        wochentag = (heute + 1) % 7
    else:
        wochentag = heute

    if tag in ('heute', 'morgen'):
        if wochentag in GESCHLOSSEN:
            tag_name = WOCHENTAG_NAMEN[wochentag]
            await interaction.response.send_message(
                f'🔒 {tag_name} hat der Frischraum geschlossen!\nVerfügbar: Montag bis Samstag'
            )
            return
        tag_slug = slugs[wochentag]
        tag_name = WOCHENTAG_NAMEN[wochentag]
    else:
        tag_slug = tag
        tag_name = tag.capitalize()

    gerichte = get_speiseplan(tag_slug)
    if not gerichte:
        await interaction.response.send_message('❌ Kein Speiseplan gefunden.')
        return

    embed = format_speiseplan_embed(gerichte, tag_name)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='frischkitty', description='Zufälliges Katzenbild 🐱')
async def frischkitty(interaction: discord.Interaction):
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    data = response.json()
    bild_url = data[0]['url']
    await interaction.response.send_message(bild_url)

@bot.tree.command(name='frischhelp', description='Zeigt alle Commands des Frischraum Bots')
async def frischhelp(interaction: discord.Interaction):
    embed = discord.Embed(
        title='🤖 Frischraum Bot',
        description='Dein Speiseplan-Bot für den Frischraum der Uni Bayreuth',
        color=discord.Color.blue()
    )
    embed.add_field(
        name='🍽️ Speiseplan',
        value=(
            '`/frischraum` — Heute\n'
            '`/frischraum morgen` — Morgen\n'
            '`/frischraum [tag]` — Bestimmter Tag\n'
            '*Dropdown mit allen Tagen erscheint automatisch!*'
        ),
        inline=False
    )
    embed.add_field(
        name='🐱 Spaß',
        value='`/frischkitty` — Zufälliges Katzenbild',
        inline=False
    )
    embed.add_field(
        name='ℹ️ Info',
        value='`/frischhelp` — Zeigt diese Übersicht',
        inline=False
    )
    embed.set_footer(text='📍 Universitätsstraße 30 · ⏰ Mo–Sa geöffnet')
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)