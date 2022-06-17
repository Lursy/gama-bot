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
        prc = rst = ''
        nome = f'Nome: {name}'
        if pericia != '':
            resul = resultado(int(pericia), valor, int(dado))
            prc = f'Pericia: {pericia}'
            rst = f'Resultado: {resul}'
        image.imagens_pericia(nome=nome, valor=str(valor), pericia=prc, resultado=rst)
        await ctx.send(file=discord.File(r'Imagens/resultado.png'))

    @commands.command(msg='lista')
    async def lista(self, ctx, per):
        per = int(per)
        normal = 21 - per
        bom = 21 - per//2
        extremo = 21  - per//5 
        await ctx.send(f'N:{normal:<4} B:{bom:<4} E:{extremo:<4}\n')

    @commands.command(msg='resul')
    async def resul(self, ctx, v, p):
        resul = resultado(p, v)
        await ctx.send(f'Essa merda é {resul}')

    @commands.command(msg='dano')
    async def dano(self, ctx, *, dano):

        card = discord.Embed(color=0x000000)
        try:
            import random
            valores = ''
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
                    print(item)
                    sinais[cont] = item

            dano = dano.split(',')

            for c, item in enumerate(dano):
                if 'd' in item:
                    dado = item.split('d')
                    for cont in range(0, int(dado[0])):
                        gerado = str(random.randint(1, int(dado[1])))
                        valores += f'{cont + 1}° d{dado[1]}: {gerado}\n'
                        if cont == 0:
                            val[c] = [gerado]
                        else:
                            val[c].append(gerado)
                        print("VAL:", val)

            for c, item in enumerate(val.keys()):
                dano.pop(item - c)

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
                dano.insert(k, v)

            card.add_field(name=f'Dados na mesa!', value=f"{rolagem.replace('*', 'x')}\n\n" + valores + "\n" + "".join(dano).replace('*', 'x') + f' = {eval(" ".join(dano))}', inline=False)
            await ctx.send(embed=card)
        except Exception as error:
            await ctx.send(f'O parâmetro "{dano}" não foi aceito\nErro: "{error}"')


def setup(bot):
    bot.add_cog(RPG(bot))
