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
            aux1 = re.search('\d+(\.|,)?(\d+)?(\s+)?(m|M)(²|2)', text)
            aux2 = re.search('R\$\s', text)
            if aux1 != None:
                number = re.sub('(m|M)(²|2)', '', aux1.group()) # Removes the m² or m2
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

        def extract_area(text):
            aux = re.search('\d+(\.|,)?(\d+)?(\s+)?(m|M)(²|2)', text)
            if aux != None:
                number = re.sub('(m|M)(²|2)', '', aux.group()) # Removes the m² or m2
                if '.' in number: # A number like 2.000 will be 2000
                    number = number.replace('.', '')
                elif ',' in number:
                    number = re.sub(',\d+', '', number) # A number like 2,000 will be 2
                return number
            else:
                return text

        TITLE = response.css('h1.sc-45jt43-0.eCghYu.sc-ifAKCX.cmFKIN::text').get()
        DESCRIPTION = response.css('span.sc-1sj3nln-1.eOSweo.sc-ifAKCX.cmFKIN::text').get()
        HOUSE_TAGS = response.css('div.duvuxf-0.h3us20-0.jyICCp')

        tags = {'Área útil' : 'AREAUTIL-ERR',
                'Área construída' : 'AREACONST-ERR',
                'Condomínio' : 'CONDO-ERR',
                'Quartos' : 'QUARTOS-ERR',
                'IPTU' : 'IPTU-ERR',
                'Banheiros' : 'BANHEIROS-ERR',
                'Município' : 'MUNICIPIO-ERR',
                'CEP' : 'CEP-ERR',
                'Categoria' : 'CATEGORIA-ERR',
                'Tipo' : 'TIPO-ERR',
                'Vagas na garagem' : 'VAGAS-ERR'}

        # Get all tags in the house tags
        first = True
        for tag in HOUSE_TAGS:
            for key, value in tags.items():
                if tag.css('dt::text').get() == key:
                    if tag.css('dd::text').get() == None:
                        dic = tag.css('a::text').get()
                        tags[key] = dic[0]
                    else:
                        tags[key] = extract_number(tag.css('dd::text').get())
                    self.logger.info('====================%s: %s====================', tag.css('dt::text').get(), tags[key])

        tags['Área título'] = extract_area(TITLE)
        tags['Área descrição'] = extract_area(DESCRIPTION)

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
        script = response.css('script').getall()
        date = re.search('\d+-\d+-\d+T\d+:\d+', re.search('listTime.{19}', script[19]).group()).group()

        ano = re.search('\d{4}', date).group()
        mes = re.search('\d+', re.search('-\d{2}', date).group()).group()
        dia = re.search('\d+', re.search('-\d{2}T', date).group()).group()
        hora = re.search('\d{2}:\d{2}', date).group()

        # Gets the seller
        rawName = re.search('sellerName":".+","ad', script[7]).group()
        corretor = re.sub('((sellerName)|"|:|(,"ad))', '', rawName)

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
            'ano' : ano,
            'mes' : mes,
            'dia' : dia,
            'hora' : hora,
            'corretor' : corretor,
            'cep' : tags['CEP'],
            'municipio' : (tags['Município']),
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
