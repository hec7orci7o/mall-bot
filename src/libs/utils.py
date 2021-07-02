import discord
from urllib.parse import urlparse

def is_url(url: str):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def fail(error: str):
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

def success(success: str):
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
    