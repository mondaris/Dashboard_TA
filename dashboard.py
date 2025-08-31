import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
from streamlit_option_menu import option_menu
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# ====== CONFIG PAGE ======
st.set_page_config(page_title="Produk Terlaris", layout='wide')

# ====== CUSTOM CSS ======
st.markdown("""
<style>
    .main-header {
        font-size: 26px;
        font-weight: bold;
        color: white;
        padding: 20px;
        text-align: center;
        border-radius: 6px;
    }
    .subheader {
        font-size: 25px;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 20px;
        color: white;
    }
    .chart-title {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 10px;
        color: white;
    }
    .card {
        background-color: #FFFF;
        border: 1px solid #444;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        color: black;
    }
    .card h3 { color: black; 
    }

    /* Konten utama flex 1 biar dorong footer ke bawah */
    .main {
        flex: 1;
        border-top: 2px solid rgba(255, 255, 255, 0.2);
    }

    /* Footer style */
    .footer {
        color: white;
        text-align: center;
        margin-top: 50px;
        padding: 20px ;
        font-size: 20px;
        font-weight: bold;
    }
            
    .copyright {
        color: white;
        text-align: center;
        margin-top: 40px;
        padding: 20px ;
        font-size: 14px;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR MENU =====
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Homepage", "Dashboard"],
        icons=["house", "bar-chart-line"],
        menu_icon="list",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#1E1E1E"},
            "icon": {"color": "white", "font-size": "14px"},
            "nav-link": {
                "font-size": "13px",
                "color": "white",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "rgba(255,255,255,0.1)",
            },
            "nav-link-selected": {
                "background-color": "rgba(255,255,255,0.2)",
                "color": "white",
            },
        }
    )

# ===================== HALAMAN HOMEPAGE =====================
if selected == "Homepage":
    st.markdown('<div class="main-header">Sistem Informasi Produk Terlaris Berdasarkan Kategori</div>', unsafe_allow_html=True)
    
    # Card 1: Selamat Datang
    st.markdown("""
    <div class="card">
        <p>Aplikasi ini dirancang untuk membantu menganalisis dan memvisualisasikan data penjualan 
        berdasarkan hasil scraping marketplace.</p>
        <p>✨ Fitur utama yang tersedia:</p>
        <ul>
            <li>📊 <strong>Klasifikasi Produk</strong> menggunakan algoritma Support Vector Machine (SVM) untuk menentukan 
            apakah produk termasuk kategori <em>Terlaris</em> atau <em>Tidak Terlaris</em>.</li>
            <li>📈 <strong>Visualisasi Tren Penjualan</strong> baik secara harian maupun mingguan untuk melihat pola 
            penjualan pada setiap kategori.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    
    col1, col2 = st.columns([1, 1])

    # Card 2: Manfaat Aplikasi
    with col1:
        st.markdown("""
        <div class="card">
            <h3>💡 Manfaat Aplikasi</h3>
            <ul>
                <li>Membantu pelaku bisnis mengidentifikasi produk dengan performa penjualan terbaik.</li>
                <li>Mendukung pengambilan keputusan strategis terkait stok, promosi, dan pengembangan produk.</li>
                <li>Menyediakan visualisasi data yang memudahkan interpretasi tren penjualan.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Card 3: Keunggulan Sistem
    with col2:
        st.markdown("""
        <div class="card">
            <h3>🚀 Keunggulan Sistem</h3>
            <ul>
                <li>Menggunakan algoritma machine learning SVM untuk klasifikasi produk secara akurat.</li>
                <li>Tampilan dashboard interaktif dan responsif.</li>
                <li>Mendukung analisis multi-kategori untuk evaluasi menyeluruh.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ===================== HALAMAN DASHBOARD =====================
elif selected == "Dashboard":
    # === Header ===
    st.markdown('<div class="main-header">Dashboard Produk Terlaris</div>', unsafe_allow_html=True)

    # === Template Dataset dari file dummy ===
    with open("template_klasifikasi.csv", "rb") as f:
        template_klasifikasi_csv = f.read()

    with open("template_tren.csv", "rb") as f:
        template_tren_csv = f.read()

    st.markdown("### 📥 Unduh Template Dataset")
    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📊 Unduh Template Klasifikasi",
            data=template_klasifikasi_csv,
            file_name="template_klasifikasi.csv",
            mime="text/csv"
        )

    with col2:
        st.download_button(
            label="📈 Unduh Template Tren Mingguan",
            data=template_tren_csv,
            file_name="template_tren.csv",
            mime="text/csv"
        )


    # === Upload Data ===
    uploaded_file = st.file_uploader("Upload file CSV hasil scraping (harus memuat kolom: 'Kategori', 'Nama_Produk', 'Lokasi_Toko', 'Harga Produk', 'Terjual', 'Rating', 'Terlaris')", type=["csv"])
    uploaded_tren = st.file_uploader("Upload file CSV hasil tren mingguan (harus memuat kolom: 'Kategori', 'Nama_Produk', 'Lokasi_Toko', 'Harga Produk', 'Terjual', 'Rating', 'Tanggal')", type=["csv"])

    if uploaded_file is not None and uploaded_tren is not None:
        df = pd.read_csv(uploaded_file)
        df_tren = pd.read_csv(uploaded_tren)
    else:
        st.warning("Silakan upload kedua file CSV terlebih dahulu.")
        st.stop()

    # === Tabs ===
    tab1, tab2 = st.tabs(["📊 Hasil Klasifikasi SVM", "📈 Tren Pasar"])

    # ========================== TAB 1 ========================== #
    with tab1:
        total_data = len(df)
        total_kategori = df['Kategori'].nunique()

        X = df[['Harga_Produk', 'Rating', 'Terjual']]
        y = df['Terlaris']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        svc = SVC()
        svc.fit(X_train, y_train)

        # Fungsi evaluasi model
        def evaluate_model(model, X_test, y_test):
            y_pred = model.predict(X_test)
            cm = confusion_matrix(y_test, y_pred)

            metrics = {}
            if cm.shape == (2, 2):
                tn, fp, fn, tp = cm.ravel()
                metrics.update({
                    'True Positive (TP)': tp,
                    'False Positive (FP)': fp,
                    'False Negative (FN)': fn,
                    'True Negative (TN)': tn
                })
            metrics['Accuracy'] = accuracy_score(y_test, y_pred)

            return metrics

        # Hitung metrik
        metrics = evaluate_model(svc, X_test, y_test)

        # ======== TAMPILKAN METRIK DALAM CARD ========
        st.markdown(f"""
        <div class="card" style="padding:15px; border-radius:10px; background-color:#f8f9fa; box-shadow: 0px 2px 8px rgba(0,0,0,0.1);">
            <h3 style="margin-bottom:10px;">Hasil Evaluasi Model SVM</h3>
            <p><strong>Accuracy:</strong> {metrics['Accuracy']*100:.2f}%</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <p>Model Support Vector Machine (SVM) digunakan untuk mengklasifikasikan produk menjadi dua kelas utama: <strong>Terlaris</strong> dan <strong>Tidak Terlaris</strong>.</p>
            <p>Akurasi model menunjukkan persentase prediksi yang benar dibandingkan dengan data aktual.</p>
        </div>
        """, unsafe_allow_html=True)


        # === Tabel ===
        st.markdown('<div class="subheader">Tabel Hasil Klasifikasi</div>', unsafe_allow_html=True)
        # df['Tanggal'] = df['Tanggal'].dt.date.astype(str)
        st.dataframe(
            df[['Kategori', 'Nama_Produk', 'Lokasi_Toko', 'Harga_Produk', 'Terjual', 'Rating', 'Terlaris']],
            use_container_width=True
        )

        st.markdown('<div class="chart-title">Distribusi Produk Terlaris vs Tidak Terlaris per Kategori</div>', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="card h3">
                <h3>Total Data Produk: {total_data:}</h3>
                <p>Jumlah Kategori: {total_kategori}</p>
            </div>
        """, unsafe_allow_html=True)    
        # Hitung jumlah produk terlaris dan tidak terlaris per kategori
        df_dist = df.groupby(['Kategori', 'Terlaris']).size().reset_index(name='Jumlah')
        # Ganti label Terlaris dari angka ke teks agar lebih informatif
        df_dist['Status'] = df_dist['Terlaris'].map({1: 'Terlaris', 0: 'Tidak Terlaris'})
        # Buat visualisasi
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(data=df_dist, y='Kategori', x='Jumlah', hue='Status', ax=ax, palette='Set2')
        # Judul dan label
        ax.set_title('Distribusi Produk Terlaris dan Tidak Terlaris per Kategori')
        ax.set_xlabel('Jumlah Produk')
        ax.set_ylabel('Kategori')
        ax.legend(title='Status')
        # Tampilkan di Streamlit
        st.pyplot(fig)
        st.markdown("""
        <div class="card">
            <ul>
                <li>Grafik menampilkan distribusi produk <strong>terlaris</strong> dan <strong>tidak terlaris</strong> pada tiap kategori.</li>
                <li>Kategori <strong>Perlengkapan Pesta</strong>, <strong>Perawatan Tubuh</strong>, dan <strong>Olahraga</strong> memiliki jumlah produk tinggi pada kedua klasifikasi.</li>
                <li>Produk <em>tidak terlaris</em> mendominasi hampir semua kategori, menunjukkan hanya sedikit produk dengan penjualan tinggi.</li>
                <li>Data ini bermanfaat untuk menganalisis potensi kompetisi dan menentukan kategori dengan rasio produk laris tertinggi untuk strategi pemasaran.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


        st.markdown('<div class="chart-title">Kategori Terlaris</div>', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="card">
                <h3>Total Data Produk: {total_data:}</h3>
            </div>
        """, unsafe_allow_html=True)
        # Hitung total produk terjual untuk setiap kategori
        df_total_terjual = df.groupby('Kategori')['Terjual'].sum().reset_index()
        # Filter hanya kategori dengan jumlah terjual lebih dari 0
        df_total_terjual = df_total_terjual[df_total_terjual['Terjual'] > 0]
        # Urutkan berdasarkan jumlah terjual dari yang tertinggi ke terendah
        df_total_terjual = df_total_terjual.sort_values(by='Terjual', ascending=False).reset_index(drop=True)
        # Tampilkan tabel di Streamlit
        st.dataframe(df_total_terjual, use_container_width=True)
        st.markdown("""
        <div class="card">
            <ul>
                <li><strong>Perlengkapan Pesta</strong> menjadi kategori dengan penjualan tertinggi (>3,28 juta unit), diikuti <strong>Kesehatan dan Kecantikan</strong> (1,76 juta unit) dan <strong>Perawatan Tubuh</strong> (1,00 juta unit).</li>
                <li><strong>Fashion</strong> dan <strong>Makanan & Minuman</strong> juga memiliki kontribusi penjualan besar, menunjukkan permintaan pasar yang tinggi.</li>
                <li>Kategori dengan kebutuhan fungsional & konsumsi rutin cenderung memiliki volume penjualan lebih tinggi, sehingga layak diprioritaskan dalam stok & strategi pemasaran.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)



    # ========================== TAB 2 ========================== #
    with tab2:
        st.markdown('<div class="subheader">Tren Pasar</div>', unsafe_allow_html=True)


        # Pastikan kolom Tanggal bertipe datetime
        df_tren['Tanggal'] = pd.to_datetime(df_tren['Tanggal'])
        # Filter hanya tanggal 23 Juli - 5 Agustus 2025
        start_date = pd.to_datetime('2025-07-23')
        end_date = pd.to_datetime('2025-08-05')
        df_tren = df_tren[(df_tren['Tanggal'] >= start_date) & (df_tren['Tanggal'] <= end_date)]
        # Tambahkan kolom Hari (1-14)
        df_tren['Hari'] = (df_tren['Tanggal'] - start_date).dt.days + 1
        # Tambahkan kolom Minggu
        df_tren['Minggu'] = df_tren['Hari'].apply(lambda x: 'Minggu 1' if x <= 7 else 'Minggu 2')
        # Hitung total terjual per kategori per hari
        df_harian = df_tren.groupby(['Hari', 'Kategori'])['Terjual'].sum().reset_index()
        # Visualisasi harian (sumbu X = Hari 1–14, garis pemisah Minggu 1 & 2)
        st.markdown('<div class="chart-title">Tren Penjualan Harian per Kategori (Hari 1–14)</div>', unsafe_allow_html=True)
        fig_harian, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df_harian, x='Hari', y='Terjual', hue='Kategori', marker='o', ax=ax)
        # Tambahkan garis vertikal di antara Minggu 1 & Minggu 2
        ax.axvline(7.5, color='red', linestyle='--', linewidth=1.5)
        ax.text(7.5, ax.get_ylim()[1]*0.95, 'Batas Minggu 1 & 2', color='red', ha='center')
        # Format tampilan
        ax.set_title("Tren Penjualan Harian per Kategori", fontsize=14)
        ax.set_xlabel("Hari", fontsize=12)
        ax.set_ylabel("Jumlah Terjual", fontsize=12)
        ax.set_xticks(range(1, 15))  # Hari 1–14
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(",", ".")))
        ax.legend(title='Kategori', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig_harian)
        st.markdown("""
        <div class="card">
            <ul>
                <li>Grafik menampilkan <strong>tren penjualan harian</strong> per kategori selama 14 hari.</li>
                <li>Garis putus-putus merah menandai <strong>batas Minggu 1 & Minggu 2</strong> (hari ke-7 & ke-8).</li>
                <li><strong>Perlengkapan Pesta</strong> & <strong>Perawatan Tubuh</strong> mendominasi penjualan, dengan puncak di hari ke-3 & ke-10.</li>
                <li><strong>Makanan & Minuman</strong>, <strong>Fashion</strong>, dan <strong>Pertukangan</strong> menunjukkan fluktuasi signifikan pada hari tertentu.</li>
                <li>Data bermanfaat untuk menentukan <strong>waktu promosi optimal</strong> & memahami potensi penjualan mingguan tiap kategori.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


        # Pastikan kolom Tanggal bertipe datetime
        df_tren['Tanggal'] = pd.to_datetime(df_tren['Tanggal'])
        # Tambahkan kolom Minggu berdasarkan tanggal
        df_tren['Minggu'] = df_tren['Tanggal'].apply(
            lambda x: 'Minggu 1' if x <= pd.to_datetime('2025-07-29') else 'Minggu 2'
        )
        # Filter hanya tanggal 23 Juli - 5 Agustus 2025
        start_date = pd.to_datetime('2025-07-23')
        end_date = pd.to_datetime('2025-08-05')
        df_tren = df_tren[(df_tren['Tanggal'] >= start_date) & (df_tren['Tanggal'] <= end_date)]
        # Hitung total terjual per kategori per minggu
        df_mingguan = df_tren.groupby(['Kategori', 'Minggu'])['Terjual'].sum().reset_index()
        # Untuk memastikan urutan minggu benar
        df_mingguan['Minggu'] = pd.Categorical(df_mingguan['Minggu'], categories=['Minggu 1', 'Minggu 2'], ordered=True)
        # Visualisasi
        st.markdown('<div class="chart-title">Tren Penjualan Mingguan per Kategori (Minggu 1 & 2: 23 Juli – 5 Agustus 2025)</div>', unsafe_allow_html=True)
        fig_mingguan, ax = plt.subplots(figsize=(6, 6))
        sns.lineplot(data=df_mingguan, x='Minggu', y='Terjual', hue='Kategori', marker='o', ax=ax)
        # Format tampilan
        ax.set_title("Tren Penjualan Mingguan per Kategori", fontsize=14)
        ax.set_xlabel("Minggu", fontsize=12)
        ax.set_ylabel("Jumlah Terjual", fontsize=12)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(",", ".")))
        ax.legend(title='Kategori', bbox_to_anchor=(1.05, 1), loc='upper left')
        # Tampilkan di Streamlit
        st.pyplot(fig_mingguan)
        st.markdown("""
        <div class="card">
            <ul>
                <li>Grafik menampilkan <strong>tren penjualan mingguan</strong> per kategori selama 2 minggu pengamatan.</li>
                <li>Mayoritas kategori mengalami <strong>penurunan penjualan</strong> dari Minggu 1 ke Minggu 2.</li>
                <li>Penurunan terbesar terjadi pada <strong>Perawatan Tubuh</strong> & <strong>Perlengkapan Pesta</strong>.</li>
                <li><strong>Fashion</strong> relatif stabil, sedangkan <strong>Properti</strong> & <strong>Buku</strong> punya volume penjualan rendah di kedua minggu.</li>
                <li>Data berguna untuk menentukan <strong>periode puncak penjualan</strong> & strategi promosi agar penurunan dapat diminimalkan.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


        # Filter hanya produk dengan Terjual > 1000 dan Rating > 0
        df_filtered = df_tren[(df_tren['Terjual'] > 1000) & (df_tren['Rating'] > 0)]
        # Hapus duplikat berdasarkan Nama_Produk
        df_filtered = df_filtered.drop_duplicates(subset=['Nama_Produk'])
        # Ambil Top 5 produk per kategori berdasarkan Rating tertinggi lalu Terjual terbanyak
        top5_produk_tren = (
            df_filtered.sort_values(['Kategori', 'Rating', 'Terjual'], ascending=[True, False, False])
                       .groupby('Kategori')
                       .head(5)
                       [['Kategori', 'Nama_Produk', 'Harga_Produk', 'Rating', 'Terjual']]
                       .reset_index(drop=True)
        )
        # Tampilkan di Streamlit
        st.markdown('<div class="chart-title">Top 5 Produk Terlaris per Kategori</div>', unsafe_allow_html=True)
        st.dataframe(top5_produk_tren, use_container_width=True)
        st.markdown("""
        <div class="card">
            <ul>
                <li>Menampilkan <strong>Top 5 produk terlaris</strong> tiap kategori, dipilih dari rating tertinggi & penjualan > 1.000 unit.</li>
                <li>Pada <strong>Fashion</strong>, produk seperti <em>CELANA CUTBRAY</em> & <em>Mister OLEZZZ</em> unggul dengan rating 5.0 & penjualan tinggi.</li>
                <li><strong>Perawatan Hewan</strong> & 🧴 <strong>Perawatan Tubuh</strong> punya produk harga tinggi namun tetap laris, seperti <em>beauty miss care virgicare</em> (Rp156.750, 9.000 unit).</li>
                <li>Berguna untuk <strong>identifikasi produk unggulan</strong> & acuan strategi pemasaran, stok, dan diversifikasi produk.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ==== KONFIGURASI EMAIL ====
    load_dotenv()

    EMAIL_PENGIRIM = st.secrets["EMAIL_PENGIRIM"]
    PASSWORD = st.secrets["PASSWORD"]
    EMAIL_TUJUAN = st.secrets["EMAIL_TUJUAN"]
    
    st.markdown("""
    <div class="main"></div>
    <div class="footer">
        Feedback Pengguna
    </div>""", unsafe_allow_html=True)
    # Form feedback
    with st.form("feedback_form"):
        nama = st.text_input("Nama (opsional)")
        email = st.text_input("Email (opsional)")
        feedback = st.text_area("Masukkan feedback Anda di sini")
        submit = st.form_submit_button("Kirim")
    
    if submit and feedback.strip() != "":
        try:
            # Membuat pesan email
            pesan = MIMEMultipart()
            pesan["From"] = EMAIL_PENGIRIM
            pesan["To"] = EMAIL_TUJUAN
            pesan["Subject"] = f"Feedback Baru dari {nama if nama else 'Pengguna'}"
    
            body = f"""
            Nama   : {nama}
            Email  : {email}
            --------------------------------
            Feedback:
            {feedback}
            """
            pesan.attach(MIMEText(body, "plain"))
    
            # Koneksi ke server Gmail
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_PENGIRIM, PASSWORD)
            server.sendmail(EMAIL_PENGIRIM, EMAIL_TUJUAN, pesan.as_string())
            server.quit()
    
            st.success("✅ Terima kasih! Feedback Anda berhasil terkirim ke email admin.")
    
        except Exception as e:
            st.error(f"❌ Gagal mengirim email: {e}")

st.markdown("""
<div class="copyright">
    Dikembangkan oleh Mohammad Nafiis Septiano<br>© 2025 Sistem Informasi Produk Terlaris Berdasarkan Kategori
</div>
""", unsafe_allow_html=True)


