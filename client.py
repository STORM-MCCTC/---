import discord
from discord.ext import commands
import random

client = commands.Bot(command_prefix="~", intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.tree.sync()
    print("Bot Connected")

@client.command(brief="", description="")
async def cutiemeter(ctx):
    rating_list = ["1/10", "2/10", "3/10", "4/10", "5/10", "6/10", "7/10", "8/10", "9/10", "10/10"]
    rating = random.choice(rating_list)
    await ctx.send(f"Your Cute o'meter rating is {rating} :3")

@client.command(brief="Pings Bot", description="Pings Bot")
async def ping(ctx):
    await ctx.send("Bot Pinged")

@client.command(brief="Roll a D4", description="Rolls a Four sided Dice")
async def d4(ctx):
    D4L = [1, 2, 3, 4]
    D4 = random.choice(D4L)
    await ctx.send(f"You rolled {D4} on a D4")

@client.command(brief="Roll a D6", description="Rolls a Six sided Dice")
async def d6(ctx):
    D6L = [1, 2, 3, 4, 5, 6]
    D6 = random.choice(D6L)
    await ctx.send(f"You rolled {D6} on a D6")

@client.command(brief="Roll a D8", description="Rolls a Eight sided Dice")
async def d8(ctx):
    D8L = [1, 2, 3, 4, 5, 6, 7, 8]
    D8 = random.choice(D8L)
    await ctx.send(f"You rolled {D8} on a D8")

@client.command(brief="Roll a D10", description="Rolls a Ten sided Dice")
async def d10(ctx):
    D10L = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    D10 = random.choice(D10L)
    await ctx.send(f"You rolled {D10} on a D10")

@client.command(brief="Roll a D12", description="Rolls a Twelve sided Dice")
async def d12(ctx):
    D12L = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    D12 = random.choice(D12L)
    await ctx.send(f"You rolled {D12} on a D12")

@client.command(brief="Roll a D20", description="Rolls a twenty sided Dice")
async def d20(ctx):
    D20L = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    D20 = random.choice(D20L)
    await ctx.send(f"You rolled {D20} on a D20")

with open("Bot_token.txt") as f:
    token = f.read()

client.run(token)