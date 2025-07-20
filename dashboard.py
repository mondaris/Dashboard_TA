import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Set page config - HARUS di atas
st.set_page_config(page_title="Dashboard Produk Terlaris", layout="wide")

# === Custom CSS ===
st.markdown("""
<style>
    /* Pusatkan layout */
    .appview-container .main .block-container {
        max-width: 1150px;
        padding-left: 2rem;
        padding-right: 2rem;
        margin-left: auto;
        margin-right: auto;
    }

    .main-header {
        font-size: 26px;
        font-weight: bold;
        color: white;
        background-color: black;
        padding: 20px;
        margin-bottom: 0;
        text-align: center;
        border-radius: 6px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: black;
        padding: 10px;
        border-radius: 6px 6px 0 0;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        color: white;
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
        background-color: #222;
        border: 1px solid #444;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .cons {
        max-width: 800px;
        padding-left: 3rem;
        padding-right: 3rem;
        margin-left: auto;
        margin-right: auto;           
    }
</style>
""", unsafe_allow_html=True)

# === Header ===
st.markdown('<div class="main-header">Dashboard Produk Terlaris</div>', unsafe_allow_html=True)

# === Load Data ===
df = pd.read_csv("hasil_klasifikasi.csv")
df['Tanggal'] = pd.to_datetime(df['Tanggal'])
df['Bulan'] = df['Tanggal'].dt.to_period('M').astype(str)

# === Tabs ===
tab1, tab2 = st.tabs(["📊 Hasil Klasifikasi SVM", "📈 Tren Pasar"])

# ========================== TAB 1 ========================== #
with tab1:
    # === Tabel ===
    st.markdown('<div class="subheader">Tabel Hasil Klasifikasi</div>', unsafe_allow_html=True)
    df['Tanggal'] = df['Tanggal'].dt.date.astype(str)
    st.dataframe(
        df[['Kategori', 'Nama_Produk', 'Lokasi_Toko', 'Harga_Produk', 'Terjual', 'Rating', 'Terlaris', 'Tanggal']],
        use_container_width=True
    )

    st.markdown('<div class="chart-title">Top 1 Produk Paling Laris per Kategori</div>', unsafe_allow_html=True)
    df_top1_produk = df.sort_values(by='Terjual', ascending=False).drop_duplicates(subset='Kategori')
    df_top1_produk = df_top1_produk[['Kategori', 'Nama_Produk', 'Terjual']].reset_index(drop=True)
    st.dataframe(df_top1_produk, use_container_width=True)
    st.markdown('<div class="chart-title">Grafik Penjualan Terbanyak Berdasarkan Kategori</div>', unsafe_allow_html=True)
    df_summary = df.groupby(['Kategori', 'Terlaris'])['Terjual'].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(15, 4))
    sns.barplot(data=df_summary, x='Kategori', y='Terjual', hue='Terlaris', ax=ax1)
    ax1.set_title("Total Penjualan per Kategori")
    ax1.set_ylabel("Jumlah Terjual")
    ax1.set_xlabel("Kategori")
    ax1.tick_params(axis='x', rotation=45)
    st.pyplot(fig1)

    st.markdown('<div class="chart-title">Distribusi Penjualan Terlaris Berdasarkan Lokasi Toko</div>', unsafe_allow_html=True)
    lokasi_terlaris = df[df['Terlaris'] == 1].groupby('Lokasi_Toko')['Terlaris'].sum().reset_index()
    lokasi_terlaris = lokasi_terlaris[lokasi_terlaris['Terlaris'] > 0]
    lokasi_terlaris = lokasi_terlaris.sort_values(by='Terlaris', ascending=False)
    fig3, ax3 = plt.subplots(figsize=(20, 20))
    sns.barplot(data=lokasi_terlaris, x='Terlaris', y='Lokasi_Toko', ax=ax3, palette='viridis')
    ax3.set_title("Penjualan Terlaris per Lokasi")
    ax3.set_xlabel("Jumlah Produk Terlaris")
    ax3.set_ylabel("Lokasi Toko")
    st.pyplot(fig3)

# ========================== TAB 2 ========================== #
with tab2:
    st.markdown('<div class="subheader">Tren Pasar</div>', unsafe_allow_html=True)

    col1, col2= st.columns([1, 1])

    with col1:
        st.markdown('<div class="chart-title">Tren Penjualan per Bulan</div>', unsafe_allow_html=True)
        df_tren = df.groupby(['Kategori', 'Bulan'])['Terjual'].sum().reset_index()
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.lineplot(data=df_tren, x='Bulan', y='Terjual', hue='Kategori', marker="o", ax=ax2)
        ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
        ax2.set_xlabel("Bulan")
        ax2.set_ylabel("Jumlah Terjual")
        ax2.set_title("Tren Bulanan")
        ax2.tick_params(axis='x', rotation=45)
        ax2.legend(title='Kategori', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig2)
    
    with col2:
        st.markdown('<div class="chart-title">Penjualan Event Tokopedia 6.6</div>', unsafe_allow_html=True)
        df_event = df[df['Tanggal'] == '2025-06-06']
        if not df_event.empty:
            df_event_summary = df_event.groupby('Kategori')['Terjual'].sum().reset_index()
            fig_event, ax_event = plt.subplots(figsize=(14,6.28))
            sns.barplot(data=df_event_summary, x='Kategori', y='Terjual', ax=ax_event)
            ax_event.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
            ax_event.set_title("Penjualan Tanggal 6 Juni 2025")
            ax_event.set_xlabel("Kategori")
            ax_event.set_ylabel("Jumlah Terjual")
            ax_event.tick_params(axis='x', rotation=45)
            st.pyplot(fig_event)
        else:
            st.info("Tidak ada data pada tanggal 2025-06-06.")

    col3, col4= st.columns([1, 1])

    with col3:    
        st.markdown('<div class="chart-title">Top 10 Kategori Dengan Harga Tinggi</div>', unsafe_allow_html=True)
        # Pastikan harga berbentuk numerik
        df['Harga_Produk'] = df['Harga_Produk'].astype(str).str.replace(",", "").str.replace(".", "").astype(float)

        # Ambil produk termahal per kategori, lalu ambil 10 kategori teratas
        df_max_price_per_kategori = df.sort_values('Harga_Produk', ascending=False).drop_duplicates('Kategori')
        df_top10_harga = df_max_price_per_kategori.sort_values(by='Harga_Produk', ascending=False).head(10)

        # Pie Chart
        fig_pie, ax_pie = plt.subplots(figsize=(10, 15))
        ax_pie.pie(
            df_top10_harga['Harga_Produk'],
            labels=df_top10_harga['Kategori'],
            autopct=lambda pct: f'{pct:.1f}%',  # tampilkan persentase
            startangle=140,
            colors=sns.color_palette('coolwarm')
        )
        ax_pie.set_title("Distribusi 10 Kategori Berdasarkan Harga Produk Tertinggi")
        st.pyplot(fig_pie)

    with col4:
        st.markdown('<div class="chart-title">Rata-rata Rating Produk per Kategori</div>', unsafe_allow_html=True)    
        df_rating = df.groupby('Kategori')['Rating'].mean().sort_values(ascending=False).reset_index()
        fig, ax = plt.subplots(figsize=(6, 7.7))
        sns.barplot(data=df_rating, x='Rating', y='Kategori', palette='coolwarm', ax=ax)
        ax.set_title("Rata-rata Rating Produk per Kategori")
        ax.set_xlabel("Rating")
        ax.set_ylabel("Kategori")
        st.pyplot(fig)

    col5, col6, col7 = st.columns([1, 2, 1])

    with col6:
        st.markdown('<div class="chart-title">Top 10 Kategori Dengan Harga Rendah</div>', unsafe_allow_html=True)
        # Pastikan harga berbentuk numerik
        df['Harga_Produk'] = df['Harga_Produk'].astype(str).str.replace(",", "").str.replace(".", "").astype(float)

        # Ambil produk termurah per kategori, lalu ambil 10 kategori teratas
        df_max_price_per_kategori = df.sort_values('Harga_Produk', ascending=True).drop_duplicates('Kategori')
        df_top10_harga = df_max_price_per_kategori.sort_values(by='Harga_Produk', ascending=True).head(10)

        # Warna solid (bisa sesuaikan jumlah dan warna sesuai preferensi)
        solid_colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A8', '#FFBD33',
                        '#33FFF2', '#8E44AD', '#2ECC71', '#E74C3C', '#2980B9']

        # Pie Chart
        fig_pie1, ax_pie = plt.subplots(figsize=(9, 7))
        ax_pie.pie(
            df_top10_harga['Harga_Produk'],
            labels=df_top10_harga['Kategori'],
            autopct=lambda pct: f'{pct:.1f}%',  # tampilkan persentase
            startangle=140,
            colors=solid_colors
        )
        ax_pie.set_title("Distribusi 10 Kategori Berdasarkan Harga Produk Terendah")
        st.pyplot(fig_pie1)
