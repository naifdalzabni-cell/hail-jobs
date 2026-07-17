import time
import telebot
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from datetime import datetime, timedelta

# التوكن وقناة حائل
TOKEN = '8926649236:AAGKwtXftZUICgJvk46NYbrKY8HWl2SSe6c'
CHANNEL_ID = '@Hail_Jobs_Channel_2026'

bot = telebot.TeleBot(TOKEN)
sent_jobs = set()

# سيرفر إبقاء البوت نشطاً
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hail Exclusive Radar is Active!')

def run_web_server():
    server_address = ('0.0.0.0', 10000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

def google_search_hail_jobs():
    print("🔎 رادار الحصريات يبحث في الويب...", flush=True)
    try:
        # بحث مركز ومحدد جداً
        query = 'وظائف حائل'
        encoded_query = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ar&gl=SA&ceid=SA:ar"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        
        # كلمات التوظيف الحصرية
        job_keywords = ["وظيفة", "وظائف", "تقديم", "توظيف", "شاغرة", "مطلوب", "تعلن", "فرص", "تعيين", "شواغر"]
        
        for item in root.findall('.//item')[:20]:
            title = item.find('title').text
            link = item.find('link').text
            
            # فلترة فورية: إعلان يخص حائل + كلمة توظيف + خلوه من أي شيء قديم أو إخباري
            if any(w in title for w in ["حائل", "حايل"]) and any(k in title for k in job_keywords):
                
                # منع التكرار
                if link not in sent_jobs:
                    sent_jobs.add(link)
                    
                    message = f"🚨 **إعلان وظيفي حصري في حائل!**\n\n" \
                              f"📌 **التفاصيل:** {title}\n\n" \
                              f"🔗 **رابط التقديم:**\n{link}\n\n" \
                              f"🤖 _رادار حائل 2026 - حصري وفوري_"
                    
                    bot.send_message(CHANNEL_ID, message, parse_mode='Markdown')
                    print(f"✅ تم نشر: {title}", flush=True)
                    time.sleep(2)
                    
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    bot.send_message(CHANNEL_ID, "🟢 رادار حائل الحصري يعمل الآن.. يرسل الوظائف فقط وبدون أي إعلانات قديمة.")
    while True:
        google_search_hail_jobs()
        time.sleep(3600) # فحص كل ساعة
