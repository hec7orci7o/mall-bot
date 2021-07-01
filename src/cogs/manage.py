import discord
from discord.ext import commands
from libs.database import DataBase
from urllib.parse import urlparse

def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = DataBase()

    @commands.command()
    async def insert(self, ctx, val=None, url=None):
        if val != None:
            # Check producto registrado
            sql = f"SELECT nombre FROM productos WHERE nombre = '{val.lower()}';"
            self.database.cursor.execute(sql)
            result = self.database.cursor.fetchall()

            # Producto registrado + img disponible
            if result != [] and url != None:
                if is_url(url):
                    sql = f"INSERT INTO imagenes (nombre, url) VALUES ('{val.lower()}', '{url}');"
                    self.database.cursor.execute(sql)
                    await ctx.send(f"New product: {val.lower()}")
                else:
                    await ctx.send("Error > Not a well formed url.")

            # Producto registrado + imagen no disponible
            elif result != [] and url == None:
                await ctx.send("Product already exist.")

            # Producto no registrado + imagen disponible
            elif result == [] and url != None:
                sql = f"INSERT INTO productos (nombre) VALUES ('{val.lower()}');"
                self.database.cursor.execute(sql)   # Registra el producto { val }
                self.database.mydb.commit()
                sql = f"INSERT INTO imagenes (nombre, url) VALUES ('{val.lower()}', '{url}');"
                self.database.cursor.execute(sql)   # Registra una img para val
                await ctx.send(f"New product: {val.lower()}")

            # Producto no registrado + imagen no disponible
            else:
                sql = f"INSERT INTO productos (nombre) VALUES ('{val.lower()}');"
                self.database.cursor.execute(sql)   # Registra el producto { val }
                await ctx.send(f"New product: {val.lower()}")

            self.database.mydb.commit()
        else:
            await ctx.send("The method needs a product")


    @commands.command()
    async def update(self, ctx, val_old, val_new):
        sql = f"SELECT * FROM productos WHERE nombre = '{val_old.lower()}';"
        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()

        if result != []:
            sql = f"UPDATE productos SET nombre = '{val_new.lower()}' WHERE nombre = '{val_old.lower()}';"
            self.database.cursor.execute(sql)
            self.database.mydb.commit()
            await ctx.send(f"Name changed to: {val_new.capitalize()}")
        else:
            await ctx.send("Error while changing the product name.")
    
    @commands.command()
    async def erase(self, ctx, val):
        sql = f"SELECT * FROM images WHERE id = '{int(val)}';"
        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()

        if result != []:
            sql = f"DELETE FROM imagenes WHERE id = {int(val)};"
            self.database.cursor.execute(sql)
            self.database.mydb.commit()
            await ctx.send(f"Product with id = {int(val)} deleted successfuly.")
        else:
            await ctx.send(f"Error while deleting the product with id: {int(val)}.")


    @commands.command()
    async def delete(self, ctx, val):
        sql = f"SELECT * FROM productos WHERE nombre = '{val.lower()}';"
        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()

        if result != []:
            sql = f"DELETE FROM productos WHERE nombre = '{val.lower()}';"
            self.database.cursor.execute(sql)
            self.database.mydb.commit()
            await ctx.send(f"Product deleted: {val.capitalize()}")
        else:
            await ctx.send("Error while deleting the product.")

    @commands.command()
    async def select(self, ctx, val):
        sql = f"SELECT * FROM productos WHERE nombre = '{val.lower()}';"
        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()

        if result != []:
            sql = f"SELECT id, nombre FROM imagenes WHERE nombre = '{val.lower()}';"
            self.database.cursor.execute(sql)
            result = self.database.cursor.fetchall()

            iter = 1
            max_items = len(result)
            for row in result:
                if iter == 5 or iter == max_items:
                    text = str(row[0]) + '.'
                else:
                    text = str(row[0]) + ', '

            embed = discord.Embed(
                description=f"IDs related to {row[1]}:\n```c++\n{text}```",
                color=9224068
            )
            embed.set_author(
                name="SQL query",
                icon_url="https://image.flaticon.com/icons/png/512/2306/2306022.png"
            )
            embed.set_footer(
                text="Made with 💘 by Hec7orci7o.",
                icon_url="https://avatars.githubusercontent.com/u/56583980?s=60&v=4"
            )
            
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description=f"```c++\nNo right product selected.```",
                color=14579829
            )
            embed.set_author(
                name="Error",
                icon_url="https://www.freeiconspng.com/uploads/x-png-18.png"
            )
            embed.set_footer(
                text="Made with 💘 by Hec7orci7o.",
                icon_url="https://avatars.githubusercontent.com/u/56583980?s=60&v=4"
            )
            await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Manage(bot))
