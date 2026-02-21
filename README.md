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

## 📈 Dashboard Features

✅ Overview & statistik  
✅ Visualisasi 4 pertanyaan bisnis  
✅ Analisis pola per jam  
✅ Filter interaktif  

## 📚 Dataset

Dataset dari UCI Machine Learning Repository - Bike Sharing Dataset
- Data harian: 731 entries (2 tahun)
- Data per jam: 17,379 entries

---

⭐ Star repository ini jika bermanfaat!
