import telebot
from telegram.ext import ConversationHandler
from datetime import datetime, timedelta

# Replace 'YOUR_BOT_TOKEN' with your actual API token
bot = telebot.TeleBot('6327127593:AAGLnFo_tJTekRh1WVoQgplKk7PxAcELlx8')

# Define conversation states
GAME_NAME, MAX_PLAYERS, DATE, TIME = range(4)

# Dictionary to store game details
game_details = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    greeting_message = f"Hello, {user_name}! I am your board game appointment bot."
    bot.send_message(user_id, greeting_message)
    bot.send_message(user_id, "You can use the following commands:")
    bot.send_message(user_id, "/help - Show available commands")
    bot.send_message(user_id, "/creategame - Create a new game")
    bot.send_message(user_id, "/joingame - Join an existing game")

@bot.message_handler(commands=['help'])
def handle_help(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "You can use the following commands:")
    bot.send_message(user_id, "/help - Show available commands")
    bot.send_message(user_id, "/creategame - Create a new game")
    bot.send_message(user_id, "/joingame - Join an existing game")

@bot.message_handler(commands=['creategame'])
def handle_create_game(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Let's create a new game. Please enter the name of the game:")
    bot.register_next_step_handler(message, get_game_name)

def get_game_name(message):
    user_id = message.from_user.id
    game_name = message.text
    game_details[user_id] = {'name': game_name}
    bot.send_message(user_id, "Great! Now, please enter the maximum number of players:")
    bot.register_next_step_handler(message, get_max_players)

def get_max_players(message):
    user_id = message.from_user.id
    max_players = message.text
    game_details[user_id]['max_players'] = max_players

    # Create a custom text keyboard with date buttons (next two weeks in DD.MM format)
    date_buttons = []

    today = datetime.now()
    for i in range(14):
        current_date = today + timedelta(days=i)
        date_text = current_date.strftime("%d.%m")
        date_buttons.append(date_text)  # Ensure date_text is a string

    reply_markup = telebot.types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True, resize_keyboard=True)
    reply_markup.add(*date_buttons)

    bot.send_message(user_id, "Please choose a date (DD.MM):", reply_markup=reply_markup)
    bot.register_next_step_handler(message, get_date)

def get_date(message):
    user_id = message.from_user.id
    selected_date = message.text
    game_details[user_id]['date'] = selected_date

    # Create a custom text keyboard with time buttons (30-minute intervals from 14:00 to 22:00)
    time_buttons = []

    times = [f"{hour:02d}:{minute:02d}" for hour in range(14, 23) for minute in (0, 30)]
    for time in times:
        time_buttons.append(time)  # Ensure time is a string

    reply_markup = telebot.types.ReplyKeyboardMarkup(row_width=4, one_time_keyboard=True, resize_keyboard=True)
    reply_markup.add(*time_buttons)

    bot.send_message(user_id, "Please choose a time:", reply_markup=reply_markup)
    bot.register_next_step_handler(message, get_time)

def get_time(message):
    user_id = message.from_user.id
    selected_time = message.text
    game_details[user_id]['time'] = selected_time

    # End the conversation
    bot.send_message(user_id, "Game details have been saved.")
    bot.send_message(user_id, f"Game Name: {game_details[user_id]['name']}")
    bot.send_message(user_id, f"Max Players: {game_details[user_id]['max_players']}")
    bot.send_message(user_id, f"Date: {game_details[user_id]['date']}")
    bot.send_message(user_id, f"Time: {game_details[user_id]['time']}")

if __name__ == "__main__":
    print("Bot is starting...")
    bot.polling()
