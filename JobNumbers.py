from typing import List, Union

from Instance import Instance
from Schedule import Schedule
from Task import Task


class JobNumbers:
    nextToSet: int = 0

    def __init__(self, instance: Union[Instance, Schedule]):
        if type(instance).__name__ == 'Instance':
            self.instance = instance
            self.jobs: List[int] = [-1 for i in range(instance.numJobs * instance.numMachines)]

        elif type(instance).__name__ == 'Schedule':
            self.instance = instance.pb

            self.jobs: List[int] = [0 for i in range(self.instance.numJobs * self.instance.numTasks)]

            nextOnJob: List[int] = [0 for i in range(self.instance.numJobs)]
            while any(elem < self.instance.numTasks for elem in nextOnJob):
                next: Task

                tmp: List[Task] = [Task(j, nextOnJob[j]) for j in range(self.instance.numJobs)]

                tmp = list(filter(lambda elem: elem.task < self.instance.numTasks, tmp))

                next = min(sorted(tmp, key=lambda x: instance.startTime(x.job, x.task)))

                self.nextToSet += 1
                self.jobs[self.nextToSet] = next.job
                nextOnJob[next.job] += 1

    def toSchedule(self) -> Schedule:

        nextFreeTimeRessource: List[int] = [0 for i in range(self.instance.numMachines)]

        nextTask: List[int] = [0 for i in range(self.instance.numJobs)]

        startTimes: List[List[int]] = [[0 for i in range(self.instance.numTasks)] for i in range(self.instance.numJobs)]

        #print("machines : ", len(self.instance.machines[0]))
        for job in self.jobs:
            task: int = nextTask[job]
            machine: int = self.instance.machine(job=job, task=task)
            if task == 0:
                est = 0
            else:
                est = startTimes[job][task - 1] + self.instance.duration(job = job, task = task - 1)
            est = max(est, nextFreeTimeRessource[machine])

            startTimes[job][task] = est
            nextFreeTimeRessource[machine] = est + self.instance.duration(job = job, task = task)
            nextTask[job] = task + 1

        return Schedule(self.instance, startTimes)

    def toString(self) -> str:
        return ''.join(str(e) for e in self.jobs[:self.nextToSet])
