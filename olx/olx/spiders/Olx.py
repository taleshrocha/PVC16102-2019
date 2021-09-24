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
        def extract_with_css(query):
            return response.css(query).get(default='EMPTY').strip()

        yield{
            'title' : extract_with_css('h1.sc-45jt43-0.eCghYu.sc-ifAKCX.cmFKIN::text'),
            #'price' : extract_with_css('h2.sc-1wimjbb-0.JzEH.sc-ifAKCX.cmFKIN::text').replace('R$ ', ''),
            #'link' : response, #TODO: Use regex to clean this string
            #'area' : extract_with_css('dd.sc-1f2ug0x-1.ljYeKO.sc-ifAKCX.kaNiaQ::text').replace('m²', ''), #TODO: Only get this by search for word
        }
