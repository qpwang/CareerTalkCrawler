from scrapy.contrib.loader import XPathItemLoader
from CareerSearch.items import CareerItem, PekingCareerItem, USTBCareerItem


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
        super(PekingItemLoader, self).__init__(item=PekingCareerItem(), selector=self._selector)
        self._init_path()

    def _init_path(self):
        self.add_xpath('title', '//li[@class="heicu"]/text()')
#        self.add_xpath('address', '//li[@class="wz1text"]/p[2]//span/text()')
#        self.add_xpath('begin_time', '//li[@class="wz1text"]/p[1]//span/text()')
#        self.add_xpath('end_time', '')
        self.add_xpath('post_time', '//ul[@class="wz1ul"]/li[2]/text()')
        self.add_xpath('content', '//li[@class="wz1text"]')
        self.add_xpath('detail', '//li[@class="wz1text"]//text()')


class RenMinItemLoader(XPathItemLoader):

    def __init__(self, selector):
        self._selector = selector
        super(RenMinItemLoader, self).__init__(item=CareerItem(), selector=self._selector)
        self._init_path()

    def _init_path(self):
        self.add_xpath('title', '//font[@color="#CC0033"]//text()')
        address = self.get_xpath('//td[@class="STYLE13"]/text()')[1]
        self.add_value('address', address)
        begin_time = self.get_xpath('//td[@class="STYLE13"]/text()')[0]
        self.add_value('begin_time', begin_time)
        content = self.get_xpath('//body/table/tr[1]')[0] + self.get_xpath('//body/table/tr[2]')[0]
        self.add_value('content', content)


class BITItemLoader(XPathItemLoader):

    def __init__(self, selector):
        self._selector = selector
        super(BITItemLoader, self).__init__(item=CareerItem(), selector=self._selector)
        self._init_path()

    def _init_path(self):
        self.add_xpath('title', '//h2/text()')
        self.add_xpath('address', '//div[@class="cont_time"]/p[3]/text()')
        self.add_xpath('begin_time', '//div[@class="cont_time"]/p[1]/text()')
        self.add_xpath('end_time', '//div[@class="cont_time"]/p[2]/text()')
        self.add_xpath('post_time', '//div[@class="cont1"]/table//td/text()')
        self.add_xpath('content', '//div[@class="cont1"]/div[2]')


class BeiHangItemLoader(XPathItemLoader):

    def __init__(self, selector):
        self._selector = selector
        super(BeiHangItemLoader, self).__init__(item=CareerItem(), selector=self._selector)
        self._init_path()

    def _init_path(self):
        self.add_xpath('title', '//div[@class="ctitle ctitle1"]/text()')
        self.add_xpath('content', '//div[@class="pbox_data"]')


class USTBItemLoader(XPathItemLoader):

    def __init__(self, selector):
        self._selector = selector
        super(USTBItemLoader, self).__init__(item=USTBCareerItem(), selector=self._selector)
        self._init_path()

    def _init_path(self):
        self.add_xpath('title', '//td[@class="title"]/text()')
        self.add_xpath('address', '//table[@id="zphxx"]//tr[2]/td/text()')
        self.add_xpath('begin_time', '//table[@id="zphxx"]//tr[1]//text()')
        self.add_xpath('content', '//table[@id="zphxx"]')
