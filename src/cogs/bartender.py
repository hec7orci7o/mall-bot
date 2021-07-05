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
        val_q = util.translate(val, src='en', dest='es')
        # Check producto registrado
        result = await self.read(ctx, f"SELECT * FROM productos WHERE nombre = '{val_q.lower()}';")

        if result == []:
            await ctx.send(embed= util.fail(f"Lo siento, no se han encontrado productos registrados con el nombre: {val.lower()}"))
        else:
            # Check disponibilidad del producto registrado
            result = await self.read(ctx, f"SELECT nombre, url FROM imagenes WHERE nombre = '{val_q.lower()}';")

            if result == []:
                await ctx.send(embed= util.fail(f"Lo siento, no hay suficientes {val.lower()}"))
            else:
                await self.get_item(ctx, val.lower(), result)
    
    async def get_item(self, ctx, val, result):
        await ctx.trigger_typing()
        embed = discord.Embed(title= "{}".format(util.translate("Por favor, Espere mientras preparo su pedido...", src='es', dest='en')), color= int("DCDCDC", 16))
        message = await ctx.send(embed= embed)
        await ctx.trigger_typing()
        await asyncio.sleep(3.5)
        embed = discord.Embed (title= "{} {}.".format(util.translate(f"Aquí está su"), val.lower()), color= int("DCDCDC", 16))
        embed.set_image(url= result[random.randint(0, len(result)-1)][1])
        await message.delete()
        message = await ctx.send(embed= embed)
        for reaction in ['👍', '👎']:
            await message.add_reaction(reaction)

    async def pagina(self, ctx, emoji: str, categoria: str):
        cat_q = util.translate(categoria, dest='en')
        result = await self.read(ctx, "SELECT nombre FROM productos WHERE categoria = '{}';".format(categoria))
        aux = list()
        for iter in range(0, len(result)):
            print(result[iter])
            aux.append( str(result[iter])[2:-3].capitalize() )
        
        if result != []:
            embed = discord.Embed(description= "```{}:\n$order <{}>```".format(util.translate("Haz tu pedido asi", dest='en'),util.translate("producto", dest='en')), color= int("8EC4FF", 16))
        else:
            embed = discord.Embed(description= "```{}```".format(util.translate("Todavía no se han agregado productos.", dest='en')), color= int("8EC4FF", 16))
        
        embed.set_author(name= f"{emoji} - {cat_q.capitalize()}", icon_url= "https://images.unsplash.com/photo-1590486145851-aae8758c4211?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1868&q=80")
        embed.set_footer(text= util.translate("Hecho con 💘 por Hec7orci7o.", dest='en'), icon_url= "https://avatars.githubusercontent.com/u/56583980?s=60&v=4")
        
        num_products = len(result)
        if result != []:
            if num_products == 1:
                p_page_1 = f"• {str(result[0])}\n"
                p_page_2, p_page_3 = "---", "---"
            elif num_products == 2:
                p_page_1, p_page_2 = f"• {str(result[0])}\n", f"• {str(result[1])}\n"
                p_page_3 = "---"
            elif num_products == 3:
                p_page_1, p_page_2, p_page_3 = f"• {str(result[0])}\n", f"• {str(result[1])}\n", f"• {str(result[2])}\n"
            elif num_products == 4:
                p_page_1, p_page_2, p_page_3 = f"• {str(result[0])}\n• {str(result[3])}", f"• {str(result[1])}\n", f"• {str(result[2])}\n"
            else:
                _s = int((len(result) / 3) + 1)
                p_page_1, p_page_2, p_page_3 = "", "", ""
                for elem in result[:_s]:     p_page_1 += f"• {str(elem)}\n"
                for elem in result[_s:2*_s]: p_page_2 += f"• {str(elem)}\n"
                for elem in result[2*_s:]:   p_page_3 += f"• {str(elem)}\n"


            embed.add_field(name=util.translate("Página 1.", dest= 'en'),value=f"{p_page_1}",inline=True)
            embed.add_field(name=util.translate("Página 2.", dest= 'en'),value=f"{p_page_2}",inline=True)
            embed.add_field(name=util.translate("Página 3.", dest= 'en'),value=f"{p_page_3}",inline=True)
        
        await ctx.send(embed = embed)


    @commands.command()
    async def carta(self, ctx):
        emojis = ["🥛", "🍺","🥩","🍣","🍨","🥜","🍭"]
        menu = [(emojis[0],"sin alcohol"),(emojis[1],"con alcohol"),(emojis[2],"carnes"),(emojis[3],"pescados"),(emojis[4],"postres"),(emojis[5],"tapas"),(emojis[6],"chuches")]
        menu_formated = ''
        for cat in menu:
            menu_formated += cat[0] + ' - ' + util.translate(cat[1], dest='en').capitalize() + '.\n'

        embed = discord.Embed(description= "```{}```".format(menu_formated, color= int("8EC4FF", 16)))
        embed.set_author(name= util.translate("Secciones:", dest='en'), icon_url= "https://static.vecteezy.com/system/resources/previews/000/639/289/original/vector-menu-icon-symbol-sign.jpg")
        embed.set_footer(text= util.translate("Hecho con 💘 por Hec7orci7o.", dest='en'), icon_url= "https://avatars.githubusercontent.com/u/56583980?s=60&v=4")
        message = await ctx.send(embed= embed)
        for reaction in emojis:
            await message.add_reaction(reaction)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in emojis
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

        if str(reaction.emoji) in emojis:
            indice = emojis.index(str(reaction.emoji))
            await message.delete()
            print(str(menu[indice][1]))
            await self.pagina(ctx, emojis[indice], str(menu[indice][1]))
            
    
def setup(bot):
    bot.add_cog(Bartender(bot))