import time
from tabulate import tabulate
from BasicSolver import solve, solve_greedyLRPT
from Instance import Instance
from RessourceOrder import RessourceOrder

bestKnown = {"la01": 666,
            "la02": 655,
             "aaa1": 11
             }

if __name__ == '__main__':
    start = time.time()
    instance = Instance.fromFile('aaa1')

    solve = solve_greedyLRPT(instance)
    makespan = solve.schedule.makespan()
    best = bestKnown['aaa1']
    ecart = round(100 * (makespan - best) / best,1)
    size = str(solve.instance.numJobs)+"x"+str(solve.instance.numTasks)
    runtime = time.time() - start
    print(tabulate([['aaa1', size, best, runtime, makespan, ecart]], headers=['instance', 'size','best', 'runtime', 'makespan', 'ecart']))
    #ressord = RessourceOrder(solve.instance)
    #print(tabulate([['la01', size, best, runtime, ressord.toSchedule().makespan(), ecart]],
                 # headers=['instance', 'size', 'best', 'runtime', 'makespan', 'ecart']))

    print("\n")

    test= RessourceOrder(solve.schedule)
    print(test.toString())

    print("\n")

    print(test.toSchedule().makespan())









