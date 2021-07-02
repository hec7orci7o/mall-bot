import discord
from discord.ext import commands
from libs.database import DataBase
import libs.utils as util


class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = DataBase()

    # sql = f"SELECT count(*) FROM imagenes WHERE nombre = '{val.lower()}';"
    async def read(self, ctx, sql):
        try:
            self.database.cursor.execute(sql)
            result = self.database.cursor.fetchall()
        except self.mysql.connector.Error as err:
            await ctx.send(embed= util.fail(err))
        return result

    async def write(self, ctx, sql):
        try:
            self.database.cursor.execute(sql)
            self.database.mydb.commit()
        except self.mysql.connector.Error as err:
            await ctx.send(embed= util.fail(err))

    @commands.command()
    async def insert(self, ctx, val: str, url: str= ""):
        result = str(await self.read(ctx, f"SELECT nombre FROM productos WHERE nombre = '{val.lower()}';"))[3:-4]
        print(result)

        # Producto ya existe
        if result == val.lower():
            print("existe")
            # if result < 5 and util.is_url(url):
            #     await self.write(ctx, f"INSERT INTO imagenes (nombre, url) VALUES ('{val.lower()}', '{url}');")
            #     await ctx.send(embed= util.success(f"New product & image for: {val.lower()}"))
            # elif result >= 5:
            #     await ctx.send(embed= util.fail("Error, to much imgs for the same product."))
            # else:
            #     await ctx.send(embed= util.fail("Error, not a well formed url."))

        # Nuevo producto
        else:
            print("no existe")
            # if url == "":
            #     await self.write(ctx, f"INSERT INTO productos (nombre) VALUES ('{val.lower()}');")
            #     await ctx.send(embed= util.success(f"New product: {val.lower()}"))
            # elif util.is_url(url):
            #     await self.write(ctx, f"INSERT INTO productos (nombre) VALUES ('{val.lower()}');")
            #     await self.write(ctx, f"INSERT INTO imagenes (nombre, url) VALUES ('{val.lower()}', '{url}');")
            #     await ctx.send(embed= util.success(f"New product & image for: {val.lower()}"))
            # else:
            #     await ctx.send(embed= util.fail("Error, not a well formed url."))

    @commands.command()
    async def update(self, ctx, val_old: str, val_new: str):
        result = await self.read(ctx, f"SELECT nombre FROM productos WHERE nombre = '{val_old.lower()}';")
        print(result)

        if result != []:
            await self.write(ctx, f"UPDATE productos SET nombre = '{val_new.lower()}' WHERE nombre = '{val_old.lower()}';")
            await ctx.send(embed= util.success(f"Name changed to: {val_new.capitalize()}"))
        else:
            await ctx.send(embed= util.fail("Error product does not exist."))
    
    @commands.command()
    async def delete(self, ctx, val: int):
        result = await self.read(ctx, f"SELECT * FROM imagenes WHERE id = '{int(val)}';")
        print(result)

        if result != []:
            await self.write(ctx, f"DELETE FROM imagenes WHERE id = {int(val)};")
            await ctx.send(embed= util.success(f"Product with id = {int(val)} deleted successfuly."))
        else:
            await ctx.send(embed= util.fail(f"Error while deleting the product with id: {int(val)}."))

    @commands.command()
    async def clear(self, ctx, val: str):
        result = str(await self.read(ctx, f"SELECT nombre FROM productos WHERE nombre = '{val.lower()}';"))[3:-4]
        print(result)

        if result == val.lower():
            await self.write(ctx, f"DELETE FROM productos WHERE nombre = '{val.lower()}';")
            await ctx.send(embed= util.success(f"Product deleted: {val.capitalize()}"))
        else:
            await ctx.send(embed= util.fail("Error while deleting the product."))

    @commands.command()
    async def select(self, ctx, val: str):
        # Comprueba que exista el prodcuto
        result = str(await self.read(ctx, f"SELECT nombre FROM productos WHERE nombre = '{val.lower()}';"))[3:-4]
        print(result)

        if result == val.lower():
            # Comprueba el numero de imagenes que existe para un producto
            result = int(str(await self.read(ctx, f"SELECT count(*) FROM imagenes WHERE nombre = '{val.lower()}';"))[2:-3])
            print(result)
            if result == 0:
                embed = discord.Embed(description=f"IDs related to {val.lower()}:\n```c++\nNo images has been added yet.```", color=9224068)
                embed.set_author(name="SQL query", icon_url="https://image.flaticon.com/icons/png/512/2306/2306022.png")
                embed.set_footer(text="Made with 💘 by Hec7orci7o.", icon_url="https://avatars.githubusercontent.com/u/56583980?s=60&v=4")
            
            else:
                result = await self.read(ctx, f"SELECT id, nombre FROM imagenes WHERE nombre = '{val.lower()}';")
                print(result)
                iter, max_items, text = 1, len(result), ""
                for row in result:
                    if iter == 5 or iter == max_items:  text += str(row[0]) + '.'
                    else:                               text += str(row[0]) + ', '
                    iter += 1

                embed = discord.Embed(description=f"IDs related to {row[1]}:\n```c++\n{text}```", color=9224068)
                embed.set_author(name="SQL query", icon_url="https://image.flaticon.com/icons/png/512/2306/2306022.png")
                embed.set_footer(text="Made with 💘 by Hec7orci7o.", icon_url="https://avatars.githubusercontent.com/u/56583980?s=60&v=4")
            await ctx.send(embed= embed)
        else:
            await ctx.send(embed= util.fail("No right product selected."))

def setup(bot):
    bot.add_cog(Manage(bot))
