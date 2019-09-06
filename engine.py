import requests
from phrases import url
from bs4 import BeautifulSoup


def format_query(q):
    # making users queries urlsafe
    q = q.lower()
    if '%' in q:
        q = q.replace('%', '%25')
    if ' ' in q:
        q = q.replace(' ', '%20')
    if '!' in q:
        q = q.replace('!', '%21')
    if '#' in q:
        q = q.replace('#', '%23')
    if '$' in q:
        q = q.replace('&', '%24')
    if '&' in q:
        q = q.replace('&', '%26')
    if '\'' in q:
        q = q.replace('\'', '%27')
    if '(' in q:
        q = q.replace('(', '%28')
    if ')' in q:
        q = q.replace(')', '%29')
    if '@' in q:
        q = q.replace('@', '%40')
    if '{' in q:
        q = q.replace('{', '%7B')
    if '}' in q:
        q = q.replace('}', '%7D')
    if '=' in q:
        q = q.replace('=', '%3D')
    if '`' in q:
        q = q.replace('`', '%60')
    if '^' in q:
        q = q.replace('^', '%5E')
    if '\\' in q:
        q = q.replace('\\', '%5C')
    if '[' in q:
        q = q.replace('[', '%5B')
    if ']' in q:
        q = q.replace(']', '%5D')
    if ':' in q:
        q = q.replace(':', '%3A')
    if ';' in q:
        q = q.replace(';', '%3B')
    if ',' in q:
        q = q.replace(',', '%2C')
    if '/' in q:
        q = q.replace('/', '%2F')
    if '?' in q:
        q = q.replace('?', '%3F')
    if '|' in q:
        q = q.replace('|', '%7C')

    return q


def add_url(q):
    # combining url and user-query
    return url + q


def get_html(link):
    # downloading html with query results
    r = requests.get(link)
    return r.text


def parse_html(html):
    # parsing performers, titles, durations and download links
    soup = BeautifulSoup(html, features='html.parser')
    tracks = list()
    for block in soup.find_all('div', class_='audio-list-entry-inner'):
        song = dict()
        name = block.find_all('div', class_='title')
        performer = name[0].next.next
        title = name[1].next
        duration = block.find('div', class_='audio-duration').next
        d_link = block.find('div', class_='download-container').find('a')['href']
        song.update({'performer': performer,
                     'title': title,
                     'duration': duration,
                     'd_link': d_link})
        tracks.append(song)

    return tracks



