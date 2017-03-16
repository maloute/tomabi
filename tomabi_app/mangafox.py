from bs4 import BeautifulSoup
import requests
import re
import collections

html = requests.get('http://mangafox.me/manga/gosu/')
soup = BeautifulSoup(html.text, "html.parser")
dict = collections.OrderedDict()
# chlist = soup.find("ul", class="chlist")
for ultag in soup.find_all('ul', {'class': 'chlist'}):
    for litag in ultag.find_all('li'):
        print litag
        for a in litag.find_all('a', {'class': 'tips'}, href=True):
            print "URL:", a['href']
            fullname = a.text
            chapter_match = re.search(r"\s(\d+)$", fullname)
            if chapter_match is not None:
                print "text:", chapter_match.group(1)
                dict[int(chapter_match.group(1))] = a['href']


for k,v in dict.items():
    print "key:"+str(k)
    print "value:"+v
dict2 = collections.OrderedDict(sorted(dict.items()))
for k,v in dict2.items():
    print "key:"+str(k)
    print "value:"+v
        # print litag
# print(chlist.get_text())
# The first tr contains the field names.
# headings = [th.get_text() for th in table.find("tr").find_all("th")]
# dict = {}
# for row in table.find_all("tr")[1:]:
#     for a in row.find_all('a', href=True):
#         print "URL:", a['href'] + " chapitre:", a['href'].split('/')[2]
#         dict[a['href'].split('/')[2]] = a['href']
