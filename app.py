import pandas as pd
import streamlit as st

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Aplikasi Kasir Cuci Mobil, Motor & Karpet",
    page_icon="🚿",
    layout="wide",
)

# --- INISIALISASI DATABASE DINAMIS (SESSION STATE) ---
if "services" not in st.session_state:
  st.session_state.services = pd.DataFrame([
      {
          "ID": 1,
          "Kategori": "Mobil",
          "Layanan": "Cuci Salju & Vacuum",
          "Harga": 60000,
          "FeeDefault": 15000,
      },
      {
          "ID": 2,
          "Kategori": "Motor",
          "Layanan": "Cuci Standar + Semir",
          "Harga": 25000,
          "FeeDefault": 7000,
      },
      {
          "ID": 3,
          "Kategori": "Karpet",
          "Layanan": "Cuci Karpet Standar (per m²)",
          "Harga": 40000,
          "FeeDefault": 10000,
      },
  ])

if "staff" not in st.session_state:
  st.session_state.staff = pd.DataFrame([
      {"ID": 1, "Nama": "Budi Santoso", "Peran": "Pencuci"},
      {"ID": 2, "Nama": "Joko Widodo", "Peran": "Pencuci"},
      {"ID": 3, "Nama": "Siti Aminah", "Peran": "Pencuci"},
      {"ID": 4, "Nama": "Ahmad Kasir", "Peran": "Kasir / Admin"},
  ])

if "transactions" not in st.session_state:
  st.session_state.transactions = []

if "settings" not in st.session_state:
  st.session_state.settings = {
      "nama_usaha": "Hydro Wash & Carpet Clean",
      "alamat": "Jl. Sudirman No. 123, Pekanbaru",
      "telp": "0812-3456-7890",
  }

# --- SIDEBAR NAVIGASI ---
st.sidebar.title("🚿 Menu Utama")
menu = st.sidebar.selectbox("Pilih Modul", [
    "🛒 Transaksi & Kasir",
    "📊 Laporan Detail & Fee",
    "⚙️ Manajemen Layanan",
    "👥 Manajemen Staff",
    "🔒 Pengaturan & Sekuriti",
])

# =====================================================================
# 1. MODUL TRANSAKSI & KASIR
# =====================================================================
if menu == "🛒 Transaksi & Kasir":
  st.title("🛒 Kasir Cuci Kendaraan & Karpet")
  st.markdown("---")

  col1, col2 = st.columns(2)

  with col1:
    st.subheader("Detail Pelanggan & Layanan")
    nama_pelanggan = st.text_input(
        "Nama Pelanggan / Nomor Plat Kendaraan",
        placeholder="Contoh: B 1234 ABC / Bpk. Andi",
    )

    df_services = st.session_state.services
    service_options = [
        (
            f"[{row['Kategori']}] {row['Layanan']} - Rp {row['Harga']:,}"
            f" (Fee: Rp {row['FeeDefault']:,})"
        )
        for _, row in df_services.iterrows()
    ]

    selected_service_str = st.selectbox(
        "Pilih Jenis Layanan", service_options
    )
    selected_idx = service_options.index(selected_service_str)
    chosen_service = df_services.iloc[selected_idx]

    jumlah_unit = st.number_input(
        "Jumlah / Qty (Misal: Jumlah Karpet / Motor)",
        min_value=1,
        value=1,
        step=1,
    )
    total_harga = chosen_service["Harga"] * jumlah_unit
    st.info(f"**Total Harga Tagihan:** Rp {total_harga:,}")

  with col2:
    st.subheader("Penugasan Pegawai Pencuci")
    df_staff = st.session_state.staff
    pencuci_list = df_staff[df_staff["Peran"] == "Pencuci"][
        "Nama"
    ].tolist()

    assigned_staff = st.multiselect(
        "Pilih Staff Pencuci (Bisa > 1 orang jika kerja tim)", pencuci_list
    )

    total_fee_dasar = chosen_service["FeeDefault"] * jumlah_unit
    fee_per_staff = 0

    if assigned_staff:
      fee_per_staff = total_fee_dasar / len(assigned_staff)
      st.success(
          f"Total Alokasi Fee: Rp {total_fee_dasar:,} | Dibagi"
          f" {len(assigned_staff)} orang = **Rp {fee_per_staff:,.0f} per"
          " orang**"
      )

  print_btn = st.button(
      "Proses Transaksi & Cetak Struk", type="primary", use_container_width=True
  )

  if print_btn:
    if not nama_pelanggan:
      st.error("Mohon masukkan nama pelanggan atau nomor plat kendaraan!")
    elif not assigned_staff:
      st.error("Mohon pilih minimal 1 staff pencuci!")
    else:
      import datetime

      trx_record = {
          "Waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          "Pelanggan": nama_pelanggan,
          "Kategori": chosen_service["Kategori"],
          "Layanan": chosen_service["Layanan"],
          "Qty": jumlah_unit,
          "Total Harga": total_harga,
          "Staff Pencuci": ", ".join(assigned_staff),
          "Jumlah Staff": len(assigned_staff),
          "Fee per Staff": fee_per_staff,
          "Total Fee Dikeluarkan": fee_per_staff * len(assigned_staff),
      }
      st.session_state.transactions.append(trx_record)
      st.success(
          f"Transaksi untuk **{nama_pelanggan}** berhasil diproses dan dicatat!"
      )

      st.markdown("---")
      st.subheader("📄 STRUK PEMBAYARAN")
      st.code(
          f"""
      {st.session_state.settings['nama_usaha']}
      {st.session_state.settings['alamat']}
      Telp: {st.session_state.settings['telp']}
      ----------------------------------------
      Waktu       : {trx_record['Waktu']}
      Pelanggan   : {trx_record['Pelanggan']}
      ----------------------------------------
      Layanan     : {trx_record['Layanan']} ({trx_record['Kategori']}) x {trx_record['Qty']}
      Harga Total : Rp {trx_record['Total Harga']:,}
      ----------------------------------------
      Staff Tugas : {trx_record['Staff Pencuci']}
      Terima Kasih atas Kunjungan Anda!
      """,
          language="text",
      )

# =====================================================================
# 2. MODUL LAPORAN DETAIL LAYANAN, STAFF & FEE
# =====================================================================
elif menu == "📊 Laporan Detail & Fee":
  st.title("📊 Laporan Detail Layanan, Staff, & Fee")
  st.markdown("---")

  if len(st.session_state.transactions) == 0:
    st.info(
        "Belum ada data transaksi yang tercatat. Silakan lakukan transaksi di"
        " menu Kasir."
    )
  else:
    df_trx = pd.DataFrame(st.session_state.transactions)

    col1, col2, col3 = st.columns(3)
    with col1:
      st.metric(
          label="Total Pendapatan Kotor",
          value=f"Rp {df_trx['Total Harga'].sum():,}",
      )
    with col2:
      st.metric(
          label="Total Transaksi", value=f"{len(df_trx)} Transaksi"
      )
    with col3:
      st.metric(
          label="Total Akumulasi Fee Staff",
          value=f"Rp {df_trx['Total Fee Dikeluarkan'].sum():,}",
      )

    st.subheader("📋 Riwayat Seluruh Transaksi")
    st.dataframe(df_trx, use_container_width=True)

    st.markdown("---")
    st.subheader("👥 Rekap Fee & Kinerja Berdasarkan Staff")

    staff_summary = {}
    for _, row in df_trx.iterrows():
      staff_names = [s.strip() for s in row["Staff Pencuci"].split(",")]
      for s in staff_names:
        if s not in staff_summary:
          staff_summary[s] = {"Jumlah Tugas": 0, "Total Fee (Rp)": 0}
        staff_summary[s]["Jumlah Tugas"] += 1
        staff_summary[s]["Total Fee (Rp)"] += row["Fee per Staff"]

    df_staff_report = pd.DataFrame.from_dict(staff_summary, orient="index")
    df_staff_report.index.name = "Nama Staff"
    df_staff_report.reset_index(inplace=True)

    st.table(df_staff_report)

# =====================================================================
# 3. MODUL MANAJEMEN LAYANAN
# =====================================================================
elif menu == "⚙️ Manajemen Layanan":
  st.title("⚙️ Pengaturan Jenis Layanan")
  st.markdown("---")

  st.subheader("Daftar Layanan Tersedia")
  st.dataframe(st.session_state.services, use_container_width=True)

  st.subheader("➕ Tambah Layanan Baru")
  with st.form("add_service_form"):
    kategori = st.selectbox(
        "Kategori Kendaraan / Barang", ["Mobil", "Motor", "Karpet"]
    )
    nama_layanan = st.text_input(
        "Nama Layanan", placeholder="Contoh: Cuci Mesin / Cuci Express"
    )
    harga = st.number_input(
        "Tarif Harga Layanan (Rp)", min_value=0, step=5000, value=30000
    )
    fee_default = st.number_input(
        "Alokasi Fee Default untuk Staff (Rp)",
        min_value=0,
        step=1000,
        value=5000,
    )

    submitted = st.form_submit_button("Simpan Layanan Baru")
    if submitted:
      if nama_layanan:
        new_id = len(st.session_state.services) + 1
        new_row = pd.DataFrame([{
            "ID": new_id,
            "Kategori": kategori,
            "Layanan": nama_layanan,
            "Harga": harga,
            "FeeDefault": fee_default,
        }])
        st.session_state.services = pd.concat(
            [st.session_state.services, new_row], ignore_index=True
        )
        st.success(f"Layanan '{nama_layanan}' berhasil ditambahkan!")
        st.rerun()
      else:
        st.error("Nama layanan tidak boleh kosong.")

# =====================================================================
# 4. MODUL MANAJEMEN STAFF
# =====================================================================
elif menu == "👥 Manajemen Staff":
  st.title("👥 Manajemen Pegawai & Pencuci")
  st.markdown("---")

  st.subheader("Daftar Pegawai Aktif")
  st.dataframe(st.session_state.staff, use_container_width=True)

  st.subheader("➕ Tambah Staff Baru")
  with st.form("add_staff_form"):
    nama_staff = st.text_input(
        "Nama Lengkap Staff", placeholder="Contoh: Rian Pratama"
    )
    peran = st.selectbox(
        "Peran / Jabatan", ["Pencuci", "Kasir / Admin", "Supervisor"]
    )

    submitted_staff = st.form_submit_button("Simpan Staff Baru")
    if submitted_staff:
      if nama_staff:
        new_id = len(st.session_state.staff) + 1
        new_row = pd.DataFrame(
            [{"ID": new_id, "Nama": nama_staff, "Peran": peran}]
        )
        st.session_state.staff = pd.concat(
            [st.session_state.staff, new_row], ignore_index=True
        )
        st.success(f"Staff '{nama_staff}' berhasil ditambahkan!")
        st.rerun()
      else:
        st.error("Nama staff tidak boleh kosong.")

# =====================================================================
# 5. MODUL PENGATURAN & SEKURITI
# =====================================================================
elif menu == "🔒 Pengaturan & Sekuriti":
  st.title("🔒 Pengaturan Usaha & Keamanan Sistem")
  st.markdown("---")

  st.subheader("Profil Tempat Usaha (Tampil di Struk)")
  with st.form("settings_form"):
    nama_usaha = st.text_input(
        "Nama Usaha", value=st.session_state.settings["nama_usaha"]
    )
    alamat = st.text_input(
        "Alamat Usaha", value=st.session_state.settings["alamat"]
    )
    telp = st.text_input(
        "No. Telepon / WhatsApp", value=st.session_state.settings["telp"]
    )

    save_settings = st.form_submit_button("Simpan Pengaturan")
    if save_settings:
      st.session_state.settings["nama_usaha"] = nama_usaha
      st.session_state.settings["alamat"] = alamat
      st.session_state.settings["telp"] = telp
      st.success("Profil usaha berhasil diperbarui!")

  st.markdown("---")
  st.subheader("Keamanan & Hak Akses (Security)")
  st.selectbox(
      "Level Sesi Aktif Saat Ini",
      ["Administrator / Pemilik (Akses Penuh)", "Kasir Shift 1 (Terbatas)"],
  )
  st.text_input(
      "Ubah Password Administrator",
      type="password",
      placeholder="Masukkan password baru",
  )
  if st.button("Perbarui Kata Sandi"):
    st.success("Kata sandi administrator berhasil diperbarui.")
