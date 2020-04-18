import pandas as pd


class Reader:
    """ Reading input files and running basic checks. """

    def __init__(self):
        self.file_name_classes = 'classes_limits.csv'
        self.file_name_teachers = 'teachers_limits.csv'

        self.classes_names = dict()
        self.classes_restrictions = dict()
        self.teachers_names = dict()
        self.teachers_restrictions = dict()
        self.subjects_names = dict()

    def read(self):
        """ Main method """
        self._file_reader()
        self._check_teachers()
        self._check_classes()
        return self.classes_names, self.classes_restrictions, self.teachers_names, self.teachers_restrictions, self.subjects_names

    def _file_reader(self):
        """
        Method for reading csv file containing hour classes_restrictions for each grade.

        Input example
        -------------
        subjects	I.A		    II.A	    III.A
        CJL	        8	LM	    7	KA	    7	VR
        ANJ	        1	HO	    2	HO	    3	AG
        SPJ         1	SP	    1	SP	    1	SP
        MAT	        4	LM	    4	KA	    5	VR

        Return
        ------
        Initialize all variables.
        """

        # Import csv as DataFrame
        path = 'resources/bc/'
        df = pd.read_csv(path + self.file_name_classes)

        # Extract subjects, convert into dictionary
        subjects = df['subjects']
        self.subjects_names = {i: subjects[i] for i in range(len(subjects))}
        subjects_dict: dict = {subjects[i]: i for i in range(len(subjects))}

        # Number of rows, columns
        row, col = df.shape

        # Select limiting columns
        col_index = [i for i in range(col) if i % 2 == 1]  # Select limiting columns indexes
        classes_restrictions = df.iloc[:, col_index].fillna(0).T.values.tolist()
        self.classes_restrictions = {i: classes_restrictions[i] for i in range(len(classes_restrictions))}

        # Extract classes
        classes_labels = [df.columns.tolist()[i] for i in col_index]
        self.classes_names = {i: classes_labels[i] for i in range(len(classes_labels))}
        classes_dict: dict = {classes_labels[i]: i for i in range(len(classes_labels))}

        # Extract teachers
        col_index = [i + 1 for i in range(col) if i % 2 == 1]  # Select limiting columns indexes

        teachers_series = pd.Series(dtype='str')

        for i in col_index:
            teachers_series = teachers_series.append(pd.Series(df.iloc[:, i].unique()))

        teachers_series = pd.Series.dropna(teachers_series)
        teachers_series = teachers_series.unique()
        teachers_list = teachers_series.tolist()

        teachers_reverse: dict = {i: teachers_list[i] for i in range(len(teachers_list))}
        self.teachers_names = teachers_reverse

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

        self.teachers_restrictions = {i: teachers_restrictions_code[i] for i in
                                      range(len(teachers_restrictions_code))}

        # Read teachers day restrictions
        path = 'resources/bc/'
        df = pd.read_csv(path + self.file_name_teachers)
        # print(df)
        return

    def _check_classes(self):
        """
        Checking input error: if each class has less than 30 hours per week.
        """

        for key, value in self.classes_restrictions.items():
            if sum(value) > 30:
                raise ValueError('Input limits for class {0} are violated. {0} has more than 30 hours per week.'
                                 .format(self.classes_names[key]))

    def _check_teachers(self):
        """ Checking input error: if each teacher teaches less than 30 hours per week. """
        # TODO: also with respect to individual preferences! e.g. only two days per week >> less than 2*6=12

        for key, value in self.teachers_restrictions.items():
            total_hours = 0
            for sub, cls in value:
                total_hours += self.classes_restrictions[cls][sub]

            if total_hours > 30:
                raise ValueError(
                    'Input limits for teacher {0} are violated. {0} teaches more classes than his/her week max limit.'
                    .format(self.teachers_names[key]))


my_reader = Reader()
my_reader.read()
