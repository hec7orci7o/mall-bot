import discord
from discord.ext import commands
import os

class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
    
    async def send_bot_help(self, mapping):
        return await super().send_bot_help(mapping)

    async def send_cog_help(self, cog):
        return await super().send_cog_help(cog)

    async def send_group_help(self, group):
        return await super().send_group_help(group)
    
    async def send_command_help(self, command):
        return await super().send_command_help(command)

class MallBot(commands.Bot):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

client = MallBot(command_prefix='$', help_command=commands.HelpCommand())

# Cogs
for filename in os.listdir('src/cogs'):
    if filename.endswith('.py'):
        try:
            client.load_extension(f'cogs.{filename[:-3]}')
            print(f'cogs.{filename[:-3]} loaded successfully.')
        except:
            print(f'error al cargar el cog {filename[:-3]}')

client.run(os.environ['TOKEN'])
