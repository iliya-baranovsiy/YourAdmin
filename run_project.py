from scraping.scrap import clean_db, run_scraping
import threading

if __name__ == '__main__':
    clean = threading.Thread(target=clean_db)
    run_scrap = threading.Thread(target=run_scraping)
    run_scrap.start()
    clean.start()
