"""
Spotify Google Play Store Review Scraper

Script untuk mengambil review aplikasi Spotify dari Google Play Store
menggunakan google-play-scraper library.
"""

import requests
import json
import pandas as pd
import time
import random
import os
from bs4 import BeautifulSoup
from google_play_scraper import app, reviews, Sort
from fake_useragent import UserAgent
from datetime import datetime
import logging

# Setup logging - simpan log di folder scraping
log_dir = os.path.dirname(__file__)
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'spotify_scraper.log')),
        logging.StreamHandler()
    ]
)

class SpotifyReviewScraper:
    def __init__(self):
        self.app_id = 'com.spotify.music'
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Setup dataset directory dengan subfolder
        self.dataset_dir = os.path.join(os.path.dirname(__file__), '..', 'dataset')
        self.csv_dir = os.path.join(self.dataset_dir, 'csv')
        self.json_dir = os.path.join(self.dataset_dir, 'json')
        
        # Buat semua direktori
        os.makedirs(self.csv_dir, exist_ok=True)
        os.makedirs(self.json_dir, exist_ok=True)
        
    def get_app_info(self):
        """Mengambil informasi dasar aplikasi Spotify"""
        try:
            logging.info("Mengambil informasi aplikasi Spotify...")
            app_info = app(self.app_id, lang='en', country='us')
            
            info = {
                'title': app_info.get('title'),
                'description': app_info.get('description'),
                'summary': app_info.get('summary'),
                'installs': app_info.get('installs'),
                'score': app_info.get('score'),
                'ratings': app_info.get('ratings'),
                'reviews_count': app_info.get('reviews'),
                'price': app_info.get('price'),
                'free': app_info.get('free'),
                'developer': app_info.get('developer'),
                'genre': app_info.get('genre'),
                'content_rating': app_info.get('contentRating'),
                'updated': app_info.get('updated'),
                'version': app_info.get('version'),
                'size': app_info.get('size')
            }
            
            logging.info(f"Informasi aplikasi berhasil diambil: {info['title']}")
            return info
        except Exception as e:
            logging.error(f"Error mengambil informasi aplikasi: {str(e)}")
            return None

    def scrape_reviews_google_play_scraper(self, count=1000, sort_type=Sort.NEWEST):
        """
        Mengambil review menggunakan google-play-scraper library
        
        Args:
            count: Jumlah review yang ingin diambil
            sort_type: Jenis sorting (NEWEST, MOST_RELEVANT, RATING)
        """
        try:
            logging.info(f"Mengambil {count} review menggunakan google-play-scraper...")
            
            result, continuation_token = reviews(
                self.app_id,
                lang='en',
                country='us',
                sort=sort_type,
                count=count,
                filter_score_with=None
            )
            
            reviews_data = []
            for review in result:
                review_data = {
                    'reviewId': review.get('reviewId'),
                    'userName': review.get('userName'),
                    'userImage': review.get('userImage'),
                    'content': review.get('content'),
                    'score': review.get('score'),
                    'thumbsUpCount': review.get('thumbsUpCount', 0),
                    'reviewCreatedVersion': review.get('reviewCreatedVersion'),
                    'at': review.get('at'),
                    'replyContent': review.get('replyContent'),
                    'replyAt': review.get('replyAt'),
                    'appVersion': review.get('appVersion')
                }
                reviews_data.append(review_data)
            
            logging.info(f"Berhasil mengambil {len(reviews_data)} review")
            return reviews_data, continuation_token
            
        except Exception as e:
            logging.error(f"Error scraping dengan google-play-scraper: {str(e)}")
            return [], None

    def scrape_more_reviews(self, continuation_token, count=500):
        """Mengambil lebih banyak review menggunakan continuation token"""
        try:
            logging.info(f"Mengambil {count} review tambahan...")
            
            result, continuation_token = reviews(
                self.app_id,
                continuation_token=continuation_token,
                lang='en',
                country='us',
                sort=Sort.NEWEST,
                count=count
            )
            
            reviews_data = []
            for review in result:
                review_data = {
                    'reviewId': review.get('reviewId'),
                    'userName': review.get('userName'),
                    'userImage': review.get('userImage'),
                    'content': review.get('content'),
                    'score': review.get('score'),
                    'thumbsUpCount': review.get('thumbsUpCount', 0),
                    'reviewCreatedVersion': review.get('reviewCreatedVersion'),
                    'at': review.get('at'),
                    'replyContent': review.get('replyContent'),
                    'replyAt': review.get('replyAt'),
                    'appVersion': review.get('appVersion')
                }
                reviews_data.append(review_data)
            
            logging.info(f"Berhasil mengambil {len(reviews_data)} review tambahan")
            return reviews_data, continuation_token
            
        except Exception as e:
            logging.error(f"Error mengambil review tambahan: {str(e)}")
            return [], None

    def scrape_reviews_by_rating(self, rating, count=200):
        """Mengambil review berdasarkan rating tertentu (1-5)"""
        try:
            logging.info(f"Mengambil {count} review dengan rating {rating}...")
            
            result, _ = reviews(
                self.app_id,
                lang='en',
                country='us',
                sort=Sort.NEWEST,
                count=count,
                filter_score_with=rating
            )
            
            reviews_data = []
            for review in result:
                review_data = {
                    'reviewId': review.get('reviewId'),
                    'userName': review.get('userName'),
                    'userImage': review.get('userImage'),
                    'content': review.get('content'),
                    'score': review.get('score'),
                    'thumbsUpCount': review.get('thumbsUpCount', 0),
                    'reviewCreatedVersion': review.get('reviewCreatedVersion'),
                    'at': review.get('at'),
                    'replyContent': review.get('replyContent'),
                    'replyAt': review.get('replyAt'),
                    'appVersion': review.get('appVersion')
                }
                reviews_data.append(review_data)
            
            logging.info(f"Berhasil mengambil {len(reviews_data)} review dengan rating {rating}")
            return reviews_data
            
        except Exception as e:
            logging.error(f"Error mengambil review rating {rating}: {str(e)}")
            return []

    def scrape_large_dataset_by_rating(self, rating, target_count=2000, batch_size=500):
        """
        Mengambil dataset besar untuk rating tertentu dengan batch processing
        
        Args:
            rating: Rating yang ingin diambil (1-5)
            target_count: Target jumlah review
            batch_size: Ukuran setiap batch
        """
        all_reviews = []
        collected = 0
        
        try:
            # Hitung jumlah batch yang dibutuhkan
            num_batches = (target_count + batch_size - 1) // batch_size  # Ceiling division
            
            for batch_num in range(num_batches):
                remaining = target_count - collected
                current_batch_size = min(batch_size, remaining)
                
                if current_batch_size <= 0:
                    break
                
                print(f"   📦 Batch {batch_num + 1}/{num_batches} - Target: {current_batch_size} review")
                
                try:
                    batch_reviews = self.scrape_reviews_by_rating(rating, count=current_batch_size)
                    
                    if batch_reviews:
                        # Filter duplikasi berdasarkan reviewId
                        existing_ids = {review['reviewId'] for review in all_reviews}
                        new_reviews = [r for r in batch_reviews if r['reviewId'] not in existing_ids]
                        
                        all_reviews.extend(new_reviews)
                        collected = len(all_reviews)
                        
                        print(f"   ✅ Batch {batch_num + 1}: +{len(new_reviews)} review baru (total: {collected})")
                    else:
                        print(f"   ⚠️ Batch {batch_num + 1}: Tidak ada review ditemukan")
                    
                    # Delay antar batch
                    time.sleep(2)
                    
                    # Break jika sudah mencapai target
                    if collected >= target_count:
                        print(f"   🎯 Target {target_count} review tercapai!")
                        break
                        
                except Exception as e:
                    print(f"   ❌ Error pada batch {batch_num + 1}: {str(e)}")
                    # Coba dengan batch size lebih kecil
                    try:
                        smaller_batch = current_batch_size // 2
                        if smaller_batch > 0:
                            print(f"   🔄 Mencoba ulang dengan batch size {smaller_batch}...")
                            batch_reviews = self.scrape_reviews_by_rating(rating, count=smaller_batch)
                            if batch_reviews:
                                existing_ids = {review['reviewId'] for review in all_reviews}
                                new_reviews = [r for r in batch_reviews if r['reviewId'] not in existing_ids]
                                all_reviews.extend(new_reviews)
                                collected = len(all_reviews)
                                print(f"   ✅ Berhasil: +{len(new_reviews)} review")
                    except:
                        print(f"   ❌ Gagal total pada batch {batch_num + 1}")
                        continue
            
            logging.info(f"Selesai mengambil {len(all_reviews)} review untuk rating {rating}")
            return all_reviews
            
        except Exception as e:
            logging.error(f"Error dalam scrape_large_dataset_by_rating: {str(e)}")
            return all_reviews

    def save_to_csv(self, data, filename=None):
        """Menyimpan data ke file CSV di folder csv"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"spotify_reviews_{timestamp}.csv"
        
        filepath = os.path.join(self.csv_dir, filename)
        
        try:
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8')
            logging.info(f"Data berhasil disimpan ke {filepath}")
            return filepath
        except Exception as e:
            logging.error(f"Error menyimpan ke CSV: {str(e)}")
            return None

    def save_app_info_json(self, data, filename):
        """Menyimpan data ke file JSON di folder dataset utama"""
        filepath = os.path.join(self.dataset_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            logging.info(f"Data berhasil disimpan ke {filepath}")
            return filepath
        except Exception as e:
            logging.error(f"Error menyimpan ke JSON: {str(e)}")
            return None

    def save_to_json(self, data, filename=None):
        """Menyimpan data review ke file JSON di folder json"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"spotify_reviews_{timestamp}.json"
        
        filepath = os.path.join(self.json_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            logging.info(f"Data berhasil disimpan ke {filepath}")
            return filepath
        except Exception as e:
            logging.error(f"Error menyimpan ke JSON: {str(e)}")
            return None

    def analyze_reviews(self, reviews_data):
        """Analisis sederhana dari data review"""
        if not reviews_data:
            return None
        
        df = pd.DataFrame(reviews_data)
        
        analysis = {
            'total_reviews': len(df),
            'average_rating': df['score'].mean(),
            'rating_distribution': df['score'].value_counts().to_dict(),
            'reviews_with_thumbs_up': len(df[df['thumbsUpCount'] > 0]),
            'average_thumbs_up': df['thumbsUpCount'].mean(),
            'reviews_with_replies': len(df[df['replyContent'].notna()]),
            'most_recent_review': df['at'].max(),
            'oldest_review': df['at'].min(),
            'positive_reviews': len(df[df['score'] >= 4]),
            'negative_reviews': len(df[df['score'] <= 2]),
            'neutral_reviews': len(df[df['score'] == 3])
        }
        
        # Tambah percentage
        total = analysis['total_reviews']
        analysis['positive_percentage'] = (analysis['positive_reviews'] / total) * 100
        analysis['negative_percentage'] = (analysis['negative_reviews'] / total) * 100
        analysis['neutral_percentage'] = (analysis['neutral_reviews'] / total) * 100
        
        return analysis

def main():
    print("="*70)
    print("   🎵 SPOTIFY GOOGLE PLAY STORE REVIEW SCRAPER 🎵")
    print("="*70)
    print("Script untuk mengambil review aplikasi Spotify dari Google Play Store")
    print("Data akan disimpan di folder 'dataset' untuk analisis sentiment\n")
    
    scraper = SpotifyReviewScraper()
    
    # Ambil informasi aplikasi
    app_info = scraper.get_app_info()
    if app_info:
        print("📱 INFORMASI APLIKASI SPOTIFY:")
        print("-" * 50)
        print(f"Nama: {app_info['title']}")
        print(f"Developer: {app_info['developer']}")
        print(f"Rating: {app_info['score']}")
        print(f"Total Ratings: {app_info['ratings']}")
        print(f"Total Reviews: {app_info['reviews_count']}")
        print(f"Installs: {app_info['installs']}")
        print(f"Version: {app_info['version']}")
    
    # Menu pilihan
    print("\n🔧 PILIHAN SCRAPING:")
    print("-" * 50)
    print("1. Scrape review terbaru (1000 review)")
    print("2. Scrape review dengan rating tertentu")
    print("3. Scrape review dalam batch besar (4000+ review)")
    print("4. Scrape review untuk analisis sentiment (balanced dataset)")
    print("5. Scrape dataset besar 10,000 review (2000 per rating)")
    
    choice = input("\nPilih opsi (1-5): ").strip()
    
    all_reviews = []
    
    try:
        if choice == "1":
            # Scrape 1000 review terbaru
            print("\n📝 Mengambil 1000 review terbaru...")
            reviews_data, token = scraper.scrape_reviews_google_play_scraper(count=1000, sort_type=Sort.NEWEST)
            all_reviews.extend(reviews_data)
            
        elif choice == "2":
            # Scrape berdasarkan rating
            rating = int(input("Masukkan rating (1-5): "))
            count = int(input("Masukkan jumlah review: "))
            print(f"\n📝 Mengambil {count} review dengan rating {rating}...")
            reviews_data = scraper.scrape_reviews_by_rating(rating, count)
            all_reviews.extend(reviews_data)
            
        elif choice == "3":
            # Scrape banyak review
            print("\n📝 Mengambil review dalam batch besar...")
            reviews_data, token = scraper.scrape_reviews_google_play_scraper(count=1000, sort_type=Sort.NEWEST)
            all_reviews.extend(reviews_data)
            
            # Ambil lebih banyak review menggunakan token
            for i in range(3):  # Ambil 3 batch tambahan (total ~4000 review)
                if token:
                    print(f"Mengambil batch {i+2}...")
                    more_reviews, token = scraper.scrape_more_reviews(token, count=1000)
                    all_reviews.extend(more_reviews)
                    time.sleep(2)  # Delay untuk menghindari rate limiting
                else:
                    break
                    
        elif choice == "4":
            # Scrape untuk analisis sentiment - dataset seimbang
            print("\n📝 Mengambil review untuk analisis sentiment...")
            print("Mengambil data seimbang dari semua rating...")
            for rating in [1, 2, 3, 4, 5]:
                print(f"Mengambil review rating {rating}...")
                reviews_data = scraper.scrape_reviews_by_rating(rating, count=200)
                all_reviews.extend(reviews_data)
                time.sleep(1)  # Delay antar request
        
        elif choice == "5":
            # Scrape dataset besar 10,000 review (2000 per rating)
            print("\n📝 MENGAMBIL DATASET BESAR 10,000 REVIEW")
            print("=" * 50)
            print("Target: 2,000 review per rating (1-5 bintang)")
            print("Metode: Batch processing dengan error handling")
            print("Estimasi waktu: 5-10 menit")
            
            confirm = input("\nLanjutkan? (y/n): ").strip().lower()
            if confirm not in ['y', 'yes']:
                print("❌ Dibatalkan oleh user")
                return
            
            print("\n🚀 MEMULAI SCRAPING DATASET BESAR...")
            print("-" * 50)
            
            total_collected = 0
            rating_stats = {}
            
            for rating in [1, 2, 3, 4, 5]:
                print(f"\n⭐ RATING {rating} STARS")
                print(f"🎯 Target: 2,000 review")
                
                # Gunakan method batch processing yang lebih robust
                rating_reviews = scraper.scrape_large_dataset_by_rating(
                    rating=rating, 
                    target_count=2000, 
                    batch_size=2000  # Ukuran batch optimal
                )
                
                all_reviews.extend(rating_reviews)
                total_collected += len(rating_reviews)
                rating_stats[rating] = len(rating_reviews)
                
                print(f"📊 Rating {rating}: {len(rating_reviews)} review berhasil dikumpulkan")
                print(f"� Progress total: {total_collected}/10,000 review")
                
                # Delay antar rating untuk menghindari rate limiting
                if rating < 5:  # Tidak delay setelah rating terakhir
                    print("⏱️ Delay 5 detik sebelum rating berikutnya...")
                    time.sleep(5)
            
            print(f"\n🎉 SCRAPING SELESAI!")
            print("=" * 50)
            print(f"📊 STATISTIK FINAL:")
            for rating, count in rating_stats.items():
                percentage = (count / total_collected) * 100 if total_collected > 0 else 0
                print(f"   ⭐ Rating {rating}: {count:,} review ({percentage:.1f}%)")
            print(f"📈 Total: {total_collected:,} review dari target 10,000")
            
            if total_collected >= 8000:  # 80% dari target
                print("✅ Dataset berhasil dikumpulkan dengan baik!")
            elif total_collected >= 5000:  # 50% dari target
                print("⚠️ Dataset terkumpul cukup untuk analisis")
            else:
                print("❌ Dataset kurang dari target, mungkin perlu mencoba lagi")
        
        else:
            print("❌ Pilihan tidak valid!")
            return
        
        if all_reviews:
            print(f"\n✅ HASIL SCRAPING:")
            print("-" * 50)
            print(f"Total review berhasil diambil: {len(all_reviews)}")
            
            # Analisis data
            analysis = scraper.analyze_reviews(all_reviews)
            if analysis:
                print("\n📊 ANALISIS REVIEW:")
                print("-" * 50)
                print(f"Total Reviews: {analysis['total_reviews']}")
                print(f"Rating Rata-rata: {analysis['average_rating']:.2f}")
                print(f"Distribusi Rating: {analysis['rating_distribution']}")
                print(f"Reviews dengan Thumbs Up: {analysis['reviews_with_thumbs_up']}")
                print(f"Reviews dengan Balasan: {analysis['reviews_with_replies']}")
                
                print(f"\n📈 SENTIMENT DISTRIBUTION:")
                print(f"Positive (4-5 ⭐): {analysis['positive_reviews']} ({analysis['positive_percentage']:.1f}%)")
                print(f"Neutral (3 ⭐): {analysis['neutral_reviews']} ({analysis['neutral_percentage']:.1f}%)")
                print(f"Negative (1-2 ⭐): {analysis['negative_reviews']} ({analysis['negative_percentage']:.1f}%)")
            
            # Preview beberapa review
            print(f"\n📖 PREVIEW REVIEW:")
            print("-" * 50)
            for i, review in enumerate(all_reviews[:3]):
                stars = "⭐" * review.get('score', 0)
                print(f"{i+1}. {review.get('userName', 'Unknown')} - {stars}")
                content = review.get('content', '')[:100]
                print(f"   \"{content}{'...' if len(review.get('content', '')) > 100 else ''}\"")
                print(f"   👍 {review.get('thumbsUpCount', 0)} helpful")
                print()
            
            # Simpan data
            save_format = input("💾 Pilih format penyimpanan (csv/json/both): ").strip().lower()
            
            if save_format in ['csv', 'both']:
                csv_file = scraper.save_to_csv(all_reviews)
                if csv_file:
                    print(f"✅ Data tersimpan dalam file CSV: {csv_file}")
            
            if save_format in ['json', 'both']:
                json_file = scraper.save_to_json(all_reviews)
                if json_file:
                    print(f"✅ Data tersimpan dalam file JSON: {json_file}")
            
            # Simpan juga informasi aplikasi dan analisis
            if app_info:
                app_file = scraper.save_app_info_json(app_info, "spotify_app_info.json")
                if app_file:
                    print(f"✅ Informasi aplikasi tersimpan: {app_file}")
                    
            if analysis:
                analysis_file = scraper.save_app_info_json(analysis, "spotify_analysis.json")
                if analysis_file:
                    print(f"✅ Hasil analisis tersimpan: {analysis_file}")
        
        else:
            print("❌ Tidak ada review yang berhasil diambil!")
    
    except KeyboardInterrupt:
        print("\n⏹️ Scraping dihentikan oleh user...")
    except ValueError as e:
        print(f"\n❌ Input tidak valid: {str(e)}")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        logging.error(f"Error dalam main: {str(e)}")
    
    print("\n🎉 Selesai! Data review Spotify siap untuk analisis sentiment.")
    print("\nFile tersimpan di folder 'dataset' dapat digunakan untuk:")
    print("✅ Sentiment Analysis dengan VADER, TextBlob, atau Transformers")
    print("✅ Text Preprocessing dan Cleaning")
    print("✅ Machine Learning Classification")
    print("✅ Data Visualization")
    print("✅ Statistical Analysis")

if __name__ == "__main__":
    main()
