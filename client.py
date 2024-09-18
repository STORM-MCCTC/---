import discord
from discord.ext import commands, tasks
import random
import time
import asyncio
import re
from datetime import datetime, timedelta, timezone
import sqlite3

#! ----------| Version - 0.1.1 |---------- !#

client = commands.Bot(command_prefix="~", intents=discord.Intents.all())

start_time = time.time()

reminders = {}

version_number = "Version - 0.1.1" 

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
    execute_sql_file('client.sql')
    await client.tree.sync()
    print("Bot Connected")

def execute_sql_file(filename):
    with open(filename, 'r') as sql_file:
        sql_script = sql_file.read()
    
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Execute the SQL script
    cursor.executescript(sql_script)
    
    conn.commit()
    conn.close()

#! Prefix commands

# ~meow
@client.command(brief="meow meow :3", description="Meow Meow :3")
async def meow(ctx):
    meow_list = ["Meow :3", "Meow meow", "Bark >:3", "Bark bark >:3", "Meow Meow :3", "*Cat sounds*", "Nuh uh", ":3", "Meow", "Meow"]
    meow = random.choice(meow_list)
    await ctx.send(meow)

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
async def quote(ctx):
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

# ~avatar
@client.command(brief="Shows the avatar of a user", description="Displays the avatar of a mentioned user or yourself if no user is mentioned.")
async def avatar(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author
    await ctx.send(f"{user.mention}'s avatar: {user.avatar.url}")

# ~remindme
@client.command(brief="Set a reminder", description="Sets a reminder with a time duration and message.")
async def remindme(ctx, duration: str, *, message: str):
    seconds = parse_duration(duration)
    if seconds is None:
        await ctx.send("Invalid duration format. Please use format like `10m` for 10 minutes.")
        return
    reminder_time = datetime.now(timezone.utc) + timedelta(seconds=seconds)
    reminders[ctx.author.id] = (reminder_time, message)
    await ctx.send(f"Reminder set for {duration} from now!")

# ~version
@client.command()
async def version(ctx):
    await ctx.send(version_number)
    

#! Slash commands

# /meow
@client.tree.command(name="meow", description="Meow Meow :3")
async def meow(interaction: discord.Interaction):
    meow_list = ["Meow :3", "Meow meow", "Bark >:3", "Bark bark >:3", "Meow Meow :3", "*Cat sounds*", "Nuh uh", ":3", "Meow", "Meow"]
    meow = random.choice(meow_list)
    await interaction.response.send_message(meow)

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

#! admin commands

# ~kick (Admin Only)
@client.command(brief="Kick a user from the server", description="Kicks the specified user with an optional reason")
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if member == ctx.author:
        await ctx.send("You cannot kick yourself!")
        return
    
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked from the server. Reason: {reason or 'No reason provided.'}")

# ~ban (Admin Only)
@client.command(brief="Ban a user from the server", description="Bans the specified user with an optional reason")
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if member == ctx.author:
        await ctx.send("You cannot ban yourself!")
        return
    
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned from the server. Reason: {reason or 'No reason provided.'}")

# ~unban (Admin Only)
@client.command(brief="Unban a previously banned user", description="Unbans the user by their name and discriminator")
@commands.has_permissions(administrator=True)  # Requires Administrator permission
async def unban(ctx, *, member_name):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member_name.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} has been unbanned.")
            return

    await ctx.send(f"User {member_name}#{member_discriminator} was not found.")

# ~mute (Admin Only)
@client.command(brief="Mute a user in the server", description="Mutes the specified user for a certain duration")
@commands.has_permissions(administrator=True)  # Requires Administrator permission
async def mute(ctx, member: discord.Member, duration: int = 10, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)
    
    await member.add_roles(muted_role)
    await ctx.send(f"{member.mention} has been muted for {duration} minutes. Reason: {reason or 'No reason provided.'}")
    
    # Unmute after the duration expires
    await discord.utils.sleep_until(datetime.now() + timedelta(minutes=duration))
    await member.remove_roles(muted_role)
    await ctx.send(f"{member.mention} has been unmuted.")

# ~warn (Admin Only)
warnings = {}  # Keep track of warnings

@client.command(brief="Warn a user", description="Issues a warning to the specified user with an optional reason")
@commands.has_permissions(administrator=True)  # Requires Administrator permission
async def warn(ctx, member: discord.Member, *, reason=None):
    if member == ctx.author:
        await ctx.send("You cannot warn yourself!")
        return
    
    if member not in warnings:
        warnings[member] = []
    
    warnings[member].append((reason, datetime.now()))
    await ctx.send(f"{member.mention} has been warned. Reason: {reason or 'No reason provided.'}")

# ~clear (Admin Only)
@client.command(brief="Clear a number of messages in a channel", description="Clears the specified number of messages from the channel")
@commands.has_permissions(administrator=True)  # Requires Administrator permission
async def clear(ctx, amount: int):
    if amount <= 0:
        await ctx.send("The number of messages to clear must be greater than zero.")
        return

    await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message itself
    await ctx.send(f"Cleared {amount} messages.", delete_after=5)

# Error handling for permission errors
@kick.error
@ban.error
@unban.error
@mute.error
@warn.error
@clear.error

async def command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the necessary permissions to use this command.")
    else:
        await ctx.send("An error occurred while processing the command.")

#! link commands

@client.command(name='setlink', brief="sets a twitch link", description="sets a twitch link")
async def set_twitch_link(ctx, twitch_link: str):
    guild_id = ctx.guild.id

    # Connect to the database
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Insert or replace the link for this guild
    cursor.execute('''
    INSERT INTO twitch_links (guild_id, twitch_link) 
    VALUES (?, ?)
    ON CONFLICT(guild_id) 
    DO UPDATE SET twitch_link=excluded.twitch_link
    ''', (guild_id, twitch_link))

    conn.commit()
    conn.close()

    await ctx.send(f"Twitch link has been set to {twitch_link}")

@client.command(name='twitch', brief="sends a twitch link", description="sets a twitch link")
async def get_twitch_link(ctx):
    guild_id = ctx.guild.id

    # Connect to the database
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Retrieve the Twitch link for the guild
    cursor.execute('SELECT twitch_link FROM twitch_links WHERE guild_id = ?', (guild_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        await ctx.send(f"Here is the Twitch link: {result[0]}")
    else:
        await ctx.send("No Twitch link set for this server.")

#! reads token and starts

with open("client_token.txt") as f:
    token = f.read()

client.run(token)