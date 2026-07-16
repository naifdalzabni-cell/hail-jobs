import time
import telebot

# ضع التوكن والقناة الخاصة بك هنا
TOKEN = '8926649236:AAGKwtXftZUICgJvk46NYbrKY8HWl2SSe6c'
CHANNEL_ID = '@Hail_Jobs_Channel_2026'

bot = telebot.TeleBot(TOKEN)

# دالة فحص وجلب الوظائف
def check_jobs():
    print("...جاري تشغيل البوت وفحص الوظائف")
    try:
        # هنا يوضع كود سحب الوظائف الخاص بك
        # مثال:
        # new_jobs = fetch_latest_jobs()
        # if new_jobs:
        #     for job in new_jobs:
        #         bot.send_message(CHANNEL_ID, job)
        print(".لم يتم العثور على وظائف جديدة في هذا الفحص")
    except Exception as e:
        print(f"حدث خطأ أثناء الفحص: {e}")

# حلقة التكرار اللانهائية لتبقي البوت حياً على السيرفر
if __name__ == "__main__":
    print("البوت بدأ العمل بنجاح...")
    while True:
        check_jobs()
        # الفحص كل ساعة (3600 ثانية) - يمكنك تعديل الوقت كما تحب
time.sleep(3600)
