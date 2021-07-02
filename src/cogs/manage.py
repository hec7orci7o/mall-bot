import discord
from discord.ext import commands
from libs.database import DataBase as db
import libs.utils as util


class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Check producto registrado
    async def check(self,ctx, val: str):
        try:
            database = db.DataBase()
            sql = f"SELECT count(*) FROM imagenes WHERE nombre = '{val.lower()}';"
            database.cursor.execute(sql)
            result = database.cursor.fetchall()
            del database
        except db.mysql.connector.Error as err:
            await ctx.send(embed= util.fail(err))
            del database
            
        print(str(result)[2:-3])
        return int(str(result)[2:-3])

    async def write(self, ctx, sql):
        try:
            database = db.DataBase()
            database.cursor.execute(sql)
            database.mydb.commit()
            del database
        except db.mysql.connector.Error as err:
            await ctx.send(embed= util.fail(err))
            del database

    @commands.command()
    async def insert(self, ctx, val: str, url: str= ""):
        result = await self.check(ctx, val)
        print(result)   # debug
        # Nuevo producto
        if result == 0:
            if url == "":
                await self.write(ctx, f"INSERT INTO productos (nombre) VALUES ('{val.lower()}');")
                await ctx.send(embed= util.success(f"New product: {val.lower()}"))
            elif util.is_url(url):
                await self.write(ctx, f"INSERT INTO productos (nombre) VALUES ('{val.lower()}');")
                await self.write(ctx, f"INSERT INTO imagenes (nombre, url) VALUES ('{val.lower()}', '{url}');")
                await ctx.send(embed= util.success(f"New product & image for: {val.lower()}"))
            else:
                await ctx.send(embed= util.fail("Error, not a well formed url."))

        # Nueva representacion (img) del producto
        elif result > 0:
            if result < 5 and util.is_url(url):
                await self.write(ctx, f"INSERT INTO imagenes (nombre, url) VALUES ('{val.lower()}', '{url}');")
                await ctx.send(embed= util.success(f"New product & image for: {val.lower()}"))
            elif result >= 5:
                await ctx.send(embed= util.fail("Error, to much imgs for the same product."))
            else:
                await ctx.send(embed= util.fail("Error, not a well formed url."))

    @commands.command()
    async def update(self, ctx, val_old: str, val_new: str):
        result = await self.check(ctx, val_old)

        if result > 0:
            await self.write(ctx, f"UPDATE productos SET nombre = '{val_new.lower()}' WHERE nombre = '{val_old.lower()}';")
            await ctx.send(embed= util.success(f"Name changed to: {val_new.capitalize()}"))
        else:
            await ctx.send(embed= util.fail("Error product does not exist."))
    
    @commands.command()
    async def delete(self, ctx, val: int):
        try:
            database = db.DataBase()
            sql = f"SELECT * FROM imagenes WHERE id = '{int(val)}';"
            database.cursor.execute(sql)
            result = database.cursor.fetchall()
            del database
        except db.mysql.connector.Error as err:
                await ctx.send(embed= util.fail(err))
                del database

        if result != []:
            await self.write(ctx, f"DELETE FROM imagenes WHERE id = {int(val)};")
            await ctx.send(embed= util.success(f"Product with id = {int(val)} deleted successfuly."))
        else:
            await ctx.send(embed= util.fail(f"Error while deleting the product with id: {int(val)}."))

    @commands.command()
    async def clear(self, ctx, val: str):
        result = await self.check(ctx, val)

        if result > 0:
            await self.write(ctx, f"DELETE FROM productos WHERE nombre = '{val.lower()}';")
            await ctx.send(embed= util.success(f"Product deleted: {val.capitalize()}"))
        else:
            await ctx.send(embed= util.fail("Error while deleting the product."))

    @commands.command()
    async def select(self, ctx, val: str):
        result = await self.check(ctx, val)

        if result > 0:
            try:
                database = db.DataBase()
                sql = f"SELECT id, nombre FROM imagenes WHERE nombre = '{val.lower()}';"
                self.database.cursor.execute(sql)
                result = self.database.cursor.fetchall()
                del database
            except self.mysql.connector.Error as err:
                await ctx.send(embed= util.fail(err))
                del database

            iter = 1
            max_items = len(result)
            text = ""
            for row in result:
                if iter == 5 or iter == max_items:  text += str(row[0]) + '.'
                else:                               text += str(row[0]) + ', '
                iter += 1

            embed = discord.Embed(description=f"IDs related to {row[1]}:\n```c++\n{text}```", color=9224068)
            embed.set_author(name="SQL query", icon_url="https://image.flaticon.com/icons/png/512/2306/2306022.png")
            embed.set_footer(text="Made with 💘 by Hec7orci7o.", icon_url="https://avatars.githubusercontent.com/u/56583980?s=60&v=4")
            
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed= util.fail("No right product selected."))

def setup(bot):
    bot.add_cog(Manage(bot))
