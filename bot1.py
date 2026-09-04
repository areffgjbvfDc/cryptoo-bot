import sys
import subprocess

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
        url = "https://api.coingecko.com/api/v3/simple/price?ids=sui,jupiter-exchange,pepe,solana,render-token,near&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=10)
        
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
                    entry_price = current_price
                    target_price = entry_price * 1.52
                    stop_loss = entry_price * 0.88
                    
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
        
    return "⚠️ خطا در اتصال به سرور قیمت‌های لایو."

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"خطا در ارسال تلگرام: {e}")

def main():
    print("🚀 اسکن خودکار بازار شروع شد...")
    signals = get_real_market_data_and_calculate()
    full_message = (
        f"🚨 **گزارش خودکار بازار (سود ۵۰٪+)** 💎\n"
        f"----------------------------------------\n\n"
        f"{signals}\n"
        f"----------------------------------------\n"
        f"🤖 *این پیام به صورت کاملاً خودکار هر ۵ دقیقه ارسال می‌شود.*"
    )
    send_telegram_message(full_message)

if __name__ == "__main__":
    main()
