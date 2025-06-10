import psycopg2
import pandas as pd
import os

# Koneksi database
conn = psycopg2.connect(
    dbname="Pertanian",
    user="postgres",
    password="1685Fami",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_table_data(table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def insert_data():
    while True:
        print("\n1. Tambah Data Tanaman")
        print("2. Tambah Data Lahan")
        print("3. Tambah Data Pupuk")
        print("4. Tambah Data Cuaca")
        print("5. Kembali ke Dashboard")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            id = int(input("Masukkan ID berupa angka tanpa huruf (ex:1): "))
            nama = input("Nama tanaman: ")
            kebutuhan_n = int(input("Kebutuhan nitrogen per bibit (gram): "))
            jarak = int(input("Jarak antar tanaman (1-100): "))
            harga = int(input("Masukkan Harga per bibit: Rp. "))

            cursor.execute("SELECT * FROM manajemen_tanaman WHERE id_tanaman = %s", (id,))
            data_lama = cursor.fetchone()

            if data_lama is None:
                cursor.execute("""
                    INSERT INTO manajemen_tanaman (id_tanaman, jenis_tanaman, harga, jarak_tumbuh_cm, kebutuhan_nitrogen)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id, nama, harga, jarak, kebutuhan_n))
                conn.commit()
                print("✅ Data berhasil ditambahkan.")
            else:
                print(f"❗ ID {id} sudah ada di dalam tabel manajemen_tanaman")
                print("1. Ganti ID")
                print("2. Update data tanaman dengan ID tersebut")

                pilih = input("Pilih 1 atau 2: ")
                if pilih == "1":
                    print("Silakan jalankan ulang dan masukkan ID yang berbeda.")
                    return
                elif pilih == "2":
                    cursor.execute("""
                        UPDATE manajemen_tanaman
                        SET jenis_tanaman=%s, harga=%s, jarak_tumbuh_cm=%s, kebutuhan_nitrogen=%s
                        WHERE id_tanaman=%s
                    """, (nama, harga, jarak, kebutuhan_n, id))
                    conn.commit()
                    print("✅ Data berhasil diupdate.")
                else:
                    print("❌ Input tidak valid.")

        elif pilihan == '2':
            id=int(input("Masukkan ID Lahan berupa angka tanpa hururf (ex:22): "))
            nama = input("Nama lahan: ")
            luas = int(input("Luas (m2): "))
            jenis = input("Jenis Lahan (ex:Liat) : ")
            cursor.execute("INSERT INTO manajemen_lahan (id_lahan,nama, jenis_lahan,luas_m2) VALUES (%s,%s, %s, %s)", (id,nama, jenis, luas))
            conn.commit()

        elif pilihan == '3':
            id=int(input("Masukkan ID Pupuk berupa angka tanpa huruf (ex:21): "))
            nama = input("Nama pupuk: ")
            kandungan_n = int(input("Kandungan nitrogen (per kg): "))
            harga = int(input("Harga per kg: "))
            cursor.execute("INSERT INTO pupuk (id_pupuk,nama, nitrogen_kg,harga_kg) VALUES (%s,%s, %s, %s)", (id,nama, kandungan_n, harga))
            conn.commit()

        elif pilihan == '4':
            id=int(input("Masukkan ID Pupuk berupa angka tanpa huruf (ex:21): "))
            nama = input("Nama cuaca/musim: ")
            sh_min=int(input("Masukkan suhu_min berupa angka tanpa huruf (ex:21): "))
            sh_max=int(input("Masukkan suhu_max berupa angka tanpa huruf (ex:21): "))
            bulan_awal = input("Bulan Awal : ")
            bulan_akhir = input("Bulan Akhir: ")
            # if id == 
            cursor.execute("INSERT INTO musim_cuaca (id_cuaca,musim,suhu_min,suhu_max,bulan_awal,bulan_akhir) VALUES (%s, %s,%s, %s,%s, %s)", (id,nama,sh_min,sh_max,bulan_awal, bulan_akhir))
            conn.commit()

        elif pilihan == '5':
            break

        else:
            print("Pilihan tidak valid")

def hubungkan_data():
    print("\nIngin lihat data dari tabel apa?")
    print("1. tanaman 2. lahan 3. pupuk 4. cuaca")
    pilihan = input("Pilih: ")
    if pilihan == '1':
        show_table_data("manajemen_tanaman")
    elif pilihan == '2':
        show_table_data("manajemen_lahan")
    elif pilihan == '3':
        show_table_data("pupuk")
    elif pilihan == '4':
        show_table_data("musim_cuaca")

    print("\nMenghubungkan data...")
    id_tanaman = input("ID tanaman: ")

    relasi = input("Hubungkan dengan (pupuk/lahan/cuaca): ").lower()
    if relasi == 'pupuk':
        id_pupuk = input("ID pupuk: ")
        cursor.execute("INSERT INTO tanaman_pupuk (id_tanaman, id_pupuk) VALUES (%s, %s)", (id_tanaman, id_pupuk))
    elif relasi == 'lahan':
        id_lahan = input("ID lahan: ")
        cursor.execute("INSERT INTO tanaman_lahan (id_tanaman, id_lahan) VALUES (%s, %s)", (id_tanaman, id_lahan))
    elif relasi == 'cuaca':
        id_cuaca = input("ID cuaca: ")
        cursor.execute("INSERT INTO tanaman_cuaca (id_tanaman, id_cuaca) VALUES (%s, %s)", (id_tanaman, id_cuaca))
    conn.commit()

def simulasi_kebutuhan():
    cursor.execute("SELECT id_lahan, nama, luas_m2 FROM manajemen_lahan")
    lahan_list = cursor.fetchall()
    print("\nDaftar Lahan:")
    for l in lahan_list:
        print(f"{l[0]} - {l[1]} (Luas: {l[2]} m²)")

    id_lahan = input("Masukkan ID lahan yang akan digunakan: ")
    cursor.execute("SELECT luas_m2 FROM manajemen_lahan WHERE id_lahan = %s", (id_lahan,))
    lahan = cursor.fetchone()
    if not lahan:
        print("Lahan tidak ditemukan!")
        return
    luas = lahan[0]
    cursor.execute("SELECT id_tanaman, jenis_tanaman, jarak_tumbuh_cm, kebutuhan_nitrogen FROM manajemen_tanaman")
    tanaman_list = cursor.fetchall()
    print("\nDaftar Tanaman:")
    for t in tanaman_list:
        print(f"{t[0]} - {t[1]} | Jarak tumbuh: {t[2]} cm | Kebutuhan N: {t[3]} g/bibit")

    id_tanaman = input("Masukkan ID tanaman yang akan digunakan: ")
    cursor.execute("SELECT jarak_tumbuh_cm, kebutuhan_nitrogen FROM manajemen_tanaman WHERE id_tanaman = %s", (id_tanaman,))
    tanaman = cursor.fetchone()
    if not tanaman:
        print("Tanaman tidak ditemukan!")
        return

    jarak_tumbuh_cm, kebutuhan_nitrogen = tanaman
    jarak_m2_per_tanaman = (jarak_tumbuh_cm / 100) ** 2  # konversi cm ke m lalu dihitung area tanaman
    total_bibit = float(luas) / jarak_m2_per_tanaman
    total_n = total_bibit * kebutuhan_nitrogen  # total nitrogen dalam gram

    print(f"Total bibit yang dibutuhkan: {total_bibit} bibit")
    print(f"Total nitrogen yang dibutuhkan: {total_n:.2f} gram")

    print("\n1. Rekomendasi pupuk optimal\n2. Rekomendasi pupuk sesuai budget")
    pilihan = input("Pilih mode: ")
    cursor.execute("""
        SELECT p.id_pupuk, p.nama, p.nitrogen_kg, p.harga_kg, tp.efektivitas
        FROM pupuk p
        JOIN tanaman_pupuk tp ON p.id_pupuk = tp.id_pupuk
        WHERE tp.id_tanaman = %s
    """, (id_tanaman,))
    pupuk_list = cursor.fetchall()
    pupuk_list = [
        (id_pupuk, nama, nitrogen_kg * 1000, harga_kg / 1000, efektivitas)
        for id_pupuk, nama, nitrogen_kg, harga_kg, efektivitas in pupuk_list
        if nitrogen_kg > 0
    ]

    if pilihan == '1':
        pupuk_list.sort(key=lambda x: x[4], reverse=True)

        kebutuhan_n = total_n
        hasil = []

        for pupuk in pupuk_list:
            id_pupuk, nama, nitrogen_g, harga_g, efektivitas = pupuk
            max_gram = kebutuhan_n / nitrogen_g
            beli_gram = max(500, round(max_gram * nitrogen_g))  # minimal 500 gram
            beli_gram = min(beli_gram, kebutuhan_n)  # jangan beli lebih dari kebutuhan
            harga_total = round(beli_gram * harga_g)
            hasil.append((nama, beli_gram / 1000, harga_total))  # tampilkan dalam kg
            kebutuhan_n -= beli_gram

            if kebutuhan_n <= 0:
                break

        print("Rekomendasi pupuk optimal:")
        for h in hasil:
            print(f"🌿 {h[0]}: {h[1]:.2f} kg, Harga: Rp{h[2]}")

    elif pilihan == '2':
        budget = int(input("Masukkan budget (Rp): "))

        pupuk_list.sort(key=lambda x: x[4] / x[2], reverse=True)  # efektivitas per gram nitrogen
        kebutuhan_n = total_n
        hasil = []
        total_biaya = 0

        for pupuk in pupuk_list:
            id_pupuk, nama, nitrogen_g, harga_g, efektivitas = pupuk
            max_gram = kebutuhan_n / nitrogen_g
            beli_gram = max(500, round(max_gram * nitrogen_g))  # minimal 500 gram
            beli_gram = min(beli_gram, kebutuhan_n)
            harga_total = beli_gram * harga_g

            if total_biaya + harga_total <= budget:
                hasil.append((nama, beli_gram / 1000, round(harga_total)))  # tampilkan dalam kg
                total_biaya += harga_total
                kebutuhan_n -= beli_gram

            if kebutuhan_n <= 0:
                break

        if kebutuhan_n > 0:
            print(f"Budget tidak mencukupi. Kekurangan sekitar {round(kebutuhan_n)} gram nitrogen.")
        else:
            print("Rekomendasi pupuk sesuai budget:")
            for h in hasil:
                print(f"{h[0]}: {h[1]:.2f} kg, Harga: Rp{h[2]}")
def rekomendasi_bibit():
    query = '''
    SELECT t.jenis_tanaman, l.nama, m.musim, p.nama
    FROM manajemen_tanaman t
    JOIN tanaman_lahan tl ON t.id_tanaman = tl.id_tanaman
    JOIN manajemen_lahan l ON l.id_lahan = tl.id_lahan
    JOIN tanaman_cuaca tc ON t.id_tanaman = tc.id_tanaman
    JOIN musim_cuaca m ON m.id_cuaca = tc.id_cuaca
    JOIN tanaman_pupuk tp ON t.id_tanaman = tp.id_tanaman
    JOIN pupuk p ON p.id_pupuk = tp.id_pupuk
    '''
    df = pd.read_sql(query, conn)
    print(df)
def main():
    while True:
        print("\nDASHBOARD SI PATANI")
        print("1. Manajemen Data & Relasi")
        print("2. Simulasi Kebutuhan & Rekomendasi Pupuk")
        print("3. Rekomendasi Bibit Sesuai Kondisi")
        print("4. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            clear_screen()
            insert_data()
            lanjut = input("Lanjut ke hubungkan data? (y/n): ")
            if lanjut.lower() == 'y':
                hubungkan_data()
        elif pilihan == '2':
            clear_screen()
            simulasi_kebutuhan()
        elif pilihan == '3':
            clear_screen()
            rekomendasi_bibit()
        elif pilihan == '4':
            break
        else:
            print("Pilihan tidak valid")

main()



