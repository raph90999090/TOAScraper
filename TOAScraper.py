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
intents.messages = True

bot = commands.Bot(command_prefix='.', intents=intents)

async def send_discord_message_twitter(tweet_link):
    channel_id = #YOUR CHANNEL ID of discord serv
    channel = bot.get_channel(channel_id)
    full_message1 = f"{tweet_link} @everyone"
    await channel.send(full_message1)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await asyncio.gather(
        twitter(),
    )


async def twitter():

    print("Initialisation des WebDriver pour Chrome...")
    #CHANGE THE RANGE() IF YOU WANT A DIFFERENT NUMBER OF SESSION , 5 = 5 sessions and 5 follow tweet account.
    services = [Service(ChromeDriverManager().install()) for _ in range(5)]
    drivers = [webdriver.Chrome(service=service) for service in services]
    #CHANGE RANGE() WITH NUMBER SESSION
    urls = ['https://news.treeofalpha.com/' for _ in range(5)]
    tweet_base_urls = [
        "https://twitter.com/NAME_OF_ACCOUNT1/status",
        "https://twitter.com/NAME_OF_ACCOUNT2/status"
    ]

    for driver, url in zip(drivers, urls):
        driver.get(url)
    time.sleep(5)
    previous_tweet_texts = [None] * 5

    while True:
        for index, (driver, tweet_base_url) in enumerate(zip(drivers, tweet_base_urls)):
            try:
                tweet_container = driver.find_element(By.CSS_SELECTOR, 'div[data-index="0"] .box.padding-smallest.rowToColumn .container.gap-small.alignCenter[style="width: 100%;"] .contentWrapper.column.gap-small')
                if tweet_container:
                    tweet_link = tweet_container.find_element(By.CSS_SELECTOR, 'h2.contentTitle a').get_attribute('href')    
                    if tweet_link.startswith(tweet_base_url):
                        tweet_text = tweet_container.find_element(By.CSS_SELECTOR, 'h2.contentTitle').text                 
                        if tweet_text != previous_tweet_texts[index]:
                            await send_discord_message_twitter(tweet_link)
                            previous_tweet_texts[index] = tweet_text
                            driver.get(urls[index])
                        else:
                            print(f"tweet not change for session {index+1}.")
                    else:
                        print(f"need correct url {index+1}.")
                else:
                    print(f"check CSS {index+1}.")
            except Exception as e:
                print(f"Error in tweet fetch {index+1} : {e}")
            await asyncio.sleep(1)


#YOUR BOT TOKEN DISCORD ---> https://discord.com/developers/applications/ create new app ---> get token --> add to server 
bot.run('BOT_TOKEN')
 



