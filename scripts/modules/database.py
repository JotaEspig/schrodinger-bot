# Psycopg
import psycopg


class Connection:
    _db = None

    def __init__(self, hostname, dbname, usr, pwd) -> None:
        self._db = psycopg.connect(f"host={hostname} dbname={dbname} user={usr} password={pwd}")

    def manage(self, sql: str) -> bool:
        """Manages the database with a command

        :param sql: Command to be executed
        :type sql: str

        :return: True if all did well, else False
        """
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()

        except:
            return False

        return True

    def consult(self, sql) -> list | None:
        """Vai consultar o banco de dados com o comando inserido

        :param sql: Command to be executed
        :type sql: str

        :return: a response from the database or None if some error has occurred
        """
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            response = cur.fetchall()
            cur.close()

        except:
            return None

        return response

    def close(self) -> None:
        """Closes the database
        """
        self._db.close()

    def __repr__(self) -> str:
        host = self._db.info.host
        dbname = self._db.info.dbname
        return f'{host}: {dbname}'
