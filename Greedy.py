from Solver import solve_greedyLRPT
from Instance import Instance
from JobNumbers import JobNumbers
from RessourceOrder import RessourceOrder

from Result import Result
from Schedule import Schedule
from Task import Task


class GreedySolver:

    @staticmethod
    def greedyLRPT_test(instance: Instance) -> Result:
        #############################
        duration = instance.durations.copy()
        sched = Schedule(pb=instance, times=instance.durations)
        return Result(instance=instance, schedule=RessourceOrder(sched).toSchedule(), cause=Result.ExitCause.Blocked)

    @staticmethod
    def greedySPT(instance: Instance) -> Result:
        dur = []
        job_sorted = [[Task(job=i, task=j) for i in range(instance.numMachines)] for j in
                      range(instance.numJobs)]
        for i in range(len(job_sorted)):
            job_sorted[i] = list(sorted(job_sorted[i], key=lambda x: instance.duration(task=x.job,job=x.task)))

        for elem in job_sorted:
            dur.append([instance.duration(task=e.job, job=e.task) for e in elem])
        sched = Schedule(pb=instance, times=list(sorted(dur)))
        return Result(instance=instance, schedule=RessourceOrder(sched).toSchedule(), cause=Result.ExitCause.Blocked)


