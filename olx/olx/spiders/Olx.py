import scrapy
import re

class Olx(scrapy.Spider):
    beginInter = 0
    endInter = 100000

    name = 'olx'
    start_urls = ['https://rn.olx.com.br/imoveis/venda?pe=' + str(endInter) + '&ps=' + str(beginInter)]

    def parse(self, response):

        string = response.css('span.sc-1mi5vq6-0.eDXljX.sc-ifAKCX.fhJlIo::text').get()
        match = re.search(pattern = "[0-9]*\.[0-9]*", string = string)

        if float(match.group()) < 4800:
            # Gets the links for each house in the page
            houseLinks = response.css('li.sc-1fcmfeb-2.juiJqh a')
            yield from response.follow_all(houseLinks, self.parse_house)

            # Gets the next interval link. Wich is the next page
            beginInter = beginInter + 50000
            endInter = endInter + 50000

            nextInterval = 'https://rn.olx.com.br/imoveis/venda?pe=' + str(endInter) + '&ps=' + str(beginInter)
            yield from response.follow_all(nextInterval, self.parse)
        else:
            yield 'Nothing to scrape'
            exit()

    def parse_house(self, response):

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
            'area' : area,
            'municipio' : municipio,
            'categoria' : categoria,
            'link' : response,
            #'value' : value,
        }
