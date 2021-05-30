import math
import time
from typing import List
from Solvers.Greedy import GreedySolver
from utils.Instance import Instance
from utils.JobNumbers import JobNumbers
from utils.RessourceOrder import RessourceOrder
from utils.Result import Result
from utils.Schedule import Schedule


class Descent:

    @staticmethod
    def sol_gen_voisins(bloc, schedule: Schedule, instance: Instance):

        m = instance.machine(task=bloc[0])
        solutions = []
        neighbors = []

        neighb_1 = []
        neighb_1.extend(bloc)
        neighb_1[1], neighb_1[0] = neighb_1[0], neighb_1[1]

        neighbors.append(neighb_1)
        new_sol = RessourceOrder(instance=schedule).tasksByMachine

        for e in new_sol[m]:
            if e.job == bloc[0].job:
                idx = new_sol[m].index(e)
                break
        new_sol[m][idx], new_sol[m][idx + 1] = new_sol[m][idx + 1], new_sol[m][idx]
        solutions.append(new_sol)

        if len(bloc) > 2:
            neighb_2 = []
            neighb_2.extend(bloc)
            neighb_2[-1], neighb_2[-2] = neighb_2[-2], neighb_2[-1]
            neighbors.append(neighb_2)

            new_sol = RessourceOrder(instance=schedule).tasksByMachine
            for e in new_sol[m]:
                if e.job == bloc[-1].job:
                    idx = new_sol[m].index(e)
                    break
            new_sol[m][idx - 1], new_sol[m][idx] = new_sol[m][idx], new_sol[m][idx - 1]
            solutions.append(new_sol)
        return solutions

    @staticmethod
    def blocks_of_critpath(crit_path, instance: Instance):
        previous_m = instance.machine(task=crit_path[0])
        block = [crit_path[0]]
        blocks = []

        for tsk in crit_path:
            if previous_m == instance.machine(task=tsk):
                block.append(tsk)
            else:
                blocks.append(block)
                block = [tsk]
            previous_m = instance.machine(task=tsk)
        blocks.append(block)
        res_blocks = []
        for b in blocks:
            if len(b) > 1:
                res_blocks.append(b)
        return res_blocks

    @staticmethod
    def neighbors(blocks, solution: Schedule, instance: Instance):

        neighbors = []
        for i in range(len(blocks)):
            b = blocks[i]
            new_sol = Descent.sol_gen_voisins(bloc=b, schedule=solution, instance=instance)
            neighbors.extend(new_sol)
            # neighbors.extend(Descent.sol_gen_voisins(bloc=blocks[i], schedule=solution, instance=instance))
        return neighbors

    @staticmethod
    def best_neigh(neighbors, instance: Instance):
        best_nei = math.inf
        for s in neighbors:
            job_nu = JobNumbers(instance=instance)
            jobs: List[int] = []
            for e in s:
                for a in e:
                    jobs.append(a.job)
            job_nu.jobs = jobs
            # print(len(jobs))
            job_nu.nextToSet = len(jobs)
            sc = job_nu.toSchedule()
            if sc.isValid():
                n_detail = sc.times
                n_eval = sc.makespan()
                if n_eval < best_nei:
                    best_nei = n_eval
                    best_sc = sc
                    assert best_sc.isValid()
            else:
                continue
        return best_sc

    @staticmethod
    def solve(instance: Instance, solution: Schedule = None, timeout: int = 8000):

        solution = GreedySolver.greedyEST_LRPT(instance=instance).schedule if solution is None else solution

        curr_sol = solution
        makespan = solution.makespan()
        path = solution.criticalPath()
        makespans = [makespan]

        start = time.time()
        while time.time() < start + timeout:

            blocks = Descent.blocks_of_critpath(crit_path=path, instance=instance)
            neighbors = Descent.neighbors(blocks=blocks, solution=curr_sol, instance=instance)

            best_neighbor = Descent.best_neigh(neighbors=neighbors, instance=instance)

            if best_neighbor.makespan() < makespan:
                makespan = best_neighbor.makespan()
                makespans.append(makespan)
                curr_sol = best_neighbor
                path = best_neighbor.criticalPath()
            else:
                break
        return Result(instance=instance, schedule=curr_sol)
