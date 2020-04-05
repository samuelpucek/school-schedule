import input
import optimization

subjects, limits = input.reader()

my_schedule = optimization.Scheduler(subjects, limits)
my_schedule.schedule()

