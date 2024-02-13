import asyncio
import websockets
import json
import logging
import requests
import sys
import sqlite3
import re
import requests
import discord
from discord.ext import commands
from discord import Intents
from discord import app_commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time





intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)


print("Initialisation du WebDriver pour Chrome...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = 'https://news.treeofalpha.com/'
print(f"Ouverture de l'URL : {url}")
driver.get(url)

print("Attente pour le chargement initial du JavaScript...")
time.sleep(5)


async def setup_hook():
    await bot.tree.sync()

bot.setup_hook = setup_hook





async def send_discord_message(tweet_text, tweet_link):
    channel_id = 1204344781593907240  # Remplacez par l'ID de votre channel Discord
    channel = bot.get_channel(channel_id)
    full_message1 = (
        f"{tweet_text}"
        f"{tweet_link}"
    )   
    await channel.send(full_message1)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await asyncio.gather(
        main(),
    )  # Démarre les deux tâches en parallèle


async def main():

    previous_tweet_text = None  # Variable pour stocker le texte du tweet précédent de Elon Musk/Vitalik
    while True:
        try:
            print("Recherche du tweet de Elon Musk dans le feed avec data-index=0...")
            tweet_container = driver.find_element(By.CSS_SELECTOR, 'div[data-index="0"] .box.padding-smallest.rowToColumn .container.gap-small.alignCenter[style="width: 100%;"] .contentWrapper.column.gap-small')
            if tweet_container:
                tweet_link = tweet_container.find_element(By.CSS_SELECTOR, 'h2.contentTitle a').get_attribute('href')
            
            # Vérifier si le lien correspond au format des tweets de Elon Musk/Vitalik
                if tweet_link.startswith("https://twitter.com/elonmusk/status/") or tweet_link.startswith("https://twitter.com/VitalikButerin/status/"):
                    tweet_text = tweet_container.find_element(By.CSS_SELECTOR, 'h2.contentTitle').text
                
                    # Vérifier si le tweet a changé par rapport au précédent
                    if tweet_text != previous_tweet_text:
                        print("Nouveau tweet de Elon Musk détecté:")
                        print(tweet_text)
                        print(tweet_link)
                        await send_discord_message(tweet_text, tweet_link)
                        previous_tweet_text = tweet_text
                    else:
                        print("Le tweet de Elon Musk n'a pas changé.")
                else:
                    print("Le tweet dans data-index=0 n'est pas de Elon Musk.")
            else:
                print("Aucun tweet trouvé avec data-index=0. Vérifiez le sélecteur CSS.")
        except Exception as e:
            print(f"Erreur lors de la recherche du tweet : {e}")
    
        print("Attente de 5 secondes avant la prochaine vérification...")
        await asyncio.sleep(2)


bot.run('DiscordToken')  # A remplacer par votre token de bot Discord
 




