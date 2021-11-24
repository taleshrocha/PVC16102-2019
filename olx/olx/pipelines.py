# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

import os
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline

DETAILS_STORE = '/home/tales/Documents/bti/pesquisa/PVC16102-2019/olx-scraper/olx/details'

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
            newItem = {"id" : self.id} # Creates a id for each house
            newItem.update(item)
            item = newItem
            self.id+=1
            with open(os.path.join(DETAILS_STORE, str(item.get('id'))), "w") as f:
                f.write('TÍTULO\n' + item.get('titulo') + '\n' + 'DESCRIÇÃO\n' + item.get('description'))
            return item

class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return str(item.get('id')) + '/' + os.path.basename(urlparse(request.url).path)
