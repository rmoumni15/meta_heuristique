import time
from tqdm import tqdm
import argparse
import pandas as pd
from datetime import datetime
from Solvers.Tabou import TabouSolver
from Solvers.Descent import Descent
from Solvers.Greedy import GreedySolver
from utils.Instance import Instance
pd.set_option('display.max_columns', None)

BEST_KNOWN = {"aaa1": 11,
              "abz5": 1234,
              "abz6": 943,
              "abz7": 656,
              "abz8": 665,
              "abz9": 679,
              "ft06": 55,
              "ft10": 930,
              "ft20": 1165,
              "la01": 666,
              "la02": 655,
              "la03": 597,
              "la04": 590,
              "la05": 593,
              "la06": 926,
              "la07": 890,
              "la08": 863,
              "la09": 951,
              "la10": 958,
              "la11": 1222,
              "la12": 1039,
              "la13": 1150,
              "la14": 1292,
              "la15": 1207,
              "la16": 945,
              "la17": 784,
              "la18": 848,
              "la19": 842,
              "la20": 902,
              "la21": 1046,
              "la22": 927,
              "la23": 1032,
              "la24": 935,
              "la25": 977,
              "la26": 1218,
              "la27": 1235,
              "la28": 1216,
              "la29": 1152,
              "la30": 1355,
              "la31": 1784,
              "la32": 1850,
              "la33": 1719,
              "la34": 1721,
              "la35": 1888,
              "la36": 1268,
              "la37": 1397,
              "la38": 1196,
              "la39": 1233,
              "la40": 1222,
              "orb01": 1059,
              "orb02": 888,
              "orb03": 1005,
              "orb04": 1005,
              "orb05": 887,
              "orb06": 1010,
              "orb07": 397,
              "orb08": 899,
              "orb09": 934,
              "orb10": 944,
              "swv01": 1407,
              "swv02": 1475,
              "swv03": 1398,
              "swv04": 1474,
              "swv05": 1424,
              "swv06": 1678,
              "swv07": 1600,
              "swv08": 1763,
              "swv09": 1661,
              "swv10": 1767,
              "swv11": 2991,
              "swv12": 3003,
              "swv13": 3104,
              "swv14": 2968,
              "swv15": 2904,
              "swv16": 2924,
              "swv17": 2794,
              "swv18": 2852,
              "swv19": 2843,
              "swv20": 2823,
              "yn1": 885,
              "yn2": 909,
              "yn3": 892,
              "yn4": 968,
              "ta01": 1231,
              "ta02": 1244,
              "ta03": 1218,
              "ta04": 1175,
              "ta05": 1224,
              "ta06": 1238,
              "ta07": 1227,
              "ta08": 1217,
              "ta09": 1274,
              "ta10": 1241,
              "ta11": 1361,
              "ta12": 1367,
              "ta13": 1342,
              "ta14": 1345,
              "ta15": 1340,
              "ta16": 1360,
              "ta17": 1462,
              "ta18": 1396,
              "ta19": 1335,
              "ta20": 1351,
              "ta21": 1644,
              "ta22": 1600,
              "ta23": 1557,
              "ta24": 1647,
              "ta25": 1595,
              "ta26": 1645,
              "ta27": 1680,
              "ta28": 1614,
              "ta29": 1635,
              "ta30": 1584,
              "ta31": 1764,
              "ta32": 1796,
              "ta33": 1793,
              "ta34": 1829,
              "ta35": 2007,
              "ta36": 1819,
              "ta37": 1778,
              "ta38": 1673,
              "ta39": 1795,
              "ta40": 1674,
              "ta41": 2018,
              "ta42": 1956,
              "ta43": 1859,
              "ta44": 1984,
              "ta45": 2000,
              "ta46": 2021,
              "ta47": 1903,
              "ta48": 1952,
              "ta49": 1968,
              "ta50": 1926,
              "ta51": 2760,
              "ta52": 2756,
              "ta53": 2717,
              "ta54": 2839,
              "ta55": 2679,
              "ta56": 2781,
              "ta57": 2943,
              "ta58": 2885,
              "ta59": 2655,
              "ta60": 2723,
              "ta61": 2868,
              "ta62": 2869,
              "ta63": 2755,
              "ta64": 2702,
              "ta65": 2725,
              "ta66": 2845,
              "ta67": 2825,
              "ta68": 2784,
              "ta69": 3071,
              "ta70": 2995}

DICT_GREEDY = {
    'SPT': GreedySolver.greedySPT,
    'LRPT': GreedySolver.greedyLRPT,
    'EST_SPT': GreedySolver.greedyEST_SPT,
    'EST_LRPT': GreedySolver.greedyEST_LRPT
}


def getvalues(solve, instance, start):
    makespan = solve.schedule.makespan()
    best = BEST_KNOWN[instance]
    ecart = round(100 * (makespan - best) / best, 1)
    size = str(solve.instance.numJobs) + "x" + str(solve.instance.numTasks)
    runtime = time.time() - start

    return size, best, round(runtime, 2), makespan, ecart


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--Instances', nargs='+', type=str, default=["ft20"], help="Liste des instances a executer")
    parser.add_argument('--Descent', type=bool, default=False, help="Executer la methode descente")
    parser.add_argument('--Taboo', type=bool, default=False, help="Execute la methode tabou")
    parser.add_argument('--stop', type=int, default=3600, help="Le temps limite pour les methodes descente et tabou")
    parser.add_argument('--maxiter', type=int, default=50, help="Nombre maximum d'iteration (methode tabou)")
    parser.add_argument('--taboo_period', type=int, default=10,
                        help="le nombre d'it??rations ou la permutation inverse est interdite pour la m??thode tabou")
    parser.add_argument('--export', type=bool, default=True, help="Exporter les r??sultats dans un fichier Excel")

    args = parser.parse_args()

    # print(f" Instances : {args.instance}")
    # print(f" Descent : {args.descent}")
    # print(f" Taboo : {args.taboo}")

    index = ['instance', 'size', 'best', 'runtime', 'makespan', 'ecart']
    pbar = tqdm(args.Instances)
    results = {}
    for inst in pbar:
        pbar.set_description("Processing %s" % inst)
        try:
            instance = Instance.fromFile('instances/' + inst)
        except(FileNotFoundError, IOError):
            print('File not found')
        for solver in DICT_GREEDY.keys():
            start = time.time()
            sol = DICT_GREEDY[solver](instance=instance)
            values_lrpt = getvalues(sol, inst, start)
            results[solver + '_' + inst] = [inst, values_lrpt[0], values_lrpt[1], values_lrpt[2], values_lrpt[3],
                                            values_lrpt[4]]

        if args.Descent:
            start = time.time()
            sol = Descent.solve(instance=instance, timeout=args.stop)
            values_descent = getvalues(sol, inst, start)
            results['descent' + '_' + inst] = [inst, values_descent[0], values_descent[1], values_descent[2],
                                               values_descent[3], values_descent[4]]

        if args.Taboo:
            start = time.time()
            sol = TabouSolver.solve(instance=instance, timeout=args.stop, tabouperiod=args.taboo_period,
                                    maxiter=args.maxiter)
            values_taboo = getvalues(sol, inst, start)
            results['tabou' + '_' + inst] = [inst, values_taboo[0], values_taboo[1], values_taboo[2], values_taboo[3],
                                             values_taboo[4]]

    results_df = pd.DataFrame(results, index=index)

    results_df.to_excel(
        'Excel_Export/Results_Export_' + datetime.today().strftime('%Y-%m-%d') + '.xlsx') if args.export else None

    print(results_df)
