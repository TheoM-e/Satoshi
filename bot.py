import json
import time
import urllib.request
import discord

client = discord.Client()

# Get discord token from ./key/discord_token.key
# discord_token.key must only contain your token
with open('keys/discord_token.key') as file:
    TOKEN = file.read()

# Get bot settings => ./settings/bot_settings.json
with open('settings/bot_settings.json') as file:
    settings = json.load(file)


# Called when discord bot is up
@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(
            type=get_status(settings['status_type'])[0],
            name=get_status(settings['status_type'])[1]
        )
    )


# Return status & status type from bot_settings.json
def get_status(type):
    if 'playing' in type.lower():
        return [discord.ActivityType.playing, settings['status']]
    elif 'streaming' in type.lower():
        return [discord.ActivityType.streaming, settings['status']]
    elif 'listening' in type.lower():
        return [discord.ActivityType.listening, settings['status']]
    elif 'watching' in type.lower():
        return [discord.ActivityType.watching, settings['status']]
    else:
        raise UnknowStatusType("Status type must be: playing/streaming/listening/watching")


def return_symbols():
    i = []
    with open('settings/tokens.json') as tokenList:
        tokens = json.load(tokenList)
    for x in tokens:
        i.append([x,tokens[x]])
    print(i)


# Return a list with prices based on the 2 crypto symbols in parameters
def return_prices(crypt1, crypt2):
    with urllib.request.urlopen(
            'https://www.binance.com/api/v3/ticker/price?symbol=' + crypt1.upper() + crypt2.upper()) as url:
        data = json.loads(url.read().decode())
    # list format: [Symbol , price]
    return [data[list(data)[0]], format(float(data[list(data)[1]]), ".2f")]


# Raised error if incorrect status type in settings
class UnknowStatusType(Exception):
    def __init__(self, error):
        super().__init__(error)


return_symbols()


client.run(TOKEN)