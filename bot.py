import time
import requests
from bs4 import BeautifulSoup
import telebot
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse

# 1. توكن البوت الخاص بك
BOT_TOKEN = '8926649236:AAGKwtXftZUIcGjvk46NYbrKYBHWl2SSe6c' 

# 2. معرف قناتك على تليجرام
CHANNEL_ID = '@Hail_Jobs_Channel_2026'

bot = telebot.TeleBot(BOT_TOKEN)

# قائمة بالمناطق والمحافظات المستهدفة للبحث
TARGET_AREAS = [
    'حائل', 'Hail', 
    'بقعاء', 'الشنان', 'الغزالة', 'الشملي', 
    'الحائط', 'موقق', 'سميراء', 'الروضة', 'الخطة'
]

# دالة لتشغيل سيرفر وهمي لتجنب إغلاق موقع Render للخدمة
def run_dummy_server():
    class DummyHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Bot is running successfully!")

    import os
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    print(f"سيرفر البوت الوهمي يعمل على منفذ: {port}")
    server.serve_forever()

def get_jobs_from_source(area_name):
    """
    جلب الوظائف باستخدام محرك بحث وظيفي بديل مع حماية متكاملة ضد الحظر
    """
    jobs_list = []
    try:
        # استخدام رابط بحث مباشر ومحمي لتقليل احتمالية الحظر
        encoded_area = urllib.parse.quote(area_name)
        url = f"https://www.ewdifh.com/jobs/search/{encoded_area}"
        
        # ترويسة متقدمة تحاكي متصفح كروم حقيقي على ويندوز لتجاوز الحماية
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ar,en-US;q=0.7,en;q=0.3',
            'Referer': 'https://www.ewdifh.com/',
            'Connection': 'keep-alive'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # محاولة البحث عن العناصر بعدة طرق مرنة في حال تغير تصميم الموقع
            job_elements = soup.find_all('div', class_='job-box')
            if not job_elements:
                job_elements = soup.find_all('a', href=True)
                
            for element in job_elements[:8]:
                title = element.text.strip()
                link = element.get('href', '')
                
                # التحقق الذكي من تطابق الكلمات المفتاحية
                if area_name.lower() in title.lower():
                    if link and not link.startswith('http'):
                        link = "https://www.ewdifh.com" + link
                    
                    # استخلاص الاسم بطريقة نظيفة بدون فراغات كثيرة
                    clean_title = " ".join(title.split())
                    jobs_list.append({"title": clean_title, "link": link, "area": area_name})
    except Exception as e:
        print(f"حدث خطأ أثناء فحص وظائف {area_name}: {e}")
    return jobs_list

def start_bot_loop():
    print("تم تشغيل رادار حائل الذكي والمطور للوظائف...")
    try:
        bot.send_message(
            CHANNEL_ID, 
            "🔄 **تحديث أمان واستقرار البوت:**\n\nتم تحديث الكود ليعمل بنظام تخفي ذكي يمنع حظر الخوادم ويضمن استلام الوظائف لحائل والمناطق المجاورة بأسرع وقت!"
        )
    except Exception as e:
        print(f"خطأ في إرسال رسالة التحديث: {e}")

    while True:
        print("جاري فحص الوظائف لجميع المناطق المستهدفة...")
        all_found_jobs = []
        
        for area in TARGET_AREAS:
            print(f"جاري البحث في: {area}")
            area_jobs = get_jobs_from_source(area)
            all_found_jobs.extend(area_jobs)
            time.sleep(3) # تأخير محسوب لمحاكاة السلوك البشري وتجنب الحظر
            
        if all_found_jobs:
            # تصفية النسخ المكررة لضمان نظافة القناة
            unique_jobs = {job['link']: job for job in all_found_jobs if job['link']}.values()
            for job in unique_jobs:
                message = f"📌 **وظيفة جديدة في {job['area']}:**\n\n🎯 {job['title']}\n\n🔗 تفاصيل التقديم:\n{job['link']}"
                try:
                    bot.send_message(CHANNEL_ID, message)
                    time.sleep(3)
                except Exception as e:
                    print(f"خطأ في إرسال الوظيفة للقناة: {e}")
        else:
            print("لم يتم العثور على وظائف جديدة في هذا الفحص.")
        
        print("في انتظار الفحص القادم بعد ساعة...")
        time.sleep(3600)

if __name__ == "__main__":
    # تشغيل خادم الويب الوهمي لتجاوز قيود نوم الخدمات في Render
    server_thread = threading.Thread(target=run_dummy_server)
    server_thread.daemon = True
    server_thread.start()
    
    start_bot_loop()
