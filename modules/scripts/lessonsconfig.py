# Standard libraries
from datetime import datetime
# Modules
from modules.scripts.database import Connection
from modules.scripts.datetimeerrors import *


class Lesson:

    def __init__(self, subject: str, url: str, lesson_date: str, lesson_time: str, guild_id: str) -> None:
        self.id = None
        self.subject = str(subject)
        self.url = str(url).strip().lower()
        self._lesson_date = str(lesson_date)
        self._lesson_time = str(lesson_time)
        self.guild_id = str(guild_id).strip().lower()

    @property
    def _lesson_date(self) -> str:
        return self.lesson_date

    @_lesson_date.setter
    def _lesson_date(self, value: str) -> None:
        value = value.strip().lower()
        try:
            datetime.strptime(value, "%Y-%m-%d")  # If it raises a error, the date format is wrong
            is_correct = True

        except ValueError:
            is_correct = False

        if not is_correct:
            raise InvalidDate("Expected: \"YYYY-MM-DD\"", f"Got: {value}")

        self.lesson_date = value

    @property
    def _lesson_time(self) -> str:
        return self.lesson_time

    @_lesson_time.setter
    def _lesson_time(self, value: str) -> None:
        value = value.strip().lower()
        try:
            datetime.strptime(value, "%H:%M")  # If it raises a error, the time format is wrong
            is_correct = True

        except ValueError:
            is_correct = False

        if not is_correct:
            try:
                datetime.strptime(value, "%H:%M:%S")
                is_correct = True

            except ValueError:  # Check the time format again, but now with the postgres time format
                is_correct = False

            if not is_correct:
                raise InvalidTime("Expected: \"hh:mm\"", f"Got: {value}")

        self.lesson_time = value

    def __repr__(self) -> str:
        return f'<{self.subject}: {self._lesson_date} / {self._lesson_time}>'


class LessonManager:
    """Manages the lessons
    """
    def __init__(self) -> None:
        self._con = Connection(
            'localhost',
            'botschrodinger',
            'postgres',
            'postgres'
        )

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

    def get_lesson(self, lesson_id: int) -> Lesson:
        """Gets a lesson from the database

        :param lesson_id: lesson's ID
        :type lesson_id: int

        :return: a object of the class "Lesson" or None
        """
        response = self._con.consult(f'SELECT * FROM lesson WHERE lessonID={lesson_id}')
        if len(response) > 0:
            info = response[0]
            lesson = Lesson(info[1], info[2], info[3], info[4], info[5])
            lesson.id = info[0]
            return lesson

    def list_lessons(self, guild_id: str) -> list[Lesson] | None:
        """Gets all the guild's lessons from the database

        :param guild_id: Guild's ID
        :type guild_id: str

        :return: A list of lessons or None
        """
        if not self.check_guild_id(guild_id):
            return None

        response = self._con.consult(f'SELECT * FROM lesson WHERE guildID=\'{guild_id}\'')
        for index, info in enumerate(response):
            lesson = Lesson(info[1], info[2], info[3], info[4], info[5])
            if lesson is not None:
                lesson.id = info[0]
                response[index] = lesson

        return response

    def list_all_lessons(self) -> list[Lesson] | None:
        """Gets all the lessons from the database

        :return: A list of lessons or None
        """
        response = self._con.consult(f'SELECT * FROM lesson')
        for index, info in enumerate(response):
            lesson = Lesson(info[1], info[2], info[3], info[4], info[5])
            if lesson is not None:
                lesson.id = info[0]
                response[index] = lesson

        return response
    
    def rm_lesson(self, lesson_id: int) -> bool:
        """Removes a lesson from the database

        :param lesson_id: lesson's ID
        :type lesson_id: int

        :return: True or false
        """
        lesson_id = int(lesson_id)
        lesson = LessonManager.get_lesson(self, lesson_id)
        if lesson is not None:
            sql = f'DELETE FROM lesson WHERE lessonID=\'{lesson_id}\''
            if self._con.manage(sql):
                return True

            else:
                return False

        return True

    def add_lesson(self, subject: str, url: str, lesson_date: str, lesson_time: str, guild_id: str) -> bool:
        """Adds a lesson in database

        :param subject: Lesson's subject
        :type subject: str
        :param url: lesson's url
        :type url: str
        :param lesson_date: lesson's data (YYYY-MM-DD)
        :type lesson_date: str
        :param lesson_time: Lesson's time
        :type lesson_time: str
        :param guild_id: Server's ID
        :type guild_id: str

        :return: True or False
        """
        if not self.check_guild_id(guild_id):
            return False

        lesson = Lesson(subject, url, lesson_date, lesson_time, guild_id)
        if lesson is not None:
            sql = f"""INSERT INTO lesson(subject, url, lessonDate, lessonTime, guildID) 
            VALUES(\'{lesson.subject}\', \'{lesson.url}\', \'{lesson.lesson_date}\', \'{lesson.lesson_time}\', 
            \'{lesson.guild_id}\') """
            if self._con.manage(sql):
                return True
        
        return False
