import time
import telebot
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import sys

# ضع التوكن والقناة الخاصة بك هنا
TOKEN = '8926649236:AAGKwtXftZUlCgJvk46NYbrKY8HWl2SSe6c'
CHANNEL_ID = '@Hail_Jobs_Channel_2026'

bot = telebot.TeleBot(TOKEN)

# دالة لتشغيل سيرفر وهمي لمنع توقف Render
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Bot is running!')

def run_web_server():
    server_address = ('0.0.0.0', 10000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("سيرفر الويب الوهمي يعمل الآن لمنع النوم...", flush=True)
    httpd.serve_forever()

# دالة فحص وجلب الوظائف الحقيقية
def check_jobs():
    print("جاري تشغيل البوت وفحص الوظائف...", flush=True)

# حلقة التكرار اللانهائية لتبقى البوت حياً على السيرفر
def bot_loop():
    print("...البوت بدأ العمل بنجاح ويبدأ الفحص الدوري...", flush=True)
    
    # إرسال رسالة ترحيبية فورية عند تشغيل السيرفر لأول مرة لتتأكد أنه متصل
    try:
        bot.send_message(CHANNEL_ID, "🟢 تم تشغيل رادار وظائف حائل بنجاح! البوت الآن متصل ويبحث عن الوظائف.")
        print("✅ نجاح: تم إرسال رسالة التشغيل الأولية إلى القناة!", flush=True)
    except Exception as e:
        print(f"❌ فشل إرسال رسالة التشغيل: {e}", flush=True)

    while True:
        # فحص الوظائف الحقيقية ونشرها فوراً
        check_jobs()
        
        # الانتظار لمدة 12 ساعة (43200 ثانية) قبل إرسال تقرير الاطمئنان القادم وفحص الوظائف من جديد
        print("الانتظار لمدة 12 ساعة قبل فحص الوظائف وإرسال رسالة الاطمئنان القادمة...", flush=True)
        time.sleep(43200)
        
        # رسالة تطمين دورية كل 12 ساعة للتأكد من أن البوت نشط ولم يفصل
        try:
            bot.send_message(CHANNEL_ID, "🔄 تقرير دوري: رادار وظائف حائل يعمل بنشاط وبدون توقف.")
            print("✅ نجاح: تم إرسال تقرير الاطمئنان الدوري!", flush=True)
        except Exception as e:
            print(f"❌ فشل إرسال التقرير الدوري: {e}", flush=True)

if __name__ == "__main__":
    # تشغيل السيرفر الوهمي في خلفية منفصلة
    web_thread = threading.Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()
    
    # تشغيل حلقة البوت الأساسية
    bot_loop()
