import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import requests
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PASTE LINK KHUSUS GOOGLE APPS SCRIPT DI SINI
# ==========================================
GOOGLE_WEB_APP_URL = "" 

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="CleanWash POS", page_icon="💧", layout="wide")

# CSS KHUSUS UNTUK TAMPILAN DASHBOARD MODERN
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        .block-container { padding-top: 2rem; padding-bottom: 2rem; background-color: #f8f9fa; }
        .stButton>button { border-radius: 8px; height: 3rem; }
        
        /* Metric Card Styling */
        .metric-card {
            background-color: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
            border: 1px solid #f0f0f0;
            margin-bottom: 20px;
        }
        .metric-title {
            color: #8c8c8c;
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 10px;
        }
        .metric-value {
            color: #262626;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .metric-trend-up { color: #52c41a; font-size: 12px; font-weight: bold; }
        .metric-trend-down { color: #f5222d; font-size: 12px; font-weight: bold; }
        
        /* Recent Visits Styling */
        .recent-visit {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        .recent-visit:last-child { border-bottom: none; }
        .visit-name { font-weight: 600; font-size: 14px; color: #262626; }
        .visit-service { font-size: 12px; color: #8c8c8c; }
        .visit-time { font-size: 12px; font-weight: 500; color: #262626; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# INISIALISASI DATA
# ==========================================
if "services" not in st.session_state:
    st.session_state.services = pd.DataFrame([
        {"Kategori": "Mobil", "Layanan": "Cuci Salju", "Harga": 50000, "FeeDefault": 15000},
        {"Kategori": "Mobil", "Layanan": "Cuci + Wax", "Harga": 80000, "FeeDefault": 20000},
        {"Kategori": "Motor", "Layanan": "Cuci Standar", "Harga": 20000, "FeeDefault": 7000},
        {"Kategori": "Karpet", "Layanan": "Cuci Karpet", "Harga": 40000, "FeeDefault": 10000},
    ])

if "staff" not in st.session_state:
    st.session_state.staff = pd.DataFrame([
        {"Nama": "Budi", "Peran": "Pencuci"},
        {"Nama": "Siti", "Peran": "Pencuci"},
        {"Nama": "Agus", "Peran": "Pencuci"},
    ])

# Data Dummy untuk Dashboard Analytics agar grafik langsung terlihat menarik
if "transactions" not in st.session_state:
    today = datetime.now()
    dummy_data = []
    for i in range(10, -1, -1):
        d = today - timedelta(days=i)
        date_str = d.strftime("%Y-%m-%d")
        dummy_data.append({"Tanggal": date_str, "Waktu": "09:00", "Pelanggan": f"Pelanggan A{i}", "Layanan": "Cuci Salju", "Kategori": "Mobil", "Harga Total": 50000, "Staff Tugas": "Budi", "Total Fee": 15000})
        dummy_data.append({"Tanggal": date_str, "Waktu": "11:30", "Pelanggan": f"Pelanggan B{i}", "Layanan": "Cuci Standar", "Kategori": "Motor", "Harga Total": 20000, "Staff Tugas": "Siti", "Total Fee": 7000})
        if i % 2 == 0:
            dummy_data.append({"Tanggal": date_str, "Waktu": "14:15", "Pelanggan": f"Pelanggan C{i}", "Layanan": "Cuci + Wax", "Kategori": "Mobil", "Harga Total": 80000, "Staff Tugas": "Agus", "Total Fee": 20000})
            dummy_data.append({"Tanggal": date_str, "Waktu": "16:00", "Pelanggan": f"Pelanggan D{i}", "Layanan": "Cuci Karpet", "Kategori": "Karpet", "Harga Total": 40000, "Staff Tugas": "Budi, Siti", "Total Fee": 10000})
            
    st.session_state.transactions = pd.DataFrame(dummy_data)

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
# HALAMAN OWNER (FOKUS KE DASHBOARD MODERN & MANAJEMEN)
# ==========================================
elif st.session_state.role == "Owner":
    st.sidebar.markdown("<h2 style='text-align: center; color: #1E88E5;'>💧 Owner Panel</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    menu = st.sidebar.radio("Navigasi", [
        "📊 Overview Dashboard", 
        "⚙️ Update Master Data", 
        "💸 Penggajian Pegawai", 
        "📋 Riwayat Transaksi"
    ])
    st.sidebar.markdown("---")
    st.sidebar.button("🚪 Keluar Akun", on_click=logout, use_container_width=True)

    df_trx = st.session_state.transactions

    # -----------------------------------------------------------
    # 1. OVERVIEW DASHBOARD (Sesuai Gambar Referensi)
    # -----------------------------------------------------------
    if menu == "📊 Overview Dashboard":
        st.markdown("<h2 style='color: #262626;'>Dashboard Analytics</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8c8c8c;'>Ringkasan performa bisnis dan operasional kasir.</p>", unsafe_allow_html=True)
        
        # --- METRIC CARDS ---
        col1, col2, col3, col4 = st.columns(4)
        
        total_pemasukan = df_trx['Harga Total'].sum() if not df_trx.empty else 0
        total_fee = df_trx['Total Fee'].sum() if not df_trx.empty else 0
        pemasukan_bersih = total_pemasukan - total_fee
        total_transaksi = len(df_trx)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Total Pendapatan Kotor</div>
                    <div class="metric-value">Rp {total_pemasukan:,}</div>
                    <div class="metric-trend-up">↑ 12.5% vs last week</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Pemasukan Bersih (Net)</div>
                    <div class="metric-value">Rp {pemasukan_bersih:,}</div>
                    <div class="metric-trend-up">↑ 8.2% vs last week</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Total Transaksi (Unit)</div>
                    <div class="metric-value">{total_transaksi}</div>
                    <div class="metric-trend-up">↑ 15.3% vs last week</div>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Total Alokasi Fee Staff</div>
                    <div class="metric-value">Rp {total_fee:,}</div>
                    <div class="metric-trend-down">↓ 2.1% vs last week</div>
                </div>
            """, unsafe_allow_html=True)

        # --- CHARTS SECTION ---
        st.markdown("<br>", unsafe_allow_html=True)
        chart_col1, chart_col2 = st.columns([7, 3])
        
        with chart_col1:
            st.markdown("<div style='background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #f0f0f0; box-shadow: 0 4px 6px rgba(0,0,0,0.02);'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color: #262626; margin-bottom: 20px;'>Tren Pendapatan Harian</h4>", unsafe_allow_html=True)
            
            if not df_trx.empty:
                daily_trend = df_trx.groupby('Tanggal')['Harga Total'].sum().reset_index()
                fig_bar = px.bar(
                    daily_trend, x='Tanggal', y='Harga Total', 
                    text='Harga Total',
                    color_discrete_sequence=['#4C6FFF']
                )
                fig_bar.update_traces(texttemplate='Rp %{text:.2s}', textposition='outside', marker_border_radius=4)
                fig_bar.update_layout(
                    plot_bgcolor='white', paper_bgcolor='white',
                    margin=dict(l=0, r=0, t=0, b=0),
                    height=320,
                    xaxis=dict(showgrid=False, title=""),
                    yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title="")
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("Belum ada data transaksi.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with chart_col2:
            st.markdown("<div style='background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #f0f0f0; box-shadow: 0 4px 6px rgba(0,0,0,0.02); height: 100%;'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color: #262626; margin-bottom: 20px;'>Proporsi Kategori</h4>", unsafe_allow_html=True)
            
            if not df_trx.empty:
                cat_dist = df_trx['Kategori'].value_counts().reset_index()
                cat_dist.columns = ['Kategori', 'Jumlah']
                fig_pie = px.pie(
                    cat_dist, values='Jumlah', names='Kategori', hole=0.65,
                    color_discrete_sequence=['#4C6FFF', '#FF7F50', '#20B2AA']
                )
                fig_pie.update_layout(
                    showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                    margin=dict(l=0, r=0, t=20, b=0), height=300
                )
                # Tambahkan total di tengah donut
                fig_pie.add_annotation(text=f"Total<br><b>{total_transaksi}</b>", x=0.5, y=0.5, font_size=20, showarrow=False)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Belum ada data.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        # --- BOTTOM SECTION (QUICK EDIT & LATEST VISITS) ---
        st.markdown("<br>", unsafe_allow_html=True)
        bot_col1, bot_col2 = st.columns([7, 3])
        
        with bot_col1:
            st.markdown("<div style='background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #f0f0f0; box-shadow: 0 4px 6px rgba(0,0,0,0.02);'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color: #262626; margin-bottom: 20px;'>⚙️ Akses Cepat Update Layanan</h4>", unsafe_allow_html=True)
            st.markdown("<p style='color: #8c8c8c; font-size: 14px;'>Ubah harga atau fee layanan langsung dari tabel ini.</p>", unsafe_allow_html=True)
            
            edited_services = st.data_editor(st.session_state.services, num_rows="dynamic", use_container_width=True)
            if st.button("💾 Simpan Update Layanan", type="primary"):
                st.session_state.services = edited_services
                st.success("Data layanan berhasil diperbarui!")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with bot_col2:
            st.markdown("<div style='background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #f0f0f0; box-shadow: 0 4px 6px rgba(0,0,0,0.02); height: 100%;'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color: #262626; margin-bottom: 20px;'>🕒 Transaksi Terakhir</h4>", unsafe_allow_html=True)
            
            if not df_trx.empty:
                # Ambil 5 transaksi terakhir
                latest = df_trx.tail(5).iloc[::-1]
                html_visits = ""
                for _, row in latest.iterrows():
                    html_visits += f"""
                    <div class="recent-visit">
                        <div>
                            <div class="visit-name">{row['Pelanggan']}</div>
                            <div class="visit-service">{row['Layanan']} • {row['Staff Tugas']}</div>
                        </div>
                        <div class="visit-time">{row['Tanggal']}<br>{row['Waktu']}</div>
                    </div>
                    """
                st.markdown(html_visits, unsafe_allow_html=True)
            else:
                st.info("Belum ada transaksi.")
            st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------
    # 2. UPDATE MASTER DATA
    # -----------------------------------------------------------
    elif menu == "⚙️ Update Master Data":
        st.markdown("<h2 style='color: #262626;'>⚙️ Manajemen Data Master</h2>", unsafe_allow_html=True)
        st.markdown("Pusat kendali Owner untuk mengubah, menambah, atau menghapus data utama aplikasi.")
        
        tab_layanan, tab_staff = st.tabs(["🚙 Pengaturan Harga & Layanan", "👷 Pengaturan Pekerja"])
        
        with tab_layanan:
            st.markdown("<div style='background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #f0f0f0;'>", unsafe_allow_html=True)
            st.markdown("#### Tabel Layanan")
            st.caption("Klik dua kali pada sel tabel untuk mengubah nilai. Tekan icon '+' di pojok kiri bawah tabel untuk menambah layanan baru.")
            edited_services_full = st.data_editor(st.session_state.services, num_rows="dynamic", use_container_width=True, height=300)
            if st.button("💾 Simpan Perubahan Layanan", key="btn_srv"): 
                st.session_state.services = edited_services_full
                st.success("Update berhasil disimpan!")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab_staff:
            st.markdown("<div style='background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #f0f0f0;'>", unsafe_allow_html=True)
            st.markdown("#### Tabel Pegawai & Staff")
            edited_staff = st.data_editor(st.session_state.staff, num_rows="dynamic", use_container_width=True, height=300)
            if st.button("💾 Simpan Perubahan Pegawai"): 
                st.session_state.staff = edited_staff
                st.success("Data pegawai berhasil diperbarui!")
            st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------
    # 3. PENGGAJIAN PEGAWAI
    # -----------------------------------------------------------
    elif menu == "💸 Penggajian Pegawai":
        st.markdown("<h2 style='color: #262626;'>💸 Hitung Gaji & Kasbon Pegawai</h2>", unsafe_allow_html=True)
        st.markdown("<div style='background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #f0f0f0;'>", unsafe_allow_html=True)
        
        list_pencuci = st.session_state.staff[st.session_state.staff["Peran"] == "Pencuci"]["Nama"].tolist()
        pilih_pegawai = st.selectbox("Pilih Pegawai yang Ingin Digaji", list_pencuci)
        
        df_trx = st.session_state.transactions
        fee_terkumpul = 0
        detail_pekerjaan_list = []
        
        if not df_trx.empty:
            df_pegawai = df_trx[df_trx['Staff Tugas'].astype(str).str.contains(pilih_pegawai, na=False)]
            
            if not df_pegawai.empty:
                st.markdown(f"#### 📋 Rekap Pekerjaan Bulan Ini: **{pilih_pegawai}**")
                st.dataframe(df_pegawai[["Tanggal", "Layanan", "Kategori", "Harga Total", "Total Fee"]], use_container_width=True, hide_index=True)
                
                for idx, row in df_pegawai.iterrows():
                    jumlah_staff = len(str(row["Staff Tugas"]).split(","))
                    fee_bagian = row["Total Fee"] / jumlah_staff
                    fee_terkumpul += fee_bagian
                    detail_pekerjaan_list.append(f"- {row['Tanggal']}: {row['Layanan']} - Harga: Rp{row['Harga Total']} (Fee: Rp{int(fee_bagian)})")
            else:
                st.info("Belum ada riwayat transaksi untuk pegawai ini.")
                
        detail_pekerjaan_str = "\n".join(detail_pekerjaan_list) if detail_pekerjaan_list else "Tidak ada riwayat transaksi."
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            fee_input = st.number_input("Total Fee Tercapai (Dihitung Otomatis / Bisa Edit)", value=int(fee_terkumpul), step=1000)
            makan_bruto = st.number_input("Uang Makan Bruto (+)", value=0, step=1000)
        with col2:
            makan_diambil = st.number_input("Uang Makan yang Diambil (-)", value=0, step=1000)
            kasbon = st.number_input("Total Kasbon (-)", value=0, step=1000)
            
        gaji_bersih = fee_input + makan_bruto - makan_diambil - kasbon
        st.success(f"### 💰 Gaji Bersih Diterima: Rp {gaji_bersih:,.0f}")
        
        if st.button("✅ Kirim Laporan Gaji ke Google Drive", type="primary", use_container_width=True):
            if GOOGLE_WEB_APP_URL != "":
                now = datetime.now()
                payload = {
                    "action": "gaji", "tanggal": now.strftime("%Y-%m-%d %H:%M"),
                    "bulan": now.strftime("%B %Y"), "staff": pilih_pegawai,
                    "detail_pekerjaan": detail_pekerjaan_str, "fee": int(fee_input),
                    "makan_bruto": int(makan_bruto), "makan_diambil": int(makan_diambil),
                    "kasbon": int(kasbon), "gaji_bersih": int(gaji_bersih)
                }
                try:
                    requests.post(GOOGLE_WEB_APP_URL, data=payload)
                    st.success(f"Berhasil membuat Sheet Gaji untuk {pilih_pegawai} di Google Spreadsheet!")
                except Exception as e:
                    st.error("Gagal terhubung ke Google Drive.")
            else:
                st.error("Link Web App Google belum dimasukkan di dalam kode.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    # -----------------------------------------------------------
    # 4. RIWAYAT TRANSAKSI
    # -----------------------------------------------------------
    elif menu == "📋 Riwayat Transaksi":
        st.markdown("<h2 style='color: #262626;'>📋 Riwayat Transaksi Global</h2>", unsafe_allow_html=True)
        st.markdown("<div style='background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #f0f0f0;'>", unsafe_allow_html=True)
        st.dataframe(st.session_state.transactions, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
