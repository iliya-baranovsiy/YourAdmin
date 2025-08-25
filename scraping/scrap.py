from bs4 import BeautifulSoup
import requests


class BaseScrap:
    def get_html(self, url):
        response = requests.get(url)
        return response.text


class GameScrap(BaseScrap):
    def __init__(self, posted=None, url="https://www.playground.ru/news"):
        self.__posted = posted
        self.__url = url

    def get_posts_url(self):

        soup = BeautifulSoup(self.get_html(self.__url), 'html.parser')
        target_divs = soup.find_all('div', class_=['post-title'])
        urls = []
        for div in target_divs:
            a_tags = div.find_all('a', href=True)
            for a in a_tags:
                urls.append(a['href'])
        return urls

    def get_url_content(self, url):
        head_key = ''
        text = ''
        html_text = self.get_html(self.__url)
        soup = BeautifulSoup(html_text, 'html.parser')

        header_tag = soup.find_all('h1', class_=['post-title'])
        for head in header_tag:
            head_key = head.text.strip().replace('/n', '')
            break
        if head_key in self.__posted:
            return None
        else:
            # content_dict[head_key] = [] - title
            figures = soup.find_all('figure')
            main_div = soup.find_all('div', class_=['article-content js-post-item-content js-redirect'])
            for figure in figures:
                a_tag = figure.find('a', href=True)
                if a_tag['href']:
                    #url picture
                    content_dict[head_key].append(a_tag['href'])
                    break
            for tags in main_div:
                paragraphs = tags.find_all('p')
                for p in paragraphs:
                    text += p.text
                content_dict[head_key].append(test(text))  # прогон через нейронку
            # добавить в бд title, url, text, date
            return content_dict
