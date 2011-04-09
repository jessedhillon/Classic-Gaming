import re
import random

from pyquery import PyQuery
from urllib import urlencode, urlretrieve

from interfaces import RomIdentifier, RomNotFoundException

system_ids = {
    'gen': 10,
    'nes': 19,
    'snes': 21,
}

url_base = "http://www.gamefaqs.com"
query_base = url_base + "/search/index.html"

class GameFAQSRomIdentifier(RomIdentifier):
    def __init__(self, system, query):
        super(GameFAQSRomIdentifier, self).__init__(system, query)
        self.lookup()

    def lookup(self):
        params = urlencode({
            'game': self.query,
            'platform': system_ids[self.system],
        })
        self.query_doc = PyQuery("%s?%s" % (query_base, params))
        best_matches = self.query_doc('div.pod').filter(lambda x: PyQuery(this)('h2.title').text() == 'Best Matches')
        if len(best_matches) == 0:
            raise RomNotFoundException()

        best_link = best_matches('tr td a:first')
        self.info_url = url_base + best_link.attr('href')
        self.info_doc = PyQuery(self.info_url)

    def get_title(self):
        return self.info_doc('#main_col h1').text()

    def get_description(self):
        return self.info_doc('.game_summary .details').text()

    def get_publisher(self):
        return self.info_doc('#gamespace_info .infobox .gameinfo li')[0].find('a').text

    def get_year(self):
        date = self.info_doc('#gamespace_info .infobox .gameinfo li')[1].find('a').text
        match = re.match(".*([0-9]{4}).*", date)
        return match.group(1) if match else None

    def get_thumbnail(self):
        boxshot_src = self.info_doc('#gamespace_info img.boxshot').attr('src')
        extension = boxshot_src.split('.')[-1]
        filename, headers = urlretrieve(boxshot_src)

        return (extension, open(filename, 'rb'))

    def get_image(self):
        self.images_doc = PyQuery(self.info_url + '/images')
        thumbs = self.images_doc('#main_col .game_imgs .contrib .thumb a')
        choice = random.choice(thumbs)
        image = PyQuery(url_base + choice.attrib['href'])

        src = image('#main_col .game_imgs .img img').attr('src')
        extension = src.split('.')[-1]

        filename, headers = urlretrieve(src)

        return (extension, open(filename, 'rb'))
