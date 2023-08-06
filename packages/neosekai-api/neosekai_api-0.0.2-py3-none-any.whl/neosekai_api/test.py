import requests
from bs4 import BeautifulSoup
# data = {'action': 'tw_ajax', 'type': 'pagination', 'id': 930068, 'page': 2}
# url = 'https://readlightnovels.net/wp-admin/admin-ajax.php'
# print(requests.post(url, data, allow_redirects=True).text)
# url = "https://www.neosekaitranslations.com/novel/saijo-no-osewa-takane-no-hana-ln/volume-2/v2-chp-2-part-3/"

# r = requests.get(
#     url, allow_redirects=False)
# with open('ch-vavcksbk-5-jitumo.html', 'w', encoding='utf-8') as f:
#     f.write(r.text)
soup = BeautifulSoup(open('ch-vavcksbk-5-jitumo.html',
                     encoding='utf-8').read(), 'lxml')
div = soup.find('div', attrs={'class': 'text-left'})
p = div.find_all('p')
for i in p:
    print(i.img)
    if i.img != None:
        print(i.img['src'])
