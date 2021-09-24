import scrapy

class olx(scrapy.Spider):
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
            #'title' : extract_with_css('h2.sc-1iuc9a2-1.dTvKuJ.sc-ifAKCX.eKQLlb::text'),
            'price' : extract_with_css('h2.sc-1wimjbb-0.JzEH.sc-ifAKCX.cmFKIN::text').replace('R$ ', ''),
            #'link' : extract_with_css('a.fnmrjs-0.fyjObc::attr(href)'),
        }
