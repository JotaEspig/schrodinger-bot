#Psycopg2
import psycopg2


class Connection:
    """Realiza a conexão com o banco de dados
    """
    _db = None

    def __init__(self, hostname, dbname, usr, pwd) -> None:
        self._db = psycopg2.connect(
            host= hostname,
            database= dbname,
            user= usr,
            password= pwd
        )

    def manage(self, sql) -> None:
        """Vai manipular o banco de dados com o comando inserido

        Args:
            sql (str): Comando para ser executado

        Returns:
            bool: True para quando não há problemas e False para quando ocorreu problemas
        """
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()

        except:
            return False
        
        return True

    def consult(self, sql) -> None:
        """Vai consultar o banco de dados com o comando inserido

        Args:
            sql (str): Comando para ser executado

        Returns:
            bool: Retorna a resposta do banco de dados ou retorna None caso aconteça algum erro
        """
        response= None
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            response = cur.fetchall()
            cur.close()
        
        except:
            return None

        return response
    
    def close(self) -> None:
        """Fecha o banco de dados
        """
        self._db.close()

    def __repr__(self) -> str:
        host = self._db.info.host
        dbname = self._db.info.dbname
        return f'{host}: {dbname}'