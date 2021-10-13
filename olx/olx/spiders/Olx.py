import logging
import scrapy
from scrapy.linkextractors import LinkExtractor
import re

logger = logging.getLogger('LOGGER')

class Olx(scrapy.Spider):
    # Attributes
    def __init__(self):
        self.ps = 90000
        self.pe = 100000

    # Increases the price interval
    def next_link(self, pe):
        self.ps = pe
        self.pe = pe + 50000

    name = 'olx'
    start_urls = ['https://rn.olx.com.br/imoveis/venda?pe=100000&ps=90000']

    # Initial parser for Scrapy. Is the "main" function.
    def parse(self, response):
        logger.info('====================INTERVAL: %d-%d====================', self.ps, self.pe)

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

        if nextPage == 'Página anterior': # There is no more pages to scrape in this price interval
            # Go to the next price interval
            self.next_link(self.pe)
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

        def extract_with_css(query, errMsg):
            return response.css(query).get(default=errMsg).strip()

        area = 'AREA-ERR'
        areaUtil = 'AREAUTIL-ERR'
        areaTitle = 'AREATITLE-ERR'
        areaDesc = 'AREADESC-ERR'
        areaUtil = 'AREAUTIL-ERR'
        areaConst = 'AREACONST-ERR'
        municipio = 'MUNICIPIO-ERR'
        categoria = 'CATEGORIA-ERR'

        houseDetails = response.css('div.duvuxf-0.h3us20-0.jyICCp')


        for detail in houseDetails:
            if detail.css('dt::text').get() == 'Área útil':
                areaUtil = detail.css('dd::text').get().replace('m²', '')
            elif detail.css('dt::text').get() == 'Área construída':
                areaConst = detail.css('dd::text').get().replace('m²', '')
            elif detail.css('dt::text').get() == 'Município':
                municipio = detail.css('dd::text').get()
            elif detail.css('dt::text').get() == 'Categoria':
                categoria = detail.css('a::text').get()[:-1]

        title = response.css('h1.sc-45jt43-0.eCghYu.sc-ifAKCX.cmFKIN::text').get()
        areaRaw = re.search(pattern = "\d+\.?\d+?\s?m²", string = title)
        if areaRaw != None:
            areaClear = re.search(pattern = "\d+", string = areaRaw.group())
            areaTitle = areaClear.group()

        # Gives preference to areaUtil over areaConst
        if areaUtil != 'AREAUTIL-ERR':
            area = areaUtil
        elif areaConst != 'AREACONST-ERR':
            area = areaConst
        elif areaTitle != 'AREATITLE-ERR':
            area = areaTitle

        yield{
            #'titulo' : extract_with_css('h1.sc-45jt43-0.eCghYu.sc-ifAKCX.cmFKIN::text', 'TITULO-ERR'),
            #'preco' : extract_with_css('h2.sc-1wimjbb-0.JzEH.sc-ifAKCX.cmFKIN::text', 'PRECO-ERR').replace('R$ ', ''),
            'area' : area,
            'areaUtil' : areaUtil,
            'areaConst' : areaConst,
            'areaTitle' : areaTitle,
            #'municipio' : municipio,
            #'categoria' : categoria,
            #'link' : self.link_extractor.extract_links(response).get(),
            'link' : response,
        }
