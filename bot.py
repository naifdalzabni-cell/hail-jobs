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
    print("🔎 رادار جوجل يبحث الآن في الويب عن وظائف حائل النشطة...", flush=True)
    try:
        # البحث بكلمة عامة تضمن جلب إعلانات التقديم المتاحة حالياً
        query = 'وظائف حائل'
        encoded_query = urllib.parse.quote(query)
        
        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ar&gl=SA&ceid=SA:ar"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        
        found_any = False
        
        # كلمات دلالية ممتازة تدل على وجود تقديم وظيفي حقيقي
        job_keywords = [
            "وظيفة", "وظائف", "تقديم", "توظيف", "شاغرة", "حراسات", "أمن", "عسكرية", 
            "مطلوب", "تعلن", "يعلن", "فرص", "شاغر", "بند", "شواغر", "مسابقة", "تعيين", 
            "رواتب", "وظايف", "طرح", "شغل", "توظف"
        ]
        
        # كلمات ممنوعة تشمل الأخبار الحكومية، الاستقبالات، الحوادث، والأمور الرسمية غير التوظيفية
        exclude_keywords = [
            "وفاة", "حادث", "طقس", "أمطار", "سمو", "الأمير", "زيارة", "افتتاح", 
            "تدشين", "ندوة", "بطولة", "مباراة", "حريق", "مرور", "قبض", "ضبط",
            "يستقبل", "استقبل", "يبحث سير", "العمل والخطط", "مدير شرطة", "أمير حائل",
            "نائب أمير", "يرعى", "إمارة", "الدفاع المدني يخمد", "لقاء", "اجتماع"
        ]
        
        # مسح نتائج البحث
        for item in root.findall('.//item')[:25]: # فحص أعمق لأول 25 نتيجة
            title = item.find('title').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
            
            # 1. التأكد من أن الإعلان يخص حائل
            has_location = any(word in title for word in ["حائل", "حايل"])
            
            # 2. التأكد من وجود كلمة تدل على وظيفة
            has_job_keyword = any(word in title for word in job_keywords)
            
            # 3. التأكد من خلو العنوان تماماً من الكلمات الإخبارية والرسمية الممنوعة
            has_exclude_keyword = any(word in title for word in exclude_keywords)
            
            # 4. فلترة تاريخ النشر (نستبعد فقط السنوات القديمة جداً 2021 و 2022 و 2023 و 2024)
            # وبذلك نسمح بظهور إعلانات 2025 المستمرة و 2026 الجديدة
            is_very_old = any(old_year in pub_date or old_year in title for old_year in ["2021", "2022", "2023", "2024"])
            
            # تشغيل الفلتر الذكي المطور والمستقر
            if has_location and has_job_keyword and not has_exclude_keyword and not is_very_old:
                found_any = True
                if link not in sent_jobs:
                    sent_jobs.add(link)
                    
                    message = f"🎯 **وظيفة جديدة مكتشفة في حائل!**\n\n" \
                              f"📌 **الإعلان:** {title}\n\n" \
                              f"🔗 **رابط التفاصيل والتقديم:**\n{link}\n\n" \
                              f"🤖 _رادار حائل الذكي_"
                    
                    bot.send_message(CHANNEL_ID, message, parse_mode='Markdown')
                    print(f"✅ تم نشر وظيفة حقيقية ونشطة: {title}", flush=True)
                    time.sleep(2)
                    
        if not found_any:
            print("💤 لم نجد إعلانات توظيف جديدة وحصريّة حالياً تفي بالشروط المحدثة.", flush=True)
            
    except Exception as e:
        print(f"❌ حدث خطأ أثناء بحث جوجل: {e}", flush=True)

# حلقة التكرار الأساسية للبوت
def bot_loop():
    try:
        bot.send_message(CHANNEL_ID, "🟢 تم تحديث رادار حائل! البوت الحين مبرمج بمرونة أكبر ليصيد وظائف 2025 المتاحة و 2026 الجديدة مع استبعاد الإعلانات القديمة جداً.")
    except Exception as e:
        print(f"❌ فشل إرسال رسالة التشغيل: {e}", flush=True)

    while True:
        google_search_hail_jobs()
        print("🕒 في وضع الانتظار لمدة ساعتين قبل مسح الويب القادم...", flush=True)
        time.sleep(7200)

if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()
    
    bot_loop()
