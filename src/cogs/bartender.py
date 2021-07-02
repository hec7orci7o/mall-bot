import os
import random
import asyncio
import discord
from discord.ext import commands
from libs.database import DataBase
import libs.utils as util
# from googletrans import Translator

class Bartender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.lang = str(os.environ['LANG']).lower()
        # self.translator = Translator()

    @commands.command(name = 'order')
    async def get_product(self, ctx, val):
        # Check producto registrado
        try:
            database = DataBase()
            sql = f"SELECT * FROM productos WHERE nombre = '{val.lower()}';"
            database.cursor.execute(sql)
            result = database.cursor.fetchall()
            del database
        except database.mysql.connector.Error as err:
                await ctx.send(embed= util.fail(err))
                del database

        if result == []:
            await ctx.send(f"Sry, there are not products registered with the name: {val.lower()}")
        else:
            # Check disponibilidad del producto registrado
            try:
                database = DataBase()
                sql = f"SELECT nombre, url FROM imagenes WHERE nombre = '{val.lower()}';"
                database.cursor.execute(sql)
                result = database.cursor.fetchall()
                del database
            except database.mysql.connector.Error as err:
                await ctx.send(embed= util.fail(err))
                del database

            if result == []:
                await ctx.send(f"Sry, there are not enought {val.lower()}")
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
    
def setup(bot):
    bot.add_cog(Bartender(bot))