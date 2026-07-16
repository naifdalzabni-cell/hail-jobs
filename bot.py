import time
import requests
from bs4 import BeautifulSoup
import telebot

# 1. ضع توكن البوت الخاص بك بين القوسين (احصل عليه من BotFather)
BOT_TOKEN = '8926649236:AAGKwtXftZUICgJvk46NYbrKY8HWl2SSe6c' 

# 2. معرف قناتك على تليجرام
CHANNEL_ID = '@Hail_Jobs_Channel_2026'

bot = telebot.TeleBot(BOT_TOKEN)

def get_hail_jobs():
    """
    دالة تقوم بفحص آخر الوظائف المنشورة في منطقة حائل
    """
    jobs_list = []
    try:
        # رابط البحث عن وظائف حائل في موقع أي وظيفة كمصدر موثوق للوظائف
        url = "https://www.ewdifh.com/jobs/search/%D8%AD%D8%A7%D8%A6%D9%84"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # البحث عن عناصر الوظائف في الصفحة
            job_elements = soup.find_all('div', class_='job-box') # بنية افتراضية للموقع
            
            if not job_elements:
                # محاولة أخرى لبنية مختلفة في حال تغير تصميم الموقع
                job_elements = soup.find_all('a', href=True)
                
            for element in job_elements[:5]:  # جلب آخر 5 وظائف فقط لتجنب الإرسال المكرر الكثيف
                title = element.text.strip()
                link = element.get('href', '')
                if 'حائل' in title or 'Hail' in title:
                    if link and not link.startswith('http'):
                        link = "https://www.ewdifh.com" + link
                    jobs_list.append({"title": title, "link": link})
    except Exception as e:
        print(f"حدث خطأ أثناء فحص الموقع: {e}")
    
    return jobs_list

def main():
    print("جاري تشغيل البوت وفحص الوظائف...")
    
    # رسالة ترحيبية للتأكد من عمل البوت بنجاح وارتباطه بالقناة
    try:
        bot.send_message(
            CHANNEL_ID, 
            "⚡ **تم تشغيل رادار وظائف حائل بنجاح!**\n\nالبوت يعمل الآن بشكل تلقائي وسيقوم بجمع ونشر أحدث الفرص الوظيفية في منطقة حائل فور توفرها."
        )
    except Exception as e:
        print(f"تنبيه: لم يتمكن البوت من إرسال رسالة الترحيب بالقناة. تأكد من أن البوت مشرف (Admin) داخل القناة ومعه صلاحية إرسال الرسائل. الخطأ: {e}")

    # جلب الوظائف وإرسالها
    jobs = get_hail_jobs()
    if jobs:
        for job in jobs:
            message = f"📌 **وظيفة جديدة في حائل:**\n\n🎯 {job['title']}\n\n🔗 تفاصيل التقديم:\n{job['link']}"
            try:
                bot.send_message(CHANNEL_ID, message)
                time.sleep(3) # فتره انتظار قصيرة بين الرسائل لمنع الحظر
            except Exception as e:
                print(f"خطأ في إرسال الوظيفة: {e}")
    else:
        print("لم يتم العثور على وظائف جديدة في هذا الفحص.")

if __name__ == "__main__":
    main()
