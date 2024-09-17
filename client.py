import discord
from discord.ext import commands, tasks
import random
import time
import asyncio
import re
from datetime import datetime, timedelta, timezone

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
    await client.tree.sync()
    print("Bot Connected")

#! Prefix commands

# ~cutiemeter
@client.command(brief="Rates how cute you are", description="Rates how cute you are on a scale of 1 to 10.")
async def cutiemeter(ctx):
    rating_list = ["1/10", "2/10", "3/10", "4/10", "5/10", "6/10", "7/10", "8/10", "9/10", "10/10"]
    rating = random.choice(rating_list)
    await ctx.send(f"{ctx.author.mention} is a {rating} on the Cute o'meter :3")

# ~ping
@client.command(brief="Pings Bot", description="Pings Bot")
async def ping(ctx):
    await ctx.send("Bot Pinged")

# ~Uptime
@client.command(brief="Bot Uptime", description="Bot Uptime")
async def uptime(ctx):
    current_time = time.time()
    uptime_seconds = int(current_time - start_time)
    uptime_str = str(timedelta(seconds=uptime_seconds))
    await ctx.send(f"Bot has been up for: {uptime_str}")

# ~roll
@client.command(brief="Roll a dice with a custom number of sides", description="Rolls a dice with the specified number of sides (e.g., 4, 6, 8, 10, 12, 20)")
async def roll(ctx, sides: int):
    if sides <= 0:
        await ctx.send(f"{ctx.author.mention}, dice must have a positive number of sides.")
        return
    roll_result = random.randint(1, sides)
    await ctx.send(f"{ctx.author.mention} rolled {roll_result} on a D{sides}")

# ~Quote
@client.command(brief="random quote", description="Returns a random inspirational quote.")
async def Quote(ctx):
    quote_list = [
    "All our dreams can come true, if we have the courage to pursue them. —Walt Disney",
    "The secret of getting ahead is getting started. —Mark Twain",
    "I’ve missed more than 9,000 shots in my career. I’ve lost almost 300 games. Twenty-six times I’ve been trusted to take the game-winning shot and missed. I’ve failed over and over and over again in my life, and that is why I succeed. —Michael Jordan",
    "Don’t limit yourself. Many people limit themselves to what they think they can do. You can go as far as your mind lets you. What you believe, remember, you can achieve. —Mary Kay Ash",
    "The best time to plant a tree was 20 years ago. The second best time is now. —Chinese proverb",
    "Only the paranoid survive. —Andy Grove",
    "It’s hard to beat a person who never gives up. —Babe Ruth",
    "I wake up every morning and think to myself, ‘How far can I push this company in the next 24 hours?’ —Leah Busque",
    "We need to accept that we won’t always make the right decisions, that we’ll screw up royally sometimes―understanding that failure is not the opposite of success, it’s part of success. —Arianna Huffington",
    "Write it. Shoot it. Publish it. Crochet it. Sauté it. Whatever. MAKE. —Joss Whedon",
    "If people are doubting how far you can go, go so far that you can’t hear them anymore. —Michele Ruiz",
    "You’ve gotta dance like there’s nobody watching, love like you’ll never be hurt, sing like there’s nobody listening, and live like it’s heaven on earth. —William W. Purkey",
    "Fairy tales are more than true: not because they tell us that dragons exist, but because they tell us that dragons can be beaten. —Neil Gaiman",
    "Everything you can imagine is real. —Pablo Picasso",
    "When one door of happiness closes, another opens; but often we look so long at the closed door that we do not see the one which has been opened for us. —Helen Keller",
    "Do one thing every day that scares you. —Eleanor Roosevelt",
    "It’s no use going back to yesterday, because I was a different person then. —Lewis Carroll",
    "Smart people learn from everything and everyone, average people from their experiences, stupid people already have all the answers. —Socrates",
    "Do what you feel in your heart to be right―for you’ll be criticized anyway. —Eleanor Roosevelt",
    "Happiness is not something ready made. It comes from your own actions. —Dalai Lama XIV",
    "Whatever you are, be a good one. —Abraham Lincoln",
    "Imagination is everything. It is the preview of life's coming attractions. —Albert Einstein",
    "If we have the attitude that it’s going to be a great day, it usually is. —Catherine Pulsifier",
    "You can either experience the pain of discipline or the pain of regret. The choice is yours. —Unknown",
    "Impossible is just an opinion. —Paulo Coelho",
    "Your passion is waiting for your courage to catch up. —Isabelle Lafleche",
    "Magic is believing in yourself. If you can make that happen, you can make anything happen. —Johann Wolfgang Von Goethe",
    "If something is important enough, even if the odds are stacked against you, you should still do it. —Elon Musk",
    "Hold the vision, trust the process. —Unknown",
    "Don’t be afraid to give up the good to go for the great. —John D. Rockefeller",
    "People who wonder if the glass is half empty or full miss the point. The glass is refillable. —Unknown"
]
    quote = random.choice(quote_list)
    await ctx.send(f"The Quote is {quote}")
# ~serverinfo
@client.command(brief="Displays server information", description="Provides details about the current server.")
async def serverinfo(ctx):
    server = ctx.guild 
    
    # Collecting server information
    server_name = server.name
    server_id = server.id
    owner = server.owner
    created_at = server.created_at.strftime('%Y-%m-%d %H:%M:%S')
    member_count = server.member_count
    text_channels = len(server.text_channels)
    voice_channels = len(server.voice_channels)
    roles = len(server.roles)
    
    # Creating an embed with the server information
    embed = discord.Embed(title=f"Server Information for {server_name}", color=discord.Color.blue())
    embed.add_field(name="Server Name", value=server_name, inline=True)
    embed.add_field(name="Server ID", value=server_id, inline=True)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Created At", value=created_at, inline=True)
    embed.add_field(name="Member Count", value=member_count, inline=True)
    embed.add_field(name="Text Channels", value=text_channels, inline=True)
    embed.add_field(name="Voice Channels", value=voice_channels, inline=True)
    embed.add_field(name="Roles", value=roles, inline=True)
    
    await ctx.send(embed=embed)

@client.command(brief="Shows the avatar of a user", description="Displays the avatar of a mentioned user or yourself if no user is mentioned.")
async def avatar(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author
    await ctx.send(f"{user.mention}'s avatar: {user.avatar.url}")

@client.command(brief="Set a reminder", description="Sets a reminder with a time duration and message.")
async def remindme(ctx, duration: str, *, message: str):
    seconds = parse_duration(duration)
    if seconds is None:
        await ctx.send("Invalid duration format. Please use format like `10m` for 10 minutes.")
        return
    reminder_time = datetime.now(timezone.utc) + timedelta(seconds=seconds)
    reminders[ctx.author.id] = (reminder_time, message)
    await ctx.send(f"Reminder set for {duration} from now!")

#! Slash commands

# /cutiemeter
@client.tree.command(name="cutiemeter", description="Rates how cute you are on a scale of 1 to 10.")
async def cutiemeter(interaction: discord.Interaction):
    rating_list = ["1/10", "2/10", "3/10", "4/10", "5/10", "6/10", "7/10", "8/10", "9/10", "10/10"]
    rating = random.choice(rating_list)
    await interaction.response.send_message(f"{interaction.user.mention} is a {rating} on the Cute o'meter :3")

# /ping
@client.tree.command(name="ping", description="Pings the bot and measures its latency.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Bot Pinged")

# /uptime
@client.tree.command(name="uptime", description="Displays how long the bot has been online.")
async def uptime(interaction: discord.Interaction):
    current_time = time.time()
    uptime_seconds = int(current_time - start_time)
    uptime_str = str(timedelta(seconds=uptime_seconds))
    await interaction.response.send_message(f"Bot has been up for: {uptime_str}")

# /roll
@client.tree.command(name="roll", description="Rolls a dice with a custom number of sides (e.g., 4, 6, 8, 10, 12, 20).")
async def roll(interaction: discord.Interaction, sides: int):
    if sides <= 0:
        await interaction.response.send_message(f"{interaction.user.mention}, dice must have a positive number of sides.")
        return
    roll_result = random.randint(1, sides)
    await interaction.response.send_message(f"{interaction.user.mention} rolled {roll_result} on a D{sides}")

# /quote
@client.tree.command(name="quote", description="Returns a random inspirational quote.")
async def quote(interaction: discord.Interaction):
    quote_list = [
        "All our dreams can come true, if we have the courage to pursue them. —Walt Disney",
        "The secret of getting ahead is getting started. —Mark Twain",
        "I’ve missed more than 9,000 shots in my career. I’ve lost almost 300 games. Twenty-six times I’ve been trusted to take the game-winning shot and missed. I’ve failed over and over and over again in my life, and that is why I succeed. —Michael Jordan",
        "Don’t limit yourself. Many people limit themselves to what they think they can do. You can go as far as your mind lets you. What you believe, remember, you can achieve. —Mary Kay Ash",
        "The best time to plant a tree was 20 years ago. The second best time is now. —Chinese proverb",
        "Only the paranoid survive. —Andy Grove",
        "It’s hard to beat a person who never gives up. —Babe Ruth",
        "I wake up every morning and think to myself, ‘How far can I push this company in the next 24 hours?’ —Leah Busque",
        "We need to accept that we won’t always make the right decisions, that we’ll screw up royally sometimes―understanding that failure is not the opposite of success, it’s part of success. —Arianna Huffington",
        "Write it. Shoot it. Publish it. Crochet it. Sauté it. Whatever. MAKE. —Joss Whedon",
        "If people are doubting how far you can go, go so far that you can’t hear them anymore. —Michele Ruiz",
        "You’ve gotta dance like there’s nobody watching, love like you’ll never be hurt, sing like there’s nobody listening, and live like it’s heaven on earth. —William W. Purkey",
        "Fairy tales are more than true: not because they tell us that dragons exist, but because they tell us that dragons can be beaten. —Neil Gaiman",
        "Everything you can imagine is real. —Pablo Picasso",
        "When one door of happiness closes, another opens; but often we look so long at the closed door that we do not see the one which has been opened for us. —Helen Keller",
        "Do one thing every day that scares you. —Eleanor Roosevelt",
        "It’s no use going back to yesterday, because I was a different person then. —Lewis Carroll",
        "Smart people learn from everything and everyone, average people from their experiences, stupid people already have all the answers. —Socrates",
        "Do what you feel in your heart to be right―for you’ll be criticized anyway. —Eleanor Roosevelt",
        "Happiness is not something ready made. It comes from your own actions. —Dalai Lama XIV",
        "Whatever you are, be a good one. —Abraham Lincoln",
        "Imagination is everything. It is the preview of life's coming attractions. —Albert Einstein",
        "If we have the attitude that it’s going to be a great day, it usually is. —Catherine Pulsifier",
        "You can either experience the pain of discipline or the pain of regret. The choice is yours. —Unknown",
        "Impossible is just an opinion. —Paulo Coelho",
        "Your passion is waiting for your courage to catch up. —Isabelle Lafleche",
        "Magic is believing in yourself. If you can make that happen, you can make anything happen. —Johann Wolfgang Von Goethe",
        "If something is important enough, even if the odds are stacked against you, you should still do it. —Elon Musk",
        "Hold the vision, trust the process. —Unknown",
        "Don’t be afraid to give up the good to go for the great. —John D. Rockefeller",
        "People who wonder if the glass is half empty or full miss the point. The glass is refillable. —Unknown"
    ]
    quote = random.choice(quote_list)
    await interaction.response.send_message(f"The Quote is: {quote}")

# /serverinfo
@client.tree.command(name="serverinfo", description="Displays detailed information about the server.")
async def serverinfo(interaction: discord.Interaction):

    server = interaction.guild
    
    # Collecting server information
    server_name = server.name
    server_id = server.id
    owner = server.owner
    created_at = server.created_at.strftime('%Y-%m-%d %H:%M:%S')
    member_count = server.member_count
    text_channels = len(server.text_channels)
    voice_channels = len(server.voice_channels)
    roles = len(server.roles)
    
    # Creating an embed with the server information
    embed = discord.Embed(title=f"Server Information for {server_name}", color=discord.Color.blue())
    embed.add_field(name="Server Name", value=server_name, inline=True)
    embed.add_field(name="Server ID", value=server_id, inline=True)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Created At", value=created_at, inline=True)
    embed.add_field(name="Member Count", value=member_count, inline=True)
    embed.add_field(name="Text Channels", value=text_channels, inline=True)
    embed.add_field(name="Voice Channels", value=voice_channels, inline=True)
    embed.add_field(name="Roles", value=roles, inline=True)
    
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="avatar", description="Displays the avatar of a mentioned user or yourself if no user is mentioned.")
async def slash_avatar(interaction: discord.Interaction, user: discord.User = None):
    if user is None:
        user = interaction.user
    await interaction.response.send_message(f"{user.mention}'s avatar: {user.avatar.url}")

@client.tree.command(name="remindme", description="Sets a reminder with a time duration and message.")
async def slash_remindme(interaction: discord.Interaction, duration: str, message: str):
    seconds = parse_duration(duration)
    if seconds is None:
        await interaction.response.send_message("Invalid duration format. Please use format like `10m` for 10 minutes.")
        return
    reminder_time = datetime.now(timezone.utc) + timedelta(seconds=seconds)
    reminders[interaction.user.id] = (reminder_time, message)
    await interaction.response.send_message(f"Reminder set for {duration} from now!")

#! reads token and starts
with open("Bot_token.txt") as f:
    token = f.read()

client.run(token)