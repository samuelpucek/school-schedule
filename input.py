import pandas as pd


def reader():
    """
    Method for reading csv file containing hour limits for each grade.

    About
    -----
    1. Create dictionary of subjects. Necessary for backwards assignment after optimization.
    2. Create list of hour limits conditions for each grade.

    Input example
    -------------
        subjects  I.  II.  III.  IV.
    0       SJL   9    8     8    8
    1       PDA   0    0     1    2
    2       VLA   0    0     1    2
    3       MAT   4    5     5    4

    :return:
    sub_dict: dictionary of subjects
    limits: list of hour limits
    """

    # Import csv as DataFrame
    df = pd.read_csv('limits.csv')

    # Extract subjects
    sub = df['subjects']

    # Convert subjects into dictionary
    sub_dict: dict = {i: sub[i] for i in range(len(sub))}

    # Extract limits for classes
    d = df.iloc[:, 1:]
    limits = d.T.values.tolist()

    # Extract classes
    classes = df.columns.tolist()[1:]

    return sub_dict, limits, classes
