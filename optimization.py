from itertools import product
from mip import Model, xsum, maximize, BINARY
import pandas as pd


class Scheduler:
    """
    Optimization and creating schedules.
    """

    def __init__(self, subjects: dict, limits: list):
        """
        Constructor - extract and save constants.
        Save subjects dictionary and limits list as local variables.

        Constants
        ---------
        C: number of classes
        S: number of subjects
        D: days of week
        H: hours per day
        """
        # Constants
        self.C = len(limits)  # number of classes
        self.S = len(subjects)  # number of subjects
        self.D = 5  # days of week
        self.H = 5  # hours per day

        # Save as range
        self.C = range(self.C)
        self.S = range(self.S)
        self.D = range(self.D)
        self.H = range(self.H)

        # Save subjects and limits as local variables
        self.sub = subjects
        self.lim = limits

    def schedule(self):
        """
        Keynote.
        """
        optimal_x = self._optimize()
        self._printer(optimal_x)
        return

    def _optimize(self):
        """
        Core optimization procedure - mixed integer programming.
        """

        # Initialize model
        model = Model('schedule')

        # Binary decision variables
        x = [[[model.add_var(var_type=BINARY, name='({},{},{})'.format(s + 1, d + 1, h + 1))
               for h in self.H] for d in self.D] for s in self.S]

        # Def objective function
        model.objective = maximize(xsum(x[s][d][h] for s in self.S for d in self.D for h in self.H))

        # Constraints
        for s in self.S:
            model += xsum(x[s][d][h] for h in self.H for d in self.D) == self.lim[0][s]

        for (d, h) in product(self.D, self.H):
            model += xsum(x[s][d][h] for s in self.S) <= 1

        for (s, d) in product(self.S, self.D):
            model += xsum(x[s][d][h] for h in self.H) <= 2  # TODO opravit

        # Optimization
        model.optimize()

        # TODO: ako spravne handlovat premenne medzi metodami? Kukni sa do Buresa aka STB
        return x

    def _printer(self, x):
        """
        Transform optimal solution (binary decision variables) and create nice human readable schedules.
        """

        # Rozvrh
        df = pd.DataFrame(index=['Pon', 'Utr', 'Str', 'Stv', 'Pia'], columns=[1, 2, 3, 4, 5])

        for (s, d, h) in product(self.S, self.D, self.H):
            if x[s][d][h].x == 1:
                df.iloc[d, h] = self.sub[s]

        df.fillna('   ', inplace=True)
        print(df)

        return x

# TODO: Prerob to na CLASS, do init daj S, H, D, dve metody: optimize, refacotr / translate
