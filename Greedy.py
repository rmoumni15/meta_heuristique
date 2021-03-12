from Instance import Instance
from JobNumbers import JobNumbers
from RessourceOrder import RessourceOrder
from Result import Result

class GreedySolver:

    @staticmethod
    def greedySPT(instance: Instance) -> Result:
        sol: JobNumbers = JobNumbers(instance = instance)
        ress_ord: RessourceOrder = RessourceOrder(instance= instance)

        SortOperations = ress_ord.tasksByMachine.copy()
        for tasks in SortOperations:
            tasks = sorted(tasks, key=lambda x: ress_ord.instance.duration(task=x))


        for tasks in SortOperations:








        for i in range(ress_ord.instance.numJobs):
            for j in range(ress_ord.instance.numTasks):







    @staticmethod
    def greedyLPT(instance: Instance) -> Result:





