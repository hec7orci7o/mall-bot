from asyncio.windows_events import NULL
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
    async def insert(self, ctx, val, url=None):
        # Check producto registrado
        sql = """SELECT nombre FROM productos WHERE nombre = '{}';""".format(val.lower())
        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()

        # Producto registrado + img disponible
        if result != [] and url != None:
            if is_url(url):
                sql = """INSERT INTO imagenes (nombre, url) VALUES ('{}', '{}');""".format(val.lower(), url)
                self.database.cursor.execute(sql)
                await ctx.send("New product: {}".format(val.lower()))
            else:
                await ctx.send("Error > Not a well formed url.")

        # Producto registrado + imagen no disponible
        elif result != [] and url == None:
            await ctx.send("Product already exist.")

        # Producto no registrado + imagen disponible
        elif result == [] and url != None:
            sql = """INSERT INTO productos (nombre) VALUES ('{}');""".format(val.lower())
            self.database.cursor.execute(sql)   # Registra el producto { val }
            self.database.mydb.commit()
            sql = """INSERT INTO imagenes (nombre, url) VALUES ('{}', '{}');""".format(val.lower(), url)
            self.database.cursor.execute(sql)   # Registra una img para val
            await ctx.send("New product: {}".format(val.lower()))

        # Producto no registrado + imagen no disponible
        else:
            sql = """INSERT INTO productos (nombre) VALUES ('{}');""".format(val.lower())
            self.database.cursor.execute(sql)   # Registra el producto { val }
            await ctx.send("New product: {}".format(val.lower()))

        
        self.database.mydb.commit()

    @commands.command()
    async def update(self, ctx, val_old, val_new):
        sql = """SELECT * FROM productos WHERE nombre = '{}';""".format(val_old.lower())
        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()

        if result != []:
            sql = """UPDATE productos SET nombre = '{}' WHERE nombre = '{}';""".format(val_new.lower(), val_old.lower())
            self.database.cursor.execute(sql)
            self.database.mydb.commit()
            await ctx.send("Name changed to: {}".format(val_new.capitalize()))
        else:
            await ctx.send("Error while changing the product name.")
    
    @commands.command()
    async def erase(self, ctx, val):
        sql = """DELETE FROM imagenes WHERE id = {};""".format(int(val))
        self.database.cursor.execute(sql)
        self.database.mydb.commit()
        await ctx.send(val)

    @commands.command()
    async def delete(self, ctx, val):
        sql = """SELECT * FROM productos WHERE nombre = '{}';""".format(val.lower())
        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()

        if result != []:
            sql = """DELETE FROM productos WHERE nombre = '{}';""".format(val.lower())
            self.database.cursor.execute(sql)
            self.database.mydb.commit()
            await ctx.send("Product deleted: {}".format(val.capitalize()))
        else:
            await ctx.send("Error while deleting the product.")

    @commands.command()
    async def select(self, ctx, val):
        sql = """SELECT * FROM productos WHERE nombre = '{}';""".format(val.lower())
        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()

        if result != []:
            sql = """SELECT id, nombre FROM imagenes WHERE nombre = '{}';""".format(val.lower())
            self.database.cursor.execute(sql)
            result = self.database.cursor.fetchall()
            for row in result:
                data = f'id: {row[0]}, product-name: {row[1]}'
                await ctx.send(data)
        else:
            await ctx.send("Error > No right product selected.")
    
def setup(bot):
    bot.add_cog(Manage(bot))
