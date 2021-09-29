class User:
    user_id = 0
    name = ""
    gender = ""
    age = 0
    height = 0
    weight = 0
    fat = False
    sport = False
    program = 0

    def set_id(self, user_id):
        self.user_id = user_id

    def set_name(self, name):
        self.name = name

    def set_gender(self, gender):
        self.gender = gender

    def set_age(self, age):
        self.age = age

    def set_height(self, height):
        self.height = height

    def set_weight(self, weight):
        self.weight = weight

    def set_fat(self, fat):
        self.fat = fat

    def set_sport(self, sport):
        self.sport = sport

    def set_program(self, program):
        self.program = program
