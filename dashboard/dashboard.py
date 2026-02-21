import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend untuk Streamlit Cloud
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import warnings
warnings.filterwarnings('ignore')

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
    import os
    
    # Coba beberapa kemungkinan path
    possible_paths = [
        'data/day.csv',  # Untuk Streamlit Cloud (root repo)
        './data/day.csv',
        '../data/day.csv',
        os.path.join(os.path.dirname(__file__), '..', 'data', 'day.csv'),  # Relative to dashboard.py
    ]
    
    day_df = None
    hour_df = None
    
    for path in possible_paths:
        try:
            day_df = pd.read_csv(path)
            hour_df = pd.read_csv(path.replace('day.csv', 'hour.csv'))
            break
        except Exception as e:
            continue
    
    if day_df is None:
        st.error("❌ File data tidak ditemukan! Pastikan file day.csv dan hour.csv ada di folder 'data/'")
        st.error(f"Tried paths: {possible_paths}")
        st.stop()
    
    # Data cleaning
    day_df = day_df.drop_duplicates()
    hour_df = hour_df.drop_duplicates()
    day_df = day_df.copy()  # Ensure we have a copy
    hour_df = hour_df.copy()
    
    # Konversi datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'], errors='coerce')
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'], errors='coerce')
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
].copy()
hour_filtered = hour_df[hour_df['season_name'].isin(selected_season)].copy()

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
    st.markdown('<h2 class="sub-header">🔍 Teknik Analisis Lanjutan</h2>', unsafe_allow_html=True)
    
    # Tab untuk berbagai analisis lanjutan
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Segmentasi Demand", "📅 Weekday vs Weekend", "👥 Casual vs Registered", "🎯 Multi-Dimensional Clustering"])
    
    # TAB 1: Manual Grouping - Segmentasi Demand
    with tab1:
        st.markdown("### Manual Grouping: Segmentasi Hari Berdasarkan Demand")
        
        # Clustering berdasarkan demand level
        q1 = day_filtered['cnt'].quantile(0.33)
        q2 = day_filtered['cnt'].quantile(0.67)
        
        day_filtered['demand_level'] = pd.cut(day_filtered['cnt'], 
                                              bins=[0, q1, q2, day_filtered['cnt'].max()],
                                              labels=['Low Demand', 'Medium Demand', 'High Demand'],
                                              include_lowest=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            low_count = len(day_filtered[day_filtered['demand_level'] == 'Low Demand'])
            st.metric("Low Demand Days", low_count, f"< {q1:.0f} penyewaan")
        
        with col2:
            med_count = len(day_filtered[day_filtered['demand_level'] == 'Medium Demand'])
            st.metric("Medium Demand Days", med_count, f"{q1:.0f}-{q2:.0f}")
        
        with col3:
            high_count = len(day_filtered[day_filtered['demand_level'] == 'High Demand'])
            st.metric("High Demand Days", high_count, f"> {q2:.0f} penyewaan")
        
        # Visualisasi
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 6))
            demand_counts = day_filtered['demand_level'].value_counts()
            colors = ['#E74C3C', '#F39C12', '#2ECC71']
            ax.bar(demand_counts.index, demand_counts.values, color=colors)
            ax.set_title('Distribusi Jumlah Hari per Demand Level', fontsize=14, fontweight='bold')
            ax.set_ylabel('Jumlah Hari', fontsize=11)
            ax.grid(axis='y', alpha=0.3)
            
            for i, (label, value) in enumerate(demand_counts.items()):
                ax.text(i, value + 2, str(value), ha='center', fontweight='bold')
            
            plt.xticks(rotation=15)
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(8, 6))
            temp_by_demand = day_filtered.groupby('demand_level', observed=True)['temp_celsius'].mean()
            ax.bar(range(len(temp_by_demand)), temp_by_demand.values, color=colors)
            ax.set_title('Rata-rata Suhu per Demand Level', fontsize=14, fontweight='bold')
            ax.set_ylabel('Suhu (°C)', fontsize=11)
            ax.set_xticks(range(len(temp_by_demand)))
            ax.set_xticklabels(temp_by_demand.index, rotation=15)
            ax.grid(axis='y', alpha=0.3)
            
            for i, value in enumerate(temp_by_demand.values):
                ax.text(i, value + 0.5, f'{value:.1f}°C', ha='center', fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig)
        
        st.success("""
        **Insight:**
        - Hari dengan **High Demand** cenderung memiliki suhu lebih tinggi (optimal)
        - Hari dengan **Low Demand** terjadi saat cuaca buruk atau suhu ekstrem
        - Segmentasi ini berguna untuk **perencanaan operasional** dan **pricing dinamis**
        """)
    
    # TAB 2: Weekday vs Weekend
    with tab2:
        st.markdown("### Analisis Weekday vs Weekend")
        
        # Tambahkan kolom day_type
        day_filtered['day_type'] = day_filtered['weekday'].apply(lambda x: 'Weekend' if x in [0, 6] else 'Weekday')
        hour_filtered['day_type'] = hour_filtered['weekday'].apply(lambda x: 'Weekend' if x in [0, 6] else 'Weekday')
        
        col1, col2 = st.columns(2)
        
        with col1:
            avg_by_type = day_filtered.groupby('day_type')['cnt'].mean()
            st.metric("Rata-rata Weekday", f"{avg_by_type.get('Weekday', 0):.0f}", "penyewaan/hari")
        
        with col2:
            st.metric("Rata-rata Weekend", f"{avg_by_type.get('Weekend', 0):.0f}", "penyewaan/hari")
        
        # Visualisasi perbandingan
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 6))
            avg_by_type.plot(kind='bar', ax=ax, color=['#3498db', '#e74c3c'])
            ax.set_title('Rata-rata Penyewaan: Weekday vs Weekend', fontsize=14, fontweight='bold')
            ax.set_ylabel('Rata-rata Penyewaan', fontsize=11)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
            ax.grid(axis='y', alpha=0.3)
            
            for i, (label, value) in enumerate(avg_by_type.items()):
                ax.text(i, value + 100, f'{value:.0f}', ha='center', fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(8, 6))
            casual_reg_data = day_filtered.groupby('day_type')[['casual', 'registered']].mean()
            x = range(len(casual_reg_data))
            width = 0.35
            ax.bar([i - width/2 for i in x], casual_reg_data['casual'], width, label='Casual', color='#f39c12')
            ax.bar([i + width/2 for i in x], casual_reg_data['registered'], width, label='Registered', color='#2ecc71')
            ax.set_title('Casual vs Registered: Weekday vs Weekend', fontsize=14, fontweight='bold')
            ax.set_ylabel('Rata-rata Penyewaan', fontsize=11)
            ax.set_xticks(x)
            ax.set_xticklabels(casual_reg_data.index)
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        
        # Pola per jam
        st.markdown("### Pola Per Jam: Weekday vs Weekend")
        
        col1, col2 = st.columns(2)
        
        with col1:
            weekday_hourly = hour_filtered[hour_filtered['day_type'] == 'Weekday'].groupby('hr')['cnt'].mean()
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(weekday_hourly.index, weekday_hourly.values, marker='o', linewidth=2, color='#3498db')
            ax.fill_between(weekday_hourly.index, weekday_hourly.values, alpha=0.3, color='#3498db')
            ax.axvspan(7, 9, alpha=0.2, color='orange', label='Rush Pagi')
            ax.axvspan(17, 19, alpha=0.2, color='red', label='Rush Sore')
            ax.set_title('Pola Weekday - Commuting Pattern', fontsize=14, fontweight='bold')
            ax.set_xlabel('Jam', fontsize=11)
            ax.set_ylabel('Rata-rata Penyewaan', fontsize=11)
            ax.set_xticks(range(0, 24, 2))
            ax.legend()
            ax.grid(alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            weekend_hourly = hour_filtered[hour_filtered['day_type'] == 'Weekend'].groupby('hr')['cnt'].mean()
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(weekend_hourly.index, weekend_hourly.values, marker='o', linewidth=2, color='#e74c3c')
            ax.fill_between(weekend_hourly.index, weekend_hourly.values, alpha=0.3, color='#e74c3c')
            ax.set_title('Pola Weekend - Recreational Pattern', fontsize=14, fontweight='bold')
            ax.set_xlabel('Jam', fontsize=11)
            ax.set_ylabel('Rata-rata Penyewaan', fontsize=11)
            ax.set_xticks(range(0, 24, 2))
            ax.grid(alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        
        st.info("""
        **Insight:**
        - **Weekday**: Pola commuting jelas dengan 2 puncak (07-08 & 17-18)
        - **Weekend**: Pola rekreasi tersebar merata sepanjang siang hari
        - **Casual users** lebih dominan di weekend
        - **Registered users** lebih konsisten di weekday (commuters)
        """)
    
    # TAB 3: Casual vs Registered
    with tab3:
        st.markdown("### Segmentasi Pengguna: Casual vs Registered")
        
        total_casual = day_filtered['casual'].sum()
        total_registered = day_filtered['registered'].sum()
        total_all = day_filtered['cnt'].sum()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Casual", f"{total_casual:,.0f}", f"{total_casual/total_all*100:.1f}%")
        
        with col2:
            st.metric("Total Registered", f"{total_registered:,.0f}", f"{total_registered/total_all*100:.1f}%")
        
        with col3:
            st.metric("Total Semua", f"{total_all:,.0f}", "100%")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            fig, ax = plt.subplots(figsize=(8, 6))
            sizes = [total_casual, total_registered]
            colors = ['#f39c12', '#2ecc71']
            explode = (0.1, 0)
            ax.pie(sizes, explode=explode, labels=['Casual', 'Registered'], 
                   autopct='%1.1f%%', colors=colors, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
            ax.set_title('Proporsi Total Penyewaan', fontsize=14, fontweight='bold')
            st.pyplot(fig)
        
        with col2:
            # Trend bulanan
            day_filtered['month'] = day_filtered['dteday'].dt.month
            monthly_users = day_filtered.groupby('month')[['casual', 'registered']].mean()
            
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(monthly_users.index, monthly_users['casual'], marker='o', label='Casual', color='#f39c12', linewidth=2)
            ax.plot(monthly_users.index, monthly_users['registered'], marker='s', label='Registered', color='#2ecc71', linewidth=2)
            ax.set_title('Trend Bulanan: Casual vs Registered', fontsize=14, fontweight='bold')
            ax.set_xlabel('Bulan', fontsize=11)
            ax.set_ylabel('Rata-rata Penyewaan', fontsize=11)
            ax.legend()
            ax.grid(alpha=0.3)
            ax.set_xticks(range(1, 13))
            plt.tight_layout()
            st.pyplot(fig)
        
        # Pengaruh cuaca
        st.markdown("### Pengaruh Kondisi Cuaca pada Tipe Pengguna")
        
        col1, col2 = st.columns(2)
        
        with col1:
            weather_casual = day_filtered.groupby('weather_name')['casual'].mean().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(range(len(weather_casual)), weather_casual.values, color='#f39c12')
            ax.set_title('Casual Users per Kondisi Cuaca', fontsize=14, fontweight='bold')
            ax.set_ylabel('Rata-rata Casual', fontsize=11)
            ax.set_xticks(range(len(weather_casual)))
            ax.set_xticklabels(weather_casual.index, rotation=15, ha='right', fontsize=9)
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            weather_registered = day_filtered.groupby('weather_name')['registered'].mean().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(range(len(weather_registered)), weather_registered.values, color='#2ecc71')
            ax.set_title('Registered Users per Kondisi Cuaca', fontsize=14, fontweight='bold')
            ax.set_ylabel('Rata-rata Registered', fontsize=11)
            ax.set_xticks(range(len(weather_registered)))
            ax.set_xticklabels(weather_registered.index, rotation=15, ha='right', fontsize=9)
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        
        # Korelasi
        corr_casual = day_filtered['casual'].corr(day_filtered['temp'])
        corr_registered = day_filtered['registered'].corr(day_filtered['temp'])
        
        st.success(f"""
        **Insight:**
        - **Registered users** mendominasi (~{total_registered/total_all*100:.0f}%) dan lebih konsisten
        - **Casual users** lebih sensitif terhadap cuaca (Korelasi suhu: {corr_casual:.3f})
        - **Registered users** lebih stabil (Korelasi suhu: {corr_registered:.3f}) - commuters reguler
        - Casual users meningkat signifikan di musim hangat & weekend
        """)
    
    # TAB 4: Multi-Dimensional Clustering
    with tab4:
        st.markdown("### Clustering Multi-Dimensional (Kombinasi Faktor)")
        
        # Buat kategori
        day_filtered['temp_level'] = pd.cut(day_filtered['temp_celsius'], 
                                            bins=[0, 15, 25, 41], 
                                            labels=['Cold', 'Moderate', 'Hot'])
        
        day_filtered['weather_quality'] = day_filtered['weathersit'].apply(
            lambda x: 'Good' if x == 1 else ('Fair' if x == 2 else 'Bad')
        )
        
        day_filtered['condition_cluster'] = day_filtered['temp_level'].astype(str) + ' + ' + day_filtered['weather_quality']
        
        # Analisis cluster
        cluster_analysis = day_filtered.groupby('condition_cluster', observed=True).agg({
            'cnt': ['count', 'mean'],
            'casual': 'mean',
            'registered': 'mean'
        })
        
        cluster_analysis.columns = ['_'.join(col).strip() for col in cluster_analysis.columns.values]
        cluster_analysis = cluster_analysis.sort_values('cnt_mean', ascending=False)
        
        # Top clusters
        top_clusters = cluster_analysis.nlargest(8, 'cnt_mean')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top Kondisi dengan Penyewaan Tertinggi")
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.barh(range(len(top_clusters)), top_clusters['cnt_mean'].values, color='#3498db')
            ax.set_yticks(range(len(top_clusters)))
            ax.set_yticklabels(top_clusters.index, fontsize=9)
            ax.set_xlabel('Rata-rata Penyewaan', fontsize=11)
            ax.grid(axis='x', alpha=0.3)
            ax.invert_yaxis()
            
            for i, value in enumerate(top_clusters['cnt_mean'].values):
                ax.text(value + 50, i, f'{value:.0f}', va='center', fontweight='bold', fontsize=9)
            
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.markdown("#### Heatmap: Suhu × Cuaca")
            heatmap_data = day_filtered.pivot_table(values='cnt', index='temp_level', 
                                                    columns='weather_quality', aggfunc='mean')
            
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='RdYlGn', ax=ax, 
                       cbar_kws={'label': 'Avg Rentals'})
            ax.set_title('Rata-rata Penyewaan (Suhu × Cuaca)', fontsize=14, fontweight='bold')
            ax.set_xlabel('Kualitas Cuaca', fontsize=11)
            ax.set_ylabel('Level Suhu', fontsize=11)
            plt.tight_layout()
            st.pyplot(fig)
        
        # Summary
        best_condition = cluster_analysis['cnt_mean'].idxmax()
        best_avg = cluster_analysis['cnt_mean'].max()
        worst_condition = cluster_analysis['cnt_mean'].idxmin()
        worst_avg = cluster_analysis['cnt_mean'].min()
        
        st.info(f"""
        **Insight:**
        - **Kondisi Terbaik**: {best_condition} → {best_avg:.0f} penyewaan/hari
        - **Kondisi Terburuk**: {worst_condition} → {worst_avg:.0f} penyewaan/hari
        - **Selisih**: {best_avg - worst_avg:.0f} penyewaan
        - **Efek Sinergis**: Kombinasi suhu optimal + cuaca baik memaksimalkan demand
        - Berguna untuk: prediksi demand, pricing dinamis, & perencanaan operasional
        """)
        
        # Top 5 clusters detail
        st.markdown("#### Detail Top 5 Kondisi")
        st.dataframe(
            top_clusters.head().style.format({
                'cnt_count': '{:.0f}',
                'cnt_mean': '{:.0f}',
                'casual_mean': '{:.0f}',
                'registered_mean': '{:.0f}'
            }),
            use_container_width=True
        )

# ========== HALAMAN KESIMPULAN ==========
elif page == "📝 Kesimpulan":
    st.markdown('<h2 class="sub-header">📝 Kesimpulan & Rekomendasi</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Kesimpulan Analisis Bike Sharing Dataset
    
    #### **📊 Analisis Pertanyaan Bisnis Utama:**
    
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
    
    ---
    
    #### **🔍 Analisis Lanjutan (Teknik Advanced):**
    
    #### 5. **Manual Grouping: Segmentasi Demand**
    - 📊 Hari dikelompokkan menjadi **Low, Medium, High Demand** berdasarkan volume penyewaan
    - 🌡️ **High Demand days** cenderung memiliki suhu hangat (20-30°C) dan cuaca cerah
    - 📉 **Low Demand days** terjadi saat cuaca buruk atau suhu ekstrem
    - 💡 Segmentasi ini membantu dalam **perencanaan operasional** dan **strategi pricing dinamis**
    
    #### 6. **Analisis Weekday vs Weekend**
    - 💼 **Weekday**: Pola commuting jelas dengan 2 puncak (jam 7-8 dan 17-18)
    - 🎉 **Weekend**: Pola rekreasi tersebar merata sepanjang siang hari
    - 👥 **Casual users** lebih dominan di weekend (recreational activities)
    - 👔 **Registered users** lebih konsisten di weekday (daily commuters)
    - 🔄 Perbedaan pola menunjukkan dua segmen pasar berbeda: commuters vs recreational users
    
    #### 7. **Segmentasi Pengguna (Casual vs Registered)**
    - 📈 **Registered users** mendominasi total penyewaan (±80%)
    - 🌤️ **Casual users** lebih **sensitif terhadap cuaca** - meningkat signifikan saat cerah
    - 🔒 **Registered users** lebih **konsisten** terlepas dari kondisi cuaca (commuters reguler)
    - 📅 Trend bulanan: kedua segmen meningkat di musim hangat (Summer & Fall)
    - 🎯 **Target marketing**: Casual = weekend promotions, Registered = loyalty programs
    
    #### 8. **Clustering Multi-Dimensional (Kombinasi Faktor)**
    - 🎯 **Kondisi optimal**: Suhu Moderate/Hot + Cuaca Good = penyewaan tertinggi
    - ⚡ **Efek sinergis**: Kombinasi suhu optimal + cuaca cerah memaksimalkan demand
    - ❌ **Kondisi terburuk**: Suhu Cold + Cuaca Bad = penyewaan terendah
    - 📊 **Heatmap analysis** menunjukkan pola clear: semakin baik cuaca & suhu, semakin tinggi penyewaan
    - 💼 Berguna untuk: **prediksi demand**, **pricing dinamis**, **perencanaan operasional**
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 💡 Rekomendasi Strategis Bisnis
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📊 Strategi Operasional
        
        1. **Optimasi Musiman**
           - 🔼 Tingkatkan ketersediaan sepeda **+30%** saat Fall & Summer
           - 📢 Program promosi khusus di Spring untuk boost demand
           - 🔄 Redistribusi armada berdasarkan forecast musiman
        
        2. **Manajemen Waktu**
           - ⏰ Tambah ketersediaan **+40%** pada rush hour (07-08, 17-18)
           - 🔧 Jadwalkan maintenance pada jam sepi (03-05 pagi)
           - 📍 Fokus penempatan di area perkantoran untuk weekday commuters
        
        3. **Respons Cuaca Real-time**
           - ☀️ Maksimalkan operasional pada hari cerah (forecast H-1)
           - 🌡️ Optimalkan saat suhu 20-30°C
           - 🌧️ Sediakan insentif khusus saat cuaca buruk untuk maintain usage
        
        4. **Segmentasi Operasional**
           - 📊 Gunakan clustering untuk **prediksi demand harian**
           - 🎯 Alokasikan sepeda berdasarkan **demand level** (Low/Med/High)
           - 📈 Implementasikan **dynamic inventory management**
        """)
    
    with col2:
        st.markdown("""
        #### 💰 Strategi Pemasaran & Pricing
        
        1. **Dynamic Pricing**
           - 💵 Premium pricing (+20%) saat: High Demand days, rush hour, cuaca cerah
           - 💸 Discount pricing (-15%) saat: Low Demand days, off-peak, cuaca buruk
           - 🎯 Pricing berbasis clustering conditions
        
        2. **Segmentasi Customer**
           - 👔 **Registered Users** (80%):
             * Paket langganan bulanan/tahunan
             * Program loyalitas dengan rewards
             * Priority access di rush hour
           - 🎉 **Casual Users** (20%):
             * Weekend special packages
             * Promosi musim hangat
             * Pay-per-ride dengan surge pricing
        
        3. **Campaign Targeting**
           - 💼 Weekday: Focus on commuters (corporate partnerships)
           - 🎊 Weekend: Recreational users (tourist packages)
           - ☀️ Summer campaign: Extended hours, family packages
           - ❄️ Winter campaign: Indoor destination partnerships
        
        4. **Ekspansi Strategis**
           - 📍 Tambah stasiun di area perkantoran & transit hubs
           - 🚉 Kerjasama dengan transportasi publik (first/last mile)
           - 🏢 Corporate membership programs
           - 🎓 Student discount programs
        """)
    
    st.markdown("---")
    
    # Summary metrics
    st.markdown("### 📈 Ringkasan Statistik Utama")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
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
    
    with col5:
        reg_pct = (day_df['registered'].sum() / day_df['cnt'].sum()) * 100
        st.metric("Registered %", f"{reg_pct:.0f}%", "Dominan")
    
    st.success("✅ **Dashboard berhasil menampilkan semua analisis utama dan lanjutan dengan teknik clustering, segmentasi, dan binning!**")
    
    st.markdown("---")
    
    st.markdown("""
    ### 🔬 Teknik Analisis yang Diterapkan
    
    ✅ **Manual Grouping & Binning**: Segmentasi demand (Low/Medium/High)  
    ✅ **Clustering Multi-Dimensional**: Kombinasi suhu × cuaca  
    ✅ **Cohort Analysis**: Weekday vs Weekend patterns  
    ✅ **User Segmentation**: Casual vs Registered behavior  
    ✅ **Correlation Analysis**: Pengaruh variabel terhadap demand  
    ✅ **Temporal Pattern Analysis**: Hourly, daily, seasonal trends  
    ✅ **Statistical Aggregation**: Mean, std, quartiles untuk segmentasi
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 1rem;'>
        <p>Dashboard Analisis Bike Sharing Dataset | Created with ❤️ using Streamlit</p>
        <p>© 2026 Rafie Najwan Anjasmara | Dicoding Fundamental Analisis Data</p>
        <p style='font-size: 0.9rem; margin-top: 0.5rem;'>
            ✅ Analisis Lanjutan: Manual Grouping | Clustering | Segmentasi | Binning
        </p>
    </div>
""", unsafe_allow_html=True)
