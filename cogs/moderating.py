import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, ChannelNotFound, MissingRequiredArgument

class ModeratingCOG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='post', description='Posts a message in given channel')
    @commands.has_permissions(kick_members=True)
    async def post(self, ctx, channel: discord.TextChannel, *args):
        if not checkstr(channel):
            if len(args) != 0:
                await channel.send(" ".join(args))
                emoji = "✅"
                await ctx.message.add_reaction(emoji)
            else:
                await ctx.send("You need to specify a message to send!")

    @commands.command(name='leave', description='Sends an image with instructions to leave')
    async def leave(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/527876598834135047/823679128117051402/unknown.png")

    @commands.command(name='emergency', description='Mentions the mods', aliases=['emerg'])
    async def emerg(self, ctx):
        guild = ctx.bot.get_guild(527869594279477251)
        role = guild.get_role(817919947862704128)
        for me in role.members:
            await me.send(f"Emergency on Davolaf's server! Issued by <@{ctx.author.id}> / {ctx.author.id}")
        await ctx.send("<@&528156484886855708> There's an emergency!")


    @commands.command(name='invite', description='Sends an invite link to the Discord')
    async def invite(self, ctx):
        await ctx.send("https://discord.gg/ru7qzEEQ5w")

    @post.error
    async def post_permerror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have the required permissions to use this command!")
        if isinstance(error, ChannelNotFound):
            await ctx.send("Please specify a valid channel!")
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("You didn't specify any channel or text!")


def checkstr(string):
    if isinstance(string, str):
        return True
    elif isinstance(string, discord.TextChannel):
        return False


def setup(bot):
    bot.add_cog(ModeratingCOG(bot))
