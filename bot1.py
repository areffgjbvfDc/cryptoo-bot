import os
import subprocess
import sys
import time

def install_packages():
    try:
        import requests
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

install_packages()
import requests

TELEGRAM_BOT_TOKEN = "8894458160:AAF-BzFii0WywRL_xA2VO6Y-NIiZKvL-y7c"
TELEGRAM_CHAT_ID = "8941826013"

def get_real_market_data_and_calculate():
    """دریافت قیمت‌های لایو واقعی از بازار و محاسبه دقیق ریاضی اهداف ۵۰٪+"""
    try:
        # دریافت قیمت‌های زنده از صرافی کوین‌گکو
        url = "https://api.coingecko.com/api/v3/simple/price?ids=sui,jupiter-exchange,pepe,solana,render-token,near&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=8)
        
        if response.status_code == 200:
            data = response.json()
            
            assets = [
                {"name": "SUI / Layer 1", "id": "sui"},
                {"name": "JUP / DeFi", "id": "jupiter-exchange"},
                {"name": "PEPE / Meme", "id": "pepe"},
                {"name": "NEAR / Layer 1", "id": "near"}
            ]
            
            report = ""
            count = 1
            
            for item in assets:
                coin_info = data.get(item["id"], {})
                current_price = coin_info.get("usd")
                change_24h = coin_info.get("usd_24h_change")
                
                if current_price is not None and change_24h is not None:
                    # محاسبه دقیق ریاضی برای سود ۵۰ درصدی و حد ضرر استاندارد
                    entry_price = current_price
                    target_price = entry_price * 1.52 # دقیقاً ۵۲ درصد بالاتر برای پوشش کارمزد و تحقق ۵۰٪ سود
                    stop_loss = entry_price * 0.88   # حد ضرر منطقی ۱۲ درصدی
                    
                    report += (
                        f"🔹 **فرصت شماره {count}:**\n"
                        f"🎯 **نام ارز:** {item['name']}\n"
                        f"📊 **تغییرات ۲۴ ساعته:** {change_24h:.2f}%\n"
                        f"🟢 **نقطه ورود (قیمت لایو دقیق):** `${entry_price:,.8f}`\n"
                        f"🔴 **سقف هدف (سود ۵۲٪):** `${target_price:,.8f}`\n"
                        f"⚠️ **حد ضرر فرمولی:** `${stop_loss:,.8f}`\n"
                        f"⏳ **تایم‌فریم محاسباتی:** ۳ تا ۵ روز\n\n"
                    )
                    count += 1
                    if count > 3:
                        break
            if report:
                return report.strip()
    except Exception as e:
        print(f"خطا در دریافت داده‌های لایو: {e}")
        
    return "⚠️ خطا در اتصال به سرور قیمت‌های لایو. لطفاً چند لحظه دیگر دوباره اسکن کنید."

def send_telegram_message_with_keyboard(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    inline_keyboard = {
        "inline_keyboard": [
            [{"text": "🔄 اسکن مجدد و محاسبه لایو قیمت‌ها", "callback_data": "get_new_signals"}]
        ]
    }
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "reply_markup": inline_keyboard
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"خطا در ارسال تلگرام: {e}")

def main():
    print("🚀 ربات اسکنر کاملاً فرمولی و قیمت لایو فعال شد...")
    send_telegram_message_with_keyboard("📡 **سیستم محاسبه‌گر دقیق و قیمت لایو فعال شد.**\n💡 از این به بعد هیچ عدد و رقمی تخمینی نیست؛ قیمت‌ها کاملاً از بازار زنده خوانده شده و نقاط ورود و هدف با **فرمول‌های ریاضیِ دقیق** حساب می‌شوند!")
    
    offset = 0
    last_auto_time = time.time()
    auto_interval = 21600
    
    while True:
        current_time = time.time()
        
        if current_time - last_auto_time >= auto_interval:
            signals = get_real_market_data_and_calculate()
            full_message = f"🚨 **سبد محاسباتی قیمت‌های لایو (سود ۵۰٪+)** 💎\n----------------------------------------\n\n{signals}\n----------------------------------------\n⚠️ *محاسبات کاملاً بر اساس قیمت لحظه‌ای صرافی است.*"
            send_telegram_message_with_keyboard(full_message)
            last_auto_time = current_time

        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={offset}&timeout=5"
            response = requests.get(url, timeout=10).json()
            
            if "result" in response:
                for update in response["result"]:
                    offset = update["update_id"] + 1
                    
                    if "callback_query" in update:
                        query = update["callback_query"]
                        query_id = query["id"]
                        chat_id = str(query["message"]["chat"]["id"])
                        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery", json={"callback_query_id": query_id})
                        
                        if chat_id == TELEGRAM_CHAT_ID:
                            send_telegram_message_with_keyboard("🔄 **در حال دریافت قیمت‌های دقیق لایو و محاسبه ریاضی اهداف...**")
                            signals = get_real_market_data_and_calculate()
                            full_message = f"🎯 **سبد جدید محاسباتی بازار (سود ۵۰٪+)** 🚀\n----------------------------------------\n\n{signals}\n----------------------------------------\n⚠️ *محاسبه‌شده بر اساس قیمت لحظه‌ای.*"
                            send_telegram_message_with_keyboard(full_message)
                            
                    elif "message" in update and "text" in update["message"]:
                        msg = update["message"]
                        chat_id = str(msg["chat"]["id"])
                        text = msg["text"].strip().lower()
                        
                        if chat_id == TELEGRAM_CHAT_ID:
                            if "signal" in text or "سیگنال" in text or "/start" in text:
                                send_telegram_message_with_keyboard("🔄 **در حال دریافت قیمت‌های دقیق لایو و محاسبه ریاضی اهداف...**")
                                signals = get_real_market_data_and_calculate()
                                full_message = f"🎯 **سبد جدید محاسباتی بازار (سود ۵۰٪+)** 🚀\n----------------------------------------\n\n{signals}\n----------------------------------------\n⚠️ *محاسبه‌شده بر اساس قیمت لحظه‌ای.*"
                                send_telegram_message_with_keyboard(full_message)
        except Exception as e:
            print(f"خطا: {e}")
            
        time.sleep(3)

if __name__ == "__main__":
    main()
