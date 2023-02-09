import openai
import telebot


openai.api_key = "" # API Key OpenAI
TELEGRAM_API_KEY = "" # API Key Bot Telegram

bot = telebot.TeleBot(TELEGRAM_API_KEY)

def chatgpt3(message):
    res = openai.Completion.create(
        model = "text-davinci-003",
        prompt = message,
        max_tokens = 150 # questo numero determina la lunghezza della risposta
    )
    return res.choices[0].text

@bot.message_handler(func=lambda message: True)
def chat(message):
    print(message.text)
    res = chatgpt3(message.text)
    bot.reply_to(message, res)

bot.infinity_polling()