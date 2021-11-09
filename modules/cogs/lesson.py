# Discord
from discord.ext import commands
from discord.ext import tasks
# Modules
from modules.scripts.lessonsconfig import LessonManager
from modules.scripts.alertsconfig import AlertManager
from modules.cogs.bot import _commands_help
import datetime


class Lesson(commands.Cog):
    
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.lesson_manager = LessonManager()
        self.alert_manager = AlertManager()
        self.check_and_send.start()
        self.is_first_run = True

    @tasks.loop(minutes=1)
    async def check_and_send(self) -> None:
        if self.is_first_run:
            self.is_first_run = False
            return

        now = datetime.datetime.now()
        all_lessons = self.lesson_manager.list_all_lessons()
        if len(all_lessons) > 0:
            for lesson in all_lessons:
                lesson_date = datetime.datetime.strptime(lesson.lesson_date, "%Y-%m-%d")
                lesson_time = datetime.datetime.strptime(lesson.lesson_time, "%H:%M:%S")
                if lesson_date.date() == now.date():
                    if lesson_time.hour == now.hour and lesson_time.minute == now.minute:
                        guild_id = int(lesson.guild_id)
                        guild = self.client.get_guild(guild_id)
                        members = guild.members
                        for member in members:
                            member_alert = self.alert_manager.get_alert(member.id)
                            if member_alert is not None:
                                member_alert = f"\nAula: {member_alert.msg}"
                                msg_to_send = member_alert.replace("&alerta&", str(lesson))
                                await member.send(msg_to_send)
                                # TODO Improve this A LOT... This is a very bad look shit

    @commands.command(aliases=['LIST_AULAS'])
    async def list_aulas(self, ctx) -> None:
        guild_id = str(ctx.guild.id)
        response = self.lesson_manager.list_lessons(guild_id)
        for lesson in response:
            await ctx.send(f'{lesson.id}: {lesson}')

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
    
    @commands.command(aliases=['RM_AULA'])
    async def rm_aula(self, ctx, lesson_id: int) -> None:
        if self.lesson_manager.rm_lesson(lesson_id):
            await ctx.message.add_reaction('✅')
            
        else:
            await ctx.message.add_reaction('❌')


def setup(client) -> None:
    client.add_cog(Lesson(client))
        