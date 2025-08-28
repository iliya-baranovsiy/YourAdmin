from scraping.scrap import test_1, test_2
import threading

if __name__ == '__main__':
    t1 = threading.Thread(target=test_1)
    t2 = threading.Thread(target=test_2)
    t1.start()
    t2.start()
