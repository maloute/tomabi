from tomabi_app.models import Manga, Chapter
import collections


def MangaPandaParser(request, manga_id):
    from bs4 import BeautifulSoup
    import requests
    user = request.user.id
    m_id = manga_id
    print m_id
    print('user:'+str(user))
    html = Manga.objects.filter(user_id=user,id=m_id).values_list('url')[0]
    html2 = html[0]
    print ('html:'+html2)
    html_body = requests.get(html2)
    soup = BeautifulSoup(html_body.text, "html.parser")
    table = soup.find("table", id="listing")
    # The first tr contains the field names.
    headings = [th.get_text() for th in table.find("tr").find_all("th")]
    try:
        max_rated_entry = Chapter.objects.filter(manga_id=m_id).latest('number')
        max_number = max_rated_entry.number
    except Chapter.DoesNotExist:
        max_number = 0

    for row in table.find_all("tr")[1:]:
        for a in row.find_all('a', href=True):
            if (int(a['href'].split('/')[2]) > int(max_number)):
                chap = Chapter(manga_id=m_id, number=a['href'].split('/')[2], url='http://www.mangapanda.com'+a['href'])
                chap.save()
    return('Hello guy!')
