from discord.ext import commands
import discord


class Extra(commands.Cog):
    """Funções extra"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(msg='cls')
    async def cls(self, ctx, qnt=1000):
        await ctx.channel.purge(limit=qnt)

    @commands.command(msg='gostosura')
    async def gostosura(self, ctx):
        import random
        card = discord.Embed(color=0x000000)
        card.add_field(name='Nivel de gostoso(a): ', value=f'Você é {random.randint(0, 100)}% GOSTOSO(a)', inline=False)
        await ctx.send(embed=card)

    @commands.command(msg='gtts')
    async def gtts(self, ctx, lang, *, frase):
        from gtts import gTTS
        member_voice = ctx.author.voice
        if member_voice and member_voice.channel:
            if not ctx.voice_client:
                await member_voice.channel.connect()
            if not ctx.voice_client.is_playing():
                busca = gTTS(text=frase, lang=lang)
                busca.save('musica.ogg')
                ctx.voice_client.play(discord.FFmpegPCMAudio(r'musica.ogg'))


def setup(bot):
    bot.add_cog(Extra(bot))
