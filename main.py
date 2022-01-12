from discord.ext import commands

bot = commands.Bot(".")

bot.load_extension(f'cogs.extra')
bot.load_extension(f'cogs.rpg')
bot.load_extension(f'cogs.music')

bot.run("ODk0MjYzMTIxNTIxMzExODM1.YVndbg.ULl9OXYuEPGzaOg7nGw7Gfz-jjc")
