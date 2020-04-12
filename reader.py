import pandas as pd


def reader():
    """
    Method for reading csv file containing hour classes_restrictions for each grade.

    About
    -----
    1. Create dictionary of subjects. Necessary for backwards assignment after optimization.
    2. Create list of hour classes_restrictions conditions for each grade.

    Input example
    -------------
    subjects	I.A		    II.A	    III.A
    CJL	        8	LM	    7	KA	    7	VR
    ANJ	        1	HO	    2	HO	    3	AG
    SPJ         1	SP	    1	SP	    1	SP
    MAT	        4	LM	    4	KA	    5	VR

    Return
    ------
    sub_dict: dictionary of subjects
    classes_restrictions: list of hour limits
    """

    # Import csv as DataFrame
    # df = pd.read_csv('resources/classes_restrictions_medium.csv')
    df = pd.read_csv('resources/limits_bc.csv')

    # Extract subjects, convert into dictionary
    subjects = df['subjects']
    subjects_dict_reverse: dict = {i: subjects[i] for i in range(len(subjects))}
    subjects_dict: dict = {subjects[i]: i for i in range(len(subjects))}

    # Number of rows, columns
    row, col = df.shape

    # Select limiting columns
    col_index = [i for i in range(col) if i % 2 == 1]  # Select limiting columns indexes
    classes_restrictions = df.iloc[:, col_index].T.values.tolist()

    # Extract classes
    classes_labels = [df.columns.tolist()[i] for i in col_index]
    classes_dict_reverse: dict = {i: classes_labels[i] for i in range(len(classes_labels))}
    classes_dict: dict = {classes_labels[i]: i for i in range(len(classes_labels))}

    # Extract teachers
    col_index = [i + 1 for i in range(col) if i % 2 == 1]  # Select limiting columns indexes

    teachers_series = pd.Series()

    for i in col_index:
        teachers_series = teachers_series.append(pd.Series(df.iloc[:, i].unique()))

    teachers_series = pd.Series.dropna(teachers_series)
    teachers_series = teachers_series.unique()
    teachers_list = teachers_series.tolist()

    teachers_dict_reverse: dict = {i: teachers_list[i] for i in range(len(teachers_list))}
    teachers_dict: dict = {teachers_list[i]: i for i in range(len(teachers_list))}

    # Select (teacher, class) pairs (with respect to subject)
    col_index = [i for i in range(col) if i % 2 == 0]  # Indexes
    teachers_table = df.iloc[:, col_index]  # teachers table
    teachers_table = teachers_table.fillna('nobody')  # fill NaN
    teachers_table.columns = ['subjects'] + classes_labels  # rename columns

    # Teachers restrictions connected with (subject-class) pairs
    teachers_restrictions = []

    for t in teachers_list:
        res = []
        for c in classes_labels:
            lst = teachers_table[teachers_table[c] == t]['subjects']
            res = res + [(s, c) for s in lst]
        teachers_restrictions.append(res)

    # Rewritten to dictionary coding
    teachers_restrictions_code = []

    for t in range(len(teachers_restrictions)):
        res = []
        for pair in teachers_restrictions[t]:
            s, c = pair  # s, c = ('SJL', 'I.A')
            pair_code = (subjects_dict[s], classes_dict[c])
            res.append(pair_code)
        teachers_restrictions_code.append(res)

    return subjects_dict_reverse, classes_restrictions, classes_labels, teachers_restrictions_code, teachers_dict_reverse
