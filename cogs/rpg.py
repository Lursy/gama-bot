from discord.ext import commands
from Imagens import image
import discord
from random import randint
def resultado(p, v, d=20):
    normal = d+1 - p
    bom = d+1 - p//2
    extremo = d+1 - p // 5
    if v >= normal:
        response = 'Normal'
    elif v > 1 < normal:
        response = 'Falha'
    else:
        response = 'Desastre'
    if v >= bom:
        response = 'Bom'
    if v >= extremo:
        response = 'Extremo'
    return response
class RPG(commands.Cog):
    """Dados para rpg"""
    def __init__(self, bot):
        self.bot = bot
    @commands.command(msg='dado')
    async def dado(self, ctx, pericia='', dado='20'):
        name = f'{ctx.author.name}'
        dado = int(dado.strip('d'))
        valor = randint(1, dado)
        if name.lower() != 'jgkill' and name.lower() != 'big chungus':
            valor2 = randint(1, dado)
            if valor2 > valor:
                valor = valor2
        prc = rst = ''
        nome = f'Nome: {name}'
        if pericia != '':
            resul = resultado(int(pericia), valor, int(dado))
            prc = f'Pericia: {pericia}'
            rst = f'Resultado: {resul}'
        image.imagens_pericia(nome=nome, valor=str(valor), pericia=prc, resultado=rst)
        await ctx.send(file=discord.File(r'Imagens/resultado.png'))
    @commands.command(msg='lista')
    async def lista(self, ctx, tam='20'):
        d = int(tam)
        if d > 70:
            await ctx.send('Quantidade de caracteres não suportada')
            return 0
        string = ''
        for p in range(1, int(d) + 1):
            normal = d + 1 - p
            bom = normal + (p + 1) // 2
            extremo = d + 1 - p // 5
            string += f'{p:<4}- N:{normal:<4} B:{bom:<4} E:{extremo:<4}\n'
        await ctx.send(string)
    @commands.command(msg='dano')
    async def dano(self, ctx, *, dados):
        try:
            line = '━━━━━━━━━━━━━━━━━━━━━'
            dx = dados.replace(' ', '').split('+')
            vd = va = resultado = ''
            adicional = {}
            dado = {}
            dano = 0
            for item in dx:
                if item.isnumeric():
                    adicional['adicional: '] = item
                else:
                    print('foi')
                    if 'd' in item.casefold():
                        valores = item.split('d')
                        for c in range(0, int(valores[0])):
                            dado[f'{c+1}° d{valores[1]} = '] = str(randint(1, int(valores[1])))
            card = discord.Embed(color=0x000000)
            for key, value in dado.items():
                if len(dado) == 1:
                    vd = key + value + '\n'
                    dano += int(value)
                    resultado = value
                else:
                    vd += f'{key+value}\n'
                    dano += int(value)
            if len(dado) > 1:
                resultado = ' + '.join(dado.values())
            vd += line
            card.add_field(name=f'Rolagem: {dados}', value=vd, inline=False)
            if adicional:
                resultado += ' + '
                for key, value in adicional.items():
                    if len(adicional) == 1:
                        va += key + value
                        dano += int(value)
                    else:
                        va += f'{key + value}\n'
                        dano += int(value)
                if len(dado) > 1:
                    resultado += ' + '.join(adicional.values())
                va += '\n' + line
                card.add_field(name=f'Adicionais', value=va, inline=False)
            resultado = f'{resultado} = {dano}'
            card.add_field(name=f'Resultado', value=resultado, inline=False)
            card.set_footer(text='Distribuição GaMa', icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=card)
        except Exception as error:
            await ctx.send(f'O parâmetro "{dados}" não foi aceito\nErro: "{error}"')
def setup(bot):
    bot.add_cog(RPG(bot))
