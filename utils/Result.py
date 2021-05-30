from utils.Instance import Instance
from utils.Schedule import Schedule


class Result:

    def __init__(self, instance: Instance, schedule: Schedule):
        self.instance = instance
        self.schedule = schedule
