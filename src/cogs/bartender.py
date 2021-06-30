import random
import asyncio
import discord
from discord.ext import commands
from libs.database import DataBase

class Bartender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = DataBase()

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
        await ctx.trigger_typing()
        embed = discord.Embed(
            title = f"Please wait while I prepare your order...",
            color = 16777215
        )
        message = await ctx.send(embed = embed)
        await ctx.trigger_typing()
        await asyncio.sleep(5)
        embed = discord.Embed (
            title = f"Here is your {val.lower()}, sir.",
            color = 16777215
        )
        url = "https://img2.pngio.com/botella-agua-png-4-png-image-botella-de-agua-png-800_600.png"
        embed.set_image(url=url)
        await message.delete()
        message = await ctx.send(embed = embed)
        for reaction in ['👍', '👎']:
            await message.add_reaction(reaction)
    
def setup(bot):
    bot.add_cog(Bartender(bot))