import csv
import os
from datetime import datetime

FILE_NAME = "data_keuangan.csv"
FIELDNAMES = ["id", "tanggal", "jenis", "kategori", "jumlah", "keterangan"]

# === Utilitas ===
def cls():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\nTekan Enter untuk kembali ke menu...")

def load_data():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_data(data):
    with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(data)

# === CRUD Transaksi ===
def tambah_transaksi(data):
    cls()
    print("=== Tambah Transaksi ===")
    tanggal = input("Tanggal (YYYY-MM-DD) [default = hari ini]: ") or datetime.now().strftime("%Y-%m-%d")
    jenis = input("Jenis (pemasukan/pengeluaran): ").lower()
    if jenis not in ['pemasukan', 'pengeluaran']:
        print("Jenis tidak valid.")
        pause()
        return
    kategori = input("Kategori (misal: gaji, makan, transport): ")
    try:
        jumlah = int(input("Jumlah (angka tanpa Rp): "))
    except ValueError:
        print("Jumlah tidak valid.")
        pause()
        return
    keterangan = input("Keterangan: ")
    id_baru = str(len(data) + 1)
    data.append({
        "id": id_baru,
        "tanggal": tanggal,
        "jenis": jenis,
        "kategori": kategori,
        "jumlah": str(jumlah),
        "keterangan": keterangan
    })
    save_data(data)
    print(" Transaksi berhasil ditambahkan.")
    pause()

def tampilkan_semua(data):
    cls()
    print("=== Daftar Semua Transaksi ===")
    if not data:
        print("Belum ada data.")
    for d in data:
        print(f"{d['id']}. [{d['tanggal']}] {d['jenis'].capitalize()} | {d['kategori']} | Rp{d['jumlah']} | {d['keterangan']}")
    pause()

def edit_transaksi(data):
    cls()
    print("=== Edit Transaksi ===")
    id_edit = input("Masukkan ID transaksi yang akan diedit: ")
    for d in data:
        if d["id"] == id_edit:
            print(f"Data sekarang: {d}")
            d["tanggal"] = input(f"Tanggal baru [{d['tanggal']}]: ") or d["tanggal"]
            d["jenis"] = input(f"Jenis baru [{d['jenis']}]: ") or d["jenis"]
            d["kategori"] = input(f"Kategori baru [{d['kategori']}]: ") or d["kategori"]
            d["jumlah"] = input(f"Jumlah baru [{d['jumlah']}]: ") or d["jumlah"]
            d["keterangan"] = input(f"Keterangan baru [{d['keterangan']}]: ") or d["keterangan"]
            save_data(data)
            print(" Transaksi berhasil diupdate.")
            pause()
            return
    print(" ID tidak ditemukan.")
    pause()

def hapus_transaksi(data):
    cls()
    print("=== Hapus Transaksi ===")
    id_hapus = input("Masukkan ID transaksi yang akan dihapus: ")
    for d in data:
        if d["id"] == id_hapus:
            data.remove(d)
            for idx, row in enumerate(data):
                row["id"] = str(idx + 1)
            save_data(data)
            print(" Transaksi berhasil dihapus.")
            pause()
            return
    print(" ID tidak ditemukan.")
    pause()

# === Analisis dan Statistik ===
def lihat_saldo(data):
    cls()
    print("=== Saldo Saat Ini ===")
    pemasukan = sum(int(d["jumlah"]) for d in data if d["jenis"] == "pemasukan")
    pengeluaran = sum(int(d["jumlah"]) for d in data if d["jenis"] == "pengeluaran")
    print(f" Total Pemasukan   : Rp{pemasukan}")
    print(f"Total Pengeluaran : Rp{pengeluaran}")
    print(f" Saldo Akhir       : Rp{pemasukan - pengeluaran}")
    pause()

def filter_berdasarkan_jenis(data):
    cls()
    jenis = input("Masukkan jenis transaksi (pemasukan/pengeluaran): ").lower()
    hasil = [d for d in data if d["jenis"] == jenis]
    if not hasil:
        print(" Tidak ada transaksi dengan jenis tersebut.")
    else:
        for d in hasil:
            print(f"{d['id']}. [{d['tanggal']}] {d['kategori']} | Rp{d['jumlah']} | {d['keterangan']}")
    pause()

def filter_berdasarkan_tanggal(data):
    cls()
    tanggal = input("Masukkan tanggal (YYYY-MM-DD): ")
    hasil = [d for d in data if d["tanggal"] == tanggal]
    if not hasil:
        print(" Tidak ada transaksi pada tanggal tersebut.")
    else:
        for d in hasil:
            print(f"{d['id']}. [{d['jenis']}] {d['kategori']} | Rp{d['jumlah']} | {d['keterangan']}")
    pause()

def ringkasan_bulanan(data):
    cls()
    print("=== Ringkasan Bulanan ===")
    bulan = input("Masukkan bulan (contoh: 2025-07): ")
    total_masuk = total_keluar = 0
    for d in data:
        if d["tanggal"].startswith(bulan):
            jumlah = int(d["jumlah"])
            if d["jenis"] == "pemasukan":
                total_masuk += jumlah
            elif d["jenis"] == "pengeluaran":
                total_keluar += jumlah
    saldo = total_masuk - total_keluar
    print(f" Bulan: {bulan}")
    print(f" Total Pemasukan   : Rp{total_masuk}")
    print(f" Total Pengeluaran : Rp{total_keluar}")
    print(f" Saldo Bulanan     : Rp{saldo}")
    pause()

def ekspor_keuangan(data):
    cls()
    nama_file = input("Masukkan nama file laporan (tanpa .txt): ") + ".txt"
    with open(nama_file, 'w', encoding='utf-8') as f:
        f.write("=== Laporan Keuangan ===\n")
        for d in data:
            f.write(f"{d['id']}. [{d['tanggal']}] {d['jenis']} | {d['kategori']} | Rp{d['jumlah']} | {d['keterangan']}\n")
    print(f"Laporan berhasil disimpan ke {nama_file}")
    pause()

def statistik_keuangan(data):
    cls()
    print("=== Statistik Keuangan ===")
    pemasukan_data = [int(d["jumlah"]) for d in data if d["jenis"] == "pemasukan"]
    pengeluaran_data = [int(d["jumlah"]) for d in data if d["jenis"] == "pengeluaran"]

    if pemasukan_data:
        print(f"Rata-rata Pemasukan  : Rp{sum(pemasukan_data)//len(pemasukan_data)}")
        print(f"Transaksi Pemasukan  : {len(pemasukan_data)}")
    if pengeluaran_data:
        print(f"Rata-rata Pengeluaran: Rp{sum(pengeluaran_data)//len(pengeluaran_data)}")
        print(f"Transaksi Pengeluaran: {len(pengeluaran_data)}")
    pause()

# === Menu Utama ===
def menu():
    data = load_data()
    while True:
        cls()
        print("=== APLIKASI KEUANGAN PRIBADI v2 ===")
        print("1. Lihat Semua Transaksi")
        print("2. Tambah Transaksi")
        print("3. Edit Transaksi")
        print("4. Hapus Transaksi")
        print("5. Lihat Saldo")
        print("6. Filter Transaksi per Jenis")
        print("7. Filter Transaksi per Tanggal")
        print("8. Ringkasan Bulanan")
        print("9. Statistik Keuangan")
        print("10. Ekspor Laporan ke TXT")
        print("11. Keluar")
        pilihan = input("Pilih menu (1-11): ")

        if pilihan == "1":
            tampilkan_semua(data)
        elif pilihan == "2":
            tambah_transaksi(data)
        elif pilihan == "3":
            edit_transaksi(data)
        elif pilihan == "4":
            hapus_transaksi(data)
        elif pilihan == "5":
            lihat_saldo(data)
        elif pilihan == "6":
            filter_berdasarkan_jenis(data)
        elif pilihan == "7":
            filter_berdasarkan_tanggal(data)
        elif pilihan == "8":
            ringkasan_bulanan(data)
        elif pilihan == "9":
            statistik_keuangan(data)
        elif pilihan == "10":
            ekspor_keuangan(data)
        elif pilihan == "11":
            print("👋 Terima kasih telah menggunakan aplikasi!")
            break
        else:
            print("❌ Pilihan tidak valid.")
            pause()

if __name__ == "__main__":
    menu()