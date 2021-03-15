import time
from tabulate import tabulate
import argparse
from Solver import solve, solve_greedyLRPT, solve_greedySPT
from Greedy import GreedySolver
from Instance import Instance
from RessourceOrder import RessourceOrder

bestKnown = {"la01": 666,
             "la02": 655,
             "aaa1": 11,
             "ft06": 55,
             "ft10": 930,
             "ft20": 1165
             }


def getvalues(solve, instance, start):
    makespan = solve.schedule.makespan()
    best = bestKnown[instance]
    ecart = round(100 * (makespan - best) / best, 1)
    size = str(solve.instance.numJobs) + "x" + str(solve.instance.numTasks)
    runtime = time.time() - start

    return size, best, round(runtime, 2), makespan, ecart


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--instances', default=None, type=str)
    args = parser.parse_args()
    instances = args.instances.split('-')
    results = []

    print('LRPT Result : \n')
    for inst in instances:
        try:
            instance = Instance.fromFile('instances/' + inst)
        except(FileNotFoundError, IOError):
            print('File not found')
        start = time.time()
        solve_lrpt = solve_greedyLRPT(instance=instance)
        values_lrpt = getvalues(solve_lrpt, inst, start)

        results.append([inst, values_lrpt[0], values_lrpt[1], values_lrpt[2], values_lrpt[3], values_lrpt[4]])
    print(tabulate(results, headers=['instance', 'size', 'best', 'runtime', 'makespan', 'ecart']))

    results = []
    print('\n')
    print('SPT Result : \n')
    for inst in instances:
        try:
            instance = Instance.fromFile('instances/' + inst)
        except(FileNotFoundError, IOError):
            print('File not found')
        start = time.time()
        solve_lrpt = GreedySolver.greedySPT(instance=instance)
        values_lrpt = getvalues(solve_lrpt, inst, start)

        results.append([inst, values_lrpt[0], values_lrpt[1], values_lrpt[2], values_lrpt[3], values_lrpt[4]])
    print(tabulate(results, headers=['instance', 'size', 'best', 'runtime', 'makespan', 'ecart']))
