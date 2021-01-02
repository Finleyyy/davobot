import discord
from discord.ext import commands

import SQL


def createEmbed(arg):
    embed = discord.Embed(title="MyAnimeList", color=0x2e51a2)
    embed.set_thumbnail(url="https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png")
    embed.add_field(name=arg + "\'s MAL:", value="https://myanimelist.net/animelist/" + arg, inline=True)
    return embed


def strToList(string):
    listRes = list(string.split(" "))
    return listRes


class MALCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='mal', description="Sends link to given MAL")
    async def mal(self, ctx, *args):
        if len(args) > 1:
            await ctx.send('The username must not contain any spaces.')
        elif len(args) == 1:
            await ctx.send(embed=createEmbed(args[0]))
        elif len(args) == 0:
            author = f"{ctx.author.name}#{ctx.author.discriminator}"
            checkLink = SQL.checkLink(author)
            if len(checkLink) > 0:
                convStr = checkLink[0].lstrip('(').rstrip(')').replace(',', '', 1).replace('\'', '', 4)
                strB = strToList(convStr)[1]
                await ctx.send(embed=createEmbed(strB))
            else:
                await ctx.send(embed=createEmbed("Davolaf"))

    @commands.command(name='malink', description="Allows you to set your MAL username")
    async def malink(self, ctx, *args):
        if len(args) == 0:
            await ctx.send('You have to specify a username!')
        elif len(args) == 1:
            author = f"{ctx.author.name}#{ctx.author.discriminator}"
            command = SQL.addLink(author, args[0])
            if str(command).startswith('duplicate'):
                await ctx.send('You already linked your MAL!')
            else:
                await ctx.send(f'You succesfully set \"{args[0]}\" as your MAL username.')
        elif len(args) > 1:
            await ctx.send('The username must not contain any spaces!')

    @commands.command(name='madlink', description="Allows you to remove your MAL username")
    async def madlink(self, ctx):
        author = f"{ctx.author.name}#{ctx.author.discriminator}"
        SQL.delLink(author)
        await ctx.send('Your MAL username was cleared!')


def setup(bot):
    bot.add_cog(MALCog(bot))
