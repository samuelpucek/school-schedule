from itertools import product
from mip import Model, xsum, maximize, BINARY
import pandas as pd

import input

sub, lim = input.reader()


def schedule(subjetcs: dict, limits: list):
    """
    Core optimization procedure - mixed integer programming.

    :param subjetcs:
    :param limits:
    :return: schedules: dataframe containing optimal schedules for each class
    """

    # Constants
    C = len(limits)  # number of classes
    S = len(subjetcs)  # number of subjects
    D = 5  # days of week
    H = 5  # hours per day

    # Save as range
    S = range(S)
    D = range(D)
    H = range(H)

    # Initialize model
    model = Model('schedule')

    # Binary decision variables
    x = [[[model.add_var(var_type=BINARY, name='({},{},{})'.format(s + 1, d + 1, h + 1))
           for h in H] for d in D] for s in S]

    # Def objective function
    model.objective = maximize(xsum(x[s][d][h] for s in S for d in D for h in H))

    # Constraints
    for s in S:
        model += xsum(x[s][d][h] for h in H for d in D) == lim[0][s]

    for (d, h) in product(D, H):
        model += xsum(x[s][d][h] for s in S) <= 1

    for (s, d) in product(S, D):
        model += xsum(x[s][d][h] for h in H) <= 2  # TODO opravit

    # Optimization
    model.optimize()

    # Rozvrh
    df = pd.DataFrame(index=['Pon', 'Utr', 'Str', 'Stv', 'Pia'], columns=[1, 2, 3, 4, 5])

    for (s, d, h) in product(S, D, H):
        if x[s][d][h].x == 1:
            df.iloc[d, h] = subjetcs[s]

    df.fillna('   ', inplace=True)
    print(df)

    return x


def transformer(x):
    """
    Transform ugly optimization output into nice readable dataframe - schedule.

    :param x: binary decision variabe - class x subject x day x hour
    :return: schedule: dataframe
    """

    # Rozvrh
    df = pd.DataFrame(index=['Pon', 'Utr', 'Str', 'Stv', 'Pia'], columns=[1, 2, 3, 4, 5])

    for (s, d, h) in product(S, D, H):
        if x[s][d][h].x == 1:
            df.iloc[d, h] = subjetcs[s]

    df.fillna('   ', inplace=True)
    print(df)

# TODO: Prerob to na CLASS, do init daj S, H, D, dve metody: optimize, refacotr / translate

