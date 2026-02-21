# 🚴 Analisis Data Bike Sharing

## 📋 Deskripsi

Analisis komprehensif dataset bike sharing untuk memahami pola penyewaan sepeda dan faktor-faktor yang mempengaruhinya.

## 🎯 Pertanyaan Bisnis

1. **Musim mana yang memiliki total penyewaan sepeda tertinggi?**
2. **Bagaimana suhu mempengaruhi total penyewaan sepeda harian?**
3. **Bagaimana suhu mempengaruhi penyewaan sepeda pada jam tertentu?**
4. **Bagaimana kondisi cuaca mempengaruhi jumlah penyewaan sepeda?**

## 🛠️ Teknologi

- **Pandas** - Analisis data
- **Matplotlib & Seaborn** - Visualisasi
- **Streamlit** - Dashboard interaktif
- **Jupyter Notebook** - Eksplorasi data

## 📁 Struktur Proyek

```
📦 Project/
┣ 📂 data/
┃ ┣ day.csv
┃ ┗ hour.csv
┣ 📂 dashboard/
┃ ┗ dashboard.py
┣ notebook.ipynb
┗ requirements.txt
```

## 🚀 Setup & Instalasi

1. **Clone repository**
   ```bash
   git clone <repository-url>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan Jupyter Notebook**
   ```bash
   jupyter notebook notebook.ipynb
   ```

4. **Jalankan Dashboard Streamlit**
   ```bash
   streamlit run dashboard/dashboard.py
   ```

## 📊 Hasil Analisis

### 1. Pola Musiman 🍂
- **Musim Fall** memiliki penyewaan tertinggi
- **Summer** di posisi kedua
- **Spring** mencatat penyewaan terendah

**Rekomendasi:** Maksimalkan stok di musim Fall dan Summer, buat promosi khusus di Spring.

### 2. Pengaruh Suhu ☀️
- Korelasi positif kuat antara suhu dan penyewaan
- **Suhu optimal: 20-30°C** menghasilkan penyewaan tertinggi
- Suhu ekstrem menurunkan penyewaan

**Rekomendasi:** Optimasi operasional saat suhu 20-30°C, dynamic pricing berdasarkan prediksi suhu.

### 3. Pola Per Jam ⏰
- Dua puncak penyewaan:
  - **Pagi**: 07:00 - 08:00
  - **Sore**: 17:00 - 18:00
- Konsisten dengan jam commuting

**Rekomendasi:** Tingkatkan ketersediaan di rush hours, target commuters dengan paket subscription.

### 4. Kondisi Cuaca 🌦️
- **Cuaca cerah** → penyewaan tertinggi
- **Hujan/salju** → penurunan signifikan

**Rekomendasi:** Promosi saat cuaca buruk, sediakan aksesoris pelindung hujan.

## 🎯 Kesimpulan

Analisis menunjukkan bahwa **musim, suhu, dan kondisi cuaca** sangat mempengaruhi pola penyewaan sepeda:

1. **Musim Fall dan Summer** adalah periode optimal untuk bisnis bike sharing
2. **Suhu 20-30°C** menghasilkan demand tertinggi
3. **Jam commuting (7-8 pagi, 17-18 sore)** adalah waktu tersibuk
4. **Cuaca cerah** meningkatkan penyewaan hingga 2-3x lipat dibanding cuaca buruk

**Rekomendasi Strategis:**
- Optimasi stok dan pricing berdasarkan musim dan prediksi cuaca
- Target segmen commuters dengan program membership
- Sediakan insentif dan fasilitas tambahan saat kondisi non-ideal

## � Analisis Lanjutan

### Teknik Analisis yang Diterapkan:

✅ **Manual Grouping & Binning**
   - Segmentasi hari berdasarkan demand level (Low/Medium/High)
   - Identifikasi karakteristik setiap segmen untuk strategi operasional

✅ **Clustering Multi-Dimensional**
   - Kombinasi faktor: Suhu × Cuaca
   - Heatmap analysis untuk identifikasi kondisi optimal
   - Efek sinergis suhu dan cuaca terhadap demand

✅ **Cohort Analysis**
   - Perbandingan pola Weekday vs Weekend
   - Perbedaan perilaku commuting vs recreational users
   - Pattern analysis per periode waktu

✅ **User Segmentation**
   - Analisis Casual vs Registered users
   - Sensitivitas terhadap cuaca dan suhu
   - Target marketing berdasarkan segmen

✅ **Temporal Pattern Analysis**
   - Pola per jam, harian, musiman
   - Rush hour identification
   - Seasonal trends

### Insight Analisis Lanjutan:

1. **Demand Segmentation:**
   - High Demand days: Suhu optimal + cuaca cerah
   - Low Demand days: Cuaca buruk + suhu ekstrem
   - Berguna untuk dynamic pricing & inventory management

2. **Weekday vs Weekend:**
   - Weekday: Pola commuting (2 puncak)
   - Weekend: Pola recreational (tersebar merata)
   - Casual users dominan di weekend (>40%)

3. **User Behavior:**
   - Registered (80%): Konsisten, tidak terpengaruh cuaca
   - Casual (20%): Sensitif cuaca, meningkat saat cerah
   - Target berbeda: loyalty program vs promotional campaigns

4. **Multi-Dimensional Clustering:**
   - Best condition: Hot/Moderate temp + Good weather
   - Worst condition: Cold temp + Bad weather
   - Selisih demand: 4-5x lipat antara best & worst

## 📈 Dashboard Features

✅ **Overview & Statistik**
   - Metrics cards dengan key performance indicators
   - Data preview & correlation matrix

✅ **Analisis Utama**
   - Visualisasi 4 pertanyaan bisnis utama
   - Interactive charts dengan insights

✅ **Analisis Lanjutan** ⭐ (NEW!)
   - Tab Segmentasi Demand (Manual Grouping)
   - Tab Weekday vs Weekend Analysis
   - Tab Casual vs Registered Segmentation
   - Tab Multi-Dimensional Clustering with Heatmap

✅ **Kesimpulan & Rekomendasi**
   - Summary lengkap analisis
   - Strategi operasional & marketing
   - Key metrics dashboard

✅ **Filter Interaktif**
   - Filter musim
   - Filter kondisi cuaca
   - Dynamic data filtering  

## 📚 Dataset

Dataset dari UCI Machine Learning Repository - Bike Sharing Dataset
- Data harian: 731 entries (2 tahun)
- Data per jam: 17,379 entries

---

⭐ Star repository ini jika bermanfaat!
