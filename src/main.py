import os
import datetime
import discord
import libs.utils as util
from discord.ext import commands, tasks

class BotHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
    
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title= "Help Menu",
            colour= int("3861FB",16)
        )
        for cog in mapping:
            if cog != None:
                lista = [command.name for command in mapping[cog]]
                value = ''
                for cmd in lista:
                    value += (f" + {cmd}\n")
                embed.add_field(name= str(cog.qualified_name).capitalize(), value= value, inline='false')
        await self.get_destination().send(embed= embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(
            title= "Cog Menu",
            colour= int("3861FB",16)
        )
        lista = [command.name for command in cog.get_commands()]
        value = ''
        for cmd in lista:
            value += (f" + {cmd}\n")
        embed.add_field(name= str(cog.qualified_name).capitalize(), value= value, inline='false')
        await self.get_destination().send(embed= embed)
    
    async def send_command_help(self, command):
        embed = discord.Embed(
            title= "Command: " + str(command.name).capitalize(),
            description= command.help,
            colour= int("3861FB",16)
        )
        await self.get_destination().send(embed= embed)

    async def send_group_help(self, group):
        await self.get_destination().send(f'{group.name}: {[command.name for index, command in enumerate(group.commands)]}')

class MallBot(commands.Bot):
    async def on_ready(self):
        embed = discord.Embed(
            description= util.translate("Si el público supiera lo que quiere,\nentonces no sería el público,\nsería el artista.", dest='en'),
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
            value= "```c++\n{}```".format(util.translate("Corriendo en {} servidores\nComenzó a las {}".format(len(client.guilds), datetime.datetime.now().strftime("%X")), dest='en')),
            inline= False
        )
        embed.set_footer(
            text= util.translate("Hecho con 💘 por Hec7orci7o.", dest='en'),
            icon_url= "https://avatars.githubusercontent.com/u/56583980?s=60&v=4"
        )
        
        channel = client.get_channel(int(os.environ['CHANNEL']))
        await channel.send(embed=embed)
        print(util.translate('Conectado como {0}!'.format(self.user)))
        print("Event loop 'change presence()' started.")
        self.presenceLoop.start()

    @tasks.loop(seconds = 3600) # repeat after every 1 hour
    async def presenceLoop(self):
        game = discord.Activity(type=discord.ActivityType.watching, name="{} {} | $help".format(len(client.guilds), util.translate("mesas")))
        await client.change_presence(status=discord.Status.idle, activity=game)

client = MallBot(command_prefix='$', help_command=BotHelpCommand())

# Cogs
for filename in os.listdir('src/cogs'):
    if filename.endswith('.py'):
        try:
            client.load_extension(f'cogs.{filename[:-3]}')
            print(util.translate(f'cogs.{filename[:-3]} cargado con exito.'))
        except:
            print(util.translate(f'Error al cargar el cog {filename[:-3]}'))

client.run(os.environ['TOKEN'])
