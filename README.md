
# Satoshi ~ DiscordCryptoBot

📊 Satoshi is a simple python discord bot using discord.py that allow you to track your favorites cryptos prices with your own bot. 
It doesn't need any skills, anyone can use, you only have to edit json files.


## How to use ?
After installing Python 3:
- You'll need to clone the Github repository:
```bash
  git clone https://github.com/TheoMesse/Satoshi-DiscordCryptoBot.git
```

- Then go in the directory and type:

```bash
  pip install -r requirements.txt
```
- Then you'll have to copy your discord bot token and paste it in:

```
  ./keys/discord_token.key
```
- Then open the `./settings/settings.json` file:\
  - In `'"status_type": '` you have to enter the status type you want: "playing" or "watching" or "listening" or "streaming",`\
  - In `'"status": '` you can enter whatever you want, it's the status that'll be displayed,
  - In `'"channel_id": '` you must enter the id of the channel where you want to track prices, for that you have to enable discord devmod and right-click on the channel then "Copy ID",
  - Finaly, in `'"interval": '` you have to choose the delay in minutes you want for your bot to send prices.
  /!\ IMPORTANT: `'"channel_id": '` & `'"interval": '` must be in int, not str so you dont have to put `""` around the value of these ones.

- To choose which crypto you want to track, open the `./settings/tokens.json` then you can add / remove cryptos by following the default template

- Then you'll have to run the bot:
    - Windows:
    ```bash
    python bot.py
    ```
    - Linux:
    ```bash
    python3 bot.py
    ```
## Authors

- [@TheoM-e](https://www.github.com/TheoM-e)

