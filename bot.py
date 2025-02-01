import discord
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
import os

load_dotenv()

client = discord.Client()

API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
CHANNEL_ID = os.getenv('DISCORD_TOKEN')

def get_best_market():
    return "EUR/USD"

def get_market_data():
    url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={symbol.split('/')[0]}&to_symbol={symbol.split('/')[1]}&interval=5min&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data 

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event 
async def on_message(message):
    if message.author == client.user:
        return 
    
    if message.content.startswith('!marketcheck'):
        symbol = message.content.split()[1]
        data = get_market_data(symbol)
        await message.channel.send(f"Market data for {symbol}: {data}")

    elif message.content.startswith('!bestmarket'):
        best_market = get_best_market()
        await message.channel.send(f"The best forex market to trade today is: {best_market}")

scheduler = AsyncIOScheduler()

def send_best_market():
    best_market = get_best_market()
    channel = client.get_channel(int(CHANNEL_ID))
    client.loop.create_task(channel.send(f"The best forex market to trade today is: {best_market}"))

scheduler.add_job(send_best_market, 'cron', hour=9, minute=0)
scheduler.start()

client.run('discordtoken')