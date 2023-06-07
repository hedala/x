from BlinkMusic import app

from pyrogram import filters

message_cache = {}

@app.on_message(filters.command("id"))

def handle_ids(_, message):

    reply = message.reply_to_message

    total_messages = app.get_chat_members_count(message.chat.id)

    if reply:

        result = (

            f"**Bu senin kimliğin**: `{message.from_user.id}`\n**{reply.from_user.first_name}'s ɪᴅ**: `{reply.from_user.id}`\n**Bu grubun kimliği**: `{message.chat.id}`\n**Toplam gönderdiğin mesaj sayısı**: `{total_messages}`"

        )

    else:

        result = (

            f"**Bu senin kimliğin**: `{message.from_user.id}`\n**Bu grubun kimliği**: `{message.chat.id}`\n**Toplam gönderdiğin mesaj sayısı**: `{total_messages}`"

        )

    message.reply_text(result)

@app.on_message(filters.command("heda"))

def handle_heda(_, message):

    keyword = message.text.split(maxsplit=1)[1].lower()

    chat_id = message.chat.id

    chat_username = message.chat.username

    if keyword in message_cache:

        last_used_message = message_cache[keyword][-1]

        last_used_message_id = last_used_message.message_id

        

        if chat_username:

            last_used_message_link = f"https://t.me/{chat_username}/{last_used_message_id}"

        else:

            last_used_message_link = f"https://t.me/c/{group_id}/{last_used_message_id}"

        

        message.reply_text(

            f"**Son kullanılan mesaj**: [burada]({last_used_message_link})"

        )

        

        # Son 5 kullanımı kontrol etmek için ilgili mesajların bağlantılarını al

        recent_usages = message_cache[keyword][-5:]

        recent_usages_links = []

        

        for msg in recent_usages:

            message_id = msg.message_id

            if chat_username:

                link = f"https://t.me/{chat_username}/{message_id}"

            else:

                link = f"https://t.me/c/{group_id}/{message_id}"

            

            recent_usages_links.append(link)

        

        recent_usages_text = "\n".join(f"[Mesaj {i+1} burada]({link})" for i, link in enumerate(recent_usages_links))

        message.reply_text(f"**Son 5 kullanım**: {recent_usages_text}")

    else:

        message.reply_text("Bu kelime grup içinde kullanılmamış.")



@app.on_message(filters.text)

def update_message_cache(_, message):

    words = message.text.lower().split()

    chat_id = message.chat.id

    for word in words:

        if word in message_cache:

            # Kelimenin son kullanımı güncelle

            message_cache[word].append(message)

        else:

            # Kelimenin ilk kullanımını ekle

            message_cache[word] = [message]

@app.on_deleted_messages()

def clear_message_cache(_, messages):

    global message_cache

    for message in messages:

        for word, cached_messages in message_cache.copy().items():

            for cached_message in cached_messages:

                if cached_message.message_id == message.message_id:

                    cached_messages.remove(cached_message)

            if not cached_messages:

                del message_cache[word]
