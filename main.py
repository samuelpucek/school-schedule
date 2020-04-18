import reader
import optimization

# Reading input file
my_reader = reader.Reader()
classes_names, classes_restrictions, teachers_names, teachers_restrictions, subjects_names = my_reader.read()

# Optimization
my_schedule = optimization.Scheduler(classes_names, classes_restrictions, teachers_names, teachers_restrictions,
                                     subjects_names)
my_schedule.schedule()

# TODO: Niektory ucitelia mozu ucit len v niektore dni
# TODO: Pridaj dvojhodinovky (SJL SJL), (VYV, VYV) atd..
# TODO: Predmety ktore su len napr. 2x za tyzden nech su dostatocne odseba
