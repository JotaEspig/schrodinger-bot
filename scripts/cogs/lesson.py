# Discord
from discord.ext import commands
# Modules
from scripts.modules.lessonsconfig import LessonManager
from scripts.cogs.bot import _commands_help


class Lesson(commands.Cog):
    
    def __init__(self, client) -> None:
        self.client = client
        self.lesson_manager = LessonManager()

    @commands.command(aliases=['ADD_AULA'])
    async def add_aula(self, ctx, subject: str, url: str, lesson_date: str, lesson_time: str) -> None:
        try:
            if self.lesson_manager.add_lesson(subject, url, lesson_date, lesson_time, str(ctx.guild.id)):
                await ctx.message.add_reaction('✅')

            else:
                await ctx.message.add_reaction('❌')

        except Exception as error:
            if error.args[0] == 'Invalid date format':
                await ctx.send('Formato de data inválido')
            elif error.args[0] == 'Invalid time format':
                await ctx.send('Formato de horário inválido')
    
    @commands.command()
    async def rm_aula(self, ctx, lesson_id: int) -> None:
        if self.lesson_manager.rm_lesson(lesson_id):
            await ctx.message.add_reaction('✅')
            
        else:
            await ctx.message.add_reaction('❌')


def setup(client) -> None:
    client.add_cog(Lesson(client))
        