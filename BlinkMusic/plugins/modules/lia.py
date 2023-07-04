import requests
import os
from BlinkMusic import app
from pyrogram import filters


@app.on_message(filters.command("deezer"))
def download_music(_, message):
    query = message.text.split(" ", 1)[1]  # Kullanıcının gönderdiği mesajdan sorguyu alıyoruz

    # Deezer API'ye istek atarak müzikleri arıyoruz
    response = requests.get(f"https://api.deezer.com/search?q={query}")

    if response.status_code == 200:
        data = response.json()

        if data.get("data"):
            track = data["data"][0]  # İlk müziği seçiyoruz
            title = track["title"]
            artist = track["artist"]["name"]
            audio_url = track["preview"]

            # Müziği indiriyoruz
            r = requests.get(audio_url, stream=True)
            if r.status_code == 200:
                with open(f"{title}.mp3", "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        f.write(chunk)

                # İndirme başarılı olduğunda kullanıcıya geri bildirim gönderiyoruz
                message.reply_text(f"**{title}** adlı şarkı {artist} tarafından indirildi.")
                # İndirilen müziği göndermek için aşağıdaki satırı da ekleyebilirsiniz
                # message.reply_audio(f"{title}.mp3")
                
                # İndirilen müziği silmek için aşağıdaki satırı ekleyebilirsiniz
                # os.remove(f"{title}.mp3")
            else:
                message.reply_text("Müzik indirilemedi.")
        else:
            message.reply_text("Aradığınız müzik bulunamadı.")
    else:
        message.reply_text("Deezer API'ye erişilemiyor.")
