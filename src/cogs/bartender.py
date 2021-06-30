import os
import random
import asyncio
import discord
from discord.ext import commands
from libs.database import DataBase
# from googletrans import Translator

class Bartender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = DataBase()
        # self.lang = str(os.environ['LANG']).lower()
        # self.translator = Translator()

    @commands.command(name = 'order')
    async def get_product(self, ctx, val):
        # Check producto registrado
        sql = f"SELECT * FROM productos WHERE nombre = '{val.lower()}';"
        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()

        if result == []:
            await ctx.send(f"Sry, there are not products registered with the name: {val.lower()}")
        else:
            # Check disponibilidad del producto registrado
            sql = f"SELECT nombre, url FROM imagenes WHERE nombre = '{val.lower()}';"
            self.database.cursor.execute(sql)
            result = self.database.cursor.fetchall()

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
        url = result[random.randint(0,len(result)-1)][1]
        embed.set_image(url=url)
        await message.delete()
        message = await ctx.send(embed = embed)
        for reaction in ['👍', '👎']:
            await message.add_reaction(reaction)
    
def setup(bot):
    bot.add_cog(Bartender(bot))