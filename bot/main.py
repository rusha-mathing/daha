from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

TOKEN = "7969990682:AAFBV-0Xtx61WEaBSlPP1CU4arggZQQBAPQ"


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("View courses", callback_data='show_courses')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Hello! I am a bot for selecting courses from daha.pro.', reply_markup=reply_markup)


def show_courses(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    API_URL = "https://api.daha.pro/courses"  # Replace with actual endpoint
    HEADERS = {"Authorization": "Bearer YOUR_API_KEY"}  # If needed

    try:
        response = requests.get(API_URL, headers=HEADERS)
        if response.status_code != 200:
            query.edit_message_text("API access error. Please check your key.")
            return

        courses = response.json()
        if not courses:
            query.edit_message_text("No courses found.")
            return

        keyboard = []
        for course in courses[:10]:  # Limit to 10 courses
            title = course.get("title", "Untitled course")
            url = course.get("url", "https://daha.pro/")
            keyboard.append([InlineKeyboardButton(title, url=url)])

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="📚 Available courses:", reply_markup=reply_markup)

    except Exception as e:
        print(f"Error: {e}")
        query.edit_message_text("⚠️ API is not responding. Please try again later.")


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(show_courses, pattern='^show_courses$'))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()