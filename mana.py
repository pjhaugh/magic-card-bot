import re
import json


class Mana:
    def __init__(self):
        with open("mana_symbols.json") as f:
            self.mana_symbols = json.loads(f.read())

    def prime(self, client):
        d = {e.name: str(e) for e in client.get_all_emojis()}
        self.mana_symbols = {
            re.escape(k): d[v] if v in d else k
            for k, v in self.mana_symbols.items()
        }
        self.mana_pat = re.compile("|".join(self.mana_symbols.keys()))

    def mana_sub(self, text):
        return self.mana_pat.sub(
            lambda a: self.mana_symbols[re.escape(a.group(0))], text)
