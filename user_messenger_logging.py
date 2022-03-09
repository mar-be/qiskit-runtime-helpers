from logging import Handler, LogRecord

from qiskit.providers.ibmq.runtime import UserMessenger


class UserMessengerHandler(Handler):

    def __init__(self, user_messenger: UserMessenger):
        super().__init__()
        self._user_messenger = user_messenger

    def emit(self, record: LogRecord) -> None:
        msg = self.format(record)
        self._user_messenger.publish(msg)
