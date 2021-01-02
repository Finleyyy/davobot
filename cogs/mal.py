import discord
from discord.ext import commands


class MALCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='mal', description="Sends link to given MAL")
    async def mal(self, ctx, arg="Davolaf"):
        malUrl = 'https://myanimelist.net/animelist/' + arg
        await ctx.send(arg + '\'s MAL: \n' + malUrl)

    @commands.command(name='test', description="Test version of the mal command")
    async def test(self, ctx, arg="Davolaf"):
        embed = discord.Embed(title="MyAnimeList", color=0x2e51a2)
        embed.set_thumbnail(url="https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png")
        embed.add_field(name=arg + "\'s MAL:", value="https://myanimelist.net/animelist/" + arg, inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MALCog(bot))
