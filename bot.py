import discord
import asyncio
import re
import requests

client = discord.Client()
pat = re.compile(r'\[\[(.*?)\]\]')

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
    requests = pat.findall(message.content)
    for card in requests:
        await client.send_message(message.channel, card)

client.run('MzQzNDM0MDAzNzMyMzY1MzEz.DGeXcw.EyLpdC6uRoS68lLMqfw1-7Gow70')
