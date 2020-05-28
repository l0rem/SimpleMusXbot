import requests
from phrases import url
from bs4 import BeautifulSoup
from dbmodels import Tracks, Users, db


def format_query(q):
    """ kinda making users query urlsafe """

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
    """ adding non-permanent website url to users formatted query """

    return url + q


def get_html(link):
    """ downloading html """

    r = requests.get(link)

    return r.text


def parse_html(html):
    """ parsing performers, titles, durations and download urls """

    soup = BeautifulSoup(html, features='html.parser')
    tracks = list()

    for block in soup.find_all('div', class_='audio'):
        track = dict()

        performer = block.find('span', class_='audio-artist').next.next.next
        
        title = performer.next
        title = title[3:]

        duration = block.find('div', class_='duration').next.next.next.replace('\n', '')

        download_url = 'https://downloadmusicvk.ru/' + block.find('a', class_='download')['href']
        download_url = download_url.replace('predownload', 'download')

        track.update({'performer': performer,
                      'title': title,
                      'duration': duration,
                      'download_url': download_url})
        tracks.append(track)

    return tracks


def store_track(uid, title, performer, file_id, download_url):

    with db:

        user = Users.get(Users.uid == uid)

        Tracks.create(user=user,
                      title=title,
                      performer=performer,
                      file_id=file_id,
                      download_url=download_url)



