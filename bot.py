import time
import telebot
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

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
    print("سيرفر الويب الوهمي يعمل الآن...")
    httpd.serve_forever()

# دالة فحص وجلب الوظائف
def check_jobs():
    print("جاري تشغيل البوت وفحص الوظائف...")
    try:
        # هنا يوضع كود سحب الوظائف الخاص بك
        # مثال:
        # new_jobs = fetch_latest_jobs()
        pass
    except Exception as e:
        print(f"حدث خطأ أثناء الفحص: {e}")

# حلقة التكرار اللانهائية لتبقى البوت حياً على السيرفر
def bot_loop():
    # إرسال رسالة تجريبية للقناة للتأكد من الربط والتشغيل
    try:
        bot.send_message(CHANNEL_ID, "🟢 تم تشغيل رادار وظائف حائل بنجاح! البوت الآن متصل ويبحث عن الوظائف.")
        print("تم إرسال رسالة التجربة إلى القناة بنجاح!")
    except Exception as e:
        print(f"فشل إرسال رسالة التجربة إلى القناة: {e}")

    print("...البوت بدأ العمل بنجاح")
    while True:
        check_jobs()
        time.sleep(3600)  # الفحص كل ساعة (3600 ثانية)

if __name__ == "__main__":
    # تشغيل السيرفر الوهمي في خلفية منفصلة لتجنب خطأ Port timeout
    web_thread = threading.Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()
    
    # تشغيل حلقة البوت الأساسية
    bot_loop()
