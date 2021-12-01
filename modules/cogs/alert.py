# Discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord.ext.commands.errors import MissingPermissions
# Modules
from modules.scripts.alertsconfig import AlertManager
from modules.cogs.bot import _commands_help


class Alert(commands.Cog):

    def __init__(self, client) -> None:
        self.client = client
        self.alert_manager = AlertManager()
        
    @commands.command(aliases=['SET_ALERTA'])
    @has_permissions(administrator=True)
    async def set_alerta(self, ctx, *, msg: str) -> None:
        alert_id = str(ctx.author.id)
        if self.alert_manager.set_alert(alert_id, msg):
            await ctx.message.add_reaction('✅')

        else:
            await ctx.message.add_reaction('❌')

    @set_alerta.error
    async def alerta_error(self, ctx, error) -> None:
        if not isinstance(error, MissingPermissions):
            await ctx.send(_commands_help['set_alerta'])

    @commands.command(aliases=['RM_ALERTA_AULA', 'rma_aula', 'RMA_AULA'])
    @has_permissions(administrator=True)
    async def rm_alerta(self, ctx) -> None:
        alert_id = str(ctx.guild.id)
        if self.alert_manager.rm_alert(alert_id):
            await ctx.message.add_reaction('✅')

        else:
            await ctx.message.add_reaction('❌')


def setup(client) -> None:
    client.add_cog(Alert(client))
