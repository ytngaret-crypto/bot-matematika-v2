import random


def buat_soal():

    operasi = random.choices(
        [
            "tambah",
            "kurang",
            "kali",
            "bagi"
        ],
        weights=[
            30,  # pertambahan
            25,  # pengurangan
            25,  # perkalian
            20   # pembagian
        ]
    )[0]



    # ==========================
    # PERTAMBAHAN
    # ==========================

    if operasi == "tambah":

        a = random.randint(10,99)
        b = random.randint(10,99)

        soal = f"{a} + {b}"

        hasil = a + b



    # ==========================
    # PENGURANGAN
    # ==========================

    elif operasi == "kurang":

        a = random.randint(20,100)
        b = random.randint(1,a)

        soal = f"{a} - {b}"

        hasil = a - b



    # ==========================
    # PERKALIAN
    # ==========================

    elif operasi == "kali":

        a = random.randint(2,15)
        b = random.randint(2,10)

        soal = f"{a} × {b}"

        hasil = a * b



    # ==========================
    # PEMBAGIAN
    # ==========================

    else:

        b = random.randint(2,10)

        hasil = random.randint(2,15)

        a = b * hasil

        soal = f"{a} ÷ {b}"



    return soal, hasil