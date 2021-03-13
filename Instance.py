class Instance:

    def __init__(self, numJobs, numTasks):
        self.numJobs = numJobs
        self.numTasks = numTasks
        self.numMachines = numTasks

        self.durations = [[0 for i in range(numTasks)] for j in range(numJobs)]
        self.machines = [[0 for i in range(numTasks)]for j in range(numJobs)]

    def duration(self, task, job=None) -> int:
        if job is None:
            return int(self.durations[task.job][task.task])
        else:
            return int(self.durations[job][task])

    def machine(self, task, job=None) -> int:
        if job is None:
            return int(self.machines[task.job][task.task])
        else:
            return int(self.machines[job][task])

    def task_with_machine(self, job, wanted_machine):
        for task in range(self.numTasks):
            if self.machine(job=job, task=task) == wanted_machine:
                return task
        print(f"No task targeting machine {wanted_machine} on job {job}")
        return None

    @staticmethod
    def fromFile(path):

        with open(path, "r") as f:
            text = f.readline().strip().split()
            num_jobs = int(text[0])
            num_tasks = int(text[1])
            inst = Instance(num_jobs, num_tasks)

            for i in range(num_jobs):
                line = f.readline().strip().split()
                line = iter(line)
                for j in range(num_tasks):
                    inst.machines[i][j] = next(line)
                    inst.durations[i][j] = next(line)

        return inst
