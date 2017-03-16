from tomabi_app.models import Manga, Chapter
import collections
import re


def MangaFoxParser(request, manga_id):
    from bs4 import BeautifulSoup
    import requests
    user = request.user.id
    m_id = manga_id
    print m_id
    print('user:'+str(user))
    dict = collections.OrderedDict()
    html = Manga.objects.filter(user_id=user,id=m_id).values_list('url')[0]
    html2 = html[0]
    print ('html:'+html2)
    html_body = requests.get(html2)
    soup = BeautifulSoup(html_body.text, "html.parser")

    try:
        max_rated_entry = Chapter.objects.filter(manga_id=m_id).latest('number')
        max_number = max_rated_entry.number
    except Chapter.DoesNotExist:
        max_number = 0

    for ultag in soup.find_all('ul', {'class': 'chlist'}):
        for litag in ultag.find_all('li'):
            print litag
            for a in litag.find_all('a', {'class': 'tips'}, href=True):
                print "URL:", a['href']
                fullname = a.text
                chapter_match = re.search(r"\s(\d+)$", fullname)
                if chapter_match is not None:
                    number = chapter_match.group(1)
                    dict[int(number)] = a['href']

    dict2 = collections.OrderedDict(sorted(dict.items()))
    for k, v in dict2.items():
        print "key:"+str(k)
        print "value:"+v
        if (k > int(max_number)):
            chap = Chapter(manga_id=m_id, number=k, url=v)
            chap.save()

    return('Hello guy!')
