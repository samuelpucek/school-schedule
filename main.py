import input
import optimization

subjects, limits, classes, teachers_restrictions_code, teachers_dict_reverse = input.reader()

my_schedule = optimization.Scheduler(subjects, limits, classes, teachers_restrictions_code, teachers_dict_reverse)
my_schedule.schedule()

# TODO: Niektory ucitelia mozu ucit len v niektore dni
# TODO: Pridaj dvojhodinovky (SJL SJL), (VYV, VYV) atd..
# TODO: Predmety ktore su len napr. 2x za tyzden nech su dostatocne odseba
