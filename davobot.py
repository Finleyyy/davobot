import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')
initial_extensions = ['cogs.mal']

bot.remove_command('mal')

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="anime"))
    botUser = bot.user.name + '#' + bot.user.discriminator
    print('Logged in as ' + botUser)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower().__contains__('davobot'):
        emoji = '👋'
        await message.add_reaction(emoji)
    await bot.process_commands(message)


@bot.command(name='ping', description="Returns the bots latency")
async def ping(ctx):
    await ctx.send('Pong! {0} seconds latency'.format(round(bot.latency, 3)))


print("Bot is ready!")
bot.run(TOKEN)
