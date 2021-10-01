import logging
import scrapy
import re

logger = logging.getLogger('LOGGER')

class Olx(scrapy.Spider):
    def __init__(self):
            self.ps = 0
            self.pe = 100000

    def next_link(pe):
            self.ps = self.pe
            self.pe = self.pe + 50000

    name = 'olx'
    start_urls = ['https://rn.olx.com.br/imoveis/venda?pe=1000&ps=10']

    def parse(self, response):
        logger.info('====================START PARSER====================')

        string = response.css('span.sc-1mi5vq6-0.eDXljX.sc-ifAKCX.fhJlIo::text').get()
        logger.info('==================== %s ====================', string)
        #match = re.search(pattern = "[0-9]*\.[0-9]*", string = string)
        match = re.search(pattern = "[0-9][0-9]", string = string)

        if float(match.group()) < 4800:
            # Gets the links for each house in the page
            houseLinks = response.css('li.sc-1fcmfeb-2.juiJqh a')
            yield from response.follow_all(houseLinks, self.parse_house)

            page = response.css('div.sc-hmzhuo.ccWJBO.sc-jTzLTM.iwtnNi span::text').get()
            if page == 'Página anterior':
            # Go to the next interval
                nextLink = 'https://rn.olx.com.br/imoveis/venda?pe=' + str(self.pe) + '&ps=' + str(self.ps)
                logger.info('====================Next link: %s====================', nextLink)
                yield response.follow_all(nextLink, self.parse)
            else:
                # Get to a smaller interval TODO
                logger.info('====================NEXT-PAGE====================')
                nextPageLinks = response.css('div.sc-hmzhuo.ccWJBO.sc-jTzLTM.iwtnNi a')
                yield from response.follow_all(nextPageLinks, self.parse)
        else:
            logger.info('====================DIED====================')
            raise CloseSpider('Nothing to scrape')

    def parse_house(self, response):
        logger.info('====================PARCE-HOUSE====================')

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
