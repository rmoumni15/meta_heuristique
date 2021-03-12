import time
from tabulate import tabulate
from BasicSolver import solve
from Instance import Instance
from RessourceOrder import RessourceOrder

bestKnown = {"la01": 666,
            "la02": 655,
             "aaa1": 11
             }

if __name__ == '__main__':
    start = time.time()
    instance = Instance.fromFile('la01.txt')

    solve = solve(instance)
    makespan = solve.schedule.makespan()
    best = bestKnown['la01']
    ecart = round(100 * (makespan - best) / best,1)
    size = str(solve.instance.numJobs)+"x"+str(solve.instance.numTasks)
    runtime = time.time() - start

    print(tabulate([['la01', size, best, runtime, makespan, ecart]], headers=['instance', 'size','best', 'runtime', 'makespan', 'ecart']))
    ressord = RessourceOrder(solve.instance)
    #print(tabulate([['la01', size, best, runtime, ressord.toSchedule().makespan(), ecart]],
                 # headers=['instance', 'size', 'best', 'runtime', 'makespan', 'ecart']))

    scc = ressord.toSchedule()

    print(scc)







