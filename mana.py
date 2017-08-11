import re
import json

with open("mana_symbols.json") as f:
    mana_symbols = json.loads(f.read())

mana_symbols = dict((re.escape(k), v) for k, v in mana_symbols.items())
mana_pat = re.compile("|".join(mana_symbols.keys()))

def mana_sub(text):
    return mana_pat.sub(lambda a: mana_symbols[re.escape(a.group(0))] , text)