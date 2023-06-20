from BlinkMusic import app
from pyrogram import filters

@app.on_message(filters.command("ara"))
def search_message(_, message):
    keyword = message.text.split(" ", 1)[1]  # İlk boşluktan sonraki kısmı alırız, kelimeyi temsil eder
    messages = app.get_chat_history(chat_id=message.chat.id, limit=1000)  # Son 1000 mesajı alırız, isteğe bağlı olarak değiştirilebilir
    
    found_messages = []  # Aranan kelimeyi içeren mesajları saklamak için bir liste oluştururuz
    
    for msg in messages:
        if keyword.lower() in msg.text.lower():  # Mesaj metninde aranan kelimeyi ararız (büyük/küçük harf duyarlı değildir)
            found_messages.append(msg)  # Aranan kelimeyi içeren mesajı listeye ekleriz
    
    if found_messages:
        reply_text = "Aşağıdaki mesajlarda aradığınız kelime bulundu:\n\n"
        for found_msg in found_messages:
            reply_text += f"{found_msg.link}\n"  # Mesajın bağlantısını yanıt metnine ekleriz
    else:
        reply_text = "Aradığınız kelimeyi içeren bir mesaj bulunamadı."
    
    message.reply_text(reply_text)
