import json
import time
import urllib.request
import discord


# Get discord token from ./key/discord_token.key
# discord_token.key must only contain your token
with open('keys/discord_token.key') as file:
    TOKEN = file.read()

# Get bot settings => ./settings/bot_settings.json
with open('settings/bot_settings.json') as file:
    settings = json.load(file)

client = discord.Client()