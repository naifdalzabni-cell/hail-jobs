import time
import telebot
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import sys

# ضع التوكن والقناة الخاصة بك هنا
TOKEN = '8926649236:AAGKwtXftZUlCgJvk46NYbrKY8HWl2SSe6c'
CHANNEL_ID = '@Hail_Jobs_Channel_2026'

bot = telebot.TeleBot(TOKEN)

# دالة لتشغيل سيرفر وهمي لإرضاء Render
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Bot is running!')

def run_web_server():
    server_address = ('0.0.0.0', 10000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("سيرفر الويب الوهمي يعمل الآن...", flush=True)
    httpd.serve_forever()

# دالة فحص وجلب الوظائف
def check_jobs():
    print("جاري تشغيل البوت وفحص الوظائف...", flush=True)

# حلقة التكرار اللانهائية لتبقى البوت حياً على السيرفر
def bot_loop():
    print("محاولة إرسال رسالة التجربة إلى القناة...", flush=True)
    try:
        # إرسال الرسالة التجريبية مع إجبار الطباعة فوراً
        bot.send_message(CHANNEL_ID, "🟢 تم تشغيل رادار وظائف حائل بنجاح! البوت الآن متصل ويبحث عن الوظائف.")
        print("✅ نجاح: تم إرسال رسالة التجربة إلى القناة بنجاح!", flush=True)
    except Exception as e:
        print(f"❌ فشل الإرسال: حدث خطأ أثناء إرسال الرسالة. السبب: {e}", flush=True)

    print("...البوت بدأ العمل بنجاح ويبدأ الفحص الدوري...", flush=True)
    while True:
        check_jobs()
        time.sleep(3600)  # الفحص كل ساعة

if __name__ == "__main__":
    # تشغيل السيرفر الوهمي في خلفية منفصلة
    web_thread = threading.Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()
    
    # تشغيل حلقة البوت الأساسية
    bot_loop()
