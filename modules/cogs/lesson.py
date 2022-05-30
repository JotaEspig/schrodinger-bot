# Discord
import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands.errors import MissingPermissions
# Modules
from modules.scripts import lessonsconfig
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

    async def send_alert(self, lesson: lessonsconfig.Lesson) -> None:
        guild_id = int(lesson.guild_id)
        guild = self.client.get_guild(guild_id)
        members = guild.members
        for member in members:
            member_alert = self.alert_manager.get_alert(member.id)
            if member_alert is not None:
                embed_var = discord.Embed(title=lesson.subject.capitalize(), color=0xFFA500)
                embed_var.add_field(name='Horário', value=lesson.lesson_time)
                embed_var.add_field(name='Data', value=lesson.lesson_date)
                embed_var.add_field(name='Link', value=lesson.url, inline=False)
                embed_var.set_footer(icon_url=self.client.user.avatar_url,
                                     text='Schrödinger Bot')
                await member.send(member_alert.msg)
                await member.send(embed=embed_var)

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
                    if lesson_time.hour == now.hour and lesson_time.minute == (now.minute + 5):
                        await self.send_alert(lesson)
                        self.lesson_manager.rm_lesson(lesson.id, lesson.guild_id)
                        continue

                    if now.minute + 30 < 60:
                        if lesson_time.hour == now.hour and lesson_time.minute == (now.minute + 30):
                            await self.send_alert(lesson)


                    else:
                        minutes = (now.minute + 30) - 60
                        if lesson_time.hour == now.hour + 1 and lesson_time.minute == minutes:
                            await self.send_alert(lesson)

    @commands.command(aliases=['GET_AULA'])
    async def get_aula(self, ctx, *, lesson_id) -> None:
        lesson = self.lesson_manager.get_lesson(lesson_id)
        if lesson is not None:
            if int(lesson.guild_id) == int(ctx.guild.id):
                embed_var = discord.Embed(title=lesson.subject.capitalize(), color=0xFFA500)
                embed_var.add_field(name='Horário', value=lesson.lesson_time)
                embed_var.add_field(name='Data', value=lesson.lesson_date)
                embed_var.add_field(name='Link', value=lesson.url, inline=False)
                embed_var.set_footer(icon_url=self.client.user.avatar_url,
                                     text='Schrödinger Bot')
                await ctx.send(embed=embed_var)
                return

        await ctx.send("Nenhuma aula encontrada com esse ID")

    @commands.command(aliases=['LIST_AULAS'])
    async def list_aulas(self, ctx) -> None:
        guild_id = str(ctx.guild.id)
        response = self.lesson_manager.list_lessons(guild_id)
        if len(response) < 1:
            await ctx.send("Nenhuma aula cadastrada")
            return

        embed_var = discord.Embed(title="Aulas marcadas", color=0xFFA500)
        for lesson in response:
            embed_var.add_field(name=lesson.id, value=f"{lesson.subject} : {lesson.lesson_date}", inline=False)

        await ctx.send(embed=embed_var)

    @commands.command(aliases=['ADD_AULA'])
    @commands.has_permissions(administrator=True)
    async def add_aula(self, ctx, url: str, lesson_date: str, lesson_time: str, *, subject: str) -> None:
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

    @add_aula.error
    async def add_aula_error(self, ctx, error) -> None:
        if not isinstance(error, MissingPermissions):
            await ctx.send(_commands_help['add_aula'])
    
    @commands.command(aliases=['RM_AULA'])
    @commands.has_permissions(administrator=True)
    async def rm_aula(self, ctx, lesson_id: int) -> None:
        if self.lesson_manager.rm_lesson(lesson_id, ctx.guild.id):
            await ctx.message.add_reaction('✅')
            
        else:
            await ctx.message.add_reaction('❌')

    @rm_aula.error
    async def rm_aula_error(self, ctx, error) -> None:
        if not isinstance(error, MissingPermissions):
            await ctx.send(_commands_help['rm_aula'])


def setup(client) -> None:
    client.add_cog(Lesson(client))
        