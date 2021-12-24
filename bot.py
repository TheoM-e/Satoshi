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


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(
            type=get_status(settings['status_type'])[0],
            name=get_status(settings['status_type'])[1]
        )
    )


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


class UnknowStatusType(Exception):
    def __init__(self, error):
        super().__init__(error)


client.run(TOKEN)