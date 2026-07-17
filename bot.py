import os
import telebot
import google.generativeai as genai

# Railway Environment Variables ထဲကနေ Key တွေကို လှမ်းယူပါမယ်
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("⚠️ Railway Variables ထဲမှာ BOT_TOKEN နဲ့ GEMINI_API_KEY ထည့်ပေးရန် လိုအပ်ပါသည်!")

# Telegram Bot နဲ့ Gemini ကို Initialize လုပ်ခြင်း
bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# Gemini Model ကို VPN/Digital Product တွေအတွက် Custom Assistant အဖြစ် စနစ်တကျ ညွှန်ကြားခြင်း
system_instruction = """
You are an elite, sharp Personal Business Assistant for a young digital merchant selling VPNs and digital products. 
When the user sends their daily business metrics (e.g., ad spend, conversions, revenue, customer messages, or ROI):
1. Analyze the performance sharply (identify wins, leaks, or trends).
2. Deliver a concise, structured 'Daily Business Briefing'.
3. End with a high-energy, actionable, and hyped 'Motivation Message' to fuel their hustle for the day. 
Use a professional yet friendly, inspiring tone with cool emojis (🤘🔥🚀). Keep it punchy and impactful!
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤘 **Hello Boss! I am your Daily Business Assistant.**\n\n"
        "ဒီနေ့အတွက် Business Metrics တွေကို ပို့ပေးလို့ရပါပြီ။\n"
        "*(ဥပမာ - Ad spend: 20,000 MMK, Messages: 50, Sales: 15, Revenue: 100,000 MMK)*\n\n"
        "Data တွေကို သုံးသပ်ပြီး Business Briefing နဲ့ Motivation Message ကို ချက်ချင်း ထုတ်ပေးပါမယ်!"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_metrics(message):
    # AI စဥ်းစားနေတုန်း Telegram မှာ 'typing...' ဆိုပြီး ပြထားပေးပါမယ်
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        # User ပို့လိုက်တဲ့ Metrics ကို Gemini ဆီပို့ပြီး ဖြေခိုင်းပါမယ်
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error processing with AI: {str(e)}")

if __name__ == "__main__":
    print("🤖 Bot is running on Railway...")
    bot.infinity_polling()
