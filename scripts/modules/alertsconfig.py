# Modules
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
            raise Exception('AM')  # 'AM' means 'alert tag missing'

        self.msg = value

    def __eq__(self, obj: object) -> bool:
        if self.__class__ == obj.__class__:
            return self.alert_id == obj.lesson_id

        else:
            return self.alert_id == obj

    def __repr__(self) -> str:
        return f'<id:{self.alert_id} | message:{self.msg}>'


class AlertManager:
    """Manage the alerts
    """
    def __init__(self) -> None:
        self._con = Connection(
            'localhost',
            'botschrodinger',
            'postgres',
            'postgres'
        )

    def get_alert(self, alert_id: str) -> Alert:
        """Gets an alert from the database

        :param alert_id: alert's ID
        :type alert_id: str

        :return: object of the class "alert" or None
        """
        alert_id = str(alert_id)
        response = self._con.consult(f'SELECT * FROM alert WHERE alertID=\'{alert_id}\'')
        if len(response) > 0:
            response = response[0]
            alert = Alert(response[0], response[1])
            return alert

    def rm_alert(self, alert_id: str) -> bool:
        """Remove the alert from the database

        :param alert_id: alert's ID
        :type alert_id: str

        :return: True or False
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
        """Sets an alert for a server or a user

        :param alert_id: alert's ID.
        :type alert_id: str
        :param msg: The message that will be registered, needs to have the word
        "&alerta&" (it's the location that the alert object will be). If you want to reset your alert, write: "none"
        :type msg: str

        :return: True or false
        """
        alert_id = str(alert_id)
        alert = Alert(alert_id, msg)
        if alert is not None:
            if AlertManager.rm_alert(self, alert.alert_id):
                sql = f'INSERT INTO alert(alertID, msg) VALUES(\'{alert.alert_id}\', \'{alert.msg}\')'
                return self._con.manage(sql)

        return False
