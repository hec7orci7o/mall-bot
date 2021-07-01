import discord
from discord.ext import commands
from libs.database import DataBase
import libs.utils as util


class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = DataBase()

    # Check producto registrado
    async def check(self, ctx, val: str):
        try:
            sql = f"SELECT count(*) FROM imagenes WHERE nombre = '{val.lower()}';"
            self.database.cursor.execute(sql)
            result = self.database.cursor.fetchall()
        except self.mysql.connector.Error as err:
            await ctx.send(embed= util.fail(err))
            del self.database
            self.database = DataBase()
        print(str(result)[2:-3])
        return int(str(result)[2:-3])

    async def write(self, ctx, sql):
        try:
            self.database.cursor.execute(sql)
            self.database.mydb.commit()
        except self.mysql.connector.Error as err:
            await ctx.send(embed= util.fail(err))
            del self.database
            self.database = DataBase()

    @commands.command()
    async def insert(self, ctx, val: str=None, url: str=None):
        if val != None:
            result = self.check(ctx, val)

            # Producto registrado + img disponible
            if result > 0 and result < 5 and url != None:
                if util.is_url(url):
                    self.write(ctx, f"INSERT INTO imagenes (nombre, url) VALUES ('{val.lower()}', '{url}');")
                    await ctx.send(embed= util.success(f"New image for: {val.lower()}\nImages left:{5-result}/5"))
                else:
                    await ctx.send(embed= util.fail("Error, not a well formed url."))

            # Producto registrado + imagen no disponible
            elif result > 0 and url == None:
                await ctx.send(embed= util.fail("Product already exist."))

            # Producto no registrado + imagen disponible
            elif result == 0 and url != None:
                if util.is_url(url):
                    self.write(ctx, f"INSERT INTO productos (nombre) VALUES ('{val.lower()}');")
                    self.write(ctx, f"INSERT INTO imagenes (nombre, url) VALUES ('{val.lower()}', '{url}');")
                    await ctx.send(embed= util.success(f"New product & image for: {val.lower()}"))
                else:
                    await ctx.send(embed= util.fail("Error, not a well formed url."))

            # Producto no registrado + imagen no disponible
            else:
                self.write(ctx, f"INSERT INTO productos (nombre) VALUES ('{val.lower()}');")
                embed = util.success(f"New product: {val.lower()}")
                await ctx.send(embed=embed)
        else:
            await ctx.send(embed= util.fail("Error, the method needs a product."))

    @commands.command()
    async def update(self, ctx, val_old: str, val_new: str):
        result = self.check(ctx, val_old)

        if result > 0:
            self.write(ctx, f"UPDATE productos SET nombre = '{val_new.lower()}' WHERE nombre = '{val_old.lower()}';")
            await ctx.send(embed= util.success(f"Name changed to: {val_new.capitalize()}"))
        else:
            await ctx.send(embed= util.fail("Error product does not exist."))
    
    @commands.command()
    async def delete(self, ctx, val: int):
        try:
            sql = f"SELECT * FROM imagenes WHERE id = '{int(val)}';"
            self.database.cursor.execute(sql)
            result = self.database.cursor.fetchall()
        except self.mysql.connector.Error as err:
                print(err)

        if result != []:
            self.write(ctx, f"DELETE FROM imagenes WHERE id = {int(val)};")
            await ctx.send(embed= util.success(f"Product with id = {int(val)} deleted successfuly."))
        else:
            await ctx.send(embed= util.fail(f"Error while deleting the product with id: {int(val)}."))

    @commands.command()
    async def clear(self, ctx, val: str):
        result = self.check(ctx, val)

        if result > 0:
            self.write(ctx, f"DELETE FROM productos WHERE nombre = '{val.lower()}';")
            await ctx.send(embed= util.success(f"Product deleted: {val.capitalize()}"))
        else:
            await ctx.send(embed= util.fail("Error while deleting the product."))

    @commands.command()
    async def select(self, ctx, val: str):
        result = self.check(ctx, val)

        if result != 0:
            try:
                sql = f"SELECT id, nombre FROM imagenes WHERE nombre = '{val.lower()}';"
                self.database.cursor.execute(sql)
                result = self.database.cursor.fetchall()
            except self.mysql.connector.Error as err:
                print(err)

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
