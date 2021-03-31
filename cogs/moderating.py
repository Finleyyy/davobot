import discord
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions, ChannelNotFound, MissingRequiredArgument
from mcstatus import MinecraftServer


class ModeratingCOG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.water.start()
        self.mcstatus.start()

    def cog_unload(self):
        self.water.cancel()
        self.mcstatus.cancel()

    async def updatemc(self, channelid):
        server = MinecraftServer.lookup("75.119.138.254:25565")
        stri = "The server is currently offline!"
        if server is not None:
            stri = f"Online players: {server.status().players.online}"
        await self.bot.get_channel(channelid).edit(topic=stri)

    @tasks.loop(minutes=5)
    async def mcstatus(self):
        await self.updatemc(818135582341070878)

    @tasks.loop(hours=1)
    async def water(self):
        # general-chatter
        channel = self.bot.get_channel(527876598834135047)
        await channel.send("Drink water guys!")

    @water.before_loop
    async def before_water(self):
        await self.bot.wait_until_ready()

    @mcstatus.before_loop
    async def before_mcstatus(self):
        await self.bot.wait_until_ready()

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
    @commands.cooldown(1, 30)
    async def emerg(self, ctx):
        guild = ctx.bot.get_guild(527869594279477251)
        role = guild.get_role(817919947862704128)
        for me in role.members:
            await me.send(f"Emergency on Davolaf's server! Issued by <@{ctx.author.id}> / {ctx.author.id}")
        await ctx.send("<@&528156484886855708> There's an emergency!")

    @commands.command(name='invite', description='Sends an invite link to the Discord')
    async def invite(self, ctx):
        await ctx.send("https://discord.gg/ru7qzEEQ5w")

    @commands.command(name='mcupdate', description='Updates the Minecraft server user count', aliases=['mcu'])
    async def mcupdate(self, ctx):
        await self.updatemc(818135582341070878)
        await ctx.message.delete()

    @commands.command(name='urbandictionary', description='Sends link to given word in Urban Dictionary', aliases=['ud', 'urban', 'urbandict'])
    async def urbandictionary(self, ctx, *, arg):
        argu = arg.replace(' ', '%20')
        await ctx.send('https://www.urbandictionary.com/define.php?term={0}'.format(argu))

    @urbandictionary.error
    async def udict_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You need to give a word to look up!')

    @emerg.error
    async def emerg_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You can't use the emergency command!")
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("The command is on cooldown!")

    @post.error
    async def post_error(self, ctx, error):
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
