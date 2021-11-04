# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

import os
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline

class OlxPipeline:
    # Attributes
    def __init__(self):
        self.id = 0

    def process_item(self, item, spider):
        # Drop the item if it has error in any value TODO implent the other values
        adapter = ItemAdapter(item)
        if adapter.get('area') == 'AREA-ERR':
                raise DropItem(f'THE AREA IS MISSING IN {item}')
        else:
            newItem = {"id" : self.id}
            newItem.update(item)
            item = newItem
            self.id+=1
            return item

class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return item.get('id') + '/' + os.path.basename(urlparse(request.url).path)
        #return 'blah/' + os.path.basename(urlparse(request.url).path)


#class DuplicatedHouse:
#    # If the house have the same CEP, area and price as another, discart
#    def __init__(self):
#        # Attributes
#        self.houses = set()
#
#
#    def process_item(self, item, spider):
#        # Drop the item if it already was parsed (if it's house was in the houses set)
#        def create_house(item):
#            # Gets the information that makes the house unique
#            adapter = ItemAdapter(item)
#            house = {
#            'cep': '',
#            'area': '',
#            'price': ''
#            }
#
#            house['cep'] = adapter.get('cep')
#            house['area'] = adapter.get('area')
#            house['price'] = adapter.get('price')
#            return house
#
#        house = create_house(item)
#        #if house in self.houses: TODO fix that
#        #    raise DropItem(f'THIS HOUSE IS DUPLICATED {item}')
#        #else:
#        #self.houses.add(house)
#        return item
