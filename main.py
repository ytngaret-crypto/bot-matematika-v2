from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import TOKEN
from soal import buat_soal

from database import (
    jawaban,
    game,
    soal_sudah_dijawab,
    tambah_poin,
    ambil_score,
    reset_score,
    restore_score,
    tambah_score_manual,
    hapus_nama_score
)



# ==========================
# START GAME
# ==========================

async def startgame(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id


    restore_score(chat_id)


    game[chat_id] = True


    soal, hasil = buat_soal()


    jawaban[chat_id] = hasil


    soal_sudah_dijawab[chat_id] = False


    await update.message.reply_text(
        f"🎮 GAME DIMULAI!\n\n"
        f"🧮 Soal:\n\n"
        f"{soal} = ?\n\n"
        f"Jawab dengan angka!"
    )



# ==========================
# STOP GAME
# ==========================

async def stopgame(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id


    game[chat_id] = False


    await update.message.reply_text(
        "🛑 Game dihentikan."
    )



# ==========================
# CEK JAWABAN
# ==========================

async def cek(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    user = update.effective_user


    if chat_id not in game:
        return


    if game[chat_id] is False:
        return


    if chat_id not in jawaban:
        return


    try:

        angka = int(update.message.text)

    except:

        return



    if angka == jawaban[chat_id]:


        if soal_sudah_dijawab.get(chat_id, False):

            return


        soal_sudah_dijawab[chat_id] = True



        tambah_poin(
            chat_id,
            user.id,
            user.first_name
        )



        data = ambil_score(chat_id)


        skor = 0


        for uid,nama,poin in data:

            if uid == user.id:

                skor = poin

                break



        await update.message.reply_text(
            f"✅ {user.first_name} menjawab benar!\n"
            f"🏆 Skor kamu: {skor}"
        )



        soal, hasil = buat_soal()


        jawaban[chat_id] = hasil


        soal_sudah_dijawab[chat_id] = False



        await update.message.reply_text(
            f"🧮 Soal Berikutnya:\n\n"
            f"{soal} = ?"
        )




# ==========================
# LEADERBOARD
# ==========================

async def showscore(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id


    restore_score(chat_id)


    data = ambil_score(chat_id)


    if not data:

        await update.message.reply_text(
            "🏆 Belum ada skor."
        )

        return



    teks = "🏆 LEADERBOARD GRUP 🏆\n\n"



    medal = [
        "🥇",
        "🥈",
        "🥉"
    ]



    for i,(uid,nama,poin) in enumerate(data):


        if i < 3:

            nomor = medal[i]

        else:

            nomor = f"{i+1}."


        teks += (
            f"{nomor} {nama} "
            f"⭐ {poin} poin\n"
        )



    await update.message.reply_text(
        teks
    )




# ==========================
# RESET SCORE
# ==========================

async def resetscore(update: Update, context: ContextTypes.DEFAULT_TYPE):

    ADMIN_ID = [
        1569084420,
        8993519217
    ]


    if update.effective_user.id not in ADMIN_ID:


        await update.message.reply_text(
            "❌ Kamu bukan admin."
        )

        return



    reset_score(
        update.effective_chat.id
    )



    await update.message.reply_text(
        "♻️ Leaderboard berhasil direset."
    )




# ==========================
# TAMBAH SCORE ADMIN
# ==========================

async def tambahscore(update: Update, context: ContextTypes.DEFAULT_TYPE):

    ADMIN_ID = [
        1569084420,
        8993519217
    ]


    if update.effective_user.id not in ADMIN_ID:

        await update.message.reply_text(
            "❌ Kamu bukan admin."
        )

        return



    if not update.message.reply_to_message:

        await update.message.reply_text(
            "Reply pesan user lalu:\n\n"
            "/tambahscore jumlah"
        )

        return



    try:

        jumlah = int(context.args[0])

    except:

        await update.message.reply_text(
            "Contoh:\n/tambahscore 50"
        )

        return



    user = update.message.reply_to_message.from_user



    tambah_score_manual(
        update.effective_chat.id,
        user.id,
        user.first_name,
        jumlah
    )



    await update.message.reply_text(
        f"✅ Score bertambah\n\n"
        f"👤 {user.first_name}\n"
        f"⭐ +{jumlah} poin"
    )




# ==========================
# HAPUS NAMA
# ==========================

async def hapusnama(update: Update, context: ContextTypes.DEFAULT_TYPE):

    ADMIN_ID = [
        1569084420,
        8993519217
    ]


    if update.effective_user.id not in ADMIN_ID:

        await update.message.reply_text(
            "❌ Kamu bukan admin."
        )

        return



    if not update.message.reply_to_message:

        await update.message.reply_text(
            "Reply pesan user lalu:\n\n"
            "/hapusnama"
        )

        return



    user = update.message.reply_to_message.from_user



    hapus_nama_score(
        update.effective_chat.id,
        user.id
    )



    await update.message.reply_text(
        f"🗑️ {user.first_name} dihapus dari leaderboard."
    )




# ==========================
# BOT
# ==========================

app = ApplicationBuilder().token(
    TOKEN
).build()



# ==========================
# COMMAND
# ==========================

app.add_handler(
    CommandHandler(
        "startgame",
        startgame
    )
)


app.add_handler(
    CommandHandler(
        "stopgame",
        stopgame
    )
)


app.add_handler(
    CommandHandler(
        "score",
        showscore
    )
)


app.add_handler(
    CommandHandler(
        "resetscore",
        resetscore
    )
)


app.add_handler(
    CommandHandler(
        "tambahscore",
        tambahscore
    )
)


app.add_handler(
    CommandHandler(
        "hapusnama",
        hapusnama
    )
)




# ==========================
# JAWABAN
# ==========================

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        cek
    )
)




print("✅ Bot Aktif")


app.run_polling()