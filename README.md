# Epic Games Promotions Discord Bot 
Discord bot that automatically sends out a message when there's a new Epic Games promotion.
## Commands
channel_ids.db (should change name for clarity) is the database storing two tables, the list of channels the bot will send messages to, and the list of games the bot has sent messages about. The bot will automatically generate this database if it does not already exist.
- /addchannel (channel_id) to add a channel to the list. (Admin perms required)
- /delchannel (channel_id) to delete a channel from the list. (Admin perms required)


## Libraries

- [APScheduler](https://github.com/agronholm/apscheduler)
- [epicstore_api](https://github.com/SD4RK/epicstore_api)
- [Pycord](https://github.com/Pycord-Development/pycord)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)



## Run Locally

Create a Discord Application in the [Developer Portal](https://discord.com/developers/applications)




Clone the project

```bash
  git clone https://link-to-project
```

Rename .env.example to .env and paste in your token

```bash
  DISCORD_TOKEN=YourToken
```

Create a virtual environment
```bash
  python -m venv /path/to/new/virtual/environment
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the bot

```bash
  python main.py
```


