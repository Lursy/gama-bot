from discord.ext import commands
from decouple import config


bot = commands.Bot(".")

bot.load_extension(f'cogs.extra')
bot.load_extension(f'cogs.rpg')
bot.load_extension(f'cogs.music')

TOKEN = config("TOKEN")
bot.run(TOKEN)