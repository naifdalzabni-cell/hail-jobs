import time
import requests
from bs4 import BeautifulSoup
import telebot
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

# 1. توكن البوت الخاص بك
BOT_TOKEN = '8926649236:AAGKwtXftZUIcGjvk46NYbrKYBHWl2SSe6c' 

# 2. معرف قناتك على تليجرام
CHANNEL_ID = '@Hail_Jobs_Channel_2026'

bot = telebot.TeleBot(BOT_TOKEN)

# دالة لتشغيل سيرفر وهمي لتجنب إغلاق موقع Render للخدمة
def run_dummy_server():
    class DummyHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Bot is running successfully!")

    # Render يرسل بورت تلقائي في المتغير البيئي PORT
    import os
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    print(f"سيرفر البوت الوهمي يعمل على منفذ: {port}")
    server.serve_forever()

def get_hail_jobs():
    jobs_list = []
    try:
        url = "https://www.ewdifh.com/jobs/search/%D8%AD%D8%A7%D8%A6%D9%84"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            job_elements = soup.find_all('div', class_='job-box')
            if not job_elements:
                job_elements = soup.find_all('a', href=True)
                
            for element in job_elements[:5]:
                title = element.text.strip()
                link = element.get('href', '')
                if 'حائل' in title or 'Hail' in title:
                    if link and not link.startswith('http'):
                        link = "https://www.ewdifh.com" + link
                    jobs_list.append({"title": title, "link": link})
    except Exception as e:
        print(f"حدث خطأ أثناء فحص الموقع: {e}")
    return jobs_list

def start_bot_loop():
    print("تم تشغيل رادار حائل للوظائف...")
    # إرسال رسالة ترحيبية لمرة واحدة عند بداية التشغيل
    try:
        bot.send_message(
            CHANNEL_ID, 
            "⚡ **تم تشغيل رادار وظائف حائل بنجاح!**\n\nالبوت يعمل الآن بشكل مستمر وسيقوم بفحص الوظائف تلقائياً كل ساعة."
        )
    except Exception as e:
        print(f"خطأ في إرسال رسالة الترحيب: {e}")

    # حلقة تكرار لانهائية تفحص كل ساعة
    while True:
        print("جاري فحص الوظائف الآن...")
        jobs = get_hail_jobs()
        if jobs:
            for job in jobs:
                message = f"📌 **وظيفة جديدة في حائل:**\n\n🎯 {job['title']}\n\n🔗 تفاصيل التقديم:\n{job['link']}"
                try:
                    bot.send_message(CHANNEL_ID, message)
                    time.sleep(3)
                except Exception as e:
                    print(f"خطأ في إرسال الوظيفة: {e}")
        else:
            print("لم يتم العثور على وظائف جديدة في هذا الفحص.")
        
        # الانتظار لمدة ساعة كاملة (3600 ثانية) قبل الفحص التالي
        print("في انتظار الفحص القادم بعد ساعة...")
        time.sleep(3600)

if __name__ == "__main__":
    # تشغيل السيرفر الوهمي في خلفية النظام
    server_thread = threading.Thread(target=run_dummy_server)
    server_thread.daemon = True
    server_thread.start()
    
    # تشغيل حلقة فحص البوت الأساسية
    start_bot_loop()
