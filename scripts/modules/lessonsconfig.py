#Modules
from scripts.modules.database import Connection


class Lesson:

    def __init__(self, subject: str, url: str, lesson_date: str, lesson_time: str, guild_id: str) -> None:
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
        if value.count('-') != 2:
            raise Exception('LD')

        if len(value) != 10:
            raise Exception('LD')
        
        self.lesson_date = value

    @property
    def _lesson_time(self) -> str:
        return self.lesson_time
    @_lesson_time.setter
    def _lesson_time(self, value: str) -> None:
        value = value.strip().lower()
        if not 1 <= value.count(':') <= 2:
            raise Exception('LT')

        if not 5 <= len(value) <= 8:
            raise Exception('LT')

        self.lesson_time = value

    def __eq__(self, obj: object) -> bool:
        return self.lesson_id == obj.lesson_id

    def __repr__(self) -> str:
        return f'{self.subject}: {self._lesson_date} / {self._lesson_time}'


class LessonManager:
    """Gerenciador de aulas
    """
    def __init__(self) -> None:
        self._con = Connection(
            'localhost',
            'botschrodinger',
            'postgres',
            'postgres'
        )
    
    def get_lesson(self, lesson_id: int) -> Lesson:
        """Retorna uma aula do banco de dados

        Args:
            lesson_id (int): id da aula

        Returns:
            Lesson: Objeto de classe Lesson ou um None
        """
        lesson_id = int(lesson_id)
        response = self._con.consult(f'SELECT * FROM lesson WHERE lessonID={lesson_id}')
        if len(response) > 0:
            response = response[0]
            lesson = Lesson(response[1], response[2], response[3], response[4], response[5])
            return lesson
    
    def rm_lesson(self, lesson_id: int) -> bool:
        """Remove uma aula do banco de dados

        Args:
            lesson_id (int): Id da aula

        Returns:
            bool: True ou False
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
        """Adiciona uma aula no banco de dados

        Args:
            subject (str): Disciplina da aula
            url (str): Link da aula
            lesson_date (str): Dia da aula/Mês da aula/Ano da aula
            lesson_time (str): Horário da aula
            guild_id (str): Id do servidor

        Returns:
            bool: True ou False
        """
        response = self._con.consult(f'SELECT * FROM guild WHERE guildID=\'{guild_id}\'')
        if len(response) == 0:
            if not self._con.manage(f'INSERT INTO guild(guildID) VALUES(\'{guild_id}\')'):
                return False

        lesson = Lesson(subject, url, lesson_date, lesson_time, guild_id)
        if lesson is not None:
            sql = f"""INSERT INTO lesson(subject, url, lessonDate, lessonTime, guildID) 
            VALUES(\'{lesson.subject}\', \'{lesson.url}\', \'{lesson._lesson_date}\', \'{lesson._lesson_time}\', \'{lesson.guild_id}\')"""
            if self._con.manage(sql):
                return True
        
        return False
