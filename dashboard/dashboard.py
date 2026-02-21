import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from pathlib import Path

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Analisis Bike Sharing",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚴 Dashboard Analisis Bike Sharing Dataset</h1>', unsafe_allow_html=True)
st.markdown("---")

# Informasi Proyek
with st.expander("ℹ️ Informasi Proyek", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Nama:** Rafie Najwan Anjasmara")
        st.write("**Email:** rafie.anjasmara@gmail.com")
    with col2:
        st.write("**ID Dicoding:** rafienajwan")
        st.write("**Dataset:** Bike Sharing Dataset")

# Sidebar
with st.sidebar:
    st.image("https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg", width=80)
    st.title("🚴 Navigation")
    
    page = st.radio(
        "Pilih Halaman:",
        ["📊 Overview", "📈 Analisis Utama", "🔍 Analisis Lanjutan", "📝 Kesimpulan"]
    )
    
    st.markdown("---")
    st.markdown("### Filter Data")
    
# Load data dengan path yang fleksibel
@st.cache_data
def load_data():
    # Coba beberapa kemungkinan path
    possible_paths = [
        './data/day.csv',
        '../data/day.csv',
        'data/day.csv',
    ]
    
    day_df = None
    hour_df = None
    
    for path in possible_paths:
        try:
            day_df = pd.read_csv(path)
            hour_df = pd.read_csv(path.replace('day.csv', 'hour.csv'))
            break
        except:
            continue
    
    if day_df is None:
        st.error("❌ File data tidak ditemukan! Pastikan file day.csv dan hour.csv ada di folder 'data/'")
        st.stop()
    
    # Data cleaning
    day_df.drop_duplicates(inplace=True)
    hour_df.drop_duplicates(inplace=True)
    day_df['season'] = day_df['season'].astype('category')
    hour_df['season'] = hour_df['season'].astype('category')
    
    # Konversi suhu ke Celsius
    day_df['temp_celsius'] = day_df['temp'] * 41
    hour_df['temp_celsius'] = hour_df['temp'] * 41
    
    # Mapping musim dan cuaca
    season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_labels = {
        1: 'Clear/Partly Cloudy',
        2: 'Mist/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Heavy Rain/Snow'
    }
    
    day_df['season_name'] = day_df['season'].map(season_labels)
    day_df['weather_name'] = day_df['weathersit'].map(weather_labels)
    hour_df['season_name'] = hour_df['season'].map(season_labels)
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Filter di sidebar
with st.sidebar:
    selected_season = st.multiselect(
        "Pilih Musim:",
        options=['Spring', 'Summer', 'Fall', 'Winter'],
        default=['Spring', 'Summer', 'Fall', 'Winter']
    )
    
    selected_weather = st.multiselect(
        "Pilih Kondisi Cuaca:",
        options=['Clear/Partly Cloudy', 'Mist/Cloudy', 'Light Snow/Rain'],
        default=['Clear/Partly Cloudy', 'Mist/Cloudy', 'Light Snow/Rain']
    )

# Filter data
day_filtered = day_df[
    (day_df['season_name'].isin(selected_season)) &
    (day_df['weather_name'].isin(selected_weather))
]
hour_filtered = hour_df[hour_df['season_name'].isin(selected_season)]

# ========== HALAMAN OVERVIEW ==========
if page == "📊 Overview":
    st.markdown('<h2 class="sub-header">📊 Overview Dataset</h2>', unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Penyewaan (2 Tahun)",
            value=f"{day_filtered['cnt'].sum():,.0f}",
            delta="Data Harian"
        )
    
    with col2:
        st.metric(
            label="Rata-rata Penyewaan/Hari",
            value=f"{day_filtered['cnt'].mean():,.0f}",
            delta=f"{day_filtered['cnt'].std():.0f} std"
        )
    
    with col3:
        st.metric(
            label="Penyewaan Tertinggi",
            value=f"{day_filtered['cnt'].max():,.0f}",
            delta="Dalam 1 Hari"
        )
    
    with col4:
        st.metric(
            label="Total Data Harian",
            value=f"{len(day_filtered)}",
            delta=f"{len(hour_filtered)} jam"
        )
    
    st.markdown("---")
    
    # Data Preview
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Dataset Harian (day.csv)")
        st.dataframe(day_filtered.head(10), use_container_width=True)
        
    with col2:
        st.subheader("🕐 Dataset Per Jam (hour.csv)")
        st.dataframe(hour_filtered.head(10), use_container_width=True)
    
    # Matriks Korelasi
    st.markdown('<h2 class="sub-header">🔗 Matriks Korelasi</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Korelasi - Data Harian**")
        fig, ax = plt.subplots(figsize=(8, 6))
        numerical_cols = day_filtered.select_dtypes(include=['float64', 'int64'])
        sns.heatmap(numerical_cols.corr(), annot=True, cmap='coolwarm', ax=ax, fmt='.2f', cbar_kws={'shrink': 0.8})
        ax.set_title('Correlation Matrix - Daily Data')
        st.pyplot(fig)
    
    with col2:
        st.write("**Korelasi - Data Per Jam**")
        fig, ax = plt.subplots(figsize=(8, 6))
        numerical_cols = hour_filtered.select_dtypes(include=['float64', 'int64'])
        sns.heatmap(numerical_cols.corr(), annot=True, cmap='coolwarm', ax=ax, fmt='.2f', cbar_kws={'shrink': 0.8})
        ax.set_title('Correlation Matrix - Hourly Data')
        st.pyplot(fig)

# ========== HALAMAN ANALISIS UTAMA ==========
elif page == "📈 Analisis Utama":
    st.markdown('<h2 class="sub-header">📈 Analisis Pertanyaan Bisnis</h2>', unsafe_allow_html=True)
    
    # Pertanyaan 1: Musim
    st.markdown("### 1️⃣ Musim dengan Total Penyewaan Tertinggi")
    
    rentals_by_season = day_filtered.groupby('season_name')['cnt'].sum().sort_values(ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        bars = ax.bar(rentals_by_season.index, rentals_by_season.values, color=colors)
        ax.set_title('Total Penyewaan Sepeda per Musim', fontsize=16, fontweight='bold')
        ax.set_xlabel('Musim', fontsize=12)
        ax.set_ylabel('Total Penyewaan', fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height):,}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("#### 📊 Insight:")
        st.info(f"""
        - **Musim Tertinggi:** {rentals_by_season.idxmax()}
        - **Total Penyewaan:** {rentals_by_season.max():,.0f}
        - **Musim Terendah:** {rentals_by_season.idxmin()}
        - **Selisih:** {rentals_by_season.max() - rentals_by_season.min():,.0f}
        
        Musim Fall dan Summer memiliki penyewaan tertinggi, kemungkinan karena cuaca yang lebih mendukung.
        """)
    
    st.markdown("---")
    
    # Pertanyaan 2: Pengaruh Suhu Harian
    st.markdown("### 2️⃣ Pengaruh Suhu terhadap Penyewaan Harian")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(day_filtered['temp_celsius'], day_filtered['cnt'], alpha=0.5, s=30)
        
        # Regression line
        z = np.polyfit(day_filtered['temp_celsius'], day_filtered['cnt'], 1)
        p = np.poly1d(z)
        ax.plot(day_filtered['temp_celsius'], p(day_filtered['temp_celsius']), "r-", linewidth=2)
        
        ax.set_title('Pengaruh Suhu terhadap Total Penyewaan Harian', fontsize=16, fontweight='bold')
        ax.set_xlabel('Suhu (°C)', fontsize=12)
        ax.set_ylabel('Total Penyewaan', fontsize=12)
        ax.grid(alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        correlation = day_filtered['temp'].corr(day_filtered['cnt'])
        st.markdown("#### 📊 Insight:")
        st.success(f"""
        - **Korelasi:** {correlation:.4f}
        - **Tipe:** Korelasi Positif Kuat
        
        Suhu memiliki pengaruh positif yang signifikan terhadap penyewaan. Semakin tinggi suhu (hingga batas optimal), semakin banyak penyewaan.
        """)
        
        # Kategori suhu
        day_filtered['temp_category'] = pd.cut(
            day_filtered['temp_celsius'], 
            bins=[0, 10, 20, 30, 41],
            labels=['Dingin', 'Sejuk', 'Hangat', 'Panas']
        )
        avg_by_temp = day_filtered.groupby('temp_category', observed=True)['cnt'].mean().sort_values(ascending=False)
        
        st.write("**Rata-rata per Kategori:**")
        for cat, val in avg_by_temp.items():
            st.write(f"- {cat}: {val:,.0f}")
    
    st.markdown("---")
    
    # Pertanyaan 3: Pengaruh Suhu per Periode Waktu
    st.markdown("### 3️⃣ Pengaruh Suhu pada Jam Tertentu")
    
    hour_filtered['hour_category'] = pd.cut(
        hour_filtered['hr'], 
        bins=[-1, 6, 12, 18, 24],
        labels=['Malam (00-06)', 'Pagi (07-12)', 'Siang (13-18)', 'Sore (19-24)']
    )
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Pengaruh Suhu terhadap Penyewaan per Periode Waktu', fontsize=16, fontweight='bold')
    
    hour_categories = ['Malam (00-06)', 'Pagi (07-12)', 'Siang (13-18)', 'Sore (19-24)']
    colors_period = ['#3498db', '#e74c3c', '#f39c12', '#9b59b6']
    
    for idx, (category, color) in enumerate(zip(hour_categories, colors_period)):
        ax = axes[idx // 2, idx % 2]
        data = hour_filtered[hour_filtered['hour_category'] == category]
        
        ax.scatter(data['temp_celsius'], data['cnt'], alpha=0.3, s=20, color=color)
        
        # Regression line
        if len(data) > 0:
            z = np.polyfit(data['temp_celsius'], data['cnt'], 1)
            p = np.poly1d(z)
            ax.plot(data['temp_celsius'], p(data['temp_celsius']), "r-", linewidth=2)
            
            corr = data['temp_celsius'].corr(data['cnt'])
            ax.text(0.05, 0.95, f'Korelasi: {corr:.3f}', 
                   transform=ax.transAxes,
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                   verticalalignment='top')
        
        ax.set_title(f'Periode: {category}', fontsize=11, fontweight='bold')
        ax.set_xlabel('Suhu (°C)', fontsize=10)
        ax.set_ylabel('Total Penyewaan', fontsize=10)
        ax.grid(alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.info("""
    **Insight:**
    - Pengaruh suhu bervariasi per periode waktu
    - Korelasi paling kuat terjadi pada periode Siang dan Sore
    - Pada malam hari, pengaruh suhu lebih lemah karena volume penyewaan rendah
    """)
    
    st.markdown("---")
    
    # Pertanyaan 4: Kondisi Cuaca
    st.markdown("### 4️⃣ Pengaruh Kondisi Cuaca")
    
    rentals_by_weather = day_filtered.groupby('weather_name')['cnt'].agg(['mean', 'sum', 'count']).sort_values('mean', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Rata-rata Penyewaan per Kondisi Cuaca**")
        fig, ax = plt.subplots(figsize=(8, 6))
        colors_weather = ['#2ECC71', '#F39C12', '#E74C3C']
        bars = ax.bar(rentals_by_weather.index, rentals_by_weather['mean'], color=colors_weather[:len(rentals_by_weather)])
        ax.set_title('Rata-rata Penyewaan per Kondisi Cuaca', fontsize=14, fontweight='bold')
        ax.set_xlabel('Kondisi Cuaca', fontsize=11)
        ax.set_ylabel('Rata-rata Penyewaan', fontsize=11)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height):,}',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.write("**Distribusi Penyewaan per Kondisi Cuaca**")
        fig, ax = plt.subplots(figsize=(8, 6))
        
        weather_order = [w for w in ['Clear/Partly Cloudy', 'Mist/Cloudy', 'Light Snow/Rain'] if w in day_filtered['weather_name'].unique()]
        
        sns.boxplot(
            x='weather_name', y='cnt', data=day_filtered, ax=ax,
            order=weather_order,
            hue='weather_name', palette=colors_weather[:len(weather_order)], legend=False
        )
        ax.set_title('Distribusi Penyewaan per Kondisi Cuaca', fontsize=14, fontweight='bold')
        ax.set_xlabel('Kondisi Cuaca', fontsize=11)
        ax.set_ylabel('Total Penyewaan', fontsize=11)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    st.success(f"""
    **Insight:**
    - **Cuaca Terbaik:** {rentals_by_weather['mean'].idxmax()} ({rentals_by_weather['mean'].max():,.0f} rata-rata)
    - **Cuaca Terburuk:** {rentals_by_weather['mean'].idxmin()} ({rentals_by_weather['mean'].min():,.0f} rata-rata)
    - Cuaca cerah menghasilkan penyewaan 2-3x lebih tinggi dibanding cuaca buruk
    """)

# ========== HALAMAN ANALISIS LANJUTAN ==========
elif page == "🔍 Analisis Lanjutan":
    st.markdown('<h2 class="sub-header">🔍 Analisis Pola Penyewaan Per Jam</h2>', unsafe_allow_html=True)
    
    hourly_pattern = hour_filtered.groupby('hr')['cnt'].mean()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(hourly_pattern.index, hourly_pattern.values, marker='o', linewidth=2, markersize=8, color='#3498db')
        ax.fill_between(hourly_pattern.index, hourly_pattern.values, alpha=0.3)
        ax.set_title('Pola Rata-rata Penyewaan Sepeda per Jam dalam Sehari', fontsize=16, fontweight='bold')
        ax.set_xlabel('Jam', fontsize=12)
        ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
        ax.grid(alpha=0.3)
        ax.set_xticks(range(0, 24))
        
        # Highlight rush hours
        rush_morning = hourly_pattern[7:9].mean()
        rush_evening = hourly_pattern[17:19].mean()
        ax.axvspan(7, 9, alpha=0.2, color='orange', label='Rush Hour Pagi')
        ax.axvspan(17, 19, alpha=0.2, color='red', label='Rush Hour Sore')
        ax.legend()
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("#### 📊 Statistik Pola Per Jam:")
        st.metric("Jam Tersibuk", f"{hourly_pattern.idxmax()}:00", f"{hourly_pattern.max():.0f} penyewaan")
        st.metric("Jam Tersepi", f"{hourly_pattern.idxmin()}:00", f"{hourly_pattern.min():.0f} penyewaan")
        st.metric("Rata-rata Rush Hour Pagi", "", f"{rush_morning:.0f} penyewaan")
        st.metric("Rata-rata Rush Hour Sore", "", f"{rush_evening:.0f} penyewaan")
        
        st.markdown("#### 🎯 Insight:")
        st.info("""
        - Terdapat **2 puncak penyewaan** (rush hour):
          * Pagi: 07:00-08:00
          * Sore: 17:00-18:00
        - Pola menunjukkan sepeda digunakan untuk **commuting**
        - Penyewaan terendah di dini hari (03:00-04:00)
        """)
    
    # Analisis per musim dan jam
    st.markdown("---")
    st.markdown("### 📅 Pola Penyewaan Per Jam Berdasarkan Musim")
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    for season in ['Spring', 'Summer', 'Fall', 'Winter']:
        if season in hour_filtered['season_name'].unique():
            season_data = hour_filtered[hour_filtered['season_name'] == season]
            hourly_by_season = season_data.groupby('hr')['cnt'].mean()
            ax.plot(hourly_by_season.index, hourly_by_season.values, marker='o', label=season, linewidth=2)
    
    ax.set_title('Pola Penyewaan Per Jam Berdasarkan Musim', fontsize=16, fontweight='bold')
    ax.set_xlabel('Jam', fontsize=12)
    ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
    ax.grid(alpha=0.3)
    ax.set_xticks(range(0, 24))
    ax.legend(title='Musim', fontsize=10)
    plt.tight_layout()
    st.pyplot(fig)

# ========== HALAMAN KESIMPULAN ==========
elif page == "📝 Kesimpulan":
    st.markdown('<h2 class="sub-header">📝 Kesimpulan & Rekomendasi</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Kesimpulan Analisis Bike Sharing Dataset
    
    #### 1. **Musim dan Penyewaan Sepeda**
    - 🍂 **Musim Fall (Gugur)** mencatat total penyewaan sepeda tertinggi
    - ☀️ Diikuti oleh **Summer (Panas)** di posisi kedua
    - 🌱 **Spring (Semi)** memiliki penyewaan terendah
    - 📊 Faktor cuaca musiman sangat berpengaruh terhadap perilaku penyewaan
    
    #### 2. **Pengaruh Suhu pada Penyewaan Harian**
    - 📈 Terdapat **korelasi positif yang kuat** antara suhu dan jumlah penyewaan
    - 🌡️ Suhu hangat **(20-30°C)** menghasilkan tingkat penyewaan optimal
    - ❄️ Suhu ekstrem (terlalu dingin atau terlalu panas) menurunkan penyewaan
    
    #### 3. **Pengaruh Suhu pada Jam Tertentu**
    - ⏰ Pengaruh suhu terhadap penyewaan **bervariasi di setiap periode waktu**
    - 🌞 Korelasi suhu-penyewaan paling kuat pada **periode siang dan sore hari**
    - 🌙 Pada malam hari, pengaruh suhu lebih lemah karena volume penyewaan rendah
    
    #### 4. **Kondisi Cuaca dan Penyewaan**
    - ☀️ Cuaca **cerah/sebagian berawan** menghasilkan rata-rata penyewaan tertinggi
    - 🌧️ Kondisi cuaca buruk (hujan/salju) **secara signifikan** menurunkan penyewaan
    - 📉 Perbedaan antara cuaca baik dan buruk sangat jelas mempengaruhi perilaku pengguna
    
    #### 5. **Pola Penyewaan Per Jam**
    - 🚴 Terdapat **2 puncak penyewaan** (rush hour): pagi (7-8) dan sore (17-18)
    - 💼 Pola menunjukkan sepeda banyak digunakan untuk **commuting** kerja/sekolah
    - 😴 Penyewaan terendah terjadi pada dini hari (03:00-04:00)
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 💡 Rekomendasi Bisnis
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📊 Strategi Operasional
        
        1. **Optimasi Musiman**
           - 🔼 Tingkatkan ketersediaan sepeda saat musim Fall dan Summer
           - 📢 Strategi promosi khusus saat musim Spring untuk meningkatkan demand
        
        2. **Manajemen Waktu**
           - ⏰ Tambah ketersediaan sepeda pada jam rush hour (07-08, 17-18)
           - 🔧 Jadwalkan maintenance pada jam-jam sepi (03-05 pagi)
        
        3. **Respons Cuaca**
           - ☀️ Maksimalkan operasional pada hari-hari dengan cuaca cerah
           - 🌡️ Optimalkan distribusi sepeda saat suhu 20-30°C
        """)
    
    with col2:
        st.markdown("""
        #### 💰 Strategi Pemasaran
        
        1. **Program Cuaca**
           - 🌧️ Diskon khusus saat cuaca buruk untuk mempertahankan pelanggan
           - ☀️ Premium pricing saat cuaca cerah dan rush hour
        
        2. **Target Segmen**
           - 💼 Fokus pada commuters (paket langganan bulanan)
           - 🎯 Program loyalitas untuk pengguna rutin
        
        3. **Ekspansi Strategis**
           - 📍 Tambah lokasi stasiun di area perkantoran
           - 🚉 Kerjasama dengan transportasi publik
        """)
    
    st.markdown("---")
    
    # Summary metrics
    st.markdown("### 📈 Ringkasan Statistik Utama")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        best_season = day_df.groupby('season_name')['cnt'].sum().idxmax()
        st.metric("Musim Terbaik", best_season, "🍂")
    
    with col2:
        correlation = day_df['temp'].corr(day_df['cnt'])
        st.metric("Korelasi Suhu", f"{correlation:.3f}", "Positif Kuat")
    
    with col3:
        best_weather = day_df.groupby('weather_name')['cnt'].mean().idxmax()
        st.metric("Cuaca Terbaik", "Clear", "☀️")
    
    with col4:
        rush_hour = hour_df.groupby('hr')['cnt'].mean().idxmax()
        st.metric("Jam Tersibuk", f"{rush_hour}:00", "🚴")
    
    st.success("✅ Dashboard berhasil menampilkan semua analisis dan rekomendasi bisnis!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 1rem;'>
        <p>Dashboard Analisis Bike Sharing Dataset | Created with ❤️ using Streamlit</p>
        <p>© 2026 Rafie Najwan Anjasmara | Dicoding Fundamental Analisis Data</p>
    </div>
""", unsafe_allow_html=True)
