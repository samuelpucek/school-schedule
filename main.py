import input
import optimization

subjects, limits = input.reader()

x = optimization.schedule(subjects, limits)

# schedule = optimization.transformer(x)

# print(schedule)