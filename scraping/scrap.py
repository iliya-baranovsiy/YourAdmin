import asyncio
import concurrent.futures
from functools import partial
from bs4 import BeautifulSoup
import requests
from services.db_work import games_news_db, it_news_db, crypto_news_db, science_news_db, culture_news_db
from services.ai_work import ai_generate


class BaseScrap:
    def _get_html(self, url):
        response = requests.get(url)
        return response.text


class GameScrap(BaseScrap):
    def __init__(self, url="https://www.playground.ru/news"):
        self.__posted = games_news_db.get_title()
        self.__url = url

    def get_posts_url(self):
        soup = BeautifulSoup(self._get_html(self.__url), 'html.parser')
        target_divs = soup.find_all('div', class_=['post-title'])
        urls = []
        for div in target_divs:
            a_tags = div.find_all('a', href=True)
            for a in a_tags:
                urls.append(a['href'])
        return urls

    def get_url_content(self, url):
        title = ''
        text = ''
        pic_url = ''
        html_text = self._get_html(url)
        soup = BeautifulSoup(html_text, 'html.parser')

        header_tag = soup.find_all('h1', class_=['post-title'])
        for head in header_tag:
            title = head.text.strip().replace('/n', '')
            break
        if title in self.__posted:
            return 0
        else:
            figures = soup.find_all('figure')
            main_div = soup.find_all('div', class_=['article-content js-post-item-content js-redirect'])
            for figure in figures:
                try:
                    a_tag = figure.find('a', href=True)
                    if a_tag['href'] and a_tag:
                        pic_url = a_tag['href']
                        break
                except:
                    pass
            for tags in main_div:
                paragraphs = tags.find_all('p')
                for p in paragraphs:
                    text += p.text
                text = ai_generate(text)
                print(text)
            games_news_db.insert_data(title=title, text=text, picture=pic_url)

    async def run_games_news_scraping(self):
        urls = self.get_posts_url()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            func_with_posted = partial(self.get_url_content)
            executor.map(func_with_posted, urls)


class ItNewsScrap(BaseScrap):
    def __init__(self):
        self.__url = 'https://habr.com/ru/news'
        self.__default_url = "https://habr.com"
        self.__in_db = it_news_db.get_title()

    def __get_page_urls(self):
        url_list = []
        count = 1
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
        return url_list

    def __get_url_content(self, url):
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
            it_news_db.insert_data(title=title, text=ai_text, picture=pic_url)

    async def run_it_news_scraping(self):
        urls = self.__get_page_urls()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            func_with_posted = partial(self.__get_url_content)
            executor.map(func_with_posted, urls)


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
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            target_func = partial(self.__get_content)
            executor.map(target_func, urls)


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
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            target_func = partial(self.__get_content)
            executor.map(target_func, urls)


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
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            target_func = partial(self.__get_url_content)
            executor.map(target_func, urls)


game_news_scrap = GameScrap()
it_news_scrap = ItNewsScrap()
crypto_news_scrap = CryptoScrap()
science_news_scrap = ScienceScrap()
culture_news_scrap = CultureScrap()
asyncio.run(culture_news_scrap.run_culture_scraping())
