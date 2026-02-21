# 🚴 Bike Sharing Dataset - Analisis Data

Proyek analisis data untuk memahami pola penyewaan sepeda dan faktor-faktor yang mempengaruhinya menggunakan dataset Bike Sharing.

---

## 📋 Project Organization

```
├── data/
│   ├── day.csv          # Data harian
│   └── hour.csv         # Data per jam
├── dashboard/
│   └── dashboard.py     # Streamlit dashboard
├── notebook.ipynb       # Analisis lengkap
├── requirements.txt     # Dependencies
├── url.txt             # Link dashboard Streamlit Cloud
└── README.md
```

---

## 🚀 Setup Environment

### 1. Clone Repository
```bash
git clone https://github.com/rafienajwan/Dicoding-Fundamental-Analisis-Data.git
cd Dicoding-Fundamental-Analisis-Data
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Analysis Notebook
```bash
jupyter notebook notebook.ipynb
```

### 4. Run Streamlit Dashboard
```bash
streamlit run dashboard/dashboard.py
```

**Dashboard akan terbuka di:** `http://localhost:8501`

**Atau akses dashboard online:** [https://submission-dfad.streamlit.app](https://submission-dfad.streamlit.app)

---

## 🎯 Business Questions

1. Musim mana yang memiliki total penyewaan sepeda tertinggi?
2. Bagaimana suhu mempengaruhi total penyewaan sepeda harian?
3. Bagaimana suhu mempengaruhi penyewaan sepeda pada jam tertentu?
4. Bagaimana kondisi cuaca mempengaruhi jumlah penyewaan sepeda?

---

## 📊 Key Findings

### 🍂 Musim & Penyewaan
- **Fall (Gugur)** → Penyewaan tertinggi
- **Summer (Panas)** → Posisi kedua
- **Spring (Semi)** → Penyewaan terendah

### 🌡️ Suhu & Demand
- **Korelasi positif kuat** (r > 0.6) antara suhu dan penyewaan
- **Suhu optimal:** 20-30°C menghasilkan demand tertinggi
- Suhu ekstrem menurunkan penyewaan signifikan

### ⏰ Pola Temporal
- **Rush hour:** 07-08 (pagi) & 17-18 (sore)
- Pola commuting jelas di weekday
- Weekend: pola recreational tersebar merata

### 🌦️ Kondisi Cuaca
- **Cerah/Partly Cloudy** → +200% vs cuaca buruk
- **Hujan/Salju** → Penurunan drastis

---

## 🔍 Advanced Analysis

### Teknik yang Diterapkan:

✅ **Manual Grouping & Binning**
- Segmentasi demand level (Low/Medium/High)
- Kategorisasi suhu, waktu, dan cuaca

✅ **Multi-Dimensional Clustering**
- Kombinasi Suhu × Cuaca × Musim
- Heatmap untuk identifikasi kondisi optimal

✅ **Cohort Analysis**
- Weekday vs Weekend patterns
- Casual vs Registered user behavior

✅ **User Segmentation**
- Registered (80%): Konsisten, tidak terpengaruh cuaca
- Casual (20%): Sensitif cuaca, recreational users

---

## 💡 Business Recommendations

### Strategi Operasional:
- 📈 Tingkatkan stok +30% saat Fall & Summer
- ⏰ Tambah kapasitas +40% pada rush hour (07-08, 17-18)
- 🌡️ Optimasi distribusi saat suhu 20-30°C

### Strategi Marketing:
- 💰 Dynamic pricing: premium saat high demand, diskon saat low demand
- 👔 Registered users: loyalty program & subscription
- 🎉 Casual users: weekend packages & promotional campaigns

---

## 📈 Dashboard Features

✅ **Overview**: Metrics, data preview, correlation matrix  
✅ **Analisis Utama**: Visualisasi 4 pertanyaan bisnis  
✅ **Analisis Lanjutan**: Segmentasi, clustering, cohort analysis  
✅ **Kesimpulan**: Summary & rekomendasi strategis  
✅ **Filter Interaktif**: Musim & cuaca

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Pandas** - Data manipulation
- **Matplotlib & Seaborn** - Visualization
- **Streamlit** - Interactive dashboard
- **Jupyter Notebook** - Analysis

---

**⭐ Don't forget to star this repository if you find it helpful!**
