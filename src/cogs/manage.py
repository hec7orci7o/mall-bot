import os
import discord
import libs.utils as util
import libs.helper as helper
from discord.ext import commands
from googletrans import Translator

def is_bartender():
    def predicate(ctx):
        return ctx.message.author.id == int(os.environ['STAFF'])
    return commands.check(predicate)

class Manage(helper.Helper, commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @is_bartender()
    @commands.command()
    async def insert(self, ctx, val: str, cat: str, url: str= ""):
        val = util.translate(val, 'es')
        cat = util.translate(cat, 'es')

        result = str(await self.read(ctx, f"SELECT * FROM categorias WHERE nombre = '{cat.lower()}';"))[3:-4]
        if result != "":
            result = str(await self.read(ctx, f"SELECT nombre FROM productos WHERE nombre = '{val.lower()}';"))[3:-4]

            # Producto ya existe
            if result == val.lower():
                result = int(str(await self.read(ctx, f"SELECT count(*) FROM imagenes WHERE nombre = '{val.lower()}';"))[2:-3])
                if result < 5 and util.is_url(url):
                    await self.write(ctx, f"INSERT INTO imagenes (nombre, url) VALUES ('{val.lower()}', '{url}');")
                    await ctx.send(embed= util.success(f"Nueva imagen para: {val.lower()}\n{5-(result+1)}/5 espacios disponibles"))
                elif result >= 5:
                    await ctx.send(embed= util.fail("Error, demasiadas imágenes para el mismo producto.\n5/5 imgs"))
                elif url == "":
                    await ctx.send(embed= util.fail("Error, el producto ya existe."))
                else:
                    await ctx.send(embed= util.fail("Error, no es una URL correcta."))

            # Nuevo producto
            else:
                if url == "":
                    await self.write(ctx, f"INSERT INTO productos (nombre, categoria) VALUES ('{val.lower()}','{cat.lower()}');")
                    await ctx.send(embed= util.success(f"New product: {val.lower()}"))
                elif util.is_url(url):
                    await self.write(ctx, f"INSERT INTO productos (nombre, categoria) VALUES ('{val.lower()}','{cat.lower()}');")
                    await self.write(ctx, f"INSERT INTO imagenes (nombre, url) VALUES ('{val.lower()}', '{url}');")
                    await ctx.send(embed= util.success(f"New product & image for: {val.lower()}"))
                else:
                    await ctx.send(embed= util.fail("Error, no es una URL correcta."))
        else:
            await ctx.send(embed= util.fail("Error, la categoria no existe"))

    @is_bartender()
    @commands.command()
    async def update_name(self, ctx, val_old: str, val_new: str):
        val_old = util.translate(val_old, 'es')
        val_new = util.translate(val_new, 'es')
        result = await self.read(ctx, f"SELECT nombre FROM productos WHERE nombre = '{val_old.lower()}';")

        if result != []:
            await self.write(ctx, f"UPDATE productos SET nombre = '{val_new.lower()}' WHERE nombre = '{val_old.lower()}';")
            await ctx.send(embed= util.success(f"Nombre cambiado a: {val_new.capitalize()}"))
        else:
            await ctx.send(embed= util.fail("Error, el producto no existe."))

    @is_bartender()
    @commands.command()
    async def update_category(self, ctx, val, cat_new: str):
        val = util.translate(val, src='en')
        result = await self.read(ctx, f"SELECT nombre FROM productos WHERE nombre = '{val.lower()}';")

        if result != []:
            cat_new = util.translate(cat_new, src='en')
            result_c = await self.read(ctx, f"SELECT nombre FROM categorias WHERE nombre = '{cat_new.lower()}';")
            if result_c != []:
                await self.write(ctx, f"UPDATE productos SET categoria = '{cat_new.lower()}' WHERE nombre = '{val.lower()}';")
                await ctx.send(embed= util.success(f"Categoría cambiada: {val.lower()} -> {cat_new.lower()}"))
            else:
                await ctx.send(embed= util.fail(f"Error, la categoria: {cat_new} no existe."))
        else:
            await ctx.send(embed= util.fail("Error, el producto no existe"))
       
    
    @is_bartender()
    @commands.command()
    async def delete(self, ctx, val: int):
        val = util.translate(val, src='en')
        result = await self.read(ctx, f"SELECT * FROM imagenes WHERE id = '{int(val)}';")

        if result != []:
            await self.write(ctx, f"DELETE FROM imagenes WHERE id = {int(val)};")
            await ctx.send(embed= util.success(f"Producto con id: {int(val)} eliminado con exito."))
        else:
            await ctx.send(embed= util.fail(f"Error al eliminar la imagen con id: {int(val)}."))

    @is_bartender()
    @commands.command()
    async def clear(self, ctx, val: str):
        val = util.translate(val, src='en')
        result = str(await self.read(ctx, f"SELECT nombre FROM productos WHERE nombre = '{val.lower()}';"))[3:-4]

        if result == val.lower():
            await self.write(ctx, f"DELETE FROM productos WHERE nombre = '{val.lower()}';")
            await ctx.send(embed= util.success(f"Producto eliminado: {val.capitalize()}"))
        else:
            await ctx.send(embed= util.fail("Error al eliminar el producto."))

    @is_bartender()
    @commands.command()
    async def select(self, ctx, val: str):
        val = util.translate(val, src='en')
        # Comprueba que exista el prodcuto
        result = str(await self.read(ctx, f"SELECT nombre FROM productos WHERE nombre = '{val.lower()}';"))[3:-4]

        if result == val.lower():
            # Comprueba el numero de imagenes que existe para un producto
            result = int(str(await self.read(ctx, f"SELECT count(*) FROM imagenes WHERE nombre = '{val.lower()}';"))[2:-3])
            if result == 0:
                embed = discord.Embed(description= "{}\n```c++\n{}```".format(util.translate(f"ID relacionados con {val.lower()}:", dest='en'), util.translate("Todavía no se han añadido imagenes del producto.", dest='en')), color= int("8EC4FF", 16))
                embed.set_author(name= util.translate("SQL query", dest='en'), icon_url="https://image.flaticon.com/icons/png/512/2306/2306022.png")
                embed.set_footer(text= util.translate("Hecho con 💘 por Hec7orci7o.", dest='en'), icon_url= "https://avatars.githubusercontent.com/u/56583980?s=60&v=4")
            else:
                result = await self.read(ctx, f"SELECT id, nombre FROM imagenes WHERE nombre = '{val.lower()}';")
                iter, max_items, text = 1, len(result), ""
                for row in result:
                    if iter == 5 or iter == max_items:  text += str(row[0]) + '.'
                    else:                               text += str(row[0]) + ', '
                    iter += 1

                embed = discord.Embed(description= "{}\n```c++\n{}```".format(util.translate(f"ID relacionados con {row[1]}:", dest='en'), text), color= int("8EC4FF", 16))
                embed.set_author(name= util.translate("SQL query", dest='en'), icon_url="https://image.flaticon.com/icons/png/512/2306/2306022.png")
                embed.set_footer(text= util.translate("Hecho con 💘 por Hec7orci7o.", dest='en'), icon_url= "https://avatars.githubusercontent.com/u/56583980?s=60&v=4")
            await ctx.send(embed= embed)
        else:
            await ctx.send(embed= util.fail("Producto incorrecto seleccionado."))

def setup(bot):
    bot.add_cog(Manage(bot))
