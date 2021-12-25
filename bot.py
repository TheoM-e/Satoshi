import json
import time
import urllib.request
import discord

client = discord.Client()
oldPrices = {'isFirstLoop': True}

# Get discord token from ./key/discord_token.key
# discord_token.key must only contain your token
with open('keys/discord_token.key') as file:
    TOKEN = file.read()

# Get bot settings => ./settings/bot_settings.json
with open('settings/settings.json') as file:
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

    with open('settings/settings.json') as param:
        param = json.load(param)
        channel_id = param['channel_id']
        interval = param['interval']

    if isinstance(channel_id, str):
        try:
            channel_id = int(channel_id)
        except ValueError:
            raise InvalidType("Invalid channel id, please use int")

    while True:
        channel = client.get_channel(channel_id)
        await channel.send(embed=symbols_to_embed(return_symbols()))
        time.sleep(interval * 60)


def symbols_to_embed(symbolsList):
    prices = []

    with open('settings/settings.json') as param:
        interval = json.load(param)['interval']

    if isinstance(interval, str):
        try:
            interval = int(interval)
        except ValueError:
            raise InvalidType("Invalid interval, please use int")

    for x in symbolsList:
        prices.append([(str(x[0]) + str(x[1])).upper(), return_prices(str(x[0]), str(x[1]))[1]])

    if oldPrices['isFirstLoop']:
        oldPrices['isFirstLoop'] = False
        for x in prices:
            oldPrices[str(x[0])] = str(x[1])

    t = time.localtime()
    current_time = time.strftime("%D %H:%M:%S", t)

    embed = discord.Embed(title="Prices ~ [m" + str(interval) + "]",
                          description=current_time, color=0xFF8008)
    embed.set_author(name="SatoshiNakamoto",
                     icon_url='https://cdn.discordapp.com/avatars/923323366197301278/8cc23d15abd47fbc1e0b7dc95dae2c38.webp?size=80')

    for x in prices:
        embed.add_field(name=str(x[0]),
                        value='$' + str(x[1]) + ' ~ ' + '[' + get_improvement(oldPrices[x[0]], x[1]) + ']')
        oldPrices[str(x[0])] = str(x[1])
    return embed


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


def get_improvement(old, new):
    old = float(old)
    new = float(new)
    i = ((new - old) / old) * 100.0
    i = format(i, ".2f")
    if new >= old:
        return '+' + str(i) + '%'
    else:
        return str(i) + '%'


def return_symbols():
    i = []
    with open('settings/tokens.json') as tokenList:
        tokens = json.load(tokenList)
    if len(tokens) > 0:
        for x in tokens:
            i.append([x, tokens[x]])
        return i
    else:
        i.append(['BTC', 'USDT'])
        return i


# Return a list with prices based on the 2 crypto symbols in parameters
def return_prices(crypt1, crypt2):
    try:
        with urllib.request.urlopen(
                'https://www.binance.com/api/v3/ticker/price?symbol=' + crypt1.upper() + crypt2.upper()) as url:
            data = json.loads(url.read().decode())
        # list format: [Symbol , price]
        return [data[list(data)[0]], format(float(data[list(data)[1]]), ".2f")]
    except urllib.error.HTTPError:
        raise InvalidType("Invalid crypto or invalid symbols in ./settings/tokens.json")


# Raised error if incorrect status type in settings
class UnknowStatusType(Exception):
    def __init__(self, error):
        super().__init__(error)


class InvalidType(Exception):
    def __init__(self, error):
        super().__init__(error)


client.run(TOKEN)
