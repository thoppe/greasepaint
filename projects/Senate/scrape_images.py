import requests, bs4

with open('List_of_members_of_the_United_States_Senate.html') as FIN:
    raw = FIN.read()

soup = bs4.BeautifulSoup(raw, 'lxml')

for a in soup.find_all('a', {"class":"image"}):

    name = a.parent.findNext('td').get_text().strip()

    if not name:
        continue

    print(name, a['href'])
