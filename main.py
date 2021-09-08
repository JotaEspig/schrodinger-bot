#Standart Libraries
import json
from os import listdir

#Discord
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions


#Defines the token and the prefix
with open('config.json') as file:
    config = json.load(file)
    TOKEN, PREFIX = config['token'], config['prefix']


#Configure the Bot
intents = discord.Intents(
    messages = True,
    guilds = True,
    reactions = True,
    members = True,
    presences = True
)
client = commands.Bot(command_prefix= PREFIX, intents= intents)

def is_it_me(ctx) -> bool:
    """Verifica se o autor da mensagem é um dos donos do BOT

    Args:
        ctx (discord.ext.commands.context.Context): Contexto passado pela API do discord

    Returns:
        bool: True se o id do autor da mensagem é igual a um dos donos
    """
    owners = [
        720686657950711909,
        621048999989870592,
        335554042736541698
    ]
    return ctx.author.id in owners

@client.command(aliases= ['LOAD'])
@commands.check(is_it_me)
async def load(ctx, extension: str) -> None:
    """Habilita um cog do BOT

    Args:
        ctx (discord.ext.commands.context.Context): Contexto passado pela API do discord
        extension (str): Nome do arquivo do cog
    """
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'\"{extension}\" carregado')

@client.command(aliases= ['UNLOAD'])
@commands.check(is_it_me)
async def unload(ctx, extension: str) -> None:
    """Desabilita um cog do BOT

    Args:
        ctx (discord.ext.commands.context.Context): Contexto passado pela API do discord
        extension (str): Nome do arquivo do cog
    """
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'\"{extension}\" descarregado')

@client.command(aliases= ['RELOAD'])
@commands.check(is_it_me)
async def reload(ctx, extension: str) -> None:
    """Reinicia um cog do BOT

    Args:
        ctx (discord.ext.commands.context.Context): Contexto passado pela API do discord
        extension (str): Nome do arquivo do cog
    """
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'\"{extension}\" recarregado')

#Load em todos os cog automaticamente
for filename in listdir('./scripts/cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'scripts.cogs.{filename[:-3]}')

#-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X
#Runs the bot
@client.event
async def on_command_error(ctx, error) -> None:
    """Trata dos erros que acontecem durante o funcionamento do BOT

    Args:
        ctx (discord.ext.commands.context.Context): Contexto passado pela API do discord
        error: Erro ocorrido
    """
    if isinstance(error, MissingPermissions):
        await ctx.send(f':hand_splayed: Você não tem permissão para usar esse comando\n:hand_splayed: {error}') 

@client.event
async def on_ready() -> None:
    """Comandos executados quando o BOT fica online
    """
    print(f'{client.user.name} online')
    await client.change_presence(activity= discord.Activity(type= discord.ActivityType.listening, name= f'{PREFIX}help'))

client.run(TOKEN)