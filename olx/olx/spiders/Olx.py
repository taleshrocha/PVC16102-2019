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
        houseLinks = response.css('li.sc-1fcmfeb-2.fvbmlV a')
        yield from response.follow_all(houseLinks, self.parse_house)

        nextPageLinks = response.css('div.sc-hmzhuo.kJjuHR.sc-jTzLTM.iwtnNi a')
        yield from response.follow_all(nextPageLinks, self.parse)

    # Extracts all the needed information of a house page.
    def parse_house(self, response):

        def extract_number(text):
            aux1 = re.search('\d+(\.|,)?(\d+)?(\s+)?m(²|2)', text)
            aux2 = re.search('R\$\s', text)
            if aux1 != None:
                number = re.sub('m(²|2)', '', aux1.group()) # Removes the m² or m2
                if '.' in number: # A number like 2.000 will be 2000
                    number = number.replace('.', '')
                elif ',' in number:
                    number = re.sub(',\d+', '', number) # A number like 2,000 will be 2
                return number
            elif aux2 != None:
                price = text.replace('R$ ', '')
                return price
            else:
                return text

        def extract_category(category):
            aux = re.search('Aluguel', category)
            if aux == None:
                return category[0], 'V'
            else:
                return category[0], 'A'

        TITLE = response.css('h1.sc-45jt43-0.eCghYu.sc-ifAKCX.cmFKIN::text').get()
        DESCRIPTION = response.css('span.sc-1sj3nln-1.eOSweo.sc-ifAKCX.cmFKIN::text').get()
        HOUSE_TAGS = response.css('div.duvuxf-0.h3us20-0.jyICCp')

        tags = {'Área útil' : 'AREAUTIL-ERR', # TODO a área pode ser chamada de tamanho or ignore all terrains?
                'Área construída' : 'AREACONST-ERR',
                'Condomínio' : 'CONDO-ERR',
                'Quartos' : 'QUARTOS-ERR',
                'IPTU' : 'IPTU-ERR',
                'Banheiros' : 'BANHEIROS-ERR',
                'Município' : 'MUNICIPIO-ERR',
                'CEP' : 'CEP-ERR',
                'Categoria' : 'CATEGORIA-ERR',
                'Vagas na garagem' : 'VAGAS-ERR'}

        # Get all tags in the house tags
        for tag in HOUSE_TAGS:
            for key, value in tags.items():
                if tag.css('dt::text').get() == key:
                    if tag.css('dd::text').get() == None:
                        dic = extract_category(tag.css('a::text').get())
                        tags[key] = dic[0]
                    else:
                        tags[key] = extract_number(tag.css('dd::text').get())
                    self.logger.info('====================%s: %s====================', tag.css('dt::text').get(), tags[key])

        tags['Tipo'] = dic[1]
        tags['Área título'] = extract_number(TITLE)
        tags['Área descrição'] = extract_number(DESCRIPTION)

        # Gives preference to areaUtil over areaConst and areaTitle variebles
        if tags['Área útil'] != 'AREAUTIL-ERR':
            area = tags['Área útil'];
        elif tags['Área construída'] != 'AREACONST-ERR':
            area = tags['Área construída'];
        elif tags['Área título'] != TITLE:
            area = tags['Área título'];
        elif tags['Área descrição'] != DESCRIPTION:
            area = tags['Área descrição'];
        else:
            area = 'AREA-ERR';

        # Gets the date that the house was published
        date = response.css('span.sc-1oq8jzc-0.jvuXUB.sc-ifAKCX.fizSrB::text').getall()
        day = re.search('\d{1,2}/\d{1,2}', date[1])
        hour = re.search('\d{1,2}:\d{1,2}', date[1])

        # Gets the url to all images in that page. Downloads in the images pipeline
        images = response.css('div.lkx530-2.bgLcPW div img::attr(src)').extract() # Gets a array with the images urls for downloading

        yield{
            'images' : images,
            'vagas' : tags['Vagas na garagem'],
            'categoria' : tags['Categoria'],
            'tipo' : tags['Tipo'],
            'condo' : tags['Condomínio'],
            'iptu' : tags['IPTU'],
            'quartos' : tags['Quartos'],
            'banheiros' : tags['Banheiros'],
            'day' : day.group(),
            'hour' : hour.group(),
            'cep' : tags['CEP'],
            'municipio' : (tags['Município'])[0],
            'area' : area,
            'preco' : extract_number(response.css('h2.sc-1wimjbb-0.JzEH.sc-ifAKCX.cmFKIN::text').get(default='PRECO-ERR').replace('R$ ', '') + 'm2'),
            'area' : area,
            #'area' : tags['Área útil'],        # For debug
            #'area' : tags['Área construida'],  # For debug
            #'area' : tags['Área título'],      # For debug
            #'area' : tags['Área descrição'],   # For debug
            'titulo' : TITLE,
            'description' : DESCRIPTION,
            'link' : response.request.url,
        }
