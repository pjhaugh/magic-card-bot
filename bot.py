import discord
import asyncio
import re
import requests
import sys
import mana

client = discord.Client()
pat = re.compile(r'\[\[(.*?)\]\]')
target = 'https://api.scryfall.com/cards/named?fuzzy={}&format=text'
autocomplete = 'https://api.scryfall.com/cards/autocomplete?q={}'
search = """I don't recognize the name: "{}"
Did you mean one of the following? :manahw:
{}"""

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
    failures = []
    for card in cards:
        name = '+'.join(card.split())
        resp = requests.get(target.format(name))
        if resp.status_code == 200:
            title, text = mana.mana_sub(resp.content.decode('UTF-8')).split('\n', 1)
            url = resp.headers['X-Scryfall-Card']
            img = resp.headers['X-Scryfall-Card-Image']
            embed = discord.Embed(title=title, description=text, url=url)
            embed.set_thumbnail(url=img)
            await client.send_message(message.channel, embed=embed)
            await client.send_message(message.channel, text)
            await asyncio.sleep(.05)
        else:
            failures.append(card)
    for name in failures:
        resp = requests.get(autocomplete.format(name))
        if resp.status_code == 200 and resp.json()['data']:
            await client.send_message(message.channel, search.format(name, '\n'.join(resp.json()['data'])))
            await asyncio.sleep(.05)


			
if len(sys.argv) == 2:
    client.run(sys.argv[1])
else:
    client.run(input())
