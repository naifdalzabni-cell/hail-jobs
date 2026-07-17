import time
import telebot
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# التوكن وقناة حائل الخاصة بك
TOKEN = '8926649236:AAGKwtXftZUICgJvk46NYbrKY8HWl2SSe6c'
CHANNEL_ID = '@Hail_Jobs_Channel_2026'

bot = telebot.TeleBot(TOKEN)

# قائمة بالروابط المرسلة سابقاً لمنع التكرار
sent_jobs = set()

# سيرفر وهمي لإبقاء البوت نشطاً على Render
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hail Google Radar is Active!')

def run_web_server():
    server_address = ('0.0.0.0', 10000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

# دالة البحث الشامل باستخدام خلاصة بحث Google للوظائف في حائل
def google_search_hail_jobs():
    print("🔎 رادار جوجل يبحث الآن في الويب عن وظائف حائل الفعلية فقط...", flush=True)
    try:
        # استعلام البحث لجوجل للتركيز على وظائف منطقة حائل
        query = 'وظائف حائل'
        encoded_query = urllib.parse.quote(query)
        
        # استخدام خلاصة أخبار جوجل للبحث بلحظتها في كل المواقع والمنصات
        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ar&gl=SA&ceid=SA:ar"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        
        found_any = False
        
        # كلمات دلالية واسعة جداً تدل على وجود فرصة عمل (لن تفوت أي وظيفة بإذن الله)
        job_keywords = [
            "وظيفة", "وظائف", "تقديم", "توظيف", "شاغرة", "حراسات", "أمن", "عسكرية", 
            "مطلوب", "تعلن", "يعلن", "فرص", "شاغر", "بند", "شواغر", "مؤسسة", "شركة", 
            "مسابقة", "تعيين", "رواتب", "وظايف", "طرح", "شغل", "توظف"
        ]
        
        # كلمات ممنوعة تدل على أنها مجرد أخبار عامة وليست فرصة تقديم
        exclude_keywords = [
            "وفاة", "حادث", "طقس", "أمطار", "سمو", "الأمير", "زيارة", "افتتاح", 
            "تدشين", "ندوة", "بطولة", "مباراة", "حريق", "مرور", "قبض", "ضبط"
        ]
        
        # مسح نتائج البحث من كل المواقع عبر الإنترنت
        for item in root.findall('.//item')[:20]:  # فحص أول 20 نتيجة بحث حديثة
            title = item.find('title').text
            link = item.find('link').text
            
            # 1. التأكد من أن الإعلان يخص حائل
            has_location = any(word in title for word in ["حائل", "حايل"])
            
            # 2. التأكد من وجود كلمة تدل على وظيفة
            has_job_keyword = any(word in title for word in job_keywords)
            
            # 3. التأكد من خلو العنوان من الكلمات الإخبارية العامة
            has_exclude_keyword = any(word in title for word in exclude_keywords)
            
            # تشغيل الفلتر الذكي
            if has_location and has_job_keyword and not has_exclude_keyword:
                found_any = True
                if link not in sent_jobs:
                    sent_jobs.add(link)
                    
                    # صياغة رسالة الرادار الشامل بوضوح واحترافية
                    message = f"🎯 **وظيفة جديدة مكتشفة في حائل!**\n\n" \
                              f"📌 **الإعلان:** {title}\n\n" \
                              f"🔗 **رابط التفاصيل والتقديم:**\n{link}\n\n" \
                              f"🤖 _رادار حائل يمسح الويب على مدار الساعة_"
                    
                    bot.send_message(CHANNEL_ID, message, parse_mode='Markdown')
                    print(f"✅ تم نشر وظيفة حقيقية: {title}", flush=True)
                    time.sleep(2)
                    
        if not found_any:
            print("💤 تم فحص الويب بنجاح، ولم نجد إعلانات توظيف جديدة تخص حائل حالياً.", flush=True)
            
    except Exception as e:
        print(f"❌ حدث خطأ أثناء بحث جوجل: {e}", flush=True)

# حلقة التكرار الأساسية للبوت
def bot_loop():
    # رسالة التنبيه الفوري بالتشغيل
    try:
        bot.send_message(CHANNEL_ID, "🟢 تم تشغيل رادار حائل الذكي! البوت الآن متصل ويبحث عن (الوظائف الحقيقية فقط) ويستبعد الأخبار العامة...")
    except Exception as e:
        print(f"❌ فشل إرسال رسالة التشغيل: {e}", flush=True)

    while True:
        # فحص الإنترنت فوراً
        google_search_hail_jobs()
        
        # فحص الإنترنت كل ساعتين (7200 ثانية) للحصول على أفضل النتائج وتفادي تكرار الفحص السريع
        print("🕒 في وضع الانتظار لمدة ساعتين قبل مسح الويب القادم...", flush=True)
        time.sleep(7200)

if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()
    
    bot_loop()
