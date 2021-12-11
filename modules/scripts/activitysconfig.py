# Standard libraries
from datetime import datetime
# Modules
from modules.scripts.database import Connection
from modules.scripts.datetimeerrors import *


class Activity:

    def __init__(self, subject: str, deadline: str, title: str, guild_id: str) -> None:
        self.id = None
        self.subject = str(subject)
        self.title = str(title)
        self._deadline = str(deadline)
        self.guild_id = str(guild_id).strip().lower()

    @property
    def _deadline(self) -> str:
        return self.deadline

    @_deadline.setter
    def _deadline(self, value: str) -> None:
        value = value.strip().lower()
        try:
            datetime.strptime(value, "%Y-%m-%d")  # If it raises a error, the date format is wrong
            is_correct = True

        except ValueError:
            is_correct = False

        if not is_correct:
            raise InvalidDate("Expected: \"YYYY-MM-DD\"", f"Got: {value}")

        self.deadline = value

    def __repr__(self) -> str:
        return f'<{self.subject}: {self._deadline}>'


class ActivityManager:
    """Manages the activities
    """

    def __init__(self) -> None:
        self._con = Connection()

    def check_guild_id(self, guild_id: str) -> bool:
        """
        Will check if the guild ID exists in the database, and if not, it will add it

        :param guild_id: guild's ID
        :type guild_id: str
        :return: True or False
        """
        response = self._con.consult(f'SELECT * FROM guild WHERE guildID=\'{guild_id}\'')
        if len(response) == 0:
            if not self._con.manage(f'INSERT INTO guild(guildID) VALUES(\'{guild_id}\')'):
                return False

        return True

    def get_activity(self, activity_id: int) -> Activity:
        """Gets a activity from the database

        :param activity_id: activity's ID
        :type activity_id: int

        :return: a object of the class "Activity" or None
        """
        activity_id = int(activity_id)
        response = self._con.consult(f'SELECT * FROM activity WHERE activityID={activity_id}')
        if len(response) > 0:
            info = response[0]
            activity = Activity(info[1], info[2], info[3], info[4])
            activity.id = info[0]
            return activity

    def list_activities(self, guild_id: str) -> list[Activity] | None:
        """Gets all the guild's activities from the database

        :param guild_id: Guild's ID
        :type guild_id: str

        :return: A list of Activities or None
        """
        if not self.check_guild_id(guild_id):
            return None

        response = self._con.consult(f'SELECT * FROM activity WHERE guildID=\'{guild_id}\'')
        for index, info in enumerate(response):
            activity = Activity(info[1], info[2], info[3], info[4])
            if activity is not None:
                activity.id = info[0]
                response[index] = activity

        return response

    def list_all_activities(self) -> list[Activity] | None:
        """Gets all the activities from the database

        :return: A list of Activities or None
        """
        response = self._con.consult(f'SELECT * FROM activity')
        for index, info in enumerate(response):
            activity = Activity(info[1], info[2], info[3], info[4])
            if activity is not None:
                activity.id = info[0]
                response[index] = activity

        return response

    def rm_activity(self, activity_id: int) -> bool:
        """Removes a activity from the database

        :param activity_id: activity's ID
        :type activity_id: int

        :return: True or false
        """
        activity_id = int(activity_id)
        activity = ActivityManager.get_activity(self, activity_id)
        if activity is not None:
            sql = f'DELETE FROM activity WHERE lessonID=\'{activity_id}\''
            if self._con.manage(sql):
                return True

            else:
                return False

        return True

    def add_activity(self, subject: str, deadline: str, title: str, guild_id: str) -> bool:
        """Adds a activity in database

        :param subject: Lesson's subject
        :type subject: str
        :param deadline: Activity's deadline
        :type deadline: str
        :param title: Activity's title
        :type title: str
        :param guild_id: Server's ID
        :type guild_id: str

        :return: True or False
        """
        if not self.check_guild_id(guild_id):
            return False

        activity = Activity(subject, deadline, title, guild_id)
        if activity is not None:
            sql = f"""INSERT INTO activity(subject, url, lessonDate, lessonTime, guildID) 
            VALUES(\'{activity.subject}\', \'{activity.deadline}\', \'{activity.title}\', \'{activity.guild_id}\')"""
            if self._con.manage(sql):
                return True

        return False
