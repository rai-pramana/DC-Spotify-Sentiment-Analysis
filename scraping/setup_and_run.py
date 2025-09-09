"""
Setup and Run Script for Spotify Review Scraper

Script otomatis untuk setup dependencies dan menjalankan scraper Spotify
"""

import subprocess
import sys
import os

def print_header():
    print("="*70)
    print("   🎵 SPOTIFY GOOGLE PLAY STORE REVIEW SCRAPER 🎵")
    print("="*70)
    print("Script ini akan menginstall dependencies dan menjalankan scraper")
    print("untuk mengumpulkan data review Spotify untuk analisis sentiment\n")

def check_python_version():
    """Check versi Python"""
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ diperlukan!")
        return False
    
    print("✅ Python version OK")
    return True

def install_requirements():
    """Install dependencies dari requirements.txt"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Upgrade pip terlebih dahulu
        print("Upgrading pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        print("Installing packages from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "../requirements.txt"])
        
        print("✅ All dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("\nTrying to install essential packages individually...")
        
        # List packages yang essential untuk scraper
        essential_packages = [
            "requests",
            "beautifulsoup4", 
            "pandas",
            "lxml",
            "google-play-scraper",
            "fake-useragent"
        ]
        
        # Install essential packages
        for package in essential_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installed")
            except:
                print(f"❌ Failed to install {package}")
        
        return True

def test_imports():
    """Test import library yang dibutuhkan"""
    print("\n🧪 Testing imports...")
    
    # Test basic imports
    required_imports = [
        ("requests", "requests"),
        ("bs4", "BeautifulSoup"),
        ("pandas", "pandas"),
        ("google_play_scraper", "google-play-scraper"),
        ("fake_useragent", "fake-useragent")
    ]
    
    all_ok = True
    for module, name in required_imports:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - REQUIRED")
            all_ok = False
    
    if not all_ok:
        print("❌ Some required packages missing!")
        return False
    
    print("✅ All required imports OK")
    return True

def check_folder_structure():
    """Check dan buat struktur folder yang diperlukan"""
    print("\n📁 Checking folder structure...")
    
    # Sekarang kita berada di folder scraping, jadi perlu check parent folder
    parent_dir = os.path.dirname(os.getcwd())
    folders = [
        os.path.join(parent_dir, 'dataset'),
        os.path.join(parent_dir, 'dataset', 'json'),
        os.path.join(parent_dir, 'dataset', 'csv')
    ]
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"📁 Created folder: {os.path.basename(folder)}")
        else:
            print(f"✅ Folder exists: {os.path.basename(folder)}")
    
    # Check if scraper file exists (current directory)
    scraper_path = 'spotify_scraper.py'
    if os.path.exists(scraper_path):
        print(f"✅ Scraper found: {scraper_path}")
        return True
    else:
        print(f"❌ Scraper not found: {scraper_path}")
        return False

def run_scraper():
    """Jalankan scraper Spotify"""
    scraper_path = 'spotify_scraper.py'
    
    print(f"\n🚀 Running Spotify Review Scraper...")
    print("="*50)
    
    try:
        # Run scraper (already in scraping directory)
        subprocess.run([sys.executable, 'spotify_scraper.py'])
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Scraping dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Error running scraper: {e}")

def main():
    print_header()
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    # Check if in correct directory
    if not os.path.exists("../requirements.txt"):
        print("❌ requirements.txt not found!")
        print("Make sure you're in the scraping directory of DC-Sentiment-Analysis project")
        input("Press Enter to exit...")
        return
    
    # Install requirements
    install_choice = input("\n📦 Install/update dependencies? (y/n): ").strip().lower()
    if install_choice in ['y', 'yes', '']:
        if not install_requirements():
            print("❌ Failed to install dependencies")
            input("Press Enter to exit...")
            return
    
    # Test imports
    if not test_imports():
        print("❌ Critical imports failed!")
        input("Press Enter to exit...")
        return
    
    # Check folder structure
    if not check_folder_structure():
        print("❌ Folder structure check failed!")
        input("Press Enter to exit...")
        return
    
    # Run scraper
    run_choice = input("\n🚀 Run Spotify Review Scraper? (y/n): ").strip().lower()
    if run_choice in ['y', 'yes', '']:
        run_scraper()
        
        # Show results
        parent_dir = os.path.dirname(os.getcwd())
        dataset_path = os.path.join(parent_dir, 'dataset')
        dataset_files = []
        
        if os.path.exists(dataset_path):
            # Collect files from both json and csv subfolders
            json_path = os.path.join(dataset_path, 'json')
            csv_path = os.path.join(dataset_path, 'csv')
            
            if os.path.exists(json_path):
                json_files = [f"json/{f}" for f in os.listdir(json_path) if f.endswith('.json')]
                dataset_files.extend(json_files)
            
            if os.path.exists(csv_path):
                csv_files = [f"csv/{f}" for f in os.listdir(csv_path) if f.endswith('.csv')]
                dataset_files.extend(csv_files)
        
        if dataset_files:
            print(f"\n📊 RESULTS:")
            print("-" * 50)
            print(f"Files generated in 'dataset' folder:")
            for file in dataset_files:
                print(f"  📄 {file}")
            
            print(f"\n🎉 Dataset ready for sentiment analysis!")
            print("You can now proceed with:")
            print("✅ Text preprocessing")
            print("✅ Sentiment analysis with VADER/TextBlob")
            print("✅ Machine learning classification")
            print("✅ Data visualization")
    
    print(f"\n👋 Thank you for using Spotify Review Scraper!")
    print("Visit the 'dataset' folder to access your scraped data.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
