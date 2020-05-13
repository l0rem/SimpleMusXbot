import requests
from phrases import url
from bs4 import BeautifulSoup
from dbmodels import Tracks, Users


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

    for block in soup.find_all('div', class_='audio-list-entry-inner'):
        track = dict()

        name = block.find('div', class_='track')

        performer = name.find('div', class_='title').next.next
        try:
            title = name.find('div', class_='special-title').next
        except AttributeError:
            title = name.find('div', class_='title').next.next

        duration = block.find('div', class_='audio-duration').next
        download_url = block.find('div', class_='download-container').find('a')['href']

        track.update({'performer': performer,
                      'title': title,
                      'duration': duration,
                      'download_url': download_url})
        tracks.append(track)

    return tracks


def store_track(uid, title, performer, file_id, download_url):

    user = Users.get(Users.uid == uid)

    Tracks.create(user=user,
                  title=title,
                  performer=performer,
                  file_id=file_id,
                  download_url=download_url)



