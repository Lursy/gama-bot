from discord.ext import commands
import discord

queues = {}
loop = False


def check_queue(ctx, guild):
    if queues[guild]:
        client_voice = ctx.voice_client
        source = queues[guild].pop(0)
        try:
            client_voice.play(source, after=lambda x: check_queue(ctx, guild))
            client_voice.is_playing()
        except:
            pass


def search(query):
    from youtube_dl import YoutubeDL
    import requests

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': 'True',
        'before_options': '- reconnect 1 - reconnect_streamed 1 - reconnect_delay_max 5',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            requests.get(query)
        except:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        else:
            info = ydl.extract_info(query, download=False)
    return info


class Music(commands.Cog):
    """Musicas do YouTube para discord"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(msg='play')
    async def play(self, ctx, *, music):
        server = ctx.message.guild
        video = search(music)
        member_voice = ctx.author.voice
        ffmpeg = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        if member_voice and member_voice.channel:
            if not ctx.voice_client:
                await member_voice.channel.connect()
            client_voice = ctx.voice_client
            som = discord.FFmpegPCMAudio(source=video['formats'][0]['url'], **ffmpeg)
            segundos = video.get('duration')
            minuto = segundos//60
            segundos = segundos - minuto*60
            card = discord.Embed(color=0x000000)
            card.add_field(name='Musica', value=video['title'], inline=False)
            card.add_field(name='Canal', value=video['channel'], inline=False)
            card.add_field(name='Tempo', value=f'{minuto} minutos e {segundos} segundos', inline=False)
            card.set_image(url=video['thumbnail'])
            card.set_footer(text='Distribuição GaMa', icon_url=self.bot.user.avatar_url)
            if client_voice.is_playing():
                await ctx.send('Adicionado a lista', embed=card)
                if server.id in queues:
                    queues[server.id].append(som)
                else:
                    queues[server.id] = [som]
            else:
                await ctx.send(embed=card)
                queues[server.id] = [som]
                check_queue(ctx, server.id)

    @commands.command(msg='exit')
    async def exit(self, ctx):
        member_voice = ctx.author.voice
        if member_voice and member_voice.channel:
            if ctx.voice_client:
                if member_voice.channel == ctx.voice_client.channel:
                    try:
                        if ctx.voice_client.is_playing():
                            ctx.voice_client.stop()
                        queues.clear()
                        await ctx.voice_client.disconnect()
                        await ctx.send("Desconectado com sucesso!")
                    except Exception as error:
                        print(error)
                        await ctx.send('Erro ao desconectar-se')
                else:
                    await ctx.send("Você não esta na chamada!")
            else:
                await ctx.send(f"Você não está em uma chamada")

    @commands.command(msg='skip')
    async def skip(self, ctx):
        member_voice = ctx.author.voice
        client_voice = ctx.voice_client
        if member_voice and member_voice.channel:
            if ctx.voice_client:
                if member_voice.channel == ctx.voice_client.channel:
                    try:
                        if client_voice.is_playing():
                            client_voice.stop()
                            check_queue(ctx, ctx.message.guild.id)
                    except Exception as error:
                        print(error)
                        await ctx.send('Erro ao pular')
                else:
                    await ctx.send("Você não esta na chamada!")
            else:
                await ctx.send(f"Você não está em uma chamada")

    @commands.command(msg='loop')
    async def loop(self, ctx):
        global loop
        if not loop:
            loop = True
            await ctx.send('Loop ativo')
        else:
            loop = False
            await ctx.send('Loop desativado')

    @commands.command(msg='stop')
    async def stop(self, ctx):
        member_voice = ctx.author.voice
        if member_voice and member_voice.channel:
            try:
                if ctx.voice_client.is_playing():
                    ctx.voice_client.stop()
            except Exception as error:
                print(error)
                await ctx.send('O bot não esta tocando uma musica')
        else:
            await ctx.send('Você não está em uma chamada')


def setup(bot):
    bot.add_cog(Music(bot))
