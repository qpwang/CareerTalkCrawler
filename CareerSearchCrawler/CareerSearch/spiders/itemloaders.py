from scrapy.contrib.loader import XPathItemLoader
from CareerSearch.items import CareerItem


class TsingHuaItemLoader(XPathItemLoader):

    def __init__(self, selector):
        self._selector = selector
        super(TsingHuaItemLoader, self).__init__(item=CareerItem(), selector=self._selector)
        self._init_path()

    def _init_path(self):
        self.add_xpath('title', '//div[@id="doc_list"]/ul/li[@class="title"]/text()')
        self.add_xpath('address', '//div[@id="doc_list"]/ul/li[@class="content"]//tr[3]/td[2]/text()')
        self.add_xpath('begin_time', '//div[@id="doc_list"]/ul/li[@class="content"]//tr[2]/td[2]/text()')
#        self.add_xpath('end_time', '')
        self.add_xpath('post_time', '//div[@id="doc_list"]//td/li[@class="title_fu"]/text()')
        self.add_xpath('content', '//div[@id="doc_list"]/ul/li[@class="content"]')


class PekingItemLoader(XPathItemLoader):

    def __init__(self, selector):
        self._selector = selector
        super(PekingItemLoader, self).__init__(item=CareerItem(), selector=self._selector)
        self._init_path()

    def _init_path(self):
        self.add_xpath('title', '//li[@class="heicu"]/text()')
        self.add_xpath('address', '//li[@class="wz1text"]/p[2]/b/text()')
        self.add_xpath('begin_time', '//li[@class="wz1text"]/p[1]/b/text()')
#        self.add_xpath('end_time', '')
        self.add_xpath('post_time', '//ul[@class="wz1ul"]/li[2]/text()')
        self.add_xpath('content', '//ul[@class="wz1ul"]')

