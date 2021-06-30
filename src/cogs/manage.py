from asyncio.windows_events import NULL
import discord
from discord.ext import commands
from libs.database import DataBase

class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = DataBase()

    @commands.command()
    async def insert(self, ctx, val, url=None):
        # Check producto registrado
        sql = """SELECT nombre FROM productos (nombre) WHERE nombre = '{}';""".format(val.lower())
        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()

        # Producto registrado + img disponible
        if result != [] and url is not None:
            sql = """INSERT INTO imagenes (nombre, url) VALUES ('{}', '{}');""".format(val.lower(), url)
            self.database.cursor.execute(sql)

        # Producto registrado + imagen no disponible
        elif result != [] and url is None:
            pass    # EXCEPCION

        # Producto no registrado + imagen disponible
        elif result == [] and url is not None:
            sql = """INSERT INTO productos (nombre) VALUES ('{}');""".format(val.lower())
            self.database.cursor.execute(sql)   # Registra el producto { val }
            self.database.mydb.commit()
            sql = """INSERT INTO imagenes (nombre, url) VALUES ('{}', '{}');""".format(val.lower(), url)
            self.database.cursor.execute(sql)   # Registra una img para val

        # Producto no registrado + imagen no disponible
        else:
            sql = """INSERT INTO productos (nombre) VALUES ('{}');""".format(val.lower())
            self.database.cursor.execute(sql)   # Registra el producto { val }
        
        self.database.mydb.commit()
        await ctx.send(val)

    @commands.command()
    async def erase(self, ctx, val):
        sql = """DELETE FROM imagenes WHERE id = {};""".format(int(val))
        self.database.cursor.execute(sql)
        self.database.mydb.commit()
        await ctx.send(val)

    @commands.command()
    async def delete(self, ctx, val):
        sql = """DELETE FROM productos WHERE nombre = '{}';""".format(val.lower())
        self.database.cursor.execute(sql)
        self.database.mydb.commit()
        await ctx.send(val)

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
    
def setup(bot):
    bot.add_cog(Manage(bot))
