# Discord
import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands.errors import MissingPermissions
# Modules
from modules.scripts import activitysconfig
from modules.scripts.activitysconfig import ActivityManager
from modules.scripts.datetimeerrors import InvalidDate
from modules.scripts.alertsconfig import AlertManager
from modules.cogs.bot import _commands_help
import datetime
from time import sleep


class Activity(commands.Cog):

    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.activity_manager = ActivityManager()
        self.alert_manager = AlertManager()
        self.check_and_send.start()
        self.is_first_run = True

    async def send_alert(self, activity: activitysconfig.Activity) -> None:
        guild_id = int(activity.guild_id)
        guild = self.client.get_guild(guild_id)
        members = guild.members
        for member in members:
            member_alert = self.alert_manager.get_alert(member.id)
            if member_alert is not None:
                embed_var = discord.Embed(title=activity.subject.capitalize(), color=0xFFA500)
                embed_var.add_field(name='Título', value=activity.title)
                embed_var.add_field(name='Data de entrega', value=activity.deadline, inline=False)
                embed_var.set_footer(icon_url=self.client.user.avatar_url,
                                     text='Schrödinger Bot')
                await member.send(member_alert.msg)
                await member.send(embed=embed_var)

    @tasks.loop(hours=24)
    async def check_and_send(self) -> None:
        if self.is_first_run:
            self.is_first_run = False
            return

        now = datetime.datetime.now()
        all_lessons = self.activity_manager.list_all_activities()
        if len(all_lessons) > 0:
            for activity in all_lessons:
                deadline = datetime.datetime.strptime(activity.deadline, "%Y-%m-%d")
                if deadline.date() == now.date():
                    await self.send_alert(activity)

                elif deadline.day == now.day - 7:
                    self.activity_manager.rm_activity(activity.id, activity.guild_id)

    @commands.command(aliases=['GET_ATIVIDADE'])
    async def get_atividade(self, ctx, *, activity_id) -> None:
        activity = self.activity_manager.get_activity(activity_id)
        if activity is not None:
            if int(activity.guild_id) == int(ctx.guild.id):
                embed_var = discord.Embed(title=activity.subject.capitalize(), color=0xFFA500)
                embed_var.add_field(name='Título', value=activity.title)
                embed_var.add_field(name='Data de entrega', value=activity.deadline, inline=False)
                embed_var.set_footer(icon_url=self.client.user.avatar_url,
                                     text='Schrödinger Bot')
                await ctx.send(embed=embed_var)
                return

        await ctx.send("Nenhuma atividade encontrada com esse ID")

    @commands.command(aliases=['LIST_ATIVIDADES'])
    async def list_atividades(self, ctx) -> None:
        guild_id = str(ctx.guild.id)
        response = self.activity_manager.list_activities(guild_id)
        if len(response) < 1:
            await ctx.send("Nenhuma atividade cadastrada")
            return

        embed_var = discord.Embed(title="Atividades marcadas", color=0xFFA500)
        for activity in response:
            embed_var.add_field(name=activity.id, value=f"{activity.title} : {activity.deadline}", inline=False)

        await ctx.send(embed=embed_var)

    @commands.command(aliases=['ADD_ATIVIDADE'])
    @commands.has_permissions(administrator=True)
    async def add_atividade(self, ctx, deadline: str, subject: str, *, title: str) -> None:
        try:
            if self.activity_manager.add_activity(subject, deadline, title, str(ctx.guild.id)):
                await ctx.message.add_reaction('✅')

            else:
                await ctx.message.add_reaction('❌')

        except InvalidDate:
            await ctx.send('Formato de data inválido')

    @add_atividade.error
    async def add_atividade_error(self, ctx, error) -> None:
        if not isinstance(error, MissingPermissions):
            await ctx.send(_commands_help['add_atividade'])

    @commands.command(aliases=['RM_ATIVIDADE'])
    @commands.has_permissions(administrator=True)
    async def rm_atividade(self, ctx, activity_id: int) -> None:
        if self.activity_manager.rm_activity(activity_id, ctx.guild.id):
            await ctx.message.add_reaction('✅')

        else:
            await ctx.message.add_reaction('❌')

    @rm_atividade.error
    async def rm_atividade_error(self, ctx, error) -> None:
        if not isinstance(error, MissingPermissions):
            await ctx.send(_commands_help['rm_atividade'])


def setup(client) -> None:
    client.add_cog(Activity(client))
