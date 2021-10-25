import scrapy
import re

class Olx(scrapy.Spider):

    name = 'olx'
    allowed_domains = ['olx.com.br']
    start_urls = ['https://rn.olx.com.br/imoveis?q=minha%20casa%20minha%20vida&sp=1',
                  'https://rn.olx.com.br/imoveis?q=mcmv&sp=1']

    # Initial parser for Scrapy. Is the "main" function.
    def parse(self, response):

        # Gets the links for each house in the page
        houseLinks = response.css('li.sc-1fcmfeb-2.juiJqh a')
        yield from response.follow_all(houseLinks, self.parse_house)

        nextPageLinks = response.css('div.sc-hmzhuo.ccWJBO.sc-jTzLTM.iwtnNi a')
        yield from response.follow_all(nextPageLinks, self.parse)

    # Extracts all the needed information of a house page.
    def parse_house(self, response):

        def extract_area_value(text, errMsg):
            aux = re.search('\d+(\.|,)?(\d+)?(\s+)?m(²|2)', text)
            if aux != None:
                number = re.sub('m(²|2)', '', aux.group()) # Removes the m² or m2
                if '.' in number: # A number like 2.000 will be 2000
                    number = number.replace('.', '')
                elif ',' in number:
                    number = re.sub(',\d+', '', number) # A number like 2,000 will be 2
                return number
            else:
                return errMsg

        tags = {'Área útil' : 'AREAUTIL-ERR',
                'Área construída' : 'AREACONST-ERR',
                'Condomínio' : 'CONDO-ERR',
                'Quartos' : 'QUARTOS-ERR',
                'IPTU' : 'IPTU-ERR',
                'Banheiros' : 'BANHEIROS-ERR',
                'Município' : 'MUNICIPIO-ERR',
                'CEP' : 'CEP-ERR',
                'Categoria' : 'CATEGORIA-ERR'}

        houseDetails = response.css('div.duvuxf-0.h3us20-0.jyICCp')

        # Get all tags in the house tags
        for houseDetail in houseDetails:
            for key, value in tags.items():
                if houseDetail.css('dt::text').get() == key:
                     tags[key] = houseDetail.css('dd::text').get()
                     self.logger.info('====================%s: %s====================', houseDetail.css('dt::text').get(), tags[key])


        ## Gets the area by the house title. If it has
        #title = response.css('h1.sc-45jt43-0.eCghYu.sc-ifAKCX.cmFKIN::text').get()
        #areaTitle = extract_area_value(title, 'AREATITLE-ERR')
#
        ## Gives preference to areaUtil over areaConst and areaTitle variebles
        #if areaUtil != 'AREAUTIL-ERR':
            #area = areaUtil
        #elif areaConst != 'AREACONST-ERR':
            #area = areaConst
        #elif areaTitle != 'AREATITLE-ERR':
            #area = areaTitle

        description = response.css('span.sc-1sj3nln-1.eOSweo.sc-ifAKCX.cmFKIN::text').get()
        areaDesc = extract_area_value(description, 'AREADESC-ERR')

        # Gets the date that the house was published
        date = response.css('span.sc-1oq8jzc-0.jvuXUB.sc-ifAKCX.fizSrB::text').getall()
        day = re.search('\d{1,2}/\d{1,2}', date[1])
        hour = re.search('\d{1,2}:\d{1,2}', date[1])

        yield{
            'condo' : tags['Condomínio'],
            'iptu' : tags['IPTU'],
            'quartos' : tags['Quartos'],
            'banheiros' : tags['Banheiros'],
            #'day' : day.group(),
            #'hour' : hour.group(),
            #'cep' : cep,
            #'categoria' : categoria,
            #'titulo' : extract_with_css('h1.sc-45jt43-0.eCghYu.sc-ifAKCX.cmFKIN::text', 'TITULO-ERR'), #TODO, dont use estract_with
            #'description' : description,
            #'area' : area,
            #'preco' : extract_with_css('h2.sc-1wimjbb-0.JzEH.sc-ifAKCX.cmFKIN::text', 'PRECO-ERR').replace('R$ ', ''),#TODO, dont use estract_with
            #'areaUtil' : areaUtil,
            #'areaConst' : areaConst,
            #'areaTitle' : areaTitle,
            #'areaDesc' : areaDesc,
            #'municipio' : municipio,
            #'link' : self.link_extractor.extract_links(response).get(),
            'link' : response.request.url,
        }
