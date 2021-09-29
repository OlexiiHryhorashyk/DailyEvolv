import telebot
# import schedule
# import time

from telebot import types
from SQL import SqlManage
from UserInfo import User
from UserTrain import MassWorkout, MidWorkout, BurnWorkout

# Ініціалізуємо бота
TOKEN = "1488600309:AAGLFXw4fUau1gbG6QmmzXg00v1xUM66zEo"
bot = telebot.TeleBot(TOKEN)


# Ініціалізуємо підключення з базою данних
db = SqlManage('db.db')

user = User()


def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton('Workout!'))
    return markup


def done_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton('Done!'))
    return markup


def test_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('Yes')
    btn2 = types.KeyboardButton('No')
    markup.add(btn1, btn2)
    return markup


# Початок бота
@bot.message_handler(commands='start')
def start(message):
    if db.user_exists(message.from_user.id):
        db.delete_user(message.from_user.id)
    bot.send_message(message.chat.id, "Hello, friend! If you want to get your body in order, I will help you.")
    user.set_id(message.from_user.id)
    sent = bot.send_message(message.chat.id, "First of all, I want to know your name.")
    bot.register_next_step_handler(sent, test_start)


def test_start(message, repeat=False):
    user.set_name(message.text)
    if not repeat:
        bot.send_message(message.chat.id, 'Ok, {name}. The first step is to take a test, based on which I will select'
                                          ' a training program just for you...'.format(name=message.text))
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('Male')
    btn2 = types.KeyboardButton('Female')
    markup.add(btn1, btn2)
    sent = bot.send_message(message.chat.id, "Choose your sex.", reply_markup=markup)
    bot.register_next_step_handler(sent, gender_test)


def gender_test(message):
    if message.text.lower() == "male" or message.text.lower() == "female":
        user.set_gender(message.text.lower())
        sent = bot.send_message(message.chat.id, "Your age:")
        bot.register_next_step_handler(sent, age_test)
    else:
        sent = bot.send_message(message.chat.id, "Incorrect gender! It should choose male or female!")
        test_start(sent, repeat=True)


def age_test(message):
    try:
        age = int(message.text)
        if age < 0:
            age = abs(age)
            bot.send_message(message.chat.id, "Probably you mean {age} years old.".format(age=age))
        if 0 < age < 10:
            bot.send_message(message.chat.id, "I'm afraid you too young for it, enjoy your childhood!")
            bot.send_message(message.chat.id, "If you entered the wrong age, restart the bot (/start).")
        elif 10 < age < 65:
            user.set_age(age)
            sent = bot.send_message(message.chat.id, "Your height (In centimeters):")
            bot.register_next_step_handler(sent, height_test)
        elif age > 100:
            sent = bot.send_message(message.chat.id, "I'm sure that you made a mistake. "
                                                     "You can't be {age} years old. ".format(age=age))
            test_start(sent, repeat=True)
        else:
            bot.send_message(message.chat.id, "Sorry, but I'm afraid you too old for it!")
            bot.send_message(message.chat.id, "If you entered the wrong age, restart the bot (/start).")
    except ValueError:
        sent = bot.send_message(message.chat.id, "Incorrect age! Please, enter only number!")
        test_start(sent, repeat=True)


def height_test(message):
    try:
        height = int(message.text)
        if height < 0:
            height = abs(height)
            bot.send_message(message.chat.id, "Probably you mean your height is {hig} centimeters.".format(hig=height))
        if 0 < height < 120:
            sent = bot.send_message(message.chat.id, "I'm sure the height is wrong! Otherwise, "
                                                     "I'm sorry, I can't help you.")
            test_start(sent, repeat=True)
        elif 120 < height < 220:
            user.set_height(height)
            sent = bot.send_message(message.chat.id, "Your weight (In kilograms):")
            bot.register_next_step_handler(sent, weight_test)
        else:
            sent = bot.send_message(message.chat.id, "I'm sure that you made a mistake. You "
                                                     "can't be {hig} centimeters tall.".format(hig=height))
            test_start(sent, repeat=True)
    except ValueError:
        sent = bot.send_message(message.chat.id, "Incorrect height! Please, enter only number!")
        test_start(sent, repeat=True)


def weight_test(message):
    try:
        weight = int(message.text)
        if weight < 0:
            weight = abs(weight)
            bot.send_message(message.chat.id, "Probably you mean your weight is {wig} kilograms.".format(wig=weight))
        if 0 < weight < 35:
            sent = bot.send_message(message.chat.id, "I'm sure the weight is wrong! Otherwise,"
                                                     " I'm sorry, I can't help you.")
            test_start(sent, repeat=True)
        elif 35 < weight < 220:
            user.set_weight(weight)
            if weight > 150:
                bot.send_message(message.chat.id, "I'll try to help you, but you should ask a doctor for help.")
            sent = bot.send_message(message.chat.id, "Do you think you have some excess fat?",
                                    reply_markup=test_keyboard())
            bot.register_next_step_handler(sent, fat_test)
        else:
            sent = bot.send_message(message.chat.id, "I'm sure that you made a mistake. "
                                                     "Otherwise, you should see a doctor.")
            test_start(sent, repeat=True)
    except ValueError:
        sent = bot.send_message(message.chat.id, "Incorrect weight! Please, enter only number!")
        test_start(sent, repeat=True)


def fat_test(message):
    if message.text == 'Yes' or message.text == 'No' or message.text == 'yes' or message.text == 'no':
        if message.text == 'Yes' or message.text == 'yes':
            user.set_fat(True)
            sent = bot.send_message(message.chat.id, "Do you have any sport experience or physical training?",
                                    reply_markup=test_keyboard())
            bot.register_next_step_handler(sent, sport_test)
        else:
            user.set_fat(False)
            sent = bot.send_message(message.chat.id, "Do you have any sport experience or physical training?",
                                    reply_markup=test_keyboard())
            bot.register_next_step_handler(sent, sport_test)
    else:
        sent = bot.send_message(message.chat.id, "It is incorrect answer. It should be Yes or No.")
        test_start(sent, repeat=True)


def sport_test(message):
    if message.text == 'Yes' or message.text == 'No' or message.text == 'yes' or message.text == 'no':
        if message.text == 'Yes' or message.text == 'yes':
            user.set_sport(True)
        else:
            user.set_sport(False)
    else:
        sent = bot.send_message(message.chat.id, "It is incorrect answer. It should be Yes or No.")
        test_start(sent, repeat=True)
    wh_index = user.weight / (user.height*user.height*0.0001)
    if wh_index < 20:
        if user.fat:
            user.set_program(2)
        else:
            user.set_program(1)
    elif 20 < wh_index < 24:
        if user.fat:
            user.set_program(3)
        else:
            user.set_program(2)
    else:
        user.set_program(3)
    db.add_user(user.user_id, user.name, user.gender, user.age, user.height, user.weight,
                user.fat, user.sport, user.program, 1, 1)
    sent = bot.send_message(message.chat.id, "Done! I will chose you a training program.", reply_markup=keyboard())
    bot.register_next_step_handler(sent, workout)


def workout(message):
    if message.text.lower() == "workout!":
        if db.user_exists(message.from_user.id):
            the_user = db.get_user_by_id(message.from_user.id)
            name = the_user['name'][0]
            gender = the_user['gender'][0]
            age = the_user['age'][0]
            sport = the_user['sport'][0]
            program = the_user['program'][0]
            cycle = the_user['cycle'][0]
            day = the_user['day'][0]
            day_number = day + 6*(cycle-1)
            work = MidWorkout
            if program == 1:
                work = MassWorkout(gender, age, sport, cycle)
            elif program == 2:
                work = MidWorkout(gender, age, sport, cycle)
            elif program == 3:
                work = BurnWorkout(gender, age, sport, cycle)
            else:
                bot.send_message(message.chat.id, "OOPS! Something went wrong!")
            work.set_workout()
            if day == 1:
                work_list = work.first_day()
                repeat = work_list[0]
                push = work_list[1]
                rev_push = work_list[2]
                tight_push = work_list[3]
                rows = work_list[4]
                plank = work_list[5]
                bot.send_message(message.chat.id, "Ok {name}, today is the day number {day}"
                                                  " of your workout!".format(name=name, day=day_number))
                sent = "And today is the day of push-ups. We are going to train chest muscles and triceps.\n" \
                       "Don't forget to warm up and then start. "
                bot.send_message(message.chat.id, sent)
                sent = "There is the list what you should do:\n" \
                    "1. {push} push-ups from floor - {rep} times.\n" \
                    "2. {rev_push} revers push-ups from a chair or bed - {rep} times.\n" \
                    "3. {tight_push} tight push-ups with your palms close to each other - {rep} times.\n" \
                    "4. {row} rows with dumbbells or something heavy, lying down on bed or floor - {rep} times.\n" \
                    "5. {plank} seconds in plank - {rep} times.\n" \
                    "Don't forget to rest between approaches" \
                       " for 60 seconds!".format(push=push, rev_push=rev_push, tight_push=tight_push, row=rows,
                                                 plank=plank, rep=repeat)
                last = bot.send_message(message.chat.id, sent, reply_markup=done_keyboard())
                bot.register_next_step_handler(last, workout_done)
            elif day == 3:
                work_list = work.third_day()
                repeat = work_list[0]
                pull = work_list[1]
                rev_pull = work_list[2]
                hyper = work_list[3]
                biceps = work_list[4]
                cranch = work_list[5]
                bot.send_message(message.chat.id, "Ok {name}, today is the day number {day}"
                                                  " of your workout!".format(name=name, day=day_number))
                sent = "And today is the day of pull-ups. We are going to train spine, biceps and abdominal muscles.\n"\
                       "Don't forget to warm up and then start. "
                bot.send_message(message.chat.id, sent)
                sent = "There is the list what you should do:\n" \
                    "1. {pull} pull-ups on horizontal bar {rep} - times.\n" \
                    "2. {rev_pull} reverse pull-ups (palms to inside) - {h_rep} times.\n" \
                    "3. {hyp} hyperextensions, lifting the torso leaning on the edge of bed or chair - {rep} times.\n"\
                    "4. {bic} on biceps using dumbbells or something heavy - {rep} times.\n" \
                    "5. {crunch} reps to pump up the abdominal muscles - {rep} times.\n" \
                    "Don't forget to rest between approaches" \
                       " for 60 seconds!".format(pull=pull, rev_pull=rev_pull, hyp=hyper, bic=biceps, crunch=cranch,
                                                 rep=repeat, h_rep=int(repeat*0.5))
                last = bot.send_message(message.chat.id, sent, reply_markup=done_keyboard())
                bot.register_next_step_handler(last, workout_done)
            elif day == 5:
                work_list = work.fifth_day()
                repeat = work_list[0]
                squats = work_list[1]
                leg_lift = work_list[2]
                should_push = work_list[3]
                rows = work_list[4]
                plank = work_list[5]
                bot.send_message(message.chat.id, "Ok {name}, today is the day number {day}"
                                                  " of your workout!".format(name=name, day=day_number))
                sent = "And today is the day of legs and shoulders.\n Don't forget to warm up and then start."
                bot.send_message(message.chat.id, sent)
                sent = "There is the list what you should do:\n" \
                       "1. {squats} squats - {rep} times.\n" \
                       "2. {leg_lift} reps of lifting your legs, lying down on bed or floor - {rep} times.\n" \
                       "3. {should_push} push-ups with your butt raised up - {rep} times.\n" \
                       "4. {row} rows with dumbbells or something heavy - {rep} times.\n" \
                       "5. {plank} seconds in plank - {rep} times.\n" \
                       "Don't forget to rest between approaches" \
                       " for 60 seconds!".format(squats=squats, leg_lift=leg_lift, should_push=should_push, row=rows,
                                                 plank=plank, rep=repeat)
                last = bot.send_message(message.chat.id, sent, reply_markup=keyboard())
                bot.register_next_step_handler(last, workout_done)
            elif day % 2 == 0:
                sent = "Yesterday you did a nice job, so today you need to allow your body to recover. " \
                       "Make a warn up and you may do the plank for 30 seconds."
                bot.send_message(message.chat.id, sent)
                last = bot.send_message(message.chat.id, "See you tomorrow!", reply_markup=done_keyboard())
                bot.register_next_step_handler(last, workout_done)
                pass
    else:
        if message.text == "/start":
            sent = bot.send_message(message.chat.id, "Restarting bot. Please input /start again")
            bot.register_next_step_handler(sent, start)
        sent = bot.send_message(message.chat.id, "It is not time for conversation!"
                                                 " It is time for workout!", reply_markup=keyboard())
        bot.register_next_step_handler(sent, workout)


def workout_done(message):
    if message.text == "/start":
        sent = bot.send_message(message.chat.id, "Restarting bot. Please input /start again")
        bot.register_next_step_handler(sent, start)
    elif message.text == "Done!":
        db.set_user_day(db.get_user_day(message.from_user.id)[0] + 1, message.from_user.id)
        if db.get_user_day(message.from_user.id)[0] > 6:
            db.set_user_day(1, message.from_user.id)
            db.set_user_cycle(db.get_user_cycle(message.from_user.id)[0] + 1, message.from_user.id)
        sent = bot.send_message(message.chat.id, "Well done! Have a good rest, and come tomorrow!",
                                reply_markup=keyboard())
        bot.register_next_step_handler(sent, workout)
    else:
        sent = bot.send_message(message.chat.id, "Have you done your workout?", reply_markup=done_keyboard())
        bot.register_next_step_handler(sent, workout_done)


# def day_counter(user_id):
#     db.set_user_day(db.get_user_day(user_id)[0]+1, user_id)
#     if db.get_user_day(user_id)[0] > 6:
#         db.set_user_day(1, user_id)
#         db.set_user_cycle(db.get_user_cycle(user_id)[0]+1, user_id)
#
#
# def workout_send():
#     users = db.get_users_id()
#     for u in users:
#         day_counter(u)
#     pass
#
#
# schedule.every().day.at("00:00").do(workout_send)
#
while True:  # этот цикл отсчитывает время. Он обязателен.
    bot.infinity_polling(True)
#     schedule.run_pending()
#     time.sleep(1)
