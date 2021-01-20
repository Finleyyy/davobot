import timeit

import discord
from discord.ext import commands, ipc


class IpcRoutes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @ipc.server.route()
    async def get_guilds(self, data):
        guilddict = {"guild": [], "id": [], "members": []}
        for guild in self.bot.guilds:
            guilddict["guild"].append(str(guild.name))
            guilddict["id"].append(guild.id)
            guilddict["members"].append(guild.member_count)
        return guilddict

    @ipc.server.route()
    async def runPost(self, data):
        aserver = data.server
        guild = self.bot.get_guild(int(aserver))
        achannel = data.channel
        bchannel = discord.utils.get(guild.channels, name=achannel.lstrip('#'))
        amsg = data.msg
        await bchannel.send(amsg)
        return "ok"

    @ipc.server.route()
    async def get_bot_latency(self, data):
        return str(round(self.bot.latency, 3)) + "s"

    @ipc.server.route()
    async def get_runtime(self, data):
        stoppedtimer = timeit.default_timer()
        roundedtime = round((stoppedtimer - self.bot.timervar), 1)
        timestr = f"{roundedtime} seconds"
        return timestr

    @ipc.server.route()
    async def get_guildchannels(self, data):
        guild = self.bot.get_guild(data.id)
        listt = []
        for channel in guild.channels:
            if channel.type == discord.ChannelType.text or channel.type == discord.ChannelType.news:
                listt.append(str(channel))
        return listt

    @ipc.server.route()
    async def get_bot_name(self, data):
        return self.bot.user.name

    @ipc.server.route()
    async def getGuildbyID(self, data):
        guildid = data.id
        return str(self.bot.get_guild(guildid))


def setup(bot):
    bot.add_cog(IpcRoutes(bot))
