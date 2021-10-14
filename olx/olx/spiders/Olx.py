import scrapy
import re

class Olx(scrapy.Spider):
    # Attributes
    def __init__(self):
        self.ps = 0
        self.pe = 25000

    # Go to the next price interval
    def next_interval(self, pe):
        self.ps = pe
        self.pe += 25000

    # In case the page shows more than 4800 results, this method will decrease the price interval in order to show less houses in the page
    def decrease_interval(self, pe):
        self.pe -= 10000

    name = 'olx'
    allowed_domains = ['olx.com.br']
    start_urls = ['https://rn.olx.com.br/imoveis/venda?pe=25000&ps=0']

    # Initial parser for Scrapy. Is the "main" function.
    def parse(self, response):
        self.logger.info('====================INTERVAL: %d-%d====================', self.ps, self.pe)

        # Gets how many houses are in the page. The maximun is 5000.
        string = response.css('span.sc-1mi5vq6-0.eDXljX.sc-ifAKCX.fhJlIo::text').get()
        aux = re.search(pattern = '\d+\.?\d+?\sresultados', string = string)
        houseQuantity = re.search(pattern = '\d+\.?\d+', string = aux.group().replace('.',''))
        self.logger.info('====================HOUSES: %.0f====================', float(houseQuantity.group()))

        if float(houseQuantity.group()) < 4800: # If i can scrape all the houses in the page
            # Gets the links for each house in the page
            houseLinks = response.css('li.sc-1fcmfeb-2.juiJqh a')
            yield from response.follow_all(houseLinks, self.parse_house)

            # Gets the next page link.
            nextPage = response.css('div.sc-hmzhuo.ccWJBO.sc-jTzLTM.iwtnNi span::text').get()

            if nextPage == 'Página anterior': # There is no more pages to scrape in this price interval
                # Go to the next price interval
                self.next_interval(self.pe)
                nextLink = 'https://rn.olx.com.br/imoveis/venda?pe=' + str(self.pe) + '&ps=' + str(self.ps)
                yield scrapy.Request(url=nextLink, callback=self.parse)
            else: # Just get the next page link and keep scraping
                nextPageLinks = response.css('div.sc-hmzhuo.ccWJBO.sc-jTzLTM.iwtnNi a')
                yield from response.follow_all(nextPageLinks, self.parse)
        else:
            # Make the interval smaller
            self.decrease_interval(self.pe)
            self.logger.info('====================DECREASE_INTERVAL: %d-%d====================', self.ps, self.pe)
            # Create the new url string and call the parcer for the new interval
            nextLink = 'https://rn.olx.com.br/imoveis/venda?pe=' + str(self.pe) + '&ps=' + str(self.ps)
            yield scrapy.Request(url=nextLink, callback=self.parse)

    # Extracts all the needed information of a house page.
    def parse_house(self, response):

        def extract_with_css(query, errMsg):
            return response.css(query).get(default=errMsg).strip()

        # Give defaut error values to all the variebles i'am going to scrape
        area = 'AREA-ERR'
        areaUtil = 'AREAUTIL-ERR'
        areaTitle = 'AREATITLE-ERR'
        areaDesc = 'AREADESC-ERR'
        areaDesc = 'AREADESC-ERR'
        areaUtil = 'AREAUTIL-ERR'
        areaConst = 'AREACONST-ERR'
        municipio = 'MUNICIPIO-ERR'
        categoria = 'CATEGORIA-ERR'
        cep = 'CEP-ERR'

        houseDetails = response.css('div.duvuxf-0.h3us20-0.jyICCp')

        for detail in houseDetails:
            if detail.css('dt::text').get() == 'Área útil':
                areaUtil = detail.css('dd::text').get().replace('m²', '')
            elif detail.css('dt::text').get() == 'Área construída':
                areaConst = detail.css('dd::text').get().replace('m²', '')
            elif detail.css('dt::text').get() == 'Município':
                municipio = detail.css('dd::text').get()
            elif detail.css('dt::text').get() == 'CEP':
                cep = detail.css('dd::text').get()
            elif detail.css('dt::text').get() == 'Categoria':
                categoria = detail.css('a::text').get()[:-1]

        # Gets the area by the house title. If it has
        title = response.css('h1.sc-45jt43-0.eCghYu.sc-ifAKCX.cmFKIN::text').get()
        aux = re.search(pattern = '\d+(\.|,)?(\d+)?(\s+)?m(²|2)', string = title) # Gets strings like '60m²' or '60 m²' or '60.01m2' and more
        if aux != None:
            areaClear = re.search(pattern = "\d+", string = aux.group()) # Gets only the numerator value
            areaTitle = areaClear.group()

        # Gives preference to areaUtil over areaConst and areaTitle variebles
        if areaUtil != 'AREAUTIL-ERR':
            area = areaUtil
        elif areaConst != 'AREACONST-ERR':
            area = areaConst
        elif areaTitle != 'AREATITLE-ERR':
            area = areaTitle

        description = response.css('span.sc-1sj3nln-1.eOSweo.sc-ifAKCX.cmFKIN::text').get()
        aux = re.search(pattern = '\d+(\.|,)?(\d+)?(\s+)?m(²|2)', string = description) # Gets strings like '60m²' or '60 m²' or '60.01m2' and more
        if aux != None:
            areaClear = re.search(pattern = "\d+", string = aux.group()) # Gets only the numerator value TODO This will make a 2.000m2 how have 2m2!
            # TODO If the float point is ',' change to '.'
            areaDesc = areaClear.group()

        yield{
            #'titulo' : extract_with_css('h1.sc-45jt43-0.eCghYu.sc-ifAKCX.cmFKIN::text', 'TITULO-ERR'),
            #'description' : description,
            'preco' : extract_with_css('h2.sc-1wimjbb-0.JzEH.sc-ifAKCX.cmFKIN::text', 'PRECO-ERR').replace('R$ ', ''),
            'area' : area,
            'cep' : cep,
            #'areaUtil' : areaUtil,
            #'areaConst' : areaConst,
            #'areaTitle' : areaTitle,
            #'areaDesc' : areaDesc,
            #'municipio' : municipio,
            #'categoria' : categoria,
            #'link' : self.link_extractor.extract_links(response).get(),
            'link' : response,
        }
