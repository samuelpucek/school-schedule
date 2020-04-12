from itertools import product
from mip import Model, xsum, maximize, BINARY
import pandas as pd
import datetime


class Scheduler:
    """
    Optimization and creating schedules.
    """

    def __init__(self, classes_names: dict, classes_restrictions: dict, teachers_names: dict,
                 teachers_restrictions: dict, subject_names: dict):
        # Constants
        self.no_classes = len(classes_restrictions)  # number of classes
        self.no_subjects = len(subject_names)  # number of subjects
        self.no_days = 5  # days of week
        self.no_hours = 6  # hours per day
        self.no_teachers = len(teachers_names)  # number of teachers

        # Save as range
        self.C = range(self.no_classes)
        self.S = range(self.no_subjects)
        self.T = range(self.no_teachers)
        self.D = range(self.no_days)
        self.H = range(self.no_hours)

        # Save subjects and limits as local variables
        self.sub = subject_names
        self.lim = classes_restrictions
        self.classes = classes_names
        self.teachers_restrictions = teachers_restrictions
        self.teachers_dict_reverse = teachers_names

    def schedule(self):
        """
        Keynote.
        """
        optimal_x = self._optimize
        self._classes_schedule_printer(optimal_x)
        self._teachers_schedule_printer(optimal_x)

        # self._file_printer(optimal_x)
        return

    @property
    def _optimize(self):
        """
        Core optimization procedure - mixed integer programming.
        """

        # Initialize model
        model = Model('schedule')

        # Binary decision variables
        x = [[[[[model.add_var(var_type=BINARY,
                               name='class:{}, subj:{}, teach:{}, day:{}, hour:{})'.format(c + 1, s + 1, t + 1, d + 1,
                                                                                           h + 1))
                 for h in self.H] for d in self.D] for t in self.T] for s in self.S] for c in self.C]

        # Objective function
        model.objective = maximize(
            xsum(x[c][s][t][d][h] for c in self.C for s in self.S for t in self.T for d in self.D for h in self.H))

        # Constraints
        # Satisfy initial conditions
        for (c, s) in product(self.C, self.S):
            model += xsum(x[c][s][t][d][h] for t in self.T for d in self.D for h in self.H) == self.lim[c][s]

        # Max one lesson per class per slot
        # Multiple teachers banned TODO: delene triedy nebudu fungovat
        for (c, d, h) in product(self.C, self.D, self.H):
            model += xsum(x[c][s][t][d][h] for s in self.S for t in self.T) <= 1

        # Teacher teaches max one lesson in one slot
        for (t, d, h) in product(self.T, self.D, self.H):
            model += xsum(x[c][s][t][d][h] for s, c in self.teachers_restrictions[t]) <= 1
            # sum only through classes and subjects teacher teach

        # Teachers restrictions, e.g.: Teacher1 teaches SJL in I.A
        for t in self.T:
            for s, c in self.teachers_restrictions[t]:
                model += xsum(x[c][s][t][d][h] for d in self.D for h in self.H) == self.lim[c][s]

        # Max limit for the same subject in the same day
        # TODO: Celkom OK, 5x za tyzden len limit 2 (chyba), dvojhodinovky VYV (pripadne ine predmety) dorobit
        daily_limits = [[i // 5 + 1 for i in self.lim[c]] for c in self.C]
        for (c, s, t, d) in product(self.C, self.S, self.T, self.D):
            model += xsum(x[c][s][t][d][h] for h in self.H) <= daily_limits[c][s]

        # Max hours per day + no empty slots
        for c in self.C:
            if sum(self.lim[c]) <= 25:  # Max 25 hours per week
                for d in self.D:  # Deny 6. hour
                    model += xsum(
                        x[c][s][t][d][h] for s in self.S for t in self.T for h in range(5, self.no_hours)) == 0
                for d in self.D:  # No empty slots
                    model += xsum(x[c][s][t][d][h] for s in self.S for t in self.T for h in range(4)) == 4

            elif sum(self.lim[c]) <= 30:  # Max 30 hours per week
                for d in self.D:  # No empty slots
                    model += xsum(x[c][s][t][d][h] for s in self.S for t in self.T for h in range(5)) == 5

        # Optimization
        model.optimize()

        return x

    def _classes_schedule_printer(self, x):
        """
        Transform optimal solution (binary decision variables) and create nice human readable schedules.
        """
        cnt = 0

        # Schedules
        for c in self.C:
            # for (c, t) in product(self.C, self.T):
            list_of_hours = [h + 1 for h in self.H]
            df = pd.DataFrame(index=['Pon', 'Utr', 'Str', 'Stv', 'Pia'], columns=list_of_hours)
            for (s, t, d, h) in product(self.S, self.T, self.D, self.H):
                # for (s, d, h) in product(self.S, self.D, self.H):
                if x[c][s][t][d][h].x == 1:
                    df.iloc[d, h] = self.sub[s]
                    cnt = cnt + 1

            df.fillna('   ', inplace=True)

            # Print out
            print('        **Class: {} **'.format(self.classes[c]))
            print(df)
            print()
        print('cnt: {}'.format(cnt))

    def _teachers_schedule_printer(self, x):
        """
        Transform optimal solution (binary decision variables) and create nice human readable schedules.
        """
        cnt = 0

        # Schedules
        for t in self.T:
            list_of_hours = [h + 1 for h in self.H]
            df = pd.DataFrame(index=['Pon', 'Utr', 'Str', 'Stv', 'Pia'], columns=list_of_hours)
            for (s, c, d, h) in product(self.S, self.C, self.D, self.H):
                if x[c][s][t][d][h].x == 1:
                    df.iloc[d, h] = (self.sub[s], self.classes[c])
                    cnt = cnt + 1

            df.fillna('   ', inplace=True)

            # Print out
            print('      ** Teacher: {} **'.format(self.teachers_dict_reverse[t]))
            print(df)
            print()
        print('cnt: {}'.format(cnt))

    def _file_printer(self, x):
        """
        Print out schedules into txt file.
        """

        # Set output filename
        now = datetime.datetime.now()
        filename = 'outputs/classes_' + now.strftime('%Y-%m-%d_%H:%M') + '.txt'

        with open(filename, 'w') as f:
            for c in self.C:
                list_of_hours = [h + 1 for h in self.H]
                df = pd.DataFrame(index=['Pon', 'Utr', 'Str', 'Stv', 'Pia'], columns=list_of_hours)
                for (s, t, d, h) in product(self.S, self.T, self.D, self.H):
                    if x[c][s][d][h].x == 1:
                        df.iloc[d, h] = self.sub[s]

                df.fillna('   ', inplace=True)

                # Print out
                print('            ** {} **'.format(self.classes[c]), file=f)
                print(df, file=f)
                print(file=f)
