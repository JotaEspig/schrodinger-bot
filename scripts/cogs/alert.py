#Discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord.ext.commands.errors import MissingPermissions
#Modules
from scripts.modules.alertsconfig import AlertManager
from scripts.cogs.bot import _commands_help



class Alert(commands.Cog):

    def __init__(self, client) -> None:
        self.client = client
        self.alert_manager = AlertManager()

    @commands.command(aliases= ['SET_ALERTA_ATIVIDADE', 'sa_ativ', 'SA_ATIV'])
    async def set_alerta_atividade(self, ctx, *, msg: str) -> None:
        alert_id = str(ctx.author.id)
        try:
            if self.alert_manager.set_alert(alert_id, msg):
                await ctx.message.add_reaction('✅')

            else:
                await ctx.message.add_reaction('❌')

        except Exception as error:
            if error.args[0] == 'AM':
                await ctx.send('Digite &alerta&')

    @set_alerta_atividade.error
    async def alerta_atividade_error(self, ctx, error) -> None:
        if not isinstance(error, MissingPermissions):
            await ctx.send(_commands_help['set_alerta_atividade'])
        
    @commands.command(aliases= ['SET_ALERTA_AULA', 'sa_aula', 'SA_AULA'])
    @has_permissions(administrator= True)
    async def set_alerta_aula(self, ctx, *, msg: str) -> None:
        alert_id = str(ctx.guild.id)
        try:
            if self.alert_manager.set_alert(alert_id, msg):
                await ctx.message.add_reaction('✅')

            else:
                await ctx.message.add_reaction('❌')

        except Exception as error:
            if error.args[0] == 'AM':
                await ctx.send('Digite &alerta&')

    @set_alerta_aula.error
    async def alerta_aula_error(self, ctx, error) -> None:
        if not isinstance(error, MissingPermissions):
            await ctx.send(_commands_help['set_alerta_aula'])

    @commands.command(aliases= ['RM_ALERTA_ATIVIDADE', 'rma_ativ', 'RMA_ATIV'])
    async def rm_alerta_atividade(self, ctx) -> None:
        alert_id = str(ctx.author.id)
        if self.alert_manager.rm_alert(alert_id):
            await ctx.message.add_reaction('✅')
            
        else:
            await ctx.message.add_reaction('❌')

    @commands.command(aliases= ['RM_ALERTA_AULA', 'rma_aula', 'RMA_AULA'])
    @has_permissions(administrator= True)
    async def rm_alerta_aula(self, ctx) -> None:
        alert_id = str(ctx.guild.id)
        if self.alert_manager.rm_alert(alert_id):
            await ctx.message.add_reaction('✅')

        else:
            await ctx.message.add_reaction('❌')


def setup(client) -> None:
    client.add_cog(Alert(client))