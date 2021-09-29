class Workout:
    pushups = 11
    pullups = 6
    squats = 11
    plank = 16
    rows = 10
    hyper = 8
    cranch = 12
    biceps = 11
    repetitions = 4

    def __init__(self, gender, age, sport, cycle):
        self.gender = gender
        self.age = age
        self.sport = sport
        self.cycle = cycle

    def cof_count(self):
        cof = 1
        if self.gender == 'male':
            cof += 0.2
        if self.sport == 1:
            cof += 0.4
        if self.age < 15:
            cof -= 0.2
        elif 15 < self.age < 20:
            cof += 0.1
        elif 20 < self.age < 35:
            cof += 0.2
        elif 35 < self.age < 43:
            cof += 0.1
        elif 43 < self.age < 50:
            cof += 0.0
        elif 50 < self.age < 55:
            cof -= 0.2
        elif 55 < self.age < 65:
            cof -= 0.3
        else:
            cof -= 0.4
        return cof


class MassWorkout(Workout):
    def set_workout(self):
        additional = 0
        cof = super().cof_count() + 0.3
        self.repetitions -= 1
        if self.cycle != 1:
            additional = self.cycle - 1
        self.pushups = int(round(self.pushups * cof + additional))
        self.pullups = int(round(self.pullups * cof + additional))
        self.squats = int(round(self.squats * cof + additional))
        self.plank = int(round(self.plank * cof + additional + 5))
        self.plank -= self.plank % 5
        self.rows = int(round(self.rows * cof + additional))
        self.cranch = int(round(self.cranch * cof + additional))
        self.cranch -= self.cranch % 5
        self.hyper = int(round(self.hyper * cof + additional))
        self.biceps = int(round(self.biceps * cof + additional))

    def first_day(self):
        tight_push = int(round(self.pushups * 0.7))
        reverse_push = int(round(self.pushups * 0.7))
        day_list = [self.repetitions, self.pushups, reverse_push, tight_push, self.rows, self.plank]
        return day_list

    def third_day(self):
        day_list = [self.repetitions, self.pullups, self.pullups, self.hyper, self.biceps, self.cranch]
        return day_list

    def fifth_day(self):
        leg_crunch = int(round(self.cranch * 0.7))
        shoulders_pushup = int(round(self.pushups * 0.7))
        day_list = [self.repetitions, self.squats, leg_crunch, shoulders_pushup, self.rows, self.plank]
        return day_list


class MidWorkout(Workout):
    def set_workout(self):
        additional = 0
        cof = super().cof_count() + 0.1
        if self.cycle != 1:
            additional = self.cycle - 1
        self.pushups = int(round(self.pushups * cof + additional))
        self.pullups = int(round(self.pullups * cof + additional))
        self.squats = int(round(self.squats * cof + additional))
        self.plank = int(round(self.plank * cof + additional + 10))
        self.plank -= self.plank % 5
        self.rows = int(round(self.rows * cof + additional))
        self.cranch = int(round(self.cranch * cof + additional + 5))
        self.cranch -= self.cranch % 5
        self.hyper = int(round(self.hyper * cof + additional))
        self.biceps = int(round(self.biceps * cof + additional))

    def first_day(self):
        tight_push = int(round(self.pushups * 0.7))
        reverse_push = int(round(self.pushups * 0.7))
        day_list = [self.repetitions, self.pushups, reverse_push, tight_push, self.rows, self.plank]
        return day_list

    def third_day(self):
        day_list = [self.repetitions, self.pullups, self.pullups, self.hyper, self.biceps, self.cranch]
        return day_list

    def fifth_day(self):
        leg_crunch = int(round(self.cranch * 0.7))
        shoulders_pushup = int(round(self.pushups * 0.7))
        day_list = [self.repetitions, self.squats, leg_crunch, shoulders_pushup, self.rows, self.plank]
        return day_list


class BurnWorkout(Workout):
    def set_workout(self):
        additional = 0
        cof = super().cof_count() - 0.2
        self.repetitions += 1
        if self.cycle != 1:
            additional = self.cycle - 1
        self.pushups = int(round(self.pushups * cof + additional))
        self.pullups = int(round(self.pullups * cof + additional))
        self.squats = int(round(self.squats * cof + additional))
        self.plank = int(round(self.plank * cof + additional + 10))
        self.plank -= self.plank % 5
        self.rows = int(round(self.rows * cof + additional))
        self.cranch = int(round(self.cranch * cof + additional + 5))
        self.cranch -= self.cranch % 5
        self.hyper = int(round(self.hyper * cof + additional))
        self.biceps = int(round(self.biceps * cof + additional))

    def first_day(self):
        tight_push = int(round(self.pushups * 0.7))
        reverse_push = int(round(self.pushups * 0.7))
        day_list = [self.repetitions, self.pushups, reverse_push, tight_push, self.rows, self.plank]
        return day_list

    def third_day(self):
        day_list = [self.repetitions, self.pullups, self.pullups, self.hyper, self.biceps, self.cranch]
        return day_list

    def fifth_day(self):
        leg_crunch = int(round(self.cranch * 0.7))
        shoulders_pushup = int(round(self.pushups * 0.7))
        day_list = [self.repetitions, self.squats, leg_crunch, shoulders_pushup, self.rows, self.plank]
        return day_list
