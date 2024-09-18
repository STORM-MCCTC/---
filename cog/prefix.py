import discord
from discord.ext import commands
import random
from datetime import timedelta
import time

class PrefixCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Meow Meow :3")
    async def meow(self, ctx):
        meow_list = ["Meow :3", "Bark >:3", "*Cat sounds*"]
        await ctx.send(random.choice(meow_list))

    @commands.command(brief="Rates how cute you are")
    async def cutiemeter(self, ctx):
        rating = random.choice([f"{x}/10" for x in range(1, 11)])
        await ctx.send(f"{ctx.author.mention} is a {rating} on the Cute o'meter!")

    @commands.command(brief="Ping the bot")
    async def ping(self, ctx):
        await ctx.send("Bot Pinged")

    @commands.command(brief="Show bot uptime")
    async def uptime(self, ctx):
        current_time = time.time()
        uptime_seconds = int(current_time - start_time)
        uptime_str = str(timedelta(seconds=uptime_seconds))
        await ctx.send(f"Bot has been up for: {uptime_str}")

# Adding the cog to the bot
async def setup(client):
    await client.add_cog(PrefixCommands(client))
