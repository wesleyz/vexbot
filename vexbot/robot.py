import sys as _sys
import logging as _logging

from vexbot.messaging import Messaging as _Messaging
from vexbot.subprocess_manager import SubprocessManager
from vexbot.scheduler import Scheduler as _Scheduler
from vexbot.observers import BotObserver as _BotObserver


class Robot:
    def __init__(self,
                 messaging: _Messaging=None,
                 command_observer: _BotObserver=None,
                 subprocess_manager=None):

        self.messaging = messaging
        self.scheduler = _Scheduler(messaging)
        self.subprocess_manager = subprocess_manager or SubprocessManager()

        if command_observer is None:
            command_observer = _BotObserver(messaging,
                                            self.subprocess_manager)

        self.command_observer = command_observer
        self.scheduler.command.subscribe(self.command_observer)

        log_name = __name__ if __name__ != '__main__' else 'vexbot.robot'
        self._logger = _logging.getLogger(log_name)

    def run(self):
        if self.messaging is None:
            e = ' No `messaging` provided to `Robot` on initialization'
            self._logger.error(e)
            _sys.exit(1)

        self.messaging.start()
        # NOTE: blocking call
        self.scheduler.run()
