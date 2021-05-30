import time
import copy

from Solvers.Greedy import GreedySolver
from utils.Instance import Instance
import math
from utils.JobNumbers import JobNumbers
from utils.RessourceOrder import RessourceOrder
from utils.Result import Result
from utils.Schedule import Schedule


class TabouSolver:

    @staticmethod
    def voisina_bloc_taboo(bloc, instance: Instance, schedule: Schedule):

        m = instance.machine(job=bloc[0].job, task=bloc[0].task)
        sols = []
        neighbors = []
        forbidden = []

        neighbor1 = copy.copy(bloc)
        forbidden.append((neighbor1[0].job, neighbor1[1].job))
        neighbor1[1], neighbor1[0] = neighbor1[0], neighbor1[1]
        neighbors.append(neighbor1)
        sol = RessourceOrder(instance=schedule).tasksByMachine
        for e in sol[m]:
            if e.job == bloc[0].job and e.task == bloc[0].task:
                i = sol[m].index(e)
                break
        sol[m][i], sol[m][i + 1] = sol[m][i + 1], sol[m][i]
        sols.append(sol)
        if len(bloc) > 2:
            neighbor2 = copy.copy(bloc)
            forbidden.append((neighbor2[-2].job, neighbor2[-1].job))
            neighbor2[-1], neighbor2[-2] = neighbor2[-2], neighbor2[-1]
            neighbors.append(neighbor2)

            sol = RessourceOrder(instance=schedule).tasksByMachine
            for e in sol[m]:
                if e.job == bloc[-1].job and e.task == bloc[-1].task:
                    i = sol[m].index(e)
                    break
            sol[m][i - 1], sol[m][i] = sol[m][i], sol[m][i - 1]
            sols.append(sol)
        return neighbors, sols, forbidden

    @staticmethod
    def extractblockCriticPath(critiques, instance: Instance):
        blocks, block = [], [critiques[0]]

        previous_m = instance.machine(task=critiques[0])

        for i in range(1, len(critiques)):
            job, tsk = critiques[i].job, critiques[i].task
            if previous_m == instance.machine(task=critiques[i]):
                block.append(critiques[i])
            else:
                blocks.append(block)
                block = [critiques[i]]
            previous_m = instance.machine(job=job, task=tsk)
        blocks.append(block)
        res = []
        for element in blocks:
            res.append(element) if len(element) > 1 else None

        return res

    @staticmethod
    def solve(instance: Instance, cur_sol: Schedule = None,  tabouperiod=5, timeout: int = 60, maxiter: int = 5):
        cur_sol = GreedySolver.greedyEST_LRPT(instance=instance).schedule if cur_sol is None else cur_sol
        best_makespan = cur_sol.makespan()
        current_makespan = best_makespan
        curr_sc = cur_sol
        best_sc = curr_sc
        critiques = cur_sol.criticalPath()
        list_makespan = [best_makespan]

        listes_taboo = [[[0] * instance.numJobs] * instance.numJobs] * instance.numTasks
        start = time.time()
        it = 0

        while (time.time() < start + timeout and it < maxiter):

            it += 1
            blocks = TabouSolver.extractblockCriticPath(critiques=critiques, instance=instance)

            best_voisin = math.inf

            for i in range(len(blocks)):
                b = blocks[i]
                m = instance.machine(task=b[0])
                liste_voisins, new_sols, liste_interdit = TabouSolver.voisina_bloc_taboo(bloc=b, instance=instance,
                                                                                         schedule=cur_sol)

                for j in range(len(liste_voisins)):

                    if listes_taboo[m][liste_interdit[j][1]][liste_interdit[j][0]] < it:
                        job_nu = JobNumbers(instance=instance)
                        jobs = []
                        for elem in liste_voisins[j]:
                            jobs.append(elem.job)
                        job_nu.jobs = jobs
                        new_sc = job_nu.toSchedule()
                        new_sol = new_sols[j]
                        new_eval = new_sc.makespan()
                        if new_sc.isValid():
                            if new_eval < best_voisin:
                                best_voisin = new_eval
                                best_voisin_sol = new_sol
                                best_sc = new_sc
                                interdit = liste_interdit[j]
                                best_m = m

                                listes_taboo[best_m][interdit[0]][interdit[1]] = it + tabouperiod

                                current_makespan = best_voisin
                                cur_sol = best_voisin_sol
                                curr_sc = new_sc
                                list_makespan.append(current_makespan)

            if curr_sc.isValid():
                if current_makespan < best_makespan:
                    best_sc = curr_sc

            return Result(instance=instance, schedule=best_sc)
