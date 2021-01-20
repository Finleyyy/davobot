import os
import timeit

import discord
from discord.ext import commands, ipc
from dotenv import load_dotenv

import SQL

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ipc_secret = os.getenv('IPC_SECRET')
initial_extensions = ['cogs.mal', 'cogs.moderating']

print('----- Running setupSQL -----')
print('...')
SQL.setupSQL()
print('----- SQL setup done -----')

intents = discord.Intents.default()
intents.guilds = True


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ipc = ipc.Server(self, "localhost", 8765, ipc_secret)
        self.load_extension("cogs.ipc")

    async def on_ready(self):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='anime'))
        print(f'-- The bot is currently in {len(bot.guilds)} servers')
        botUser = bot.user.name + '#' + bot.user.discriminator
        print(f'-- Logged in as {botUser}')

    async def on_ipc_ready(self):
        print('IPC ready')


bot = Bot(command_prefix="!", case_insensitive=True, intents=intents)

bot.remove_command('help')
bot.timervar = timeit.default_timer()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower().__contains__('davobot'):
        emoji = '👋'
        await message.add_reaction(emoji)
        print(message.author.id)
    await bot.process_commands(message)


@bot.command(name='ping', description='Returns the bots latency')
async def ping(ctx):
    await ctx.send('Pong! {0} seconds latency'.format(round(bot.latency, 3)))


if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)
    bot.ipc.start()
    bot.run(TOKEN)
