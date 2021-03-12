from enum import Enum

from Instance import Instance
from Schedule import Schedule


class Result:
    class ExitCause(Enum):
        Timeout = 1
        ProvedOptimal = 2
        Blocked = 3

    def __init__(self, instance: Instance, schedule: Schedule, cause: ExitCause):
        self.instance = instance
        self.schedule = schedule
        self.cause = cause
