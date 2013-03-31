from scrapy.exceptions import DropItem
from CareerSearch.db import career
from CareerSearch.db.itemadapters import CareerItemAdapterFactory
from CareerSearch.utils import log_error

class CareerItemAdapterPipeline(object):

    def process_item(self, item, spider):
        try:
            adapter = CareerItemAdapterFactory.get_itemadapter(item.get('source'))
            if adapter:
                item = adapter.adapt(item)
            return item
        except Exception, e:
            log_error(e)
            raise DropItem()

class CareerItemStorePipeline(object):

    def process_item(self, item, spider):
        try:
            if spider.is_item_valid(item, 1):
                career.save_item(item, spider.name)
                return item
            else:
                raise DropItem("invalid item: %s" % item)
        except Exception, e:
            log_error(e)
            raise DropItem()

class CareerItemQueueImagePipeline(object):

    def process_item(self, item, spider):
        try:
#            icon_dic = {}
#            icon_dic['url'] = item['icon_link']
#            icon_dic['source_link'] = item['source_link']
#            icon_dic['source'] = 'icon'
#            career.push_image_url(icon_dic)
#
#            image_dic = {}
#            image_dic['url'] = item['images']
#            image_dic['source_link'] = item['source_link']
#            image_dic['source'] = 'image'
#            career.push_image_url(image_dic)
            return item
        except Exception, e:
            log_error(e)
            raise DropItem()

