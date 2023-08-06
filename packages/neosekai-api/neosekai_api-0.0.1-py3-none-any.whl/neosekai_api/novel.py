import requests
from bs4 import BeautifulSoup
from helper import heavy_translate
import json


class Novel:

    def __init__(self, url):
        self.url = url
        self.response_object = requests.get(self.url, timeout=10)
        self.novel_tags = self.__initialiser()

    def __initialiser(self):

        soup = BeautifulSoup(self.response_object.content, 'lxml')

        # finding title
        title = soup.find('title').text.split(' - NeoSekai')[0]

        # finding rating
        rating = soup.find('span', attrs={'id': 'averagerate'}).parent.text + \
            'out of ' + soup.find('span', attrs={'id': 'countrate'}).text

        # finding everything else
        novel_tags = {'title': title, 'rating': rating}
        post_content_divs = soup.find_all(
            'div', attrs={'class': 'post-content_item'})

        for i in post_content_divs:
            if post_content_divs.index(i) == 0:
                continue
            else:
                x = i.children
                for i in x:
                    if i.name == 'div':
                        if i['class'] == ['summary-heading']:
                            j = i.find_next(
                                'div', attrs={'class': 'summary-content'})
                            key = str(i.text).strip()
                            value = str(j.text).strip()

                            if key == 'Rank':
                                key = 'rank'
                            elif key == 'Alternative':
                                key = 'alternative_titles'
                                value = value.split(', ')
                            elif key == 'Author(s)':
                                key = 'authors'
                                value = value.split(', ')
                            elif key == 'Genre(s)':
                                key = 'genre'
                                value = value.split(', ')
                            elif key == 'Tag(s)':
                                key = 'tags'
                                value = value.split(', ')
                            elif key == 'Release':
                                key = 'release'
                            elif key == 'Status':
                                key = 'status'
                            else:
                                continue

                            novel_tags[key] = value

        return novel_tags

    def get_synopsis(self, fancy=True):
        soup = BeautifulSoup(self.response_object.content, 'lxml')
        synopsis = soup.find('div', attrs={
            'class': ['summary__content', 'show-more']}).text

        if fancy:
            return synopsis
        else:
            return heavy_translate(synopsis)

    def get_index_page(self):
        url = 'https://www.neosekaitranslations.com/wp-admin/admin-ajax.php'
        soup = BeautifulSoup(self.response_object.content, 'lxml')
        data_id = soup.find(
            'div', attrs={'id': 'manga-chapters-holder'})['data-id']
        data = {'action': 'manga_get_chapters', 'manga': data_id}
        soup_2 = BeautifulSoup(requests.post(url, data).content, 'lxml')
        content_dict = {}
        main_wrapper = soup_2.find('ul', attrs={'class': 'main version-chap'})
        volumes_li = list(main_wrapper.find_all(
            'li', recursive=False))
        volumes_li.reverse()
        n = 1
        for i in volumes_li:
            lines = list(i.find_all(
                'li', attrs={'class': 'wp-manga-chapter'}))
            lines.reverse()
            volume = i.a.text.strip()
            for j in lines:
                name = j.a.text.strip()
                _url = j.a['href']
                date = j.span.text.strip()
                content_dict[f"{n}"] = {"volume": volume,
                                        "chapter_name": name, "url": _url, "release_date": date}
                n += 1
        return eval(json.dumps(content_dict, indent=4))
