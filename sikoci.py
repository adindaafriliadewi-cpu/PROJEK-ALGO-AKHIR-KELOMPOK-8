import pandas as pd

def menu_awal():
    while True:
        print("\n" + "=" * 55)
        print("   SELAMAT DATANG DI SISTEM ANTREAN CUCI VEHICLE   ".center(55))
        print("=" * 55)
        print("1. Login Kasir")
        print("2. Login Pemilik / Owner")
        print("0. Selesaikan Program / Keluar")
        print("=" * 55)

        pilihan = input("Masukkan Pilihan (Angka): ").strip()

        if pilihan == "1":
            login_sistem("kasir")
        elif pilihan == "2":
            login_sistem("owner")
        elif pilihan == "0":
            print("\nTerima kasih telah menggunakan layanan kami! Program selesai.")
            break
        else:
            print("\n[Error] Pilihan tidak valid, harap masukkan angka yang benar.")
#Login disini dindaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
def tambah_antrean():
    print("\n--- TAMBAH ANTREAN BARU ---")

    try:
        df_layanan = pd.read_csv("layanan.csv")
    except FileNotFoundError:
        df_layanan = pd.DataFrame([
            {"ID_Paket": "P01", "Nama_Paket": "Cuci Motor Standard", "Jenis_Kendaraan": "Motor", "Harga": 15000},
            {"ID_Paket": "P02", "Nama_Paket": "Cuci Motor Express", "Jenis_Kendaraan": "Motor", "Harga": 25000},
            {"ID_Paket": "P03", "Nama_Paket": "Cuci Mobil Regular", "Jenis_Kendaraan": "Mobil", "Harga": 40000},
            {"ID_Paket": "P04", "Nama_Paket": "Cuci Mobil Premium Wax", "Jenis_Kendaraan": "Mobil", "Harga": 65000}
        ])
        df_layanan.to_csv("layanan.csv", index=False)

    print("\nPilihan Paket Cuci:")

    for idx, row in df_layanan.iterrows():
        print(f"{idx + 1}. [{row['Jenis_Kendaraan']}] {row['Nama_Paket']} - Rp{int(row['Harga']):,}")

    pilihan_input = input("\nPilih paket (nomor): ").strip()

    if not pilihan_input.isdigit():
        print("[Error] Input pilihan harus berupa angka!")
        return

    pilihan = int(pilihan_input) - 1

    if pilihan < 0 or pilihan >= len(df_layanan):
        print("[Error] Pilihan paket tidak valid!")
        return

    paket_terpilih = df_layanan.iloc[pilihan]

    plat = input("Masukkan Nomor Plat    : ").strip().upper()
    nama = input("Masukkan Nama Pelanggan: ").strip()

    # >>> TAMBAHAN VALIDASI
    if plat == "" or nama == "":
        print("[Error] Nomor plat dan nama pelanggan tidak boleh kosong!")
        return
    # >>> AKHIR TAMBAHAN VALIDASI

    try:
        df_antrean = pd.read_csv("antrean.csv", dtype=str)
    except FileNotFoundError:
        df_antrean = pd.DataFrame(columns=[
            "ID_Antrean", "Plat_Nomor", "Nama",
            "Jenis_Kendaraan", "Paket", "Harga", "Status"
        ])

    id_antrean = f"A{len(df_antrean) + 1:03d}"

    data_baru = pd.DataFrame([{
        "ID_Antrean": id_antrean,
        "Plat_Nomor": plat,
        "Nama": nama,
        "Jenis_Kendaraan": paket_terpilih["Jenis_Kendaraan"],
        "Paket": paket_terpilih["Nama_Paket"],
        "Harga": str(paket_terpilih["Harga"]),
        "Status": "Menunggu"
    }])

    df_antrean = pd.concat([df_antrean, data_baru], ignore_index=True)
    df_antrean.to_csv("antrean.csv", index=False)

    print(f"[Berhasil] Antrean {id_antrean} berhasil ditambahkan!")


def update_status_antrean():
    tampilkan_antrean_aktif()

    try:
        df_antrean = pd.read_csv("antrean.csv", dtype=str)
    except FileNotFoundError:
        return

    if df_antrean.empty:
        return

    pilihan_input = input("\nPilih nomor urut antrean yang ingin diubah statusnya: ").strip()

    if not pilihan_input.isdigit():
        print("[Error] Input pilihan harus berupa angka!")
        return

    idx = int(pilihan_input) - 1

    if idx < 0 or idx >= len(df_antrean):
        print("[Error] Nomor urut antrean tidak valid!")
        return

    id_target = df_antrean.iloc[idx]["ID_Antrean"]

    print(f"Status antrean {id_target} saat ini: {df_antrean.iloc[idx]['Status']}")
    print("Pilih Status Baru:")
    print("1. Sedang Dicuci")
    print("2. Selesai")

    status_opt = input("Pilihan (1/2): ").strip()

    if status_opt == "1":
        df_antrean.iloc[idx, df_antrean.columns.get_loc("Status")] = "Sedang Dicuci"
    elif status_opt == "2":
        df_antrean.iloc[idx, df_antrean.columns.get_loc("Status")] = "Selesai"
    else:
        print("[Error] Pilihan status tidak valid!")
        return

    df_antrean.to_csv("antrean.csv", index=False)

    print(f"[Berhasil] Status antrean {id_target} diperbarui menjadi '{df_antrean.iloc[idx]['Status']}'.")


def proses_pembayaran():
    tampilkan_antrean_aktif()

    try:
        df_antrean = pd.read_csv("antrean.csv", dtype=str)
    except FileNotFoundError:
        return

    if df_antrean.empty:
        return

    pilihan_input = input("\nPilih nomor urut antrean yang akan dibayar: ").strip()

    if not pilihan_input.isdigit():
        print("[Error] Input pilihan harus berupa angka!")
        return

    idx = int(pilihan_input) - 1

    if idx < 0 or idx >= len(df_antrean):
        print("[Error] Nomor urut antrean tidak valid!")
        return

    row_target = df_antrean.iloc[idx]

    if row_target["Status"] != "Selesai":
        print(f"[Peringatan] Antrean masih dalam status '{row_target['Status']}'. Pengerjaan harus 'Selesai' terlebih dahulu.")
        return

    harga = int(row_target["Harga"])

    print(f"\nTotal Tagihan: Rp{harga:,}")

    bayar_input = input("Nominal Uang Bayar: Rp").strip()

    if not bayar_input.isdigit():
        print("[Error] Input pembayaran harus berupa angka!")
        return

    bayar = int(bayar_input)

    if bayar < harga:
        print("[Error] Nominal uang pembayaran kurang!")
        return

    kembalian = bayar - harga

    print("\n" + "=" * 40)
    print("         STRUK PEMBAYARAN CUCI         ")
    print("=" * 40)
    print(f"NO PLAT  : {row_target['Plat_Nomor']}")
    print(f"NAMA     : {row_target['Nama']}")
    print(f"PAKET    : {row_target['Paket']}")
    print("-" * 40)
    print(f"TOTAL    : Rp{harga:,}")
    print(f"BAYAR    : Rp{bayar:,}")
    print(f"KEMBALI  : Rp{kembalian:,}")
    print("=" * 40)
    print("    Terima Kasih Atas Kunjungan Anda!   \n")

    try:
        df_transaksi = pd.read_csv("transaksi.csv", dtype=str)
    except FileNotFoundError:
        df_transaksi = pd.DataFrame(columns=[
            "ID_Transaksi", "Plat_Nomor", "Paket", "Total_Bayar"
        ])

    id_trx = f"TRX{len(df_transaksi) + 1:04d}"

    data_trx = pd.DataFrame([{
        "ID_Transaksi": id_trx,
        "Plat_Nomor": row_target["Plat_Nomor"],
        "Paket": row_target["Paket"],
        "Total_Bayar": str(harga)
    }])

    df_transaksi = pd.concat([df_transaksi, data_trx], ignore_index=True)
    df_transaksi.to_csv("transaksi.csv", index=False)

    df_antrean = df_antrean.drop(df_antrean.index[idx]).reset_index(drop=True)
    df_antrean.to_csv("antrean.csv", index=False)

    print(f"[Berhasil] Transaksi {id_trx} berhasil disimpan!")

def batal_antrean():
    tampilkan_antrean_aktif()

    try:
        df_antrean = pd.read_csv("antrean.csv", dtype=str)
    except FileNotFoundError:
        return

    if df_antrean.empty:
        return

    pilihan_input = input("\nPilih nomor urut antrean yang ingin dibatalkan: ").strip()

    if not pilihan_input.isdigit():
        print("[Error] Input pilihan harus berupa angka!")
        return

    idx = int(pilihan_input) - 1

    if idx < 0 or idx >= len(df_antrean):
        print("[Error] Nomor urut antrean tidak valid!")
        return

    id_target = df_antrean.iloc[idx]["ID_Antrean"]

    df_antrean = df_antrean.drop(df_antrean.index[idx]).reset_index(drop=True)
    df_antrean.to_csv("antrean.csv", index=False)

    print(f"[Berhasil] Antrean {id_target} telah dibatalkan.")


# >>> TAMBAHAN FUNGSI PENCARIAN ANTREAN
def cari_antrean():
    try:
        df_antrean = pd.read_csv("antrean.csv", dtype=str)
    except FileNotFoundError:
        print("Belum ada data antrean.")
        return

    if df_antrean.empty:
        print("Belum ada antrean yang dapat dicari.")
        return

    plat = input("Masukkan nomor plat yang dicari: ").strip().upper()

    if plat == "":
        print("[Error] Nomor plat tidak boleh kosong!")
        return

    hasil = df_antrean[
        df_antrean["Plat_Nomor"].str.upper() == plat
    ]

    if not hasil.empty:
        print("\nData antrean ditemukan:")
        print(hasil.to_string(index=False))
    else:
        print("\nAntrean dengan nomor plat tersebut tidak ditemukan.")
# >>> AKHIR TAMBAHAN FUNGSI PENCARIAN ANTREAN


# ==========================================
# 4. FITUR PEMILIK / OWNER
# ==========================================
def menu_owner():
    while True:
        print("\n==============================")
        print("        MENU PEMILIK          ")
        print("==============================")
        print("1. Laporan Keuangan & Transaksi")
        print("2. Kelola Tarif & Paket Cuci")
        print("3. Analisis Paket Terlaris")
        print("0. Logout (Kembali ke Menu Awal)")
        print("==============================")

        pilihan = input("Pilih menu (0-3): ").strip()

        if pilihan == "1":
            tampil_laporan_keuangan()
        elif pilihan == "2":
            kelola_layanan()
        elif pilihan == "3":
            analisis_paket_terlaris()
        elif pilihan == "0":
            print("\n[Logout] Berhasil keluar dari akun Pemilik.")
            break
        else:
            print("[Error] Pilihan tidak valid.")


def tampil_laporan_keuangan():
    try:
        df_transaksi = pd.read_csv("transaksi.csv")
    except FileNotFoundError:
        df_transaksi = pd.DataFrame(columns=[
            "ID_Transaksi", "Plat_Nomor", "Paket", "Total_Bayar"
        ])
        df_transaksi.to_csv("transaksi.csv", index=False)

    print("\n" + "=" * 60)
    print("LAPORAN KEUANGAN & TRANSAKSI".center(60))
    print("=" * 60)

    if df_transaksi.empty:
        print("Belum ada riwayat transaksi tersimpan.")
    else:
        df_tampil = df_transaksi.copy()
        df_tampil.index = range(1, len(df_tampil) + 1)
        print(df_tampil.to_string())

        total_pemasukan = df_transaksi["Total_Bayar"].astype(int).sum()
        persentase_margin = 0.6
        estimasi_keuntungan = int(total_pemasukan * persentase_margin)

        print("=" * 60)
        print(f"Total Unit Selesai   : {len(df_transaksi)} kendaraan")
        print(f"Total Pendapatan     : Rp{total_pemasukan:,}")
        print(f"Estimasi Keuntungan  : Rp{estimasi_keuntungan:,}")

    print("=" * 60)
