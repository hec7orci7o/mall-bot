import os
import random
import asyncio
import discord
import libs.utils as util
import libs.helper as helper
from discord.ext import commands
from libs.database import DataBase
import libs.utils as util
# from googletrans import Translator

class Bartender(helper.Helper, commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.lang = str(os.environ['LANG']).lower()
        # self.translator = Translator()

    @commands.command(name = 'order')
    async def get_product(self, ctx, val):
        # Check producto registrado
        result = await self.read(ctx, f"SELECT * FROM productos WHERE nombre = '{val.lower()}';")

        if result == []:
            await ctx.send(embed= util.fail(f"Sry, there are not products registered with the name: {val.lower()}"))
        else:
            # Check disponibilidad del producto registrado
            result = await self.read(ctx, f"SELECT nombre, url FROM imagenes WHERE nombre = '{val.lower()}';")

            if result == []:
                await ctx.send(embed= util.fail(f"Sry, there are not enought {val.lower()}"))
            else:
                await self.get_item(ctx, val.lower(), result)
    
    async def get_item(self, ctx, val, result):
        msg_1 = "Please wait while I prepare your order..."
        msg_2 = f"Here is your {val.lower()}."

        # msg_1 = str(self.translator.translate(text=msg_1, dest=self.lang).text)
        # msg_2 = str(self.translator.translate(text=msg_2, dest=self.lang).text)

        await ctx.trigger_typing()
        embed = discord.Embed(
            title = f"{msg_1}",
            color = 16777215
        )
        message = await ctx.send(embed = embed)
        await ctx.trigger_typing()
        await asyncio.sleep(5)
        embed = discord.Embed (
            title = f"{msg_2}",
            color = 16777215
        )
        embed.set_image(url= result[random.randint(0,len(result)-1)][1])
        await message.delete()
        message = await ctx.send(embed= embed)
        for reaction in ['👍', '👎']:
            await message.add_reaction(reaction)

    async def carta(self, ctx):
        menu = [("🥛","sin alcohol"),("🍺","con alcohol"),("🥩","carne"),("🍣","pescado"),("🍨","postres"),("🥜","tapas"),("🍭","chuches")]
        menu_formated = ''
        menu_formated += menu[iter][0] + ' - ' + menu[iter][1] + '.\n'

        embed = discord.Embed(description=f"```c++\n{menu_formated}```", color=9224068)
        embed.set_author(name="Sections:", icon_url="https://static.vecteezy.com/system/resources/previews/000/639/289/original/vector-menu-icon-symbol-sign.jpg")
        embed.set_footer(text="Made with 💘 by Hec7orci7o.", icon_url="https://avatars.githubusercontent.com/u/56583980?s=60&v=4")
        await ctx.send(embed= embed)
        # query que muestra todas las categorias
        # añadir reacciones con los tipos de categoria
            # escoger siguiente pagina a mostrar (ej : bebidas sin alcohol)
        # borrar embed anterior y mostrar el siguiente. Mostrar 5 productos en 3 columnas (5 5 5) 
            # y si hay mas mostrar un boton de paginacion avanzar y retroceder abajo
        pass
    
def setup(bot):
    bot.add_cog(Bartender(bot))