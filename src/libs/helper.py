import discord
import libs.utils as util
from discord.ext import commands
from libs.database import DataBase

class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def read(self, ctx, sql):
        try:
            database = DataBase()
            database.cursor.execute(sql)
            result = database.cursor.fetchall()
            del database
        except database.mysql.connector.Error as err:
            await ctx.send(embed= util.fail(err))
            del database
        return result

    async def write(self, ctx, sql):
        try:
            database = DataBase()
            database.cursor.execute(sql)
            database.mydb.commit()
            del database
        except database.mysql.connector.Error as err:
            await ctx.send(embed= util.fail(err))
            del database
