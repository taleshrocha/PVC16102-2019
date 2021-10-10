import logging
import scrapy
import re

logger = logging.getLogger('LOGGER')

class Olx(scrapy.Spider):
    def __init__(self):
            self.ps = 90000
            self.pe = 100000

    def next_link(self, pe):
            self.ps = pe
            self.pe = pe + 50000

    name = 'olx'
    start_urls = ['https://rn.olx.com.br/imoveis/venda?pe=100000&ps=90000']

    # Initial parser for Scrapy. Is the "main" function.
    def parse(self, response):
        logger.info('====================START-PARSER====================')
        logger.info('====================START-INTERVAL: %d-%d====================', self.ps, self.pe)

        # Gets how many houses are in the page. The maximun is 5000.
        string = response.css('span.sc-1mi5vq6-0.eDXljX.sc-ifAKCX.fhJlIo::text').get()
        houseQuantity = re.search(pattern = "[0-9][0-9]", string = string)
        logger.info('====================houseQuatity: %s====================', houseQuantity.group())

        #if float(houseQuantity.group()) < 4800000:
        # Gets the links for each house in the page
        houseLinks = response.css('li.sc-1fcmfeb-2.juiJqh a')
        yield from response.follow_all(houseLinks, self.parse_house)

        # Gets the next page link.
        nextPage = response.css('div.sc-hmzhuo.ccWJBO.sc-jTzLTM.iwtnNi span::text').get()
        logger.info('====================nextPage: %s====================', nextPage)
        if nextPage == 'Página anterior': # There is no more pages to scrape in this price interval.
            # Go to the next interval
            self.next_link(self.pe)
            logger.info('====================NEW-INTERVAL: %d-%d====================', self.ps, self.pe)
            nextLink = 'https://rn.olx.com.br/imoveis/venda?pe=' + str(self.pe) + '&ps=' + str(self.ps)
            logger.info('====================NEXT-LINK: %s====================', nextLink)
            yield scrapy.Request(url=nextLink, callback=self.parse)
        else:
            logger.info('====================NEXT-PAGE====================')
            nextPageLinks = response.css('div.sc-hmzhuo.ccWJBO.sc-jTzLTM.iwtnNi a')
            yield from response.follow_all(nextPageLinks, self.parse)
        #else:
        #    logger.info('====================DIED====================')
        #    raise CloseSpider('Nothing to scrape')

    # Extracts all the needed information of a house page.
    def parse_house(self, response):
        #logger.info('====================PARCE-HOUSE====================')

        def extract_with_css(query):
            return response.css(query).get(default='EMPTY').strip()

        area = 'EMPTY'
        municipio = 'EMPTY'
        categoria = 'EMPTY'
        houseDetails = response.css('div.duvuxf-0.h3us20-0.jyICCp')

        for detail in houseDetails:
            if detail.css('dt::text').get() == 'Área útil' or detail.css('dt::text').get() == 'Área construída':
                area = detail.css('dd::text').get().replace('m²', '') #TODO: There is other varieble for the area to. To much emptyes
            elif detail.css('dt::text').get() == 'Município':
                municipio = detail.css('dd::text').get()
            elif detail.css('dt::text').get() == 'Categoria':
                categoria = detail.css('a::text').get()[:-1]

        yield{
            #'titulo' : extract_with_css('h1.sc-45jt43-0.eCghYu.sc-ifAKCX.cmFKIN::text'),
            'preco' : extract_with_css('h2.sc-1wimjbb-0.JzEH.sc-ifAKCX.cmFKIN::text').replace('R$ ', ''),
            #'area' : area,
            #'municipio' : municipio,
            #'categoria' : categoria,
            #'link' : response,
            #'value' : value,
        }
