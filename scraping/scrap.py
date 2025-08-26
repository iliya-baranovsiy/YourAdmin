import asyncio
import concurrent.futures
from functools import partial
from bs4 import BeautifulSoup
import requests
from services.db_work import games_news_db, it_news_db
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
            func_with_posted = partial(self.get_url_content, )
            executor.map(func_with_posted, urls)


class ItNewsScrap(BaseScrap):
    def __init__(self, url="https://habr.com/ru/news"):
        self.__url = url
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
        await asyncio.sleep(3)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            func_with_posted = partial(self.__get_url_content, )
            executor.map(func_with_posted, urls)


game_news_scrap = GameScrap()
it_news_scrap = ItNewsScrap()
asyncio.run(it_news_scrap.run_it_news_scraping())
