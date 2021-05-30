class Task:

    def __init__(self, job: int, task: int):
        self.job = job
        self.task = task

    def equals(self, o) -> bool:
        if self == o:
            return True
        if o is None or self.__class__.__name__ != o.__class__.__name__:
            return False

    def toString(self) -> str:

        return "(" + str(self.job) + "," + str(self.task) + ")"

    def __hash__(self) -> int:
        return super().__hash__()
