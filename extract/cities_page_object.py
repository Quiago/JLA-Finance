import bs4
import logging
from common import config
from retry_url import persistent_request
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HomePage:
    def __init__(self, url):
        #self._url = url
        self._config = config()['web_sites']['cities']
        self._queries = self._config['queries']
        self._html = None

        self._visit(url)

    def _visit(self, url):
        response = persistent_request(url)
        #logging.info('Successfully connection with the url!')
        self._html = bs4.BeautifulSoup(response.text, 'lxml')

        #time.sleep(1)
        
    def _select(self, query_strings):
        return self._html.select(query_strings)
    
    def _find_with_attr(self, query_string, id_tag, id_attr):
        tags = self._queries[query_string]['tags']
        attrs = self._queries[query_string]['attrs']
        if tags.split(' ')[id_tag]:
            element = tags.split(' ')[id_tag]
        else:
            element = tags
        
        if attrs.split(' ')[id_attr]:
            attr = attrs.split(' ')[id_attr]
        else:
            attr = attrs

        return self._html.find(element, href=attr)
    

class Cities(HomePage):
    def __init__(self, url):
        super().__init__(url)

    @property
    def city_name(self):
        cities = [city.text for city in self._select(self._queries['city_element']['tags']) if city.has_attr('title')]
        logger.info('City names already scrapped!')
        return cities
    @property
    def city_links(self):
        links = [link['href'] for link in self._select(self._queries['city_element']['tags']) if link.has_attr('href')]
        logger.info('Link of each city already scrapped!')
        return links
class PostalCode(HomePage):
    def __init__(self, url):
        super().__init__(url)

    @property
    def postal_code(self):
        city_postal_code = self._find_with_attr('city_element', 1, 0)
        
        city_postal_code = city_postal_code.parent
        city_code = [code for code in city_postal_code.next_siblings][1].text
        return city_code

