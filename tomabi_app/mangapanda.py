from bs4 import BeautifulSoup
import requests

html = requests.get('http://www.mangapanda.com/toriko')
soup = BeautifulSoup(html.text, "html.parser")
table = soup.find("table", id="listing")
# The first tr contains the field names.
headings = [th.get_text() for th in table.find("tr").find_all("th")]
dict = {}
for row in table.find_all("tr")[1:]:
    for a in row.find_all('a', href=True):
        print "URL:", a['href'] + " chapitre:", a['href'].split('/')[2]
        dict[a['href'].split('/')[2]] = a['href']
