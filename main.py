# Standard Libraries
import json
from os import listdir

# Discord
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions


# Defines the token and the prefix
with open('config.json', 'r') as file:
    config = json.load(file)
    TOKEN, PREFIX = config['token'], config['prefix']

# Configure the Bot
intents = discord.Intents(
    messages=True,
    guilds=True,
    reactions=True,
    members=True,
    presences=True
)
client = commands.Bot(command_prefix=PREFIX, intents=intents)


def is_it_me(ctx) -> bool:
    """
    Check if the author of the message is one of the owners of the Bot

    :param ctx: Context provided by Discord API
    """
    owners = [
        720686657950711909,
        621048999989870592,
        335554042736541698
    ]
    return ctx.author.id in owners


@client.command(aliases=['LOAD'])
@commands.check(is_it_me)
async def load(ctx, extension: str) -> None:
    """
    Enable a bot's cog

    :param ctx: Context provided by Discord API
    :param extension: cog's name
    """

    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'\"{extension}\" carregado')


@client.command(aliases=['UNLOAD'])
@commands.check(is_it_me)
async def unload(ctx, extension: str) -> None:
    """Disable a bot's cog

    :param ctx: Context provided by Discord API
    :param extension: cog's name
    """
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'\"{extension}\" descarregado')


@client.command(aliases=['RELOAD'])
@commands.check(is_it_me)
async def reload(ctx, extension: str) -> None:
    """Reload a bot's cog

    :param ctx: Context provided by Discord API
    :param extension: cog's name
    """
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'\"{extension}\" recarregado')

# Load all cogs automatically
for filename in listdir('./scripts/cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'scripts.cogs.{filename[:-3]}')


# -X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X
# Runs the bot
@client.event
async def on_command_error(ctx, error) -> None:
    """Treats the errors that happen during the operation of the bot

    :param ctx: Context provided by Discord API
    :param error: Error
    """
    if isinstance(error, MissingPermissions):
        await ctx.send(f':hand_splayed: Você não tem permissão para usar esse comando\n:hand_splayed: {error}')


@client.event
async def on_ready() -> None:
    print(f'{client.user.name} online')
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=f'{PREFIX}help')
    )


if __name__ == '__main__':
    client.run(TOKEN)
