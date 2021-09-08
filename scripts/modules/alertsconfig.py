#Modules
from scripts.modules.database import Connection


class Alert:
    
    def __init__(self, alert_id: str, msg: str) -> None:
        self.alert_id = str(alert_id)
        self._msg = str(msg)

    @property
    def _msg(self) -> str:
        return self.msg
    @_msg.setter
    def _msg(self, value: str) -> None:
        value = value.strip()
        if value == 'none':
            value = '&alerta&'
        if '&alerta&' not in value:
            raise Exception('AM')

        self.msg = value

    def __eq__(self, obj: object) -> bool:
        return self.alert_id == obj.lesson_id

    def __repr__(self) -> str:
        return f'id:{self.alert_id}'


class AlertManager:
    """Gerencia os alertas do sistema
    """
    def __init__(self) -> None:
        self._con = Connection(
            'localhost',
            'botschrodinger',
            'postgres',
            'postgres'
        )

    def get_alert(self, alert_id: str) -> Alert:
        """Retorna um alerta existente no banco de dados

        Args:
            alert_id (str): Id do alerta

        Returns:
            Alert: Objeto de classe Alert ou None
        """
        alert_id = str(alert_id)
        response = self._con.consult(f'SELECT * FROM alert WHERE alertID=\'{alert_id}\'')
        if len(response) > 0:
            response = response[0]
            alert = Alert(response[0], response[1])
            return alert

    def rm_alert(self, alert_id: str) -> bool:
        """Remove o alerta do banco de dados

        Args:
            alert_id (str): Id do alerta

        Returns:
            bool: True ou False
        """
        alert_id = str(alert_id)
        alert = AlertManager.get_alert(self, alert_id)
        if alert is not None:
            sql = f'DELETE FROM alert WHERE alertID=\'{alert.alert_id}\''
            if self._con.manage(sql):
                return True

            else:
                return False
            
        return True

    def set_alert(self, alert_id: str, msg: str) -> bool:
        """Configura um alerta para o servidor ou usuário

        Args:
            alert_id (str): Id do alerta
            msg (str): Mensagem que irá ser cadastrada, precisa conter a palavra \"&alerta&\" (é onde as variáveis do alerta vão ir) ou \"none\" (configura a mensagem para o padrão)

        Returns:
            bool: True ou False
        """
        alert_id = str(alert_id)
        alert = Alert(alert_id, msg)
        if alert is not None:
            if AlertManager.rm_alert(self, alert.alert_id):
                sql = f'INSERT INTO alert(alertID, msg) VALUES(\'{alert.alert_id}\', \'{alert.msg}\')'
                if self._con.manage(sql):
                    return True

        return False
