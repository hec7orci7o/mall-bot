import os
import random
import asyncio
import discord
import libs.utils as util
import libs.helper as helper
from discord.ext import commands
from libs.database import DataBase
import libs.utils as util
# from googletrans import Translator

class Bartender(helper.Helper, commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.lang = str(os.environ['LANG']).lower()
        # self.translator = Translator()

    @commands.command(name = 'order')
    async def get_product(self, ctx, val):
        # Check producto registrado
        result = await self.read(ctx, f"SELECT * FROM productos WHERE nombre = '{val.lower()}';")

        if result == []:
            await ctx.send(embed= util.fail(f"Sry, there are not products registered with the name: {val.lower()}"))
        else:
            # Check disponibilidad del producto registrado
            result = await self.read(ctx, f"SELECT nombre, url FROM imagenes WHERE nombre = '{val.lower()}';")

            if result == []:
                await ctx.send(embed= util.fail(f"Sry, there are not enought {val.lower()}"))
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
        await asyncio.sleep(3.5)
        embed = discord.Embed (
            title = f"{msg_2}",
            color = 16777215
        )
        embed.set_image(url= result[random.randint(0,len(result)-1)][1])
        await message.delete()
        message = await ctx.send(embed= embed)
        for reaction in ['👍', '👎']:
            await message.add_reaction(reaction)

    async def pagina(self, ctx, emoji: str, categoria: str):
        embed = discord.Embed(
              description=f"```Haz tu pedido asi:\n$order <producto>```",
             color=14579829)
        embed.set_author(name=f"{emoji} - {categoria}",icon_url="https://images.unsplash.com/photo-1590486145851-aae8758c4211?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1868&q=80")
        embed.set_footer(text="Made with 💘 by Hec7orci7o.",icon_url="https://avatars.githubusercontent.com/u/56583980?s=60&v=4")
        
        result = await self.read(ctx, f"select nombre from productos where categoria = '{categoria.lower()}';")
        _s = int((len(result) / 3) + 1)
        l_p_page_1, l_p_page_2, l_p_page_3 = result[:_s], result[_s:2*_s], result[2*_s:]
        p_page_1, p_page_2, p_page_3 = "", "", ""
        for elem in l_p_page_1: p_page_1 += f"• {str(elem)[2:-3]}\n"
        for elem in l_p_page_2: p_page_2 += f"• {str(elem)[2:-3]}\n"
        for elem in l_p_page_3: p_page_3 += f"• {str(elem)[2:-3]}\n"


        embed.add_field(name="Page 1.",value=f"{p_page_1}",inline=True)
        embed.add_field(name="Page 2.",value=f"{p_page_2}",inline=True)
        embed.add_field(name="Page 3.",value=f"{p_page_3}",inline=True)
        return embed

    @commands.command()
    async def carta(self, ctx):
        menu = [("🥛","sin alcohol"),("🍺","con alcohol"),("🥩","carne"),("🍣","pescado"),("🍨","postres"),("🥜","tapas"),("🍭","chuches")]
        menu_formated = ''
        for cat in menu:
            menu_formated += cat[0] + ' - ' + cat[1] + '.\n'

        embed = discord.Embed(description=f"```{menu_formated}```", color=9224068)
        embed.set_author(name="Sections:", icon_url="https://static.vecteezy.com/system/resources/previews/000/639/289/original/vector-menu-icon-symbol-sign.jpg")
        embed.set_footer(text="Made with 💘 by Hec7orci7o.", icon_url="https://avatars.githubusercontent.com/u/56583980?s=60&v=4")
        message = await ctx.send(embed= embed)
        for reaction in ['🥛', '🍺','🥩','🍣','🍨','🥜','🍭']:
            await message.add_reaction(reaction)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['🥛', '🍺','🥩','🍣','🍨','🥜','🍭']
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

        if str(reaction.emoji) == "🥛":
            await message.delete()
            await ctx.send(embed = await self.pagina(ctx, "🥛", str(menu[0][1])))
        elif str(reaction.emoji) == "🍺":
            await message.delete()
            await ctx.send(embed = await self.pagina(ctx, "🍺", str(menu[1][1])))
        elif str(reaction.emoji) == "🥩":
            await message.delete()
            await ctx.send(embed = await self.pagina(ctx, "🥩", str(menu[2][1])))
        elif str(reaction.emoji) == "🍣":
            await message.delete()
            await ctx.send(embed = await self.pagina(ctx, "🍣", str(menu[3][1])))
        elif str(reaction.emoji) == "🍨":
            await message.delete()
            await ctx.send(embed = await self.pagina(ctx, "🍨", str(menu[4][1])))
        elif str(reaction.emoji) == "🥜":
            await message.delete()
            await ctx.send(embed = await self.pagina(ctx, "🥜", str(menu[5][1])))
        elif str(reaction.emoji) == "🍭":
            await message.delete()
            await ctx.send(embed = await self.pagina(ctx, "🍭", str(menu[6][1])))
    
def setup(bot):
    bot.add_cog(Bartender(bot))