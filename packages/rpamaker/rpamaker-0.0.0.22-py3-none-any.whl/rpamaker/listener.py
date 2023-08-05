"""Listener interface module"""
import datetime

from robot.libraries.BuiltIn import BuiltIn

from rpamaker.orquestador import OrquestadorAPI


class Listener:
    ROBOT_LISTENER_API_VERSION = 2
    LOG_DELAY = 2

    def __init__(self):
        self.console_flag = None
        self.errors = False
        self.id_t = ""
        self.last_log = datetime.datetime(2000, 1, 1)
        self.last_ping = datetime.datetime(2000, 1, 1)
        self.logs = []
        self.path_log = ""
        self.path_report = ""

    def _ping_orquestador(self):
        self.orquestador_api.ping()
        self.last_ping = datetime.datetime.now()

    def _send_status(self, status, message):
        self.orquestador_api.send_status(status, message)

    def _send_status_log_files(self, path_log, path_report, status, message):
        self.orquestador_api.send_status_logs(path_log, path_report, status, message)

    def _log_records(self):
        if self.logs:
            self.orquestador_api.log_records(self.logs)
            self.logs = []
            self.last_log = datetime.datetime.now()

    def start_suite(self, name, attrs):  # pylint: disable=unused-argument
        """Called when a test suite starts"""
        print("Calling start suite")
        self.id_t = BuiltIn().get_variables()["${id_t}"]
        print(f"ID_T: {self.id_t}")
        console_flag = BuiltIn().get_variables()["${console_flag}"]
        self.console_flag = console_flag == "True"
        print("Transition id: %s", self.id_t)
        print("Console flag: %s", self.console_flag)

        self.orquestador_api = OrquestadorAPI(self.id_t)
        self.orquestador_api.send_status("STARTED", "Robot iniciado")
        self._ping_orquestador()

    def end_suite(self, name, attrs):  # pylint: disable=unused-argument
        """Called when a test suite ends"""
        print("Calling end suite")
        id_t = self.id_t
        self._log_records()
        self._ping_orquestador()
        self.final_status = attrs["status"]

    def log_message(self, message):
        """
        Level Numeric value
        CRITICAL 50
        ERROR 40
        WARNING 30
        INFO 20
        DEBUG 10
        NOTSET 0
        """
        # print(f"{message['timestamp']}-{message['level']}- {message['message']}")

        if message["level"] in ["CRITICAL", "ERROR", "WARNING", "WARN"]:
            self.errors = True

        if self.console_flag:
            self.logs.append(str(message))
            if (datetime.datetime.now() - self.last_log) > datetime.timedelta(
                    seconds=1
            ):
                self._log_records()
        if (datetime.datetime.now() - self.last_ping) > datetime.timedelta(seconds=30):
            self._ping_orquestador()

    def log_file(self, path):
        """Called when writing to a log file is ready"""
        print("Log file: %s", path)
        self.path_log = path

    def report_file(self, path):
        """Called when writing to a report file is ready"""
        print("Report file: %s", path)
        self.path_report = path

    def close(self):
        """Called when the whole test execution ends"""
        print("Calling Close")
        if self.final_status == "FAIL":
            self._send_status_log_files(self.path_log, self.path_report, "FAILURE", "Ha ocurrido un error en el Robot")
        elif self.errors:
            self._send_status_log_files(self.path_log, self.path_report, "WARNING",
                                        "El robot ha finalizado la ejecucion con advertencias")
        else:
            self._send_status_log_files(self.path_log, self.path_report, "SUCCESS", "Robot ejecutado con exito")

        print("Close called")
