import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- الإعدادات الأساسية ---
TOKEN = '8848314386:AAFWmAnoRVtVw1mBI2cBU9dV4kNgBsi0sVQ'
ADMIN_ID = 8954030421  # ضع الآيدي الخاص بك هنا

bot = telebot.TeleBot(TOKEN)

# --- رسالة الترحيب ---
@bot.message_handler(commands=['start'])
def welcome_message(message):
    if message.chat.id == ADMIN_ID:
        bot.reply_to(message, "☑️ <b>تم تسجيل الدخول بصلاحيات الإدارة (Prime)</b>\n\n🛡️ البوت جاهز الآن لاستقبال الرسائل وتشفيرها.", parse_mode="HTML")
    else:
        bot.reply_to(message, "أهلاً بك في بوت التواصل الرسمي ☑️\n\nأرسل رسالتك هنا وستصل للإدارة بسرية تامة 🛡️\n\n<i>(ملاحظة: النظام محمي وموثق لحفظ حقوق الجميع 💎)</i>", parse_mode="HTML")

# --- استقبال رسائل المستخدمين وإنشاء زر الرد للآدمن ---
@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID)
def handle_anonymous_message(message):
    user_id = message.from_user.id
    # إذا لم يكن لديه يوزر، نظهر كلمة "مخفي" لزيادة طابع الخصوصية
    username = f"@{message.from_user.username}" if message.from_user.username else "مخفي 🔒"
    
    admin_text = (
        f"💎 <b>رسالة واردة (نظام برايم)</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👤 <b>اليوزر:</b> {username}\n"
        f"🆔 <b>الآيدي:</b> <code>{user_id}</code> ☑️\n\n"
        f"📝 <b>النص:</b>\n{message.text}\n"
        f"━━━━━━━━━━━━━━━━"
    )
    
    # إنشاء زر الرد الشفاف بشكل برايم
    markup = InlineKeyboardMarkup()
    reply_button = InlineKeyboardButton("💠 رد سريع (Prime) 💠", callback_data=f"reply_{user_id}")
    markup.add(reply_button)
    
    # إرسال الرسالة للآدمن
    bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML", reply_markup=markup)
    
    # تأكيد فخم للمستخدم
    bot.reply_to(message, "☑️ <b>تمت العملية:</b> تم إرسال رسالتك للإدارة بنجاح وفي بيئة آمنة 🛡️.", parse_mode="HTML")

# --- التفاعل عند ضغط الآدمن على زر الرد ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def handle_reply_button(call):
    user_id = call.data.split("_")[1]
    
    msg = bot.send_message(call.message.chat.id, "✍️ <b>وضع الرد مفعل ☑️:</b>\n(أرسل النص الآن ليتم تحويله فوراً)", parse_mode="HTML")
    bot.register_next_step_handler(msg, send_reply_to_user, user_id)
    
    bot.answer_callback_query(call.id)

# --- إرسال نص الآدمن إلى المستخدم ---
def send_reply_to_user(message, user_id):
    if message.text: 
        # رسالة الرد التي ستصل للمستخدم بشكل رسمي
        user_msg = f"💎 <b>إشعار رسمي من الإدارة ☑️:</b>\n\n{message.text}"
        try:
            bot.send_message(user_id, user_msg, parse_mode="HTML")
            bot.reply_to(message, "☑️ <b>تم توصيل الرد بنجاح 💎</b>", parse_mode="HTML")
        except Exception as e:
            bot.reply_to(message, f"⚠️ خطأ في الإرسال (ربما قام المستخدم بحظر البوت): {e}")
    else:
        bot.reply_to(message, "⚠️ النظام يقبل النصوص فقط. اضغط على زر الرد مجدداً للمحاولة.")

# --- تشغيل البوت ---
print("تم تشغيل نظام Prime بنجاح...")
bot.infinity_polling()