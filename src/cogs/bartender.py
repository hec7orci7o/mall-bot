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

    @commands.command()
    async def carta(self, ctx):
        menu = [("🥛","sin alcohol"),("🍺","con alcohol"),("🥩","carne"),("🍣","pescado"),("🍨","postres"),("🥜","tapas"),("🍭","chuches")]
        menu_formated = ''
        for cat in menu:
            menu_formated += cat[0] + ' - ' + cat[1] + '.\n'

        embed = discord.Embed(description=f"```{menu_formated}```", color=9224068)
        embed.set_author(name="Sections:", icon_url="https://static.vecteezy.com/system/resources/previews/000/639/289/original/vector-menu-icon-symbol-sign.jpg")
        embed.set_footer(text="Made with 💘 by Hec7orci7o.", icon_url="https://avatars.githubusercontent.com/u/56583980?s=60&v=4")
        message = await ctx.send(embed= embed)
        for reaction in ['🥛', '🍺','🥩','🍣','🍨','🥜','🍭']:
            await message.add_reaction(reaction)
        

        def check(reaction, user):
            if user == ctx.author and str(reaction.emoji) in ['🥛', '🍺','🥩','🍣','🍨','🥜','🍭']:
                return str(reaction.emoji)
            else:
                return ""

        reaction, user = await commands.wait_for('reaction_add', timeout=60.0, check=check)

        if reaction.emoji == "🥛":
            await ctx.send("sin alcohol")
        elif reaction.emoji == "🍺":
            await ctx.send("con alcohol")
        elif reaction.emoji == "🥩":
            await ctx.send("carne")
        elif reaction.emoji == "🍣":
            await ctx.send("pescado")
        elif reaction.emoji == "🍨":
            await ctx.send("postres")
        elif reaction.emoji == "🥜":
            await ctx.send("tapas")
        elif reaction.emoji == "🍭":
            await ctx.send("cuches")
        # https://stackoverflow.com/questions/52210855/give-role-when-a-user-add-reaction-discord-py
        
        # query que muestra todas las categorias
        # añadir reacciones con los tipos de categoria
            # escoger siguiente pagina a mostrar (ej : bebidas sin alcohol)
        # borrar embed anterior y mostrar el siguiente. Mostrar 5 productos en 3 columnas (5 5 5) 
            # y si hay mas mostrar un boton de paginacion avanzar y retroceder abajo
    
def setup(bot):
    bot.add_cog(Bartender(bot))