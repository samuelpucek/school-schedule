from itertools import product
from mip import Model, xsum, maximize, BINARY
import pandas as pd

# Constants
S = 12  # subjects
D = 5  # days
H = 5  # max hours per day

S = range(S)
D = range(D)
H = range(H)

model = Model('school-schedule')

x = [[[model.add_var(var_type=BINARY, name='({},{},{})'.format(s+1, d+1, h+1)) for h in H] for d in D] for s in S]

lim = [[9, 0, 0, 4, 2, 0, 3, 0, 2, 1, 0, 1],
       [8, 0, 0, 5, 2, 2, 2, 0, 2, 1, 0, 1]]

model.objective = maximize(xsum(x[s][d][h] for s in S for d in D for h in H))

for s in S:
    model += xsum(x[s][d][h] for h in H for d in D) == lim[0][s]

for (d, h) in product(D, H):
    model += xsum(x[s][d][h] for s in S) <= 1

for (s, d) in product(S, D):
    model += xsum(x[s][d][h] for h in H) <= 2  #TODO opravit

model.optimize()


print(100*'=')

# Rozvrh
df = pd.DataFrame(index=['Pon', 'Utr', 'Str', 'Stv', 'Pia'], columns=[1, 2, 3, 4, 5])

pred = {0: 'SJL', 1: 'PDA', 2: 'VLA', 3: 'MAT', 4: 'VYV', 5: 'ANJ', 6: 'TSV', 7: 'IFV', 8: 'PVO', 9: 'HUV', 10: 'PVC', 11: 'NB/E'}

for (s, d, h) in product(S, D, H):
    if x[s][d][h].x == 1:
        df.iloc[d, h] = pred[s]

df.fillna('   ', inplace=True)
print(df)