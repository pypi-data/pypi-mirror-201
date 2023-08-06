from novel import Novel
import requests
from bs4 import BeautifulSoup


class NovelChapter:

    def __init__(self, _url) -> None:
        self.url = self.__urlformatter(_url)
        self.__response_object = requests.get(self.url, timeout=10)
        self.details = self.chapter_details()
        self.volume = self.details['volume']
        self.name = self.details['chapter_name']
        self.release_date = self.details['release_date']

    def __urlformatter(self, _url):
        __url = ''
        if 'https://' not in _url:
            _url == 'https://' + _url
        else:
            return _url

    def chapter_details(self):
        novel_url = self.url[:self.url.index('/', 43)]
        novel = Novel(novel_url)
        index_page = novel.get_index_page()
        for i in index_page:
            if index_page[i]['url'] == self.url:
                return index_page[i]

    def get_chapter_content(self):
        soup = BeautifulSoup(self.__response_object.text, 'lxml')
        div = soup.find('div', attrs={'class': 'text-left'})
        paras = div.find_all('p')
        content = {}
        n = 1
        for i in paras:
            if i.span != None:
                content[str(n)] = {'type': 'text',
                                   'content': i.span.text.strip()}
                n += 1
            elif i.img != None:
                content[str(n)] = {'type': 'img', 'content': i.img['src']}
                n += 1
            else:
                continue
        return content
