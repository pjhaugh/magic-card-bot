import re
import json

class Mana:

    def __init__(self):
	    with open("mana_symbols.json") as f:
            self.mana_symbols = json.loads(f.read())
    
	def prime(self, client):
        d = {e.name, e.id for emoji in client.get_all_emoji()}
		self.mana_symbols = dict((re.escape(k), "<:{}:{}>".format(v, d[v])) for k, v in self.mana_symbols.items())
        self.mana_pat = re.compile("|".join(mana_symbols.keys()))

    def mana_sub(self.text):
        return mana_pat.sub(lambda a: mana_symbols[re.escape(a.group(0))] , text)