import pandas as pd
import streamlit as st
from datetime import datetime
import requests

# ==========================================
# PASTE LINK KHUSUS GOOGLE APPS SCRIPT DI SINI
# ==========================================
GOOGLE_WEB_APP_URL = ""  # <-- Masukkan URL Web App di sini

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="CleanWash POS", page_icon="💧", layout="wide")
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        .stButton>button { border-radius: 8px; height: 3rem; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# INISIALISASI DATA
# ==========================================
if "services" not in st.session_state:
    st.session_state.services = pd.DataFrame([
        {"Kategori": "Mobil", "Layanan": "Cuci Salju", "Harga": 50000, "FeeDefault": 15000},
        {"Kategori": "Motor", "Layanan": "Cuci Standar", "Harga": 20000, "FeeDefault": 7000},
        {"Kategori": "Karpet", "Layanan": "Cuci Karpet", "Harga": 40000, "FeeDefault": 10000},
    ])

if "staff" not in st.session_state:
    st.session_state.staff = pd.DataFrame([
        {"Nama": "Budi", "Peran": "Pencuci"},
        {"Nama": "Siti", "Peran": "Pencuci"},
    ])

if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=[
        "Tanggal", "Waktu", "Pelanggan", "Layanan", "Kategori", "Harga Total", "Staff Tugas", "Total Fee"
    ])

if "role" not in st.session_state: st.session_state.role = None
def login(role_name): st.session_state.role = role_name
def logout(): st.session_state.role = None

# ==========================================
# HALAMAN LOGIN
# ==========================================
if st.session_state.role is None:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #1E88E5;'>💧 CleanWash POS</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='background-color: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>", unsafe_allow_html=True)
        st.button("👤 Masuk sebagai Kasir", on_click=login, args=("Kasir",), use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("👑 Masuk sebagai Owner", on_click=login, args=("Owner",), type="primary", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================
# HALAMAN KASIR
# ==========================================
if st.session_state.role == "Kasir":
    col_header1, col_header2 = st.columns([4, 1])
    with col_header1: st.title("🛒 Mode Kasir (Point of Sale)")
    with col_header2: st.button("🚪 Keluar Akun", on_click=logout, use_container_width=True)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📝 Detail Pesanan")
        pelanggan = st.text_input("Nama Pelanggan / Plat Nomor", placeholder="Contoh: B 1234 XYZ")
        opsi_layanan = [f"[{r['Kategori']}] {r['Layanan']} - Rp {r['Harga']:,}" for i, r in st.session_state.services.iterrows()]
        layanan_terpilih = st.selectbox("Pilih Layanan", opsi_layanan)
        data_layanan = st.session_state.services.iloc[opsi_layanan.index(layanan_terpilih)]
        
    with col2:
        st.markdown("### 👷 Penugasan Pekerja")
        list_pencuci = st.session_state.staff[st.session_state.staff["Peran"] == "Pencuci"]["Nama"].tolist()
        staff_tugas = st.multiselect("Pilih Pencuci (Bisa lebih dari 1)", list_pencuci)
        st.info(f"💰 Total Tagihan: **Rp {data_layanan['Harga']:,}**\n💸 Alokasi Fee Pekerja: **Rp {data_layanan['FeeDefault']:,}**")
        
    if st.button("✅ Selesaikan & Catat Transaksi", type="primary", use_container_width=True):
        if not pelanggan or not staff_tugas:
            st.error("⚠️ Data pelanggan dan pekerja harus diisi!")
        else:
            now = datetime.now()
            tgl, wkt = now.strftime("%Y-%m-%d"), now.strftime("%H:%M")
            pekerja = ", ".join(staff_tugas)
            
            new_trx = pd.DataFrame([{
                "Tanggal": tgl, "Waktu": wkt, "Pelanggan": pelanggan, 
                "Layanan": data_layanan["Layanan"], "Kategori": data_layanan["Kategori"], 
                "Harga Total": int(data_layanan["Harga"]), "Staff Tugas": pekerja, 
                "Total Fee": int(data_layanan["FeeDefault"])
            }])
            st.session_state.transactions = pd.concat([st.session_state.transactions, new_trx], ignore_index=True)
            
            # Kirim Data Transaksi ke Google Drive
            if GOOGLE_WEB_APP_URL != "":
                payload = {
                    "action": "transaksi",
                    "tanggal": tgl, "waktu": wkt, "pelanggan": pelanggan,
                    "layanan": data_layanan["Layanan"], "kategori": data_layanan["Kategori"],
                    "harga": int(data_layanan["Harga"]), "staff": pekerja, "fee": int(data_layanan["FeeDefault"])
                }
                try:
                    requests.post(GOOGLE_WEB_APP_URL, data=payload)
                    st.success("🎉 Transaksi berhasil dicatat dan disinkronkan ke Drive!")
                except Exception:
                    st.warning("⚠️ Tersimpan lokal, tapi gagal kirim ke Drive.")
            else:
                st.success("🎉 Transaksi dicatat lokal.")

# ==========================================
# HALAMAN OWNER
# ==========================================
elif st.session_state.role == "Owner":
    st.sidebar.markdown("<h2 style='text-align: center;'>👑 Owner Panel</h2>", unsafe_allow_html=True)
    menu = st.sidebar.radio("Navigasi Menu", ["📈 Dashboard Analytics", "💸 Penggajian Pegawai", "📋 Riwayat", "⚙️ Manajemen Data"])
    st.sidebar.button("🚪 Keluar Akun", on_click=logout, use_container_width=True)

    if menu == "📈 Dashboard Analytics":
        st.title("📈 Dashboard Analytics")
        df_trx = st.session_state.transactions
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Pemasukan Bersih", f"Rp {df_trx['Harga Total'].sum() - df_trx['Total Fee'].sum():,}")
        col2.metric("🚗 Transaksi", f"{len(df_trx)} Unit")
        col3.metric("💸 Fee Pekerja", f"Rp {df_trx['Total Fee'].sum():,}")
        
    elif menu == "💸 Penggajian Pegawai":
        st.title("💸 Hitung Gaji & Kasbon Pegawai")
        st.markdown("Perhitungan: **Total Fee + Uang Makan Bruto - Uang Makan Diambil - Kasbon**")
        
        list_pencuci = st.session_state.staff[st.session_state.staff["Peran"] == "Pencuci"]["Nama"].tolist()
        pilih_pegawai = st.selectbox("Pilih Pegawai", list_pencuci)
        
        df_trx = st.session_state.transactions
        fee_terkumpul = 0
        detail_pekerjaan_list = []
        
        # Tarik data pekerjaan khusus pegawai yang dipilih
        if not df_trx.empty:
            df_pegawai = df_trx[df_trx['Staff Tugas'].astype(str).str.contains(pilih_pegawai, na=False)]
            
            if not df_pegawai.empty:
                st.markdown(f"### 📋 Rincian Pekerjaan: **{pilih_pegawai}**")
                st.dataframe(df_pegawai[["Tanggal", "Waktu", "Layanan", "Kategori", "Harga Total", "Total Fee"]], use_container_width=True, hide_index=True)
                
                for idx, row in df_pegawai.iterrows():
                    jumlah_staff = len(str(row["Staff Tugas"]).split(","))
                    fee_bagian = row["Total Fee"] / jumlah_staff
                    fee_terkumpul += fee_bagian
                    detail_pekerjaan_list.append(f"- {row['Tanggal']}: {row['Layanan']} - Harga: Rp{row['Harga Total']} (Fee: Rp{int(fee_bagian)})")
            else:
                st.info("Belum ada riwayat transaksi untuk pegawai ini.")
        else:
            st.info("Sistem belum memiliki data transaksi.")
            
        detail_pekerjaan_str = "\n".join(detail_pekerjaan_list) if detail_pekerjaan_list else "Tidak ada riwayat transaksi."
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            fee_input = st.number_input("Total Fee Tercapai (Otomatis / Edit Manual)", value=int(fee_terkumpul), step=1000)
            makan_bruto = st.number_input("Uang Makan Bruto (+)", value=0, step=1000)
        with col2:
            makan_diambil = st.number_input("Uang Makan yang Diambil (-)", value=0, step=1000)
            kasbon = st.number_input("Total Kasbon (-)", value=0, step=1000)
            
        gaji_bersih = fee_input + makan_bruto - makan_diambil - kasbon
        st.success(f"### 💰 Gaji Bersih Diterima: Rp {gaji_bersih:,.0f}")
        
        if st.button("Kirim Laporan Gaji ke Google Drive", type="primary", use_container_width=True):
            if GOOGLE_WEB_APP_URL != "":
                now = datetime.now()
                payload = {
                    "action": "gaji",
                    "tanggal": now.strftime("%Y-%m-%d %H:%M"),
                    "bulan": now.strftime("%B %Y"),
                    "staff": pilih_pegawai,
                    "detail_pekerjaan": detail_pekerjaan_str,
                    "fee": int(fee_input),
                    "makan_bruto": int(makan_bruto),
                    "makan_diambil": int(makan_diambil),
                    "kasbon": int(kasbon),
                    "gaji_bersih": int(gaji_bersih)
                }
                try:
                    requests.post(GOOGLE_WEB_APP_URL, data=payload)
                    st.success(f"Berhasil membuat/update Sheet Gaji untuk {pilih_pegawai} di Google Spreadsheet!")
                    # Kosongkan list atau tandai sudah digaji jika diperlukan untuk pengembangan selanjutnya
                except Exception as e:
                    st.error(f"Gagal terhubung ke Google Drive: {e}")
            else:
                st.error("Link Web App Google (URL) belum dimasukkan di dalam kode aplikasi.")
        
    elif menu == "📋 Riwayat":
        st.title("📋 Riwayat Transaksi Global")
        st.dataframe(st.session_state.transactions, use_container_width=True, hide_index=True)
        
    elif menu == "⚙️ Manajemen Data":
        st.title("⚙️ Manajemen Data Master")
        tab_layanan, tab_staff = st.tabs(["🚙 Layanan", "👷 Pekerja"])
        with tab_layanan:
            st.session_state.services = st.data_editor(st.session_state.services, num_rows="dynamic", use_container_width=True)
        with tab_staff:
            st.session_state.staff = st.data_editor(st.session_state.staff, num_rows="dynamic", use_container_width=True)
