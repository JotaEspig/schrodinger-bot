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

# Configures the Bot
intents = discord.Intents(
    messages=True,
    guilds=True,
    reactions=True,
    members=True,
    presences=True
)
client = commands.Bot(command_prefix=PREFIX, intents=intents)


def is_owner(ctx) -> bool:
    """
    Checks if the author of the message is one of the owners of the Bot

    :param ctx: Context provided by Discord API
    """
    owners = [
        720686657950711909,  # JVE
        621048999989870592,  # IG
        335554042736541698,  # FJH
        609516579549347863   # LRB
    ]
    return ctx.author.id in owners


@client.command(aliases=['LOAD'])
@commands.check(is_owner)
async def load(ctx, extension: str) -> None:
    """
    Enables a bot's cog

    :param ctx: Context provided by Discord API
    :param extension: cog's name
    """

    client.load_extension(f'modules.cogs.{extension}')
    await ctx.send(f'\"{extension}\" carregado')


@client.command(aliases=['UNLOAD'])
@commands.check(is_owner)
async def unload(ctx, extension: str) -> None:
    """Disables a bot's cog

    :param ctx: Context provided by Discord API
    :param extension: cog's name
    """
    client.unload_extension(f'modules.cogs.{extension}')
    await ctx.send(f'\"{extension}\" descarregado')


@client.command(aliases=['RELOAD'])
@commands.check(is_owner)
async def reload(ctx, extension: str) -> None:
    """Reloads a bot's cog

    :param ctx: Context provided by Discord API
    :param extension: cog's name
    """
    client.unload_extension(f'modules.cogs.{extension}')
    client.load_extension(f'modules.cogs.{extension}')
    await ctx.send(f'\"{extension}\" recarregado')


@client.command(aliases=['stop', 'STOP', 'logout', 'LOGOUT', 'SHUTDOWN'])
@commands.check(is_owner)
async def shutdown(ctx) -> None:
    """Logouts the bot

    :param ctx: Context provided by Discord API
    """
    await ctx.message.add_reaction('✅')
    await client.close()


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
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=f'{PREFIX}help'
        )
    )


if __name__ == '__main__':
    # Load all cogs automatically
    for filename in listdir('./modules/cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'modules.cogs.{filename[:-3]}')

    client.run(TOKEN)
