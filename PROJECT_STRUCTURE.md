# PROJECT STRUCTURE DOCUMENTATION

## Struktur Folder Final

```
DC-Sentiment-Analysis/
├── scraping/
│   ├── spotify_scraper.py          # Script utama untuk scraping review Spotify
│   ├── setup_and_run.py           # Script setup otomatis
│   └── spotify_scraper.log        # Log file scraping
├── dataset/
│   ├── csv/
│   │   └── spotify_reviews_*.csv   # Data review dalam format CSV
│   ├── json/
│   │   └── spotify_reviews_*.json  # Data review dalam format JSON
│   ├── spotify_app_info.json       # Informasi aplikasi Spotify
│   ├── spotify_analysis.json       # Hasil analisis review
│   └── .gitkeep                    # Placeholder untuk git tracking
├── README.md                       # Dokumentasi utama proyek
├── requirements.txt                # Dependencies Python
└── .gitignore                     # File untuk git ignore
```

## File Utama

### 🎵 scraping/spotify_scraper.py

-   Script utama untuk scraping review aplikasi Spotify
-   Menggunakan google-play-scraper library
-   Menyimpan hasil ke folder dataset secara otomatis
-   Support multiple scraping options
-   Error handling yang robust

### 🚀 setup_and_run.py

-   Setup otomatis dependencies
-   Menjalankan scraper dengan guidance
-   Check folder structure
-   Test imports yang diperlukan

## Cara Menggunakan

1. **Quick Start:**

    ```bash
    python setup_and_run.py
    ```

2. **Manual:**

    ```bash
    pip install -r requirements.txt
    cd scraping
    python spotify_scraper.py
    ```

## Data Flow

1. **Scraping** → `scraping/spotify_scraper.py` mengambil data dari Google Play Store
2. **Storage** → Data review disimpan di `dataset/csv/` dan `dataset/json/`, info aplikasi & analisis di `dataset/`
3. **Output** → Hasil analisis dan visualisasi disimpan di `dataset/`

## Dependencies

Core requirements:

-   requests
-   beautifulsoup4
-   google-play-scraper
-   pandas
-   fake-useragent

Optional untuk analisis:

-   matplotlib
-   seaborn
-   numpy

## Data Schema

### Review Data Structure:

```json
{
  "reviewId": "unique_review_id",
  "userName": "reviewer_name",
  "content": "review_text_content",
  "score": 1-5,
  "thumbsUpCount": 0,
  "at": "2024-01-01T00:00:00",
  "replyContent": "developer_reply",
  "appVersion": "8.8.98.488"
}
```

### App Info Structure:

```json
{
    "title": "Spotify: Music and Podcasts",
    "developer": "Spotify AB",
    "score": 4.3,
    "ratings": 5200000,
    "installs": "1,000,000,000+",
    "version": "8.8.98.488"
}
```

## Next Steps untuk Sentiment Analysis

Setelah mendapatkan dataset, Anda dapat:

1. **Text Preprocessing**

    - Cleaning teks (remove URLs, special chars)
    - Tokenization
    - Stemming/Lemmatization
    - Remove stopwords

2. **Feature Engineering**

    - TF-IDF vectorization
    - Word embeddings (Word2Vec, GloVe)
    - N-grams analysis

3. **Sentiment Classification**

    - Rule-based (VADER, TextBlob)
    - Machine Learning (SVM, Random Forest)
    - Deep Learning (LSTM, BERT, RoBERTa)

4. **Evaluation & Visualization**
    - Confusion matrix
    - Classification report
    - Sentiment trends over time
    - Word clouds by sentiment

## Troubleshooting

### Common Issues:

1. **Import Error google_play_scraper**: `pip install google-play-scraper`
2. **Pandas NumPy Error**: `pip install --upgrade pandas numpy`
3. **Empty Dataset**: Check internet connection and Google Play Store access
4. **Permission Error**: Run with administrator privileges if needed

### Log Files:

Check `dataset/spotify_scraper.log` for detailed scraping logs and error messages.

---

**Project Ready for Sentiment Analysis! 🎉**
