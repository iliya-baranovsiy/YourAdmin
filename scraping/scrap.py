import asyncio
import concurrent.futures
from functools import partial
from bs4 import BeautifulSoup
import requests
from services.scrap_db_work import games_news_db, it_news_db, crypto_news_db, science_news_db, culture_news_db, \
    sport_mews_db
from services.ai_work import ai_generate
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='scrap_logs.log', level=logging.INFO)


class BaseScrap:

    def _get_html(self, url, headers=None):
        response = requests.get(url, headers=headers)
        return response.text


class GameScrap(BaseScrap):
    def __init__(self, url="https://www.playground.ru/news"):
        self.__posted = games_news_db.get_title()
        self.__url = url

    def get_posts_url(self):
        soup = BeautifulSoup(self._get_html(self.__url), 'html.parser')
        target_divs = soup.find_all('div', class_=['post-title'])
        logger.info('Start scrap of game urls posts')
        urls = []
        for div in target_divs:
            a_tags = div.find_all('a', href=True)
            for a in a_tags:
                urls.append(a['href'])
        logger.info('Scrapping of game urls posts is success')
        return urls

    def get_url_content(self, url):
        title = ''
        html_text = self._get_html(url)
        soup = BeautifulSoup(html_text, 'html.parser')

        header_tag = soup.find_all('h1', class_=['post-title'])
        for head in header_tag:
            title = head.text.strip().replace('/n', '')
            break
        if title in self.__posted:
            return 0
        else:
            text = ''
            pic_url = ''
            figures = soup.find_all('figure')
            main_div = soup.find_all('div', class_=['article-content js-post-item-content js-redirect'])
            for figure in figures:
                try:
                    a_tag = figure.find('a', href=True)
                    if a_tag['href'] and a_tag:
                        pic_url = a_tag['href']
                        break
                except:
                    logger.info('Pic dont found in games post')
                    pic_url = None
            for tags in main_div:
                paragraphs = tags.find_all('p')
                for p in paragraphs:
                    text += p.text
                text = ai_generate(text)
            logger.info('Data in db')
            games_news_db.insert_data(title=title, text=text, picture=pic_url)

    async def run_games_news_scraping(self):
        urls = self.get_posts_url()
        logger.info('Start game scraper')
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            func_with_posted = partial(self.get_url_content)
            executor.map(func_with_posted, urls)
        logger.info('End of game scraper work')


class ItNewsScrap(BaseScrap):
    def __init__(self):
        self.__url = 'https://habr.com/ru/news'
        self.__default_url = "https://habr.com"
        self.__in_db = it_news_db.get_title()

    def __get_page_urls(self):
        url_list = []
        count = 1
        logger.info('run it news urls scrap')
        for i in range(0, 3):
            if i == 0:
                page_url = self.__url
            else:
                page_url = self.__url + f'/page{count}'
            soup = BeautifulSoup(self._get_html(page_url), 'html.parser')
            target_articles = soup.find_all('article', class_=['tm-articles-list__item'])
            for article in target_articles:
                h2_tag = article.find('h2')
                if h2_tag:
                    target_url = h2_tag.find('a', href=True)
                    url_list.append(self.__default_url + target_url['href'])
            count += 1
        logger.info('end of it news urls scrap')
        return url_list

    def __get_url_content(self, url):
        logger.info('run it news content scrap')
        text = ''
        html_text = self._get_html(url)
        soup = BeautifulSoup(html_text, 'html.parser')
        header_tag = soup.find('h1', class_=['tm-title tm-title_h1'])
        title = header_tag.find('span').text
        if title in self.__in_db:
            return 0
        else:
            target_picture = soup.find('figure', class_=['full-width'])
            pic_url = target_picture.find('img').attrs['src']
            target_div = soup.find_all('div', class_=[
                'article-formatted-body article-formatted-body article-formatted-body_version-2'])
            for el in target_div:
                paragraphs = el.find_all('p')
                for p in paragraphs:
                    text += p.text
            ai_text = ai_generate(text)
            logger.info('It news in db')
            it_news_db.insert_data(title=title, text=ai_text, picture=pic_url)

    async def run_it_news_scraping(self):
        urls = self.__get_page_urls()
        logger.info('run scrap it news')
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            func_with_posted = partial(self.__get_url_content)
            executor.map(func_with_posted, urls)
        logger.info('end of scrap it news')


class CryptoScrap(BaseScrap):
    def __init__(self):
        self.__url = 'https://forklog.com/news'
        self.__db_select = crypto_news_db.get_title()

    def __get_page_urls(self):
        soup = BeautifulSoup(self._get_html(self.__url), 'html.parser')
        div_list = soup.find_all('div', class_=['cell'])
        urls_list = []
        for div in div_list:
            into_div = div.find('a', href=True)
            urls_list.append(into_div['href'])
        return urls_list

    def __get_content(self, url):
        soup = BeautifulSoup(self._get_html(url), 'html.parser')
        title = soup.find('h1').text
        if title in crypto_news_db.get_title():
            return 0
        else:
            text = ''
            div_content = soup.find('div', class_='article_thumbnail')
            img_url = div_content.find('img').attrs['src']
            post_content = soup.find('div', class_='post_content')
            paragraphs = post_content.find_all('p')
            for p in paragraphs:
                text += p.text
            ai_text = ai_generate(text)
            crypto_news_db.insert_data(title=title, picture=img_url, text=ai_text)

    async def run_crypto_scraper(self):
        urls = self.__get_page_urls()
        logger.info('run scrap crypto news')
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            target_func = partial(self.__get_content)
            executor.map(target_func, urls)
        logger.info('end scrap crypto news')


class ScienceScrap(BaseScrap):
    def __init__(self):
        self.__url = 'https://new-science.ru'
        self.__titles_in_db = science_news_db.get_title()

    def __get_urls(self):
        soup = BeautifulSoup(self._get_html(self.__url), 'html.parser')
        a_tags = soup.find_all('a', class_=['more-link button'])
        urls = []
        for a in a_tags:
            urls.append(self.__url + '/' + a['href'])
        return urls

    def __get_content(self, url):
        soup = BeautifulSoup(self._get_html(url), 'html.parser')
        title = soup.find('h1', class_=['post-title entry-title']).text.strip()
        if title in science_news_db.get_title():
            return 0
        else:
            picture = self.__url + soup.find('figure', class_=['single-featured-image']).find('img').attrs['src']
            text = ''
            paragraphs = soup.find('div', class_=['entry-content entry clearfix']).find_all('p')
            for p in paragraphs:
                text += p.text
            ai_text = ai_generate(text)
            science_news_db.insert_data(title=title, picture=picture, text=ai_text)

    async def run_science_scraping(self):
        urls = self.__get_urls()
        logger.info('run scrap science news')
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            target_func = partial(self.__get_content)
            executor.map(target_func, urls)
        logger.info('end scrap science news')


class CultureScrap(BaseScrap):
    def __init__(self):
        self.__url = 'https://www.buro247.ru/beauty'
        self.__base_url = 'https://www.buro247.ru'
        self.__titles_in_db = culture_news_db.get_title()

    def __get_urls(self):
        soup = BeautifulSoup(self._get_html(self.__url), 'html.parser')
        divs = soup.find_all('div', class_=['news_item'])
        url_list = []
        for div in divs:
            a_tags = div.find_all('a', href=True)
            for a in a_tags:
                url = a['href']
                if '.html' in url:
                    url_list.append(self.__base_url + url)
        return url_list

    def __get_url_content(self, url):
        soup = BeautifulSoup(self._get_html(url), 'html.parser')
        title = soup.find('h1', class_=['article_title']).text
        if title in self.__titles_in_db:
            return 0
        else:
            picture = self.__base_url + soup.find('figure', class_=['stk-reset stk-image-figure']).find('img').attrs[
                'src']
            paragraphs = soup.find_all('p', class_=['stk-reset'])
            text = ''
            for p in paragraphs:
                text += p.text
            ai_text = ai_generate(text)
            culture_news_db.insert_data(title=title, picture=picture, text=ai_text)

    async def run_culture_scraping(self):
        urls = self.__get_urls()
        logger.info('run culture scrap')
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            target_func = partial(self.__get_url_content)
            executor.map(target_func, urls)
        logger.info('end of culture scrap')


class SportScrap(BaseScrap):
    def __init__(self):
        self.__url = 'https://www.championat.com/news/1.html'
        self.__default_url = 'https://www.championat.com'
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/115.0.0.0 Safari/537.36'
        }
        self.__in_db = sport_mews_db.get_title()

    def __get_urls(self):
        soup = BeautifulSoup(self._get_html(self.__url, self.__headers), 'html.parser')
        divs = soup.find_all('div', class_=['news-item__content'])
        url_list = []
        for div in divs:
            a = div.find('a', href=True)
            url_list.append(self.__default_url + a['href'])
        return url_list

    def __get_url_content(self, url):
        soup = BeautifulSoup(self._get_html(url, self.__headers), 'html.parser')
        title = soup.find('div', class_=['article-head__title']).text
        if title in self.__in_db:
            return 0
        else:
            text = ''
            picture = None
            try:
                picture = soup.find('div', class_=['article-head__photo']).find('img').attrs['src']
            except:
                pass
            div_content = soup.find('div', class_=['article-content'])
            paragraphs = div_content.find_all('p')
            for p in paragraphs:
                text += p.text
            ai_text = ai_generate(text)
            sport_mews_db.insert_data(title=title, picture=picture, text=ai_text)

    async def run_sport_scraping(self):
        urls = self.__get_urls()
        logger.info('run of sport scrap')
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            target_func = partial(self.__get_url_content)
            executor.map(target_func, urls)
        logger.info('end of sport scrap')


game_news_scrap = GameScrap()
it_news_scrap = ItNewsScrap()
crypto_news_scrap = CryptoScrap()
science_news_scrap = ScienceScrap()
culture_news_scrap = CultureScrap()
sport_news_scrap = SportScrap()
