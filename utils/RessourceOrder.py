from typing import Union, Optional

from utils.Instance import Instance
from utils.Schedule import Schedule

from utils.Task import Task


class RessourceOrder:
    instance: Instance

    def __init__(self, instance: Union[Instance, Schedule]):
        if type(instance).__name__ == 'Instance':
            self.instance = instance
            self.tasksByMachine = [[None for i in range(instance.numJobs)] for j in range(instance.numMachines)]

            self.nextFreeSlot = [0 for i in range(instance.numMachines)]

        elif type(instance).__name__ == 'Schedule':
            self.instance = instance.pb
            pb = instance.pb

            self.tasksByMachine = [[] for i in range(pb.numMachines)]
            self.nextFreeSlot = [0 for i in range(self.instance.numMachines)]

            for m in range(pb.numMachines):
                machine = m

                self.tasksByMachine[m] = [Task(job=j, task=pb.task_with_machine(job=j, wanted_machine=machine)) for j in
                                          range(pb.numJobs)]
                self.tasksByMachine[m] = list(
                    sorted(self.tasksByMachine[m], key=lambda t: instance.startTime(job=t.job,  task=t.task)))

                self.nextFreeSlot[m] = self.instance.numJobs

    def toSchedule(self) -> Schedule:
        startTimes = [[0 for i in range(self.instance.numTasks)] for j in range(self.instance.numJobs)]

        nextToScheduleByJob = [0 for i in range(self.instance.numJobs)]

        nextToScheduleByMachine = [0 for i in range(self.instance.numMachines)]

        releaseTimeOfMachine = [0 for i in range(self.instance.numMachines)]

        while any(nextToScheduleByJob[elem] < self.instance.numTasks for elem in range(self.instance.numJobs)):

            schedulable: Optional[Task]

            tmp = list(filter(lambda x: nextToScheduleByMachine[x] < self.instance.numJobs,
                              list(range(self.instance.numMachines))))
            # print(tmp)
            tmp = [self.tasksByMachine[m][nextToScheduleByMachine[m]] for m in tmp]
            # print(tmp)
            tmp = list(filter(lambda task: task.task == nextToScheduleByJob[task.job], tmp))
            #print(tmp)
            schedulable = tmp[0] if tmp else None

            if schedulable:
                t: Task = schedulable
                machine: int = self.instance.machine(job=t.job, task=t.task)
                est: int
                if t.task == 0:
                    est = 0
                else:
                    est = startTimes[t.job][t.task - 1] + self.instance.duration(job=t.job, task=t.task - 1)
                est = max(est, releaseTimeOfMachine[self.instance.machine(task=t)])
                startTimes[t.job][t.task] = est

                nextToScheduleByJob[t.job] += 1
                nextToScheduleByMachine[machine] += 1

                releaseTimeOfMachine[machine] = est + self.instance.duration(job=t.job, task=t.task)
            else:
                return None

        return Schedule(self.instance, startTimes)

    def copy(self):
        return RessourceOrder(self.toSchedule())

    def toString(self) -> str:
        string = ""
        for m in range(self.instance.numMachines):
            string += 'Machine ' + str(m) + ' : '
            for j in range(self.instance.numJobs):
                string += str(self.tasksByMachine[m][j].toString()) + ' ; '
            string += "\n"
        return str(string)


