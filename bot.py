import discord
import asyncio
import re
import requests

client = discord.Client()
pat = re.compile(r'\[\[(.*?)\]\]')
target = 'https://api.scryfall.com/cards/named?fuzzy={}&format=text'

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    cards = pat.findall(message.content)
    for card in cards:
        name = '+'.join(card.split())
        resp = requests.get(target.format(name))
        if resp.status_code == 200:
            await client.send_message(message.channel, resp.content.decode('UTF-8'))
            await asyncio.sleep(.05)

client.run('MzQzNDM0MDAzNzMyMzY1MzEz.DGeXcw.EyLpdC6uRoS68lLMqfw1-7Gow70')
