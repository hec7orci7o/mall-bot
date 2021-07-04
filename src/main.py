import os
import datetime
import discord
import libs.utils as util
from discord.ext import commands

class BotHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
    
    async def send_bot_help(self, mapping):
        for cog in mapping:
            await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in mapping[cog]]}')

    async def send_cog_help(self, cog):
        await self.get_destination().send(f'{cog.cualified_name}: {[command.name for command in cog.get_command()]}')
    
    async def send_command_help(self, command):
        await self.get_destination().send(command.name)

    async def send_group_help(self, group):
        await self.get_destination().send(f'{group.name}: {[command.name for index, command in enumerate(group.commands)]}')

class MallBot(commands.Bot):
    async def on_ready(self):
        embed = discord.Embed(
            description= util.translate("If the public knew what they want,\nthen it would not be the public,\nit would be the artist."),
            color= int("8CBF84", 16)
        )
        embed.set_thumbnail(
            url= "https://images.unsplash.com/photo-1543007630-9710e4a00a20?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80"
        )
        embed.set_author(
            name= f"{str(self.user)[:-5]}",
            url= "https://hec7or.me/",
            icon_url= "https://images.unsplash.com/photo-1590486145851-aae8758c4211?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1868&q=80"
        )
        embed.add_field(
            name= util.translate("Stats:"),
            value= util.translate("```c++\nRunning on {} servers\nStarted at {}```".format(len(client.guilds), datetime.datetime.now().strftime("%X"))),
            inline= False
        )
        embed.set_footer(
            text= util.translate("Made with 💘 by Hec7orci7o."),
            icon_url= "https://avatars.githubusercontent.com/u/56583980?s=60&v=4"
        )
        channel = client.get_channel(int(os.environ['CHANNEL']))
        await channel.send(embed=embed)
        print(util.translate('Logged on as {0}!'.format(self.user)))

client = MallBot(command_prefix='$', help_command=BotHelpCommand())

# Cogs
for filename in os.listdir('src/cogs'):
    if filename.endswith('.py'):
        try:
            client.load_extension(f'cogs.{filename[:-3]}')
            print(util.translate(f'cogs.{filename[:-3]} loaded successfully.'))
        except:
            print(util.translate(f'Error al cargar el cog {filename[:-3]}'))

client.run(os.environ['TOKEN'])
