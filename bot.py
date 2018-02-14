import discord
import asyncio
import re
import aiohttp
import sys
import mana
client = discord.Client()
pat = re.compile('\\[\\[(.*?)\\]\\]')
target = 'https://api.scryfall.com/cards/named?fuzzy={}&format=text'
autocomplete = 'https://api.scryfall.com/cards/autocomplete?q={}'
search = 'I don\'t recognize the name: "{}"\nDid you mean one of the following?\n{}'
col = discord.Colour(7506394)
replacer = mana.Mana()


@client.event
async def on_ready():
    replacer.prime(client)
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
    async with aiohttp.ClientSession() as session:
        for card in cards:
            name = '+'.join(card.strip('!').split())
            async with session.get(target.format(name)) as resp:
                if resp.status == 200:
                    content = await resp.text()
                    (title, text) = replacer.mana_sub(content).split('\n', 1)
                    url = resp.headers['X-Scryfall-Card']
                    img = resp.headers['X-Scryfall-Card-Image']
                    if card.startswith('!'):
                        embed = discord.Embed(colour=col)
                        embed.set_image(url=img)
                    else:
                        embed = discord.Embed(title=title, description=text, url=url, colour=col)
                        embed.set_thumbnail(url=img)
                    await message.channel.send(embed=embed)
                    await asyncio.sleep(0.05)
                else:
                    failures.append(card)
        for name in failures:
            async with session.get(autocomplete.format(name)) as resp:
                json = await resp.json()
                if (resp.status == 200) and json['data']:
                    await message.channel.send(search.format(name, '\n'.join(json['data'])))
                await asyncio.sleep(0.05)


if len(sys.argv) == 2:
    client.run(sys.argv[1])
else:
    client.run(input())
