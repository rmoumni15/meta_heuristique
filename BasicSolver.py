from Instance import Instance
from JobNumbers import JobNumbers
from Result import Result


def solve(instance: Instance, deadline: float = 0) -> Result:
    sol: JobNumbers = JobNumbers(instance)
    #print(sol.jobs)
    for i in range(instance.numTasks):
        for j in range(instance.numJobs):
            #print(instance.numJobs)
            sol.jobs[sol.nextToSet] = j
            sol.nextToSet += 1

    #print(sol.jobs)
    return Result(instance, sol.toSchedule(), Result.ExitCause.Blocked)
