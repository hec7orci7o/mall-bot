import random
import asyncio
import discord
from discord.ext import commands
from libs.database import DataBase
from googletrans import Translator
# import os
from decouple import config

class Bartender(commands.Cog):
    def __init__(self, bot):
        self.bot  = bot
        # self.lang = os.environ['LANG']  
        self.lang = config('LANG')
        self.database   = DataBase()
        self.translator = Translator()

    @commands.command(name = 'order')
    async def get_product(self, ctx, val):
        # Check producto registrado
        sql = """SELECT nombre FROM productos WHERE nombre = '{}';""".format(val.lower())
        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()

        if result == []:
            await ctx.send("Sry, there are not products registered with the name: {}".format(val.lower()))
        else:
            # Check disponibilidad del producto registrado
            sql = """SELECT nombre, url FROM imagenes WHERE nombre = '{}';""".format(val.lower())
            self.database.cursor.execute(sql)
            result = self.database.cursor.fetchall()

            if result == []:
                await ctx.send("Sry, there are not enought {}".format(val.lower()))
            else:
                await self.get_item(ctx, val.lower(), result)

    async def get_item(self, ctx, val, result):
        msg_1 = "Please wait while I prepare your order..."
        msg_2 = f"Here is your {val.lower()}."

        await ctx.trigger_typing()
        embed = discord.Embed(
            title = f"{self.translator.translate(text=msg_1, dest=self.lang).text}",
            color = 16777215
        )
        message = await ctx.send(embed = embed)
        await ctx.trigger_typing()
        await asyncio.sleep(5)
        embed = discord.Embed (
            title = f"{self.translator.translate(text=msg_2, dest=self.lang).text}",
            color = 16777215
        )
        url = result[random.randint(0,len(result)-1)][1]
        embed.set_image(url=url)
        await message.delete()
        message = await ctx.send(embed = embed)
        for reaction in ['👍', '👎']:
            await message.add_reaction(reaction)
    
def setup(bot):
    bot.add_cog(Bartender(bot))