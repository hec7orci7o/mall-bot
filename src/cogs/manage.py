import discord
from discord.ext import commands
from libs.database import DataBase
from urllib.parse import urlparse
from mysql.connector import errorcode

def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def fail(error):
    embed = discord.Embed(
        description=f"```c++\n{error}```",
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
    return embed

def success(success):
    embed = discord.Embed(
        description=f"```c++\n{success}```",
        color=9224068
    )
    embed.set_author(
        name="Success",
        icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Flat_tick_icon.svg/240px-Flat_tick_icon.svg.png"
    )
    embed.set_footer(
        text="Made with 💘 by Hec7orci7o.",
        icon_url="https://avatars.githubusercontent.com/u/56583980?s=60&v=4"
    )
    return embed

class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = DataBase()

    # Check producto registrado
    def check(self, val: str):
        try:
            sql = f"SELECT count(*) FROM imagenes WHERE nombre = '{val.lower()}';"
            self.database.cursor.execute(sql)
            result = self.database.cursor.fetchall()
        except self.mysql.connector.Error as err:
            print(err)
        return int(result[0])

    @commands.command()
    async def insert(self, ctx, val: str=None, url: str=None):
        if val != None:
            result = self.check(val)

            # Producto registrado + img disponible
            if result > 0 and result < 5 and url != None:
                if is_url(url):
                    try:
                        sql = f"INSERT INTO imagenes (nombre, url) VALUES ('{val.lower()}', '{url}');"
                        self.database.cursor.execute(sql)
                    except self.mysql.connector.Error as err:
                        print(err)
                    embed = success(f"New image for: {val.lower()}\nImages left:{5-result}/5")
                    await ctx.send(embed=embed)
                else:
                    embed = fail("Error, not a well formed url.")
                    await ctx.send(embed=embed)

            # Producto registrado + imagen no disponible
            elif result > 0 and url == None:
                embed = fail("Product already exist.")
                await ctx.send(embed=embed)

            # Producto no registrado + imagen disponible
            elif result == 0 and url != None:
                if is_url(url):
                    try:
                        sql = f"INSERT INTO productos (nombre) VALUES ('{val.lower()}');"
                        self.database.cursor.execute(sql)   # Registra el producto { val }
                        self.database.mydb.commit()
                    except self.mysql.connector.Error as err:
                        print(err)
                    try:
                        sql = f"INSERT INTO imagenes (nombre, url) VALUES ('{val.lower()}', '{url}');"
                        self.database.cursor.execute(sql)   # Registra una img para val
                    except self.mysql.connector.Error as err:
                        print(err)
                    embed = success(f"New product & image for: {val.lower()}")
                    await ctx.send(embed=embed)
                else:
                    embed = fail("Error, not a well formed url.")
                    await ctx.send(embed=embed)

            # Producto no registrado + imagen no disponible
            else:
                try:
                    sql = f"INSERT INTO productos (nombre) VALUES ('{val.lower()}');"
                    self.database.cursor.execute(sql)   # Registra el producto { val }
                except self.mysql.connector.Error as err:
                    print(err)
                embed = success(f"New product: {val.lower()}")
                await ctx.send(embed=embed)
            try:
                self.database.mydb.commit()
            except self.mysql.connector.Error as err:
                print(err)
        else:
            embed = fail("Error, the method needs a product.")
            await ctx.send(embed=embed)

    @commands.command()
    async def update(self, ctx, val_old: str, val_new: str):
        result = self.check(val_old)

        if result > 0:
            try:
                sql = f"UPDATE productos SET nombre = '{val_new.lower()}' WHERE nombre = '{val_old.lower()}';"
                self.database.cursor.execute(sql)
                self.database.mydb.commit()
            except self.mysql.connector.Error as err:
                print(err)
            embed = success(f"Name changed to: {val_new.capitalize()}")
            await ctx.send(embed=embed)
        else:
            embed = fail("Error product does not exist.")
            await ctx.send(embed=embed)
    
    @commands.command()
    async def delete(self, ctx, val: int):
        try:
            sql = f"SELECT * FROM imagenes WHERE id = '{int(val)}';"
            self.database.cursor.execute(sql)
            result = self.database.cursor.fetchall()
        except self.mysql.connector.Error as err:
                print(err)

        if result != []:
            try:
                sql = f"DELETE FROM imagenes WHERE id = {int(val)};"
                self.database.cursor.execute(sql)
                self.database.mydb.commit()
            except self.mysql.connector.Error as err:
                print(err)
            embed = success(f"Product with id = {int(val)} deleted successfuly.")
            await ctx.send(embed=embed)
        else:
            embed = fail(f"Error while deleting the product with id: {int(val)}.")
            await ctx.send(embed=embed)

    @commands.command()
    async def clear(self, ctx, val: str):
        result = self.check(val)

        if result != []:
            try:
                sql = f"DELETE FROM productos WHERE nombre = '{val.lower()}';"
                self.database.cursor.execute(sql)
                self.database.mydb.commit()
            except self.mysql.connector.Error as err:
                print(err)
            embed = success(f"Product deleted: {val.capitalize()}")
            await ctx.send(embed=embed)
        else:
            embed = fail("Error while deleting the product.")
            await ctx.send(embed=embed)

    @commands.command()
    async def select(self, ctx, val: str):
        result = self.check(val)

        if result > 0:
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
                if iter == 5 or iter == max_items:
                    text += str(row[0]) + '.'
                else:
                    text += str(row[0]) + ', '
                iter+=1

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
            embed = fail("No right product selected.")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Manage(bot))
