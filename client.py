import discord
from discord.ext import commands, tasks
import random
import time
import asyncio
import re
from datetime import datetime, timedelta, timezone
from cog.slash import SlashCommands
from cog.prefix import PrefixCommands
from cog.Admin_commands import AdminCommands
import cog.Admin_commands
import cog.prefix
import cog.slash

# Read bot token from Bot_token.txt
with open("Bot_token.txt", "r") as token_file:
    TOKEN = token_file.read().strip()

client = commands.Bot(command_prefix="~", intents=discord.Intents.all())

start_time = time.time()

reminders = {}

def parse_duration(duration: str) -> int:
    time_units = {
        's': 1,  # seconds
        'm': 60, # minutes
        'h': 3600, # hours
        'd': 86400  # days
    }
    match = re.match(r'(\d+)([smhd])', duration)
    if match:
        value, unit = match.groups()
        return int(value) * time_units[unit]
    return None

@tasks.loop(seconds=10)
async def check_reminders():
    now = datetime.now(timezone.utc)
    for user_id, (reminder_time, message) in list(reminders.items()):
        if reminder_time <= now:
            user = client.get_user(user_id)
            if user:
                await user.send(message)
            del reminders[user_id]

@client.event
async def on_ready():
    check_reminders.start()
    await client.add_cog(SlashCommands(commands.Cog))
    await client.add_cog(PrefixCommands(commands.Cog))
    await client.add_cog(AdminCommands(commands.Cog))
    await client.tree.sync()
    print("Bot Connected")

# All your other commands and functionality go here...

# Finally, run the bot using the token from the file
client.run(TOKEN)
