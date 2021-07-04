import random
import asyncio
import discord
import libs.utils as util
import libs.helper as helper
from discord.ext import commands
import libs.utils as util

class Bartender(helper.Helper, commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'order')
    async def get_product(self, ctx, val):
        # Check producto registrado
        result = await self.read(ctx, f"SELECT * FROM productos WHERE nombre = '{val.lower()}';")

        if result == []:
            await ctx.send(embed= util.fail(f"Lo sentimos, no hay productos registrados con el nombre: {val.lower()}"))
        else:
            # Check disponibilidad del producto registrado
            result = await self.read(ctx, f"SELECT nombre, url FROM imagenes WHERE nombre = '{val.lower()}';")

            if result == []:
                await ctx.send(embed= util.fail(f"Lo siento, no hay suficientes {val.lower()}"))
            else:
                await self.get_item(ctx, val.lower(), result)
    
    async def get_item(self, ctx, val, result):
        await ctx.trigger_typing()
        embed = discord.Embed(title= "{}".format(util.translate("Por favor, Espere mientras preparo su pedido...")), color= int("DCDCDC", 16))
        message = await ctx.send(embed= embed)
        await ctx.trigger_typing()
        await asyncio.sleep(3.5)
        embed = discord.Embed (title= "{}".format(util.translate(f"Aquí está su {val.lower()}.")), color= int("DCDCDC", 16))
        embed.set_image(url= result[random.randint(0, len(result)-1)][1])
        await message.delete()
        message = await ctx.send(embed= embed)
        for reaction in ['👍', '👎']:
            await message.add_reaction(reaction)

    async def pagina(self, ctx, emoji: str, categoria: str):
        result = await self.read(ctx, util.translate("SELECT nombre FROM productos WHERE categoria = '{}';".format(util.translate(categoria.lower(),'es'))))
        for name in result: name = util.translate(name)
        
        if result != []:
            embed = discord.Embed(description= "```{}```".format(util.translate("Haz tu pedido asi:\n$order <producto>")), color= int("8EC4FF", 16))
        else:
            embed = discord.Embed(description= "```{}```".format(util.translate("No products have been added yet.")), color= int("8EC4FF", 16))
        
        embed.set_author(name= "{} - {}".format(emoji, util.translate(categoria)), icon_url= "https://images.unsplash.com/photo-1590486145851-aae8758c4211?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1868&q=80")
        embed.set_footer(text= util.translate("Made with 💘 by Hec7orci7o."), icon_url= "https://avatars.githubusercontent.com/u/56583980?s=60&v=4")
        
        num_products = len(result)
        if result != []:
            if num_products == 1:
                p_page_1 = f"• {str(result[0])[2:-3]}\n"
                p_page_2, p_page_3 = "---", "---"
            elif num_products == 2:
                p_page_1, p_page_2 = f"• {str(result[0])[2:-3]}\n", f"• {str(result[1])[2:-3]}\n"
                p_page_3 = "---"
            elif num_products == 3:
                p_page_1, p_page_2, p_page_3 = f"• {str(result[0])[2:-3]}\n", f"• {str(result[1])[2:-3]}\n", f"• {str(result[2])[2:-3]}\n"
            elif num_products == 4:
                p_page_1, p_page_2, p_page_3 = f"• {str(result[0])[2:-3]}\n• {str(result[3])[2:-3]}", f"• {str(result[1])[2:-3]}\n", f"• {str(result[2])[2:-3]}\n"
            else:
                _s = int((len(result) / 3) + 1)
                p_page_1, p_page_2, p_page_3 = "", "", ""
                for elem in result[:_s]:     p_page_1 += f"• {str(elem)[2:-3]}\n"
                for elem in result[_s:2*_s]: p_page_2 += f"• {str(elem)[2:-3]}\n"
                for elem in result[2*_s:]:   p_page_3 += f"• {str(elem)[2:-3]}\n"


            embed.add_field(name=util.translate("Page 1."),value=f"{p_page_1}",inline=True)
            embed.add_field(name=util.translate("Page 2."),value=f"{p_page_2}",inline=True)
            embed.add_field(name=util.translate("Page 3."),value=f"{p_page_3}",inline=True)
            return embed
        else:
            return embed


    @commands.command()
    async def carta(self, ctx):
        emojis = ["🥛", "🍺","🥩","🍣","🍨","🥜","🍭"]
        menu = [(emojis[0],"sin alcohol"),(emojis[1],"con alcohol"),(emojis[2],"carnes"),(emojis[3],"pescados"),(emojis[4],"postres"),(emojis[5],"tapas"),(emojis[6],"chuches")]
        menu_formated = ''
        for cat in menu:
            menu_formated += cat[0] + ' - ' + cat[1] + '.\n'

        embed = discord.Embed(description= "```{}```".format(util.translate(menu_formated)), color= int("8EC4FF", 16))
        embed.set_author(name= util.translate("Sections:"), icon_url= "https://static.vecteezy.com/system/resources/previews/000/639/289/original/vector-menu-icon-symbol-sign.jpg")
        embed.set_footer(text= util.translate("Made with 💘 by Hec7orci7o."), icon_url= "https://avatars.githubusercontent.com/u/56583980?s=60&v=4")
        message = await ctx.send(embed= embed)
        for reaction in emojis:
            await message.add_reaction(reaction)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in emojis
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

        if str(reaction.emoji) in emojis:
            indice = emojis.index(str(reaction.emoji))
            await message.delete()
            await ctx.send(embed = await self.pagina(ctx, emojis[indice], util.translate(str(menu[indice][1])).capitalize()))
    
def setup(bot):
    bot.add_cog(Bartender(bot))