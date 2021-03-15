from typing import List, Union

from Instance import Instance
import numpy as np

from Task import Task


class Schedule:

    def __init__(self, pb: Instance, times):
        self.pb = pb
        self.times = [[] for i in range(pb.numJobs)]

        for i in range(pb.numJobs):
            self.times[i] = times[i]
            if len(times[i]) - pb.numTasks > 0:
                siz = [0 for i in range(len(times[i]) - pb.numTasks)]
                self.times[i] += siz

    def startTime(self, job, task=None):
        if task is None:
            return self.startTime(job=task.job,task= task.task)
        else:
            return self.times[job][task]

    def isValid(self) -> bool:

        for j in range(self.pb.numJobs):
            for t in range(1, self.pb.numTasks):
                if self.startTime(j, t - 1) + self.pb.duration(j, t - 1) > self.startTime(j, t):
                    return False

            for t in range(self.pb.numTasks):
                if self.startTime(j, t) < 0:
                    return False

        for machine in range(self.pb.machines):
            for j1 in range(self.pb.numJobs):
                t1 = self.pb.task_with_machine(j1, machine)
                for j2 in range(j1 + 1, self.pb.numJobs):
                    t2 = self.pb.task_with_machine(j2, machine)

                    t1_first: bool = self.startTime(j1, t1) + self.pb.duration(j1, t1) <= self.startTime(j2, t2)
                    t2_first: bool = self.startTime(j2, t2) + self.pb.duration(j2, t2) <= self.startTime(j1, t1)

                    if t1_first is False and t2_first is False:
                        return False

        return True

    def makespan(self) -> int:
        max_ = -1

        for j in range(self.pb.numJobs):
            max_ = max(max_,
                      self.startTime(job=j, task=self.pb.numTasks - 1) + self.pb.duration(job=j, task=self.pb.numTasks - 1))
        return max_

    def endTime(self, task: Task) -> int:
        return self.startTime(task) + self.pb.duration(job=task.job,task= task.task)

    def isCriticalPath(self, path: List[Task]) -> bool:
        if self.startTime(path[0]) != 0:
            return False
        elif self.endTime(path[len(path) - 1]) != self.makespan():
            return False
        for i in range(len(path) - 1):
            if self.endTime(path[i]) != self.startTime(path[i + 1]):
                return False
        return True

    def criticalPath(self) -> List[Task]:
        ldd: Task
        tmp = [Task(job=j, task= self.pb.numTasks - 1) for j in range(self.pb.numJobs)]
        ldd = max(sorted(tmp, key=lambda x: self.endTime(task=x), reverse=True))
        assert self.endTime(task=ldd) == self.makespan()

        path: List[Task]
        path.insert(0, ldd)

        while self.startTime(task=path[0]) != 0:
            cur: Task = path[0]
            machine: int = self.pb.machine(job=cur.job,task= cur.task)

            latestPredecessor = None

            if cur.task > 0:
                predOnJob: Task = Task(job=cur.job,task= cur.task - 1)

                if self.endTime(task=predOnJob) == self.startTime(task=cur):
                    latestPredecessor = predOnJob
            if (latestPredecessor is None):
                latestPredecessor = [Task(j, self.pb.task_with_machine(job=j,wanted_machine= machine)) for j in range(self.pb.numJobs)]
                latestPredecessor = list(
                    filter(lambda elem: self.endTime(task=elem) == self.startTime(cur), latestPredecessor))
                latestPredecessor = latestPredecessor[0]

            assert latestPredecessor is not None and self.endTime(task=latestPredecessor) == self.startTime(task=cur)

            path.insert(0, latestPredecessor)
        assert self.isCriticalPath(path)
        return path
