from BasicSolver import solve_greedyLRPT
from Instance import Instance
from JobNumbers import JobNumbers
from RessourceOrder import RessourceOrder

from Result import Result
from Task import Task


class GreedySolver:

    @staticmethod
    def greedySPT(instance: Instance):
        #############################
        ress_ord: RessourceOrder = RessourceOrder(instance=instance)
        #############################
        StartTimes = [[] for _ in range(instance.numJobs)]
        ress_ord.tasksByMachine = [[Task(job=i, task=j) for i in range(instance.numJobs)] for j in range(instance.numMachines)]

        SortOperations = instance.machines.copy()
        for i in range(len(ress_ord.tasksByMachine)):
            ress_ord.tasksByMachine[i] = list(sorted(ress_ord.tasksByMachine[i], key=lambda x: instance.duration(task=x)))
        return ress_ord

    @staticmethod
    def greedyLPT(instance: Instance) -> Result:
        return None


instance = Instance.fromFile('la01.txt')
test = GreedySolver.greedySPT(instance)

print(test.toSchedule())

'''
for elem in test.tasksByMachine:
    for e in elem:
        print('--'+str(instance.duration(task=e))+'--')
    print('####################"')
'''