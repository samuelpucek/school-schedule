from itertools import product
from mip import Model, xsum, maximize, BINARY
import pandas as pd


class Scheduler:
    """
    Optimization and creating schedules.
    """

    def __init__(self, subjects: dict, limits: list, classes: list):
        """
        Constructor - extract and save constants.
        Save subjects dictionary, limits list and list of classes as local variables.

        Constants
        ---------
        C: number of classes
        S: number of subjects
        D: days of week
        H: hours per day
        """
        # Constants
        self.no_classes = len(limits)  # number of classes
        self.no_subjects = len(subjects)  # number of subjects
        self.no_days = 5  # days of week
        self.no_hours = 6  # hours per day

        # Save as range
        self.C = range(self.no_classes)
        self.S = range(self.no_subjects)
        self.D = range(self.no_days)
        self.H = range(self.no_hours)

        # Save subjects and limits as local variables
        self.sub = subjects
        self.lim = limits
        self.classes = classes

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
        x = [[[[model.add_var(var_type=BINARY,
                              name='class:{}, subj:{}, day:{}, hour:{})'.format(c + 1, s + 1, d + 1, h + 1))
                for h in self.H] for d in self.D] for s in self.S] for c in self.C]

        # Objective function
        model.objective = maximize(xsum(x[c][s][d][h] for c in self.C for s in self.S for d in self.D for h in self.H))

        # Constraints
        # Satisfy initial conditions
        for (c, s) in product(self.C, self.S):
            model += xsum(x[c][s][d][h] for h in self.H for d in self.D) == self.lim[c][s]

        # Max one lesson in one slot
        for (c, d, h) in product(self.C, self.D, self.H):
            model += xsum(x[c][s][d][h] for s in self.S) <= 1

        # Max limit for the same subject in the same day
        daily_limits = [[i // 5 + 1 for i in self.lim[c]] for c in self.C]
        for (c, s, d) in product(self.C, self.S, self.D):
            model += xsum(x[c][s][d][h] for h in self.H) <= daily_limits[c][s]
        # TODO: Celkom OK, 5x za tyzden len limit 2 (chyba), dvojhodinovky VYV (pripadne ine predmety) dorobit

        # Max hours per day + no empty slots
        for c in self.C:
            if sum(self.lim[c]) <= 25:  # Max 25 hours per week
                for d in self.D:  # Deny 6. hour
                    model += xsum(x[c][s][d][h] for s in self.S for h in range(5, self.no_hours)) == 0
                for d in self.D:  # No empty slots
                    model += xsum(x[c][s][d][h] for s in self.S for h in range(4)) == 4

            elif sum(self.lim[c]) <= 30:  # Max 30 hours per week
                for d in self.D:  # No empty slots
                    model += xsum(x[c][s][d][h] for s in self.S for h in range(5)) == 5
            # TODO: Sprav obecnejsie, ako kumulativny sucet, nemusis to pisat zvlast pre max 25 a max 30

        # Optimization
        model.optimize()

        # TODO: Pridaj dalsie triedy
        # TODO: Pridaj ucitelov (? uvazky)

        return x

    def _printer(self, x):
        """
        Transform optimal solution (binary decision variables) and create nice human readable schedules.
        """
        cnt = 0

        # Schedules
        for c in self.C:
            list_of_hours = [h + 1 for h in self.H]
            df = pd.DataFrame(index=['Pon', 'Utr', 'Str', 'Stv', 'Pia'], columns=list_of_hours)
            for (s, d, h) in product(self.S, self.D, self.H):
                if x[c][s][d][h].x == 1:
                    df.iloc[d, h] = self.sub[s]
                    cnt = cnt + 1

            df.fillna('   ', inplace=True)

            # Print out
            print('        ** {} trieda **'.format(self.classes[c]))
            print(df)
            print()
        print('cnt: {}'.format(cnt))
        return x
