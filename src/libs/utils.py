import os
import discord
from urllib.parse import urlparse
from googletrans import Translator

def translate(txt: str):
    translator = Translator()
    dest = os.environ['LANG']
    traduccion = str(translator.translate(text= txt, dest= dest).text)
    del translator
    return traduccion

def is_url(url: str):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def fail(error: str):
    embed = discord.Embed(
        description= "```c++\n{}```".format(translate(error)),
        color= int("DE7875", 16)
    )
    embed.set_author(
        name= translate("Error"),
        icon_url= "https://www.freeiconspng.com/uploads/x-png-18.png"
    )
    embed.set_footer(
        text= translate("Made with 💘 by Hec7orci7o."),
        icon_url= "https://avatars.githubusercontent.com/u/56583980?s=60&v=4"
    )
    return embed

def success(success: str):
    embed = discord.Embed(
        description= "```c++\n{}```".format(translate(success)),
        color= int("8CBF84", 16)
    )
    embed.set_author(
        name= translate("Success"),
        icon_url= "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Flat_tick_icon.svg/240px-Flat_tick_icon.svg.png"
    )
    embed.set_footer(
        text= translate("Made with 💘 by Hec7orci7o."),
        icon_url= "https://avatars.githubusercontent.com/u/56583980?s=60&v=4"
    )
    return embed
    