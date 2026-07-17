import os
import telebot
import google.generativeai as genai

# Railway Environment Variables ထဲကနေ Key တွေကို လှမ်းယူပါမယ်
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Railway ပေါ်မှာ ချက်ချင်း Crash မဖြစ်စေဘဲ ရှင်းလင်းတဲ့ Error ပြပေးရန်
if not BOT_TOKEN or not GEMINI_API_KEY:
    print("⚠️ ERROR: BOT_TOKEN နှင့် GEMINI_API_KEY ကို Railway Variables တွင် ထည့်ပေးရန် လိုအပ်ပါသည်!")
    exit(1)

# Telegram Bot နှင့် Gemini ကို Initialize လုပ်ခြင်း
bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# All-round Co-pilot အဖြစ် စနစ်တကျ ညွှန်ကြားခြင်း
system_instruction = """
You are an elite, super-smart Personal Assistant and Business Co-pilot for a young digital entrepreneur selling VPNs and digital products.
You handle ANYTHING the user throws at you with sharp intellect, high energy, and loyalty.

How you should react:
1. IF THE USER SENDS BUSINESS METRICS (ad spend, sales, revenue, ROI, customer messages, etc.):
   - Analyze the numbers sharply (identify wins, leaks, or trends).
   - Deliver your signature structured 'Daily Business Briefing'.
   - End with a hyped, actionable 'Motivation Message' (🤘🔥🚀) to fuel their hustle.

2. IF THE USER SENDS ANYTHING ELSE (questions, brainstorming, coding help, casual talk, ideas, problems):
   - Act as a knowledgeable, empathetic peer and expert advisor.
   - Provide direct, clear, and actionable answers without unnecessary fluff.
   - Maintain a supportive, entrepreneurial, and cool tone.

Always match the user's vibe and keep it punchy!
"""

# Model မရခဲ့ရင် အလိုအလျောက် အငြိမ်ဆုံး Model သို့ ပြောင်းပေးမယ့် စနစ်
try:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_instruction
    )
except Exception:
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=system_instruction
    )

# User တစ်ယောက်ချင်းစီရဲ့ Chat History (Memory) ကို မှတ်ထားနိုင်ရန်
user_chats = {}

def get_user_chat(user_id):
    if user_id not in user_chats:
        user_chats[user_id] = model.start_chat(history=[])
    return user_chats[user_id]

@bot.message_handler(commands=['start', 'help', 'reset'])
def send_welcome(message):
    if message.text == '/reset':
        user_chats[message.chat.id] = model.start_chat(history=[])
        bot.reply_to(message, "🔄 **Memory Cleared!** စကားဝိုင်း အသစ်ပြန်စပါပြီ Boss 🤘")
        return

    welcome_text = (
        "🤘 **Hello Boss! I am your All-in-One Personal Co-pilot.**\n\n"
        "ကျွန်တော့်ဆီကို **ကြိုက်တာအကုန်** ပို့လို့ရပါပြီ-\n"
        "📊 **Daily Metrics:** Ad spend, sales, profit တွေ ပို့ပြီး Briefing & Motivation ယူနိုင်သလို\n"
        "💡 **Brainstorm / Ideas:** လုပ်ငန်း အကြံဉာဏ်၊ Marketing strategy တွေ တိုင်ပင်လို့ရပါတယ်\n"
        "💻 **Coding & Tech:** Error ရှင်းတာ၊ Code ရေးခိုင်းတာတွေလည်း လုပ်ပေးပါတယ်\n"
        "💬 **General Chat:** မေးချင်တာရှိရင်လည်း ကြိုက်တဲ့အချိန် မေးလို့ရပါတယ်\n\n"
        "*(စကားပြောထားတာတွေကို မှတ်မိနေမှာဖြစ်လို့ စကားဝိုင်း အသစ်ပြန်စချင်ရင် `/reset` ကို နှိပ်ပါ)*"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        chat_session = get_user_chat(message.chat.id)
        response = chat_session.send_message(message.text)
        
        try:
            bot.reply_to(message, response.text, parse_mode="Markdown")
        except Exception:
            bot.reply_to(message, response.text)
            
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error processing with AI: {str(e)}")

if __name__ == "__main__":
    print("🤖 All-in-One Co-pilot Bot is running on Railway...")
    bot.infinity_polling()
