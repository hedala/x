import requests
from BlinkMusic import app
from pyrogram import filters
import locale
from datetime import datetime
import pytz

@app.on_message(filters.command("coin"))
def get_crypto_price(_, message):
    crypto_symbol = message.text.split(" ", 1)[1].lower()

    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url).json()

    crypto_id = None

    if isinstance(response, list):
        for crypto in response:
            if crypto.get("symbol") == crypto_symbol:
                crypto_id = crypto["id"]
                break
    else:
        message.reply_text("Hata: Geçersiz API yanıtı!")
        return

    if crypto_id:
        if crypto_id.startswith("binance-peg-"):
            crypto_id = crypto_id.replace("binance-peg-", "")

        price_url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
        stats_url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"

        price_response = requests.get(price_url).json()
        stats_response = requests.get(stats_url).json()

        if crypto_id in price_response:
            crypto_price = price_response[crypto_id]["usd"]
            crypto_name = crypto_symbol.upper()

            market_cap = stats_response.get("market_data", {}).get("market_cap", {}).get("usd")
            volume = stats_response.get("market_data", {}).get("total_volume", {}).get("usd")

            # Sayıları okunaklı bir şekilde formatla
            locale.setlocale(locale.LC_ALL, "C")
            formatted_price = locale.format_string("%.2f", crypto_price, grouping=True)
            formatted_market_cap = format_large_number(market_cap) if market_cap else None
            formatted_volume = format_large_number(volume) if volume else None

            reply_text = f"{crypto_name} anlık fiyatı: {formatted_price} USD\n"
            if formatted_market_cap:
                reply_text += f"{crypto_name} piyasa değeri: {formatted_market_cap} USD\n"
            if formatted_volume:
                reply_text += f"{crypto_name} 24 saatlik işlem hacmi: {formatted_volume} USD"

            # Anlık zamanı al ve mesajın sonuna ekle (Türkiye saati)
            istanbul_tz = pytz.timezone("Europe/Istanbul")
            current_time = datetime.now(istanbul_tz).strftime("%H:%M:%S")
            reply_text += f"\n\n**Güncelleme Zamanı:** {current_time}"

            message.reply_text(reply_text)
        else:
            message.reply_text("Hata: Fiyat bilgisi bulunamadı!")
    else:
        message.reply_text("Hata: Kripto birimi bulunamadı!")


def format_large_number(number):
    if number is None:
        return None

    if abs(number) >= 1_000_000_000:
        formatted_number = f"{number / 1_000_000_000:.2f}B"
    elif abs(number) >= 1_000_000:
        formatted_number = f"{number / 1_000_000:.2f}M"
    else:
        formatted_number = f"{number:,.2f}"

    return formatted_number
