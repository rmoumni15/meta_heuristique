from typing import List

from utils.Instance import Instance
from utils.JobNumbers import JobNumbers

from utils.Result import Result
from utils.Task import Task


class GreedySolver:

    @staticmethod
    def greedyLRPT(instance: Instance) -> Result:

        machines_daterelease = [0 for _ in range(instance.numMachines)]
        tasks = [Task(job=job, task=0) for job in range(instance.numJobs)]
        remaining_time = [[-1 for _ in range(instance.numTasks)] for _ in range(instance.numJobs)]

        sol = JobNumbers(instance=instance)

        def best_tsk(tasks: List[Task]) -> Task:

            task_1 = tasks[0]

            for i in range(len(tasks)):
                curr_tsk = tasks[i]

                if remaining_time[curr_tsk.job][curr_tsk.task] == -1:
                    remaining_time[curr_tsk.job][curr_tsk.task] = 0

                    for t in range(curr_tsk.task, instance.numTasks):
                        remaining_time[curr_tsk.job][curr_tsk.task] += instance.duration(task=t,
                                                                                         job=curr_tsk.job)
                if remaining_time[task_1.job][task_1.task] < remaining_time[curr_tsk.job][curr_tsk.task]:
                    task_1 = curr_tsk
            return task_1

        while len(tasks) > 0:
            selected_tsk: Task = best_tsk(tasks)
            sol.jobs[sol.nextToSet] = selected_tsk.job
            sol.nextToSet = sol.nextToSet + 1

            machines_daterelease[instance.machine(task=selected_tsk)] += instance.duration(task=selected_tsk)
            tasks.remove(selected_tsk)
            if selected_tsk.task < instance.numTasks - 1:
                tasks.append(Task(job=selected_tsk.job, task=selected_tsk.task + 1))
        return Result(instance=instance, schedule=sol.toSchedule())

    @staticmethod
    def greedySPT(instance: Instance) -> Result:

        sol: JobNumbers = JobNumbers(instance=instance)
        tasks = [Task(job=job, task=0) for job in range(instance.numJobs)]
        machine_daterelease = [0 for _ in range(instance.numMachines)]

        def best_tsk(tasks: List[Task]) -> Task:

            tasks_1 = tasks[0]

            for i in range(len(tasks)):
                curr_tsk: Task = tasks[i]

                if instance.duration(task=curr_tsk) < instance.duration(task=tasks_1):
                    tasks_1 = curr_tsk
            return tasks_1

        while len(tasks) > 0:
            selected_tsk: Task = best_tsk(tasks=tasks)

            sol.jobs[sol.nextToSet] = selected_tsk.job
            sol.nextToSet += 1

            machine_daterelease[instance.machine(task=selected_tsk)] += instance.duration(task=selected_tsk)
            tasks.remove(selected_tsk)

            if selected_tsk.task < instance.numTasks - 1:
                tasks.append(Task(job=selected_tsk.job, task=selected_tsk.task + 1))

        return Result(instance=instance, schedule=sol.toSchedule())

    @staticmethod
    def greedyEST_LRPT(instance: Instance):

        machines_daterelease = [0 for _ in range(instance.numMachines)]
        tasks = [Task(job=job, task=0) for job in range(instance.numJobs)]
        remaining_time = [[-1 for _ in range(instance.numTasks)] for _ in range(instance.numJobs)]
        sol: JobNumbers = JobNumbers(instance=instance)

        def best_tsk(tasks: List[Task]) -> Task:
            task_1: Task = tasks[0]

            for i in range(len(tasks)):
                curr_tsk = tasks[i]
                if remaining_time[curr_tsk.job][curr_tsk.task] == -1:
                    remaining_time[curr_tsk.job][curr_tsk.task] = 0
                    for task in range(curr_tsk.task, instance.numTasks):
                        remaining_time[curr_tsk.job][curr_tsk.task] += instance.duration(job=curr_tsk.job,
                                                                                                 task=task)
                if machines_daterelease[instance.machine(task=task_1)] > machines_daterelease[
                    instance.machine(task=curr_tsk)]:
                    if remaining_time[task_1.job][task_1.task] < remaining_time[curr_tsk.job][curr_tsk.task]:
                        task_1 = curr_tsk
            return task_1

        while len(tasks) > 0:
            selected_tsk: Task = best_tsk(tasks)
            sol.jobs[sol.nextToSet] = selected_tsk.job
            sol.nextToSet += 1
            machines_daterelease[instance.machine(task=selected_tsk)] += instance.duration(task=selected_tsk)

            tasks.remove(selected_tsk)
            if selected_tsk.task < instance.numTasks - 1:
                tasks.append(Task(job=selected_tsk.job, task=selected_tsk.task + 1))

        return Result(instance=instance, schedule=sol.toSchedule())

    @staticmethod
    def greedyEST_SPT(instance: Instance):

        machine_daterelease = [0 for _ in range(instance.numMachines)]
        tasks = [Task(job=job, task=0) for job in range(instance.numJobs)]
        sol: JobNumbers = JobNumbers(instance=instance)

        def best_tsk(tasks: List[Task]) -> Task:

            task_1 = tasks[0]

            for i in range(len(tasks)):
                current_task = tasks[i]
                if machine_daterelease[instance.machine(task=task_1)] > machine_daterelease[
                    instance.machine(task=current_task)]:
                    if instance.duration(task=task_1) > instance.duration(task=current_task):
                        task_1 = current_task
            return task_1


        while len(tasks) > 0:
            selected_tsk = best_tsk(tasks)

            sol.jobs[sol.nextToSet] = selected_tsk.job
            sol.nextToSet += 1

            machine_daterelease[instance.machine(task=selected_tsk)] += instance.duration(task=selected_tsk)
            tasks.remove(selected_tsk)
            if selected_tsk.task < instance.numTasks - 1:
                tasks.append(Task(job=selected_tsk.job, task=selected_tsk.task + 1))

        return Result(instance=instance, schedule=sol.toSchedule())
