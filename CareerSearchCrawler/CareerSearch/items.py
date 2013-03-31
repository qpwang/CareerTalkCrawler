# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.loader.processor import MapCompose, TakeFirst, Join
from scrapy.utils.markup import unquote_markup
from CareerSearch.utils import strip_space


class CrawledItem(Item):
    title = Field(input_processor=MapCompose(unquote_markup, strip_space), output_processor=TakeFirst(),)
    address = Field(default='', input_processor=MapCompose(unquote_markup, strip_space), output_processor=TakeFirst(),)
    begin_time = Field(default='', input_processor=MapCompose(unquote_markup, strip_space), output_processor=TakeFirst(),)
    end_time = Field(default='', input_processor=MapCompose(unquote_markup, strip_space), output_processor=TakeFirst(),)
    post_time = Field(default='', input_processor=MapCompose(unquote_markup, strip_space), output_processor=TakeFirst(),)
    content = Field(default='', input_processor=MapCompose(unquote_markup, strip_space), output_processor=TakeFirst(),)

class CareerItem(CrawledItem):
    source = Field(output_processor=TakeFirst(),)
    source_link = Field(output_processor=TakeFirst(),)
    content_md5 = Field(output_processor=TakeFirst(),)
    add_time = Field(output_processor=TakeFirst(),)
    update_time = Field(output_processor=TakeFirst(),)

class PekingCareerItem(CareerItem):
    address = Field(default='', input_processor=MapCompose(unquote_markup, strip_space), output_processor=Join(),)
