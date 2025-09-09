# Spotify Google Play Store Review Scraper

Proyek untuk melakukan scraping review aplikasi Spotify dari Google Play Store dan menyiapkan dataset untuk analisis sentiment.

## 📁 Struktur Proyek

```
DC-Sentiment-Analysis/
├── scraping/
│   └── spotify_scraper.py     # Script scraper utama
├── dataset/                   # Folder untuk menyimpan hasil scraping
│   ├── spotify_reviews_*.csv  # Data review dalam format CSV
│   ├── spotify_reviews_*.json # Data review dalam format JSON
│   ├── spotify_app_info.json  # Informasi aplikasi Spotify
│   ├── spotify_analysis.json  # Hasil analisis review
│   └── spotify_scraper.log    # Log file scraping
├── requirements.txt           # Dependencies Python
├── setup_and_run.py          # Script setup otomatis
└── README.md                 # Dokumentasi proyek
```

## 🚀 Quick Start

### Metode 1: Setup Otomatis
```cmd
python setup_and_run.py
```

### Metode 2: Manual Setup

1. **Install Dependencies**
```cmd
pip install -r requirements.txt
```

2. **Jalankan Scraper**
```cmd
cd scraping
python spotify_scraper.py
```

## 📊 Fitur Scraper

### 🎵 Spotify Scraper (`scraping/spotify_scraper.py`)
- ✅ Menggunakan `google-play-scraper` library yang stabil dan reliable
- ✅ Dapat mengambil ribuan review dengan continuation token
- ✅ Filter berdasarkan rating (1-5 stars) untuk dataset seimbang
- ✅ Sorting options (newest, most relevant, rating)
- ✅ Informasi lengkap aplikasi Spotify
- ✅ Export otomatis ke CSV dan JSON dalam folder `dataset`
- ✅ Analisis sentiment dasar (positive/neutral/negative)
- ✅ Error handling yang robust dengan retry mechanism

## 📋 Data yang Dikumpulkan

### 📱 Informasi Aplikasi
- Nama aplikasi dan developer
- Rating rata-rata dan jumlah total ratings
- Jumlah total reviews dan downloads
- Versi aplikasi terbaru
- Genre dan content rating
- Deskripsi aplikasi

### 📝 Data Review
- Review ID unik
- Username reviewer
- Rating (1-5 stars)
- Konten review lengkap
- Tanggal review
- Jumlah helpful votes
- Balasan dari developer (jika ada)
- Versi app saat review dibuat

## 🔧 Pilihan Scraping

1. **Review Terbaru (1000 review)** - Untuk analisis trending sentiment
2. **Review berdasarkan Rating** - Untuk dataset spesifik rating tertentu
3. **Batch Besar (4000+ review)** - Untuk dataset komprehensif
4. **Balanced Dataset** - 200 review per rating (1-5 stars) untuk analisis sentiment

## 💾 Format Output

Semua file disimpan di folder `dataset/`:

- **CSV**: Format tabel untuk analisis dengan Excel/Pandas
- **JSON**: Format struktur untuk penggunaan programmatic
- **Log files**: Detail proses scraping untuk debugging

## 📈 Penggunaan untuk Sentiment Analysis

Dataset yang dihasilkan siap untuk:

### 1. Text Preprocessing
- Cleaning dan normalisasi teks
- Tokenization dan stemming
- Removal stopwords

### 2. Sentiment Analysis
- **VADER Sentiment** - Rule-based sentiment analyzer
- **TextBlob** - Simple sentiment polarity detection
- **Transformers** - BERT, RoBERTa untuk sentiment classification

### 3. Machine Learning
- Feature extraction (TF-IDF, Word2Vec)
- Classification models (SVM, Random Forest, Neural Networks)
- Model evaluation dan tuning

### 4. Data Visualization
- Sentiment distribution plots
- Word clouds dari review
- Timeline sentiment analysis
- Rating vs sentiment correlation

## 📊 Contoh Analisis yang Dihasilkan

```
📈 SENTIMENT DISTRIBUTION:
Positive (4-5 ⭐): 2,850 reviews (71.2%)
Neutral (3 ⭐): 450 reviews (11.2%)
Negative (1-2 ⭐): 700 reviews (17.6%)

📋 STATISTIK LAINNYA:
Reviews dengan Thumbs Up: 1,245
Reviews dengan Balasan Developer: 89
Panjang Review Rata-rata: 127 karakter
```

## 🛠️ Troubleshooting

### Error google-play-scraper:
```cmd
pip install --upgrade google-play-scraper
```

### Error pandas/numpy:
```cmd
pip install --upgrade pandas numpy
```

### SSL Certificate Error:
```cmd
pip install --upgrade requests[security] certifi
```

## ⚖️ Legal & Ethical Use

- ✅ Hanya untuk tujuan research dan educational
- ✅ Respects Google Play Store rate limiting
- ✅ Menggunakan data public yang tersedia
- ✅ Tidak melanggar Terms of Service

## 🔄 Update Log

- **v2.0**: Struktur folder terorganisir dengan `scraping/` dan `dataset/`
- **v2.0**: Fokus pada satu scraper yang reliable (`spotify_scraper.py`)
- **v2.0**: Auto-save ke folder `dataset` untuk analisis sentiment
- **v2.0**: Enhanced error handling dan logging
- **v2.0**: Balanced dataset option untuk machine learning

---

**Ready for Sentiment Analysis!** 🚀
Dataset Spotify reviews siap digunakan untuk proyek analisis sentiment dan machine learning.
