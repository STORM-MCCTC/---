from discord import app_commands
from discord.ext import commands
import discord
import random
from datetime import datetime, timedelta, timezone

class SlashCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="meow", description="Meow Meow :3")
    async def meow(self, interaction: discord.Interaction):
        meow_list = ["Meow :3", "Bark >:3", "*Cat sounds*"]
        meow = random.choice(meow_list)
        await interaction.response.send_message(meow)

    @app_commands.command(name="cutiemeter", description="Rates how cute you are")
    async def cutiemeter(self, interaction: discord.Interaction):
        rating = random.choice([f"{x}/10" for x in range(1, 11)])
        await interaction.response.send_message(f"{interaction.user.mention} is a {rating} on the Cute o'meter!")

    @app_commands.command(name="ping", description="Ping the bot")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Bot Pinged")

    @app_commands.command(name="roll", description="Roll a dice")
    async def roll(self, interaction: discord.Interaction, sides: int):
        if sides <= 0:
            await interaction.response.send_message("Sides must be greater than zero.")
            return
        roll_result = random.randint(1, sides)
        await interaction.response.send_message(f"{interaction.user.mention} rolled {roll_result} on a D{sides}")

# Adding the cog to the bot
async def setup(client):
    await client.add_cog(SlashCommands(client))
