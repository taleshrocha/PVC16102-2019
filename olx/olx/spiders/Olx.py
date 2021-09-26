import scrapy

class Olx(scrapy.Spider):
    name = 'olx'
    start_urls = ['https://rn.olx.com.br/imoveis/venda?sf=1']

    def parse(self, response):
        houseLinks = response.css('li.sc-1fcmfeb-2.juiJqh a')
        yield from response.follow_all(houseLinks, self.parse_house)

        nextPageLinks = response.css('div.sc-hmzhuo.ccWJBO.sc-jTzLTM.iwtnNi a')
        yield from response.follow_all(nextPageLinks, self.parse)

    def parse_house(self, response):
        area = 'EMPTY'
        municipio = 'EMPTY'
        categoria = 'EMPTY'

        def extract_with_css(query):
            return response.css(query).get(default='EMPTY').strip()

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
            'link' : response, #TODO: Use regex to clean this string
            #'value' : value,
        }
