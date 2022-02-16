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
        if name.lower() != 'big chungus':
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
    async def dano(self, ctx, *, dano):

        card = discord.Embed(color=0x000000)
        try:
            import random

            rolagem = dano
            val = {}
            sinais = {}
            cont = 0
            dano = dano.replace(' ', '')

            for c, item in enumerate(dano):
                if not item.isalnum():
                    if c != 0:
                        cont += 1
                        dano = dano.replace(item, ',')
                    else:
                        dano = dano[1:]
                    sinais[cont] = item

            dano = dano.split(',')

            for c, item in enumerate(dano):
                if 'd' in item:
                    dado = item.split('d')
                    for cont in range(0, int(dado[0])):
                        if cont == 0:
                            dano.pop(c)
                            val[c] = [str(random.randint(1, int(dado[1])))]
                        else:
                            val[c].append(str(random.randint(1, int(dado[1]))))

            tam = len(dano)

            for key, value in val.items():
                if len(dano) != tam:
                    key += 1
                    tam = len(dano)
                dano.insert(key, str(eval('+'.join((value)))))

            tam = len(dano)
            cont = 1

            for k, v in sinais.items():
                if len(dano) != tam:
                    k += cont
                    cont += 1
                    tam = len(dano)
                dano.insert(k, v.replace('*', '×'))

            card.add_field(name=f'Dados na mesa!', value=f"{rolagem}\n"+"".join(dano) + f' = {eval(" ".join(dano))}', inline=False)
            await ctx.send(embed=card)
        except Exception as error:
            await ctx.send(f'O parâmetro "{dano}" não foi aceito\nErro: "{error}"')


def setup(bot):
    bot.add_cog(RPG(bot))
