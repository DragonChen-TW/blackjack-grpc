import requests
from bs4 import BeautifulSoup

# url = 'https://commons.wikimedia.org/wiki/File:10C.svg'
base_url = 'https://commons.wikimedia.org/wiki/File:{}{}.svg'

def parse_img(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    img = soup.select('#file a')[0]
    return img['href']

def download_img(url, i):
    res = requests.get(url)
    f_name = url.split('/')[-1]

    if i == 1:
        f_name = f_name.replace('A', '1')
    elif i == 11:
        f_name = f_name.replace('J', '11')
    elif i == 12:
        f_name = f_name.replace('Q', '12')
    elif i == 13:
        f_name = f_name.replace('K', '13')

    with open(f_name, 'wb') as f:
        f.write(res.content)

i = 1
for p in ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']:
    for f in ['S', 'H', 'D', 'C']:
        print('download', p, f)
        url = base_url.format(p, f)
        img = parse_img(url)
        download_img(img, i)
    i += 1

# url = base_url.format(7, 'C')
# img = parse_img(url)
# download_img(img)