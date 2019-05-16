import requests, bs4, os, time, tqdm

with open('List_of_members_of_the_United_States_Senate.html') as FIN:
    raw = FIN.read()

soup = bs4.BeautifulSoup(raw, 'lxml')
sess = requests.session()

for a in tqdm.tqdm(soup.find_all('a', {"class":"image"})):

    name = a.parent.findNext('td').get_text().strip()

    if not name:
        continue

    name = name.replace(' ', '_').replace('.','')
    f_save = os.path.join(f'images/{name}.jpg')
    if os.path.exists(f_save):
        continue

    print(name, a['href'])
    url = "https://en.wikipedia.org/" + a['href']

    r = sess.get(url)
    assert(r.status_code == 200)
    
    soup = bs4.BeautifulSoup(r.content, 'lxml')

    link = soup.find('div', {"class":"fullMedia"})
    link = link.a

    if link is None:
        print(url)
        assert(link is not None)

    url = "https://" + link['href'].strip('/')
    r = sess.get(url)
    assert(r.status_code == 200)

    img = r.content
    with open(f_save, 'wb') as FOUT:
        FOUT.write(img)

    print(f_save)
    time.sleep(3)


#https://upload.wikimedia.org/wikipedia/commons/c/c5/Richard_Shelby%2C_official_portrait%2C_112th_Congress_%28cropped%29.jpg
