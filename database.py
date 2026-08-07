import os
import sqlite3


# ==========================
# DATA GAME
# ==========================

jawaban = {}
game = {}
soal_sudah_dijawab = {}


# ==========================
# DATABASE SQLITE
# ==========================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DB_PATH = os.path.join(
    BASE_DIR,
    "score.db"
)


conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False
)

cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS skor (

    chat_id INTEGER,

    user_id INTEGER,

    nama TEXT,

    poin INTEGER DEFAULT 0,

    PRIMARY KEY(chat_id,user_id)

)
""")


conn.commit()



# ==========================
# LEADERBOARD LAMA
# ==========================

LEADERBOARD_LAMA = [

    ("Navesca D.", 1044),
    ("Karou", 1025),
    ("holaa meong", 89),
    ("MailSeven7", 87),
    ("liam", 81),
    ("ꫝ 𝘔𝘢𝘶𝘥𝘺.", 78),
    ("Setyaa.", 59),
    ("Bebe", 50),
    ("epan kebasyok", 45),
    ("dya⋆.𐙚", 39),
    ("Aurie Molaaaangg", 27),
    ("saudade", 26),
    ("˚｡𖦹𝔟𝔞𝐌𝔬𝔰𝔈 ⩔♕jea", 22),
    ("Zen", 18),
    ("𝗞𝗜𝗡𝗔𝗡 OPEN CV NFT", 15),
    ("Senna", 12),
    ("kara", 12),
    ("Phelia.", 5),
    ("ayy", 2),
    ("brian", 2),
    ("Kael", 1),
    ("cy", 1),
    ("Jokerkc || tidur🥱", 1),
    ("Axcel_yz™", 1)

]



# ==========================
# RESTORE SCORE LAMA
# ==========================

def restore_score(chat_id):

    cursor.execute("""
    SELECT COUNT(*)
    FROM skor
    WHERE chat_id=?
    """,
    (chat_id,)
    )


    jumlah = cursor.fetchone()[0]


    if jumlah > 0:
        return False



    for nomor,(nama,poin) in enumerate(
        LEADERBOARD_LAMA,
        start=1
    ):

        temporary_id = -nomor


        cursor.execute("""
        INSERT OR IGNORE INTO skor
        (chat_id,user_id,nama,poin)

        VALUES (?,?,?,?)

        """,
        (
            chat_id,
            temporary_id,
            nama,
            poin
        ))


    conn.commit()

    return True




# ==========================
# TAMBAH POIN GAME
# ==========================

def tambah_poin(
    chat_id,
    user_id,
    nama
):


    cursor.execute("""
    SELECT poin
    FROM skor

    WHERE chat_id=?
    AND user_id=?

    """,
    (
        chat_id,
        user_id
    ))


    data = cursor.fetchone()



    if data:


        cursor.execute("""
        UPDATE skor

        SET poin=poin+1,
            nama=?

        WHERE chat_id=?
        AND user_id=?

        """,
        (
            nama,
            chat_id,
            user_id
        ))


    else:


        cursor.execute("""
        SELECT user_id,poin

        FROM skor

        WHERE chat_id=?
        AND nama=?
        AND user_id<0

        LIMIT 1

        """,
        (
            chat_id,
            nama
        ))



        lama = cursor.fetchone()



        if lama:


            temp_id = lama[0]
            poin_lama = lama[1]


            cursor.execute("""
            DELETE FROM skor

            WHERE chat_id=?
            AND user_id=?

            """,
            (
                chat_id,
                temp_id
            ))



            cursor.execute("""
            INSERT INTO skor

            (chat_id,user_id,nama,poin)

            VALUES (?,?,?,?)

            """,
            (
                chat_id,
                user_id,
                nama,
                poin_lama+1
            ))



        else:


            cursor.execute("""
            INSERT INTO skor

            (chat_id,user_id,nama,poin)

            VALUES (?,?,?,1)

            """,
            (
                chat_id,
                user_id,
                nama
            ))



    conn.commit()




# ==========================
# TAMBAH SCORE MANUAL ADMIN
# ==========================

def tambah_score_manual(
    chat_id,
    user_id,
    nama,
    jumlah
):


    cursor.execute("""
    SELECT poin

    FROM skor

    WHERE chat_id=?
    AND user_id=?

    """,
    (
        chat_id,
        user_id
    ))


    data = cursor.fetchone()



    if data:


        cursor.execute("""
        UPDATE skor

        SET poin=poin+?,
            nama=?

        WHERE chat_id=?
        AND user_id=?

        """,
        (
            jumlah,
            nama,
            chat_id,
            user_id
        ))



    else:


        cursor.execute("""
        INSERT INTO skor

        (chat_id,user_id,nama,poin)

        VALUES (?,?,?,?)

        """,
        (
            chat_id,
            user_id,
            nama,
            jumlah
        ))



    conn.commit()




# ==========================
# HAPUS NAMA LEADERBOARD
# ==========================

def hapus_nama_score(
    chat_id,
    user_id
):


    cursor.execute("""
    DELETE FROM skor

    WHERE chat_id=?
    AND user_id=?

    """,
    (
        chat_id,
        user_id
    ))


    conn.commit()




# ==========================
# AMBIL SCORE
# ==========================

def ambil_score(chat_id):


    cursor.execute("""
    SELECT user_id,nama,poin

    FROM skor

    WHERE chat_id=?

    ORDER BY poin DESC

    """,
    (
        chat_id,
    ))


    return cursor.fetchall()




# ==========================
# RESET SCORE
# ==========================

def reset_score(chat_id):


    cursor.execute("""
    DELETE FROM skor

    WHERE chat_id=?

    """,
    (
        chat_id,
    ))


    conn.commit()




# ==========================
# CEK SCORE
# ==========================

def ada_score(chat_id):


    cursor.execute("""
    SELECT COUNT(*)

    FROM skor

    WHERE chat_id=?

    """,
    (
        chat_id,
    ))


    jumlah = cursor.fetchone()[0]


    return jumlah > 0