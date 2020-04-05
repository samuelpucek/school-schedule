import input
import optimization

subjects, limits, classes = input.reader()

my_schedule = optimization.Scheduler(subjects, limits, classes)
my_schedule.schedule()
