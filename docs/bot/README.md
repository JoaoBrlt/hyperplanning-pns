# Discord bot

Use the application through the help of a discord bot.

## Preview

<img src="images/bot.png" width="500" alt="Bot preview"/>
<img src="images/bot2.png" width="500" alt="Bot preview 2"/>

## Requirements

1. Install Python 3 and pip.
2. Clone the repository.
3. Move to the repository.
4. Copy the `.env.example` file to `.env`.
```bash
cp .env.example .env
```
5. Install the dependencies.
```bash
pip install -r requirements.txt
```

## Usage

1. Create a Discord application.
2. Create a Discord bot associated to the Discord application.
3. Copy the Discord bot token.
4. Paste the Discord bot token inside the `.env` file.
5. Add the bot to your Discord server.
6. Run the bot.
```bash
python bot.py
```

## Commands

| Name                                      | Description                                                              |
|-------------------------------------------|--------------------------------------------------------------------------|
| !help                                     | Shows the help message.                                                  |
| [!hyperplanning](hyperplanning/README.md) | Shows a list of available classrooms according to the specified filters. |
