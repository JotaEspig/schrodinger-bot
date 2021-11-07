# Discord
from discord.ext import commands


_commands_help = {
            'set_alerta_atividade': 'Esse comando configura uma mensagem customizável para os alertas de '
                                    'atividades\n\n**Sintaxe do comando:**\n`&set_alerta_atividade <mensagem '
                                    'customizada>`\n`&alerta&` é a marcação da posição onde as informações da aula '
                                    'ficaram.\nObs.: Essa marcação é obrigatória na mensagem\n\n**Formas de usar o '
                                    'comando:**\n`&set_alerta_atividade`, `&sa_ativ`',
            'set_alerta_aula': 'Esse comando configura uma mensagem customizável para os alertas de '
                               'aulas\n\n**Sintaxe do comando:**\n`&set_alerta_aula <mensagem '
                               'customizada>`\n`&alerta&` é a marcação da posição onde as informações da aula '
                               'ficaram.\nObs.: Essa marcação é obrigatória\n\n**Formas de usar o '
                               'comando:**\n`&set_alerta_aula`, `&sa_aula`',
            'rm_alerta_atividade': 'Esse comando desabilita o alerta para suas atividades\nEsse comando não necessita '
                                   'de parâmetros\n\n**Formas de usar o comando:**\n`&rm_alerta_atividade`, '
                                   '`&rma_ativ`',
            'rm_alerta_aula': 'Esse comando desabilita o alerta para as aulas\nEsse comando não necessita de '
                              'parâmetros\n\n**Formas de usar o comando:**\n`&rm_alerta_aula`, `&rma_aula` '
        }


class Bot(commands.Cog):
    
    def __init__(self, client) -> None:
        self.client = client
    
    @commands.command(aliases=['PING'])
    async def ping(self, ctx) -> None:
        await ctx.send(f'{round(self.client.latency * 1000)}ms de ping')
            

def setup(client) -> None:
    client.add_cog(Bot(client))
