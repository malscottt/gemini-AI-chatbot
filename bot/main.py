import asyncio
import logging
import os
import sys
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Bot and Dispatcher
if not BOT_TOKEN:
    logging.error("BOT_TOKEN is not set in environment variables.")
    sys.exit(1)

if not GEMINI_API_KEY:
    logging.warning("GEMINI_API_KEY is not set. AI features will not work.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Initialize Gemini Model
model = genai.GenerativeModel('AI_MODEL_NAME') # change the model name to the one you want to use 

@dp.message()
async def chat_with_gemini(message: types.Message):
    """
    Handler for generic messages to chat with Gemini
    """
    if not GEMINI_API_KEY:
        await message.answer("I am not configured with an AI key yet. Please tell my admin to set GEMINI_API_KEY.")
        return

    try:
        # Send 'typing' action while processing
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        logging.error(f"Error generating response: {e}", exc_info=True)
        await message.answer("Sorry, I had trouble thinking of a response.")

async def main():
    """
    Main function to start the bot
    """
    logging.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")