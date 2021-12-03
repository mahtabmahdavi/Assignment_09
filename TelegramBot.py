import telebot
import random
from khayyam import JalaliDatetime
from gtts import gTTS
import qrcode


bot = telebot.TeleBot("TOKEN")


@bot.message_handler(commands = ['start'])
def start(message):
    bot.reply_to(message, message.from_user.first_name + " خوش آمدی")


@bot.message_handler(commands = ['help'])
def help(message):
    bot.reply_to(message, """/start
خوش‌آمد گویی!

/game
بازی حدس اعداد رو با این می‌تونی بازی کنی.

/age
تاریخ تولدت رو با فرمت "1376/9/9" وارد کن، سنت رو خیلی دقیق ببین.

/voice
یه جملۀ انگلیسی به من می‌دی، منم اون رو به صورت voice بهت می‌دم.

/max
یه آرایه با فرمت "14,7,78,15,8,19,20" به من می‌دی، منم بهت می‌گم بزرگ‌ترین عدد کدومه :)

/argmax
یه آرایه با فرمت "14,7,78,15,8,19,20" به من می‌دی، منم بهت می‌گم بزرگ‌ترین عدد تو خونۀ چندمه :)

/qrcode
متن خودت رو به من می‌دی، منم QR code اون رو بهت می‌دم.

/help
برای کمک به تو یه سری چیزمیز بهت می‌گه!""")


@bot.message_handler(commands = ['game'])
def game(message):
    global random_number
    random_number = random.randint(1, 100)
    user_message = bot.send_message(message.chat.id, "قراره یه عدد بین 1 تا 100 رو حدس بزنی. حالا حدست رو وارد کن.")
    bot.register_next_step_handler(user_message, game_helper)

markup = telebot.types.ReplyKeyboardMarkup(row_width = 1)
button = telebot.types.KeyboardButton("new game")
markup.add(button)

def game_helper(message):
    global random_number

    try:
        if message.text == "new game":
            random_number = random.randint(1, 100)
            user_message = bot.send_message(message.chat.id, "دوباره بازی رو شروع می‌کنیم. حدست رو وارد کن.")
            bot.register_next_step_handler(user_message, game_helper)

        elif int(message.text) < random_number:
            user_message = bot.send_message(message.chat.id, "برو بالا", reply_markup = markup)
            bot.register_next_step_handler(user_message, game_helper)

        elif int(message.text) > random_number:
            user_message = bot.send_message(message.chat.id, "برو پایین", reply_markup = markup)
            bot.register_next_step_handler(user_message, game_helper)

        elif int(message.text) == random_number:
            bot.send_message(message.chat.id, "برنده شدی!", reply_markup = telebot.types.ReplyKeyboardRemove(selective = True))
            
    except:
        user_message = bot.send_message(message.chat.id, "عدد وارد نکردی، لطفاً یه عدد بین 1 تا 100 رو وارد کن.")
        bot.register_next_step_handler(user_message, game_helper)


@bot.message_handler(commands = ['age'])
def age(message):
    user_message = bot.send_message(message.chat.id, "تاریخ تولدت رو با فرمت \"1376/9/9\" وارد کن.")
    bot.register_next_step_handler(user_message, calculate_age)

def calculate_age(message):
    try:
        birth_date = message.text.split('/')
        difference = JalaliDatetime.now() - JalaliDatetime(birth_date[0], birth_date[1], birth_date[2])
        year = difference.days // 365
        difference = difference.days % 365
        month = difference // 30
        day = difference % 30
        bot.send_message(message.chat.id, "تو " + str(year) + " سال و " + str(month) + " ماه و " + str(day) + " روزه هستی.")
    except:
        user_message = bot.send_message(message.chat.id, "حتماً باید تاریخ تولدت رو با فرمت بالا وارد کنی.")
        bot.register_next_step_handler(user_message, calculate_age)


@bot.message_handler(commands = ['voice'])
def voice(message):
    user_message = bot.send_message(message.chat.id, "یه جملۀ انگلیسی بنویس.")
    bot.register_next_step_handler(user_message, voice_maker)

def voice_maker(message):
    try:
        language = "en"
        message_voice = gTTS(text = message.text, lang = language, slow = False)
        message_voice.save("voice.mp3")
        voice_file = open("voice.mp3", "rb")
        bot.send_voice(message.chat.id, voice_file)
    except:
        user_message = bot.send_message(message.chat.id, "فقط متن وارد کن نه چیز دیگه!")
        bot.register_next_step_handler(user_message, voice_maker)


@bot.message_handler(commands = ['max'])
def maximum(message):
    user_message = bot.send_message(message.chat.id, "قراره بزرگ‌ترین عدد تو یه آرایه رو پیدا کنیم.\nآرایۀ مورد نظرت رو طبق فرمت \"14,7,78,15,8,19,20\" وارد کن.")
    bot.register_next_step_handler(user_message, max_number)

def max_number(message):
    try:
        numbers = list(map(int, message.text.split(',')))
        maximum = max(numbers)
        bot.reply_to(message, "بزرگ‌ترین عدد " + str(maximum) + " هست.")
    except:
        user_message = bot.send_message(message.chat.id, "اشتباه وارد کردی!\nلطفاً اعداد رو با فرمت \"14,7,78,15,8,19,20\" وارد کن.")
        bot.register_next_step_handler(user_message, max_number)


@bot.message_handler(commands = ['argmax'])
def argmax(message):
    user_message = bot.send_message(message.chat.id, "قراره موقعیت بزرگ‌ترین عدد تو یه آرایه رو پیدا کنیم.\nآرایۀ مورد نظرت رو طبق فرمت \"14,7,78,15,8,19,20\" وارد کن.")
    bot.register_next_step_handler(user_message, max_index)

def max_index(message):
    try:
        numbers = list(map(int, message.text.split(',')))
        index = numbers.index(max(numbers))
        bot.reply_to(message, "بزرگ‌ترین عدد در موقعیت " + str(index + 1) + " قرار داره.")
    except:
        user_message = bot.send_message(message.chat.id, "اشتباه وارد کردی!\nلطفاً اعداد رو با فرمت \"14,7,78,15,8,19,20\" وارد کن.")
        bot.register_next_step_handler(user_message, max_index)


@bot.message_handler(commands = ['qrcode'])
def QRcode(message):
    user_message = bot.send_message(message.chat.id, "متن خودت رو وارد کن.")
    bot.register_next_step_handler(user_message, make_qrcode)

def make_qrcode(message):
    if isinstance(message.text, str) == True:
        qrcode_image = qrcode.make(message.text)
        qrcode_image.save("QR.jpg")
        qrcode_file = open("QR.jpg", "rb")
        bot.send_photo(message.chat.id, qrcode_file)
    else:
        user_message = bot.send_message(message.chat.id, "فقط متن وارد کن نه چیز دیگه!")
        bot.register_next_step_handler(user_message, make_qrcode)


bot.infinity_polling()
