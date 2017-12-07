import discord
import asyncio
import re
import aiohttp
import sys
import mana

client = discord.Client()
pat = re.compile(r'\[\[(.*?)\]\]')
target = 'https://api.scryfall.com/cards/named?fuzzy={}&format=text'
autocomplete = 'https://api.scryfall.com/cards/autocomplete?q={}'
search = """\
I don't recognize the name: "{}"
Did you mean one of the following?
{}"""
col = discord.Colour(0x7289DA)

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
    for card in cards:
        name = '+'.join(card.strip('!').split())
        async with aiohttp.get(target.format(name)) as resp:
            if resp.status == 200:
                content = await resp.text()
                title, text = replacer.mana_sub(content).split('\n', 1)
                url = resp.headers['X-Scryfall-Card']
                img = resp.headers['X-Scryfall-Card-Image']
                if card.startswith('!'):
                    embed = discord.Embed(colour=col)
                    embed.set_image(url=img)
                else:
                    embed = discord.Embed(
                        title=title, description=text, url=url, colour=col)
                    embed.set_thumbnail(url=img)
                await client.send_message(message.channel, embed=embed)
                await asyncio.sleep(.05)
            else:
                failures.append(card)
    for name in failures:
        async with aiohttp.get(autocomplete.format(name)) as resp:
            json = await resp.json()
            if resp.status == 200 and json['data']:
                await client.send_message(message.channel,
                                          search.format(
                                              name, '\n'.join(json['data'])))
                await asyncio.sleep(.05)


if len(sys.argv) == 2:
    client.run(sys.argv[1])
else:
    client.run(input())
