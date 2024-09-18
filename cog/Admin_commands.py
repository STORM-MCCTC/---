from discord.ext import commands
import discord

class AdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Kick a user", description="Kicks the specified user with an optional reason")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if member == ctx.author:
            await ctx.send("You cannot kick yourself!")
            return
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked. Reason: {reason or 'No reason provided.'}")

    @commands.command(brief="Ban a user", description="Bans the specified user with an optional reason")
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if member == ctx.author:
            await ctx.send("You cannot ban yourself!")
            return
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned. Reason: {reason or 'No reason provided.'}")

    @commands.command(brief="Unban a user", description="Unbans a previously banned user")
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member_name):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member_name.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention} has been unbanned.")
                return
        await ctx.send(f"User {member_name}#{member_discriminator} not found.")

    @commands.command(brief="Mute a user", description="Mutes the user for a specified duration")
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, duration: int = 10, *, reason=None):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)
        await member.add_roles(muted_role)
        await ctx.send(f"{member.mention} muted for {duration} minutes. Reason: {reason or 'No reason provided.'}")
        await discord.utils.sleep_until(datetime.now() + timedelta(minutes=duration))
        await member.remove_roles(muted_role)
        await ctx.send(f"{member.mention} has been unmuted.")

# Adding the cog to the bot
async def setup(client):
    await client.add_cog(AdminCommands(client))
