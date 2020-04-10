import pandas as pd

# Import csv as DataFrame
# df = pd.read_csv('resources/limits_basic.csv')
df = pd.read_csv('resources/limits_medium.csv')
df

# Extract subjects, convert into dictionary
subjects = df['subjects']
# subjects_dict: dict = {i: subjects[i] for i in range(len(subjects))}
subjects_dict: dict = {subjects[i]: i for i in range(len(subjects))}

# Number of rows, columns
row, col = df.shape

# Select limiting columns
col_index = [i for i in range(col) if i % 2 == 1]  # Select limiting columns indexes
limits = df.iloc[:, col_index].T.values.tolist()

# Extract classes
classes_labels = [df.columns.tolist()[i] for i in col_index]
# classes_dict: dict = {i: classes_labels[i] for i in range(len(classes_labels))}
classes_dict: dict = {classes_labels[i]: i for i in range(len(classes_labels))}

# List of teachers
teachers_list = ['Ucitel1', 'Dongova', 'Krchnakova', 'Papiernikova', 'Vavrekova', 'Mutnanska', 'Humerova', 'Gabrisova',
                 'Farar', 'Simakova', 'Ha']
# teachers_dict: dict = {i: teachers_list[i] for i in range(len(teachers_list))}
teachers_dict: dict = {teachers_list[i]: i for i in range(len(teachers_list))}

# Or Series are better idea than dictionaries?
teachers_series = pd.Series(teachers_list)
classes_series = pd.Series(classes_labels)
subjects_series = pd.Series(subjects)

# Select (teacher, class) pairs (with respect to subject)
col_index = [i for i in range(col) if i % 2 == 0]  # Indexes
teachers_table = df.iloc[:, col_index]  # teachers table
teachers_table = teachers_table.fillna('nobody')  # fill NaN
teachers_table.columns = ['subjects'] + classes_labels  # rename columns

teachers_restrictions = []

for t in teachers_list:
    res = []
    for c in classes_labels:
        lst = teachers_table[teachers_table[c] == t]['subjects']
        res = res + [(s, c) for s in lst]
    teachers_restrictions.append(res)

teachers_restrictions


s, c = ('SJL', 'I.A')
subjects_series

subjects_dict[s]
classes_dict[c]


teachers_restrictions_code = []

for t in range(len(teachers_restrictions)):
    res = []
    for pair in teachers_restrictions[t]:
        s, c = pair
        pair_code = (subjects_dict[s], classes_dict[c])
        res.append(pair_code)
    teachers_restrictions_code.append(res)

teachers_restrictions
teachers_restrictions_code

teachers_restrictions_code[0]


# TODO: Status: ucitelia su pripraveny, je potrebne previest vsetky potrebne premenne do Optimizeru a tam pridat podmienky pre ucitelov.


import datetime

filename = datetime.datetime.now()

with open(filename.strftime("classes_%Y-%m-%d_%H:%M") + ".txt", "w") as file:
    file.write("")



# create empty file
def create_file():
    # Function creates an empty file
    # %d - date, %B - month, %Y - Year
    with open(filename.strftime("%d %B %Y") + ".txt", "w") as file:
        file.write("")

    # Driver Code


create_file()