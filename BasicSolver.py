from typing import List

from Instance import Instance
from JobNumbers import JobNumbers
from Result import Result
from Task import Task


def solve(instance: Instance, deadline: float = 0) -> Result:
    sol: JobNumbers = JobNumbers(instance)
    # print(sol.jobs)
    for i in range(instance.numTasks):
        for j in range(instance.numJobs):
            # print(instance.numJobs)
            sol.jobs[sol.nextToSet] = j
            sol.nextToSet += 1

    # print(sol.jobs)
    return Result(instance, sol.toSchedule(), Result.ExitCause.Blocked)


def sum_process(instance: Instance, jobs_to_sort: List[Task]):
    durations = [instance.duration(task= jobs_to_sort[0])]
    duration = instance.duration(task=jobs_to_sort[0])

    for task in jobs_to_sort:

        if task is not duration:
            duration += instance.duration(task= task)
            durations.append(duration)
        else:
            pass
    return min(durations)


def solve_greedyLRPT(instance: Instance, deadline: float = 0) -> Result:
    sol: JobNumbers = JobNumbers(instance)
    job_sorted = [[Task(job=i, task=j) for i in range(instance.numJobs)] for j in
                  range(instance.numMachines)]
    for i in range(len(job_sorted)):
        job_sorted[i] = list(sorted(job_sorted[i], key=lambda x: instance.duration(task=x), reverse=True))
    job_sorted_ = [item.job for sublist in job_sorted for item in sublist]
    # print(job_sorted_)
    sol.jobs = job_sorted_
    sol.nextToSet = len(sol.jobs)

    return Result(instance, sol.toSchedule(), Result.ExitCause.Blocked)

def solve_greedySPT(instance: Instance, deadline: float = 0) -> Result:
    sol: JobNumbers = JobNumbers(instance)
    job_sorted = [[Task(job=i, task=j) for i in range(instance.numJobs)] for j in
                  range(instance.numMachines)]
    for i in range(len(job_sorted)):
        job_sorted[i] = list(sorted(job_sorted[i], key=lambda x: instance.duration(task=x)))
    job_sorted_ = [item.job for sublist in job_sorted for item in sublist]
    # print(job_sorted_)
    sol.jobs = job_sorted_
    sch = sol.toSchedule()
    for i in range(len(job_sorted)):
        job_sorted[i] = list(sorted(job_sorted[i], key=lambda x: sch.endTime(task=x)))
    job_sorted_ = [item.job for sublist in job_sorted for item in sublist]
    # print(job_sorted_)
    sol.jobs = job_sorted_

    sol.nextToSet = len(sol.jobs)

    return Result(instance, sol.toSchedule(), Result.ExitCause.Blocked)
