import scrapy

class olx(scrapy.Spider):
    name = 'olx'
    start_urls = ['https://rn.olx.com.br/imoveis']
    #handle_httpstatus_list = [403]

    def parse(self, response):
        for houses in response.css('div.fnmrjs-1.gIEtsI'):
            try:
                yield {
                        'name' : houses.css('h2.sc-1iuc9a2-1.dTvKuJ.sc-ifAKCX.eKQLlb::text').get(),
                        'price' : houses.css('p.sc-1iuc9a2-8.bTklot.sc-ifAKCX.eoKYee::text').get().replace('R$ ', ''),
                        'link' : response.css('a.fnmrjs-0.fyjObc').attrib['href'],
                        }
            except:
                yield {
                        'name' : houses.css('h2.sc-1iuc9a2-1.dTvKuJ.sc-ifAKCX.eKQLlb::text').get(),
                        'price' : 'Sold Out',
                        'link' : response.css('a.fnmrjs-0.fyjObc').attrib['href'],
                        }

        nextPage = response.css('a.sc-248j9g-1.lfGTeV').attrib['href']
        if nextPage is not  None:
            yield response.follow(nextPage, callback=self.parse)

