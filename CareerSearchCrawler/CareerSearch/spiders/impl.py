import re
import time
from CareerSearch import service
from CareerSearch.spiders.base import CareerSpider
from CareerSearch.spiders.itemloaders import TsingHuaItemLoader, PekingItemLoader, RenMinItemLoader
from CareerSearch.spiders.scriptprocessors import TsingHuaScriptProcessor, PekingScriptProcessor, RenMinScriptProcessor
from CareerSearch.spiders.sourcelinkprocessors import TsingHuaSourceLinkProcessor, PekingSourceLinkProcessor, RenMinSourceLinkProcessor
from CareerSearch.gen.ttypes import LinkType


def _matches(url, regexs):
    for r in regexs:
        if r.search(url):
            return True
    return False


class TsingHuaSpider(CareerSpider):

    name = "tsinghua"
    itemloader_class = TsingHuaItemLoader
    sourcelinkprocessor_class = TsingHuaSourceLinkProcessor
    scriptprocessor_class = TsingHuaScriptProcessor

    item_regexs = [re.compile(r'^http://career.tsinghua.edu.cn/docinfo/career/jyzpxx/zphDetail_zc.jsp\?id=.*')]
    def __init__(self, name=None, **kwarg):
        super(TsingHuaSpider, self).__init__(name, **kwarg)

    def get_callback(self, link):
        return self.parse_item if _matches(link, self.item_regexs) else self.parse

    def get_rule_list(self):
        return [
                   {
                    'allow' : r'^http://career.tsinghua.edu.cn/docinfo/career/jyzpxx/jrqzph_more.jsp(\?pagenp=[0-9]+)?',
                    'process_links' : 'process_links',
                    'check_url' : True,
                   },
                   {
                    'allow' : r'^http://career.tsinghua.edu.cn/docinfo/career/jyzpxx/zphDetail_zc.jsp\?id=.*',
                    'process_links' : 'process_links',
                    'check_url' : False,
                    'link_type' : LinkType.LEAF
                   },
               ]


class PekingSpider(CareerSpider):

    name = 'peking'
    itemloader_class = PekingItemLoader
    sourcelinkprocess_class = PekingSourceLinkProcessor
    scriptprocessor_class = PekingScriptProcessor

    item_regexs = [re.compile(r'^http://scc.pku.edu.cn/zpxx/zphd/[0-9]+\.htm$')]
    def __init__(self, name=None, **kwarg):
        super(PekingSpider, self).__init__(name, **kwarg)

    def get_callback(self, link):
        return self.parse_item if _matches(link, self.item_regexs) else self.parse

    def get_rule_list(self):
        return [
                   {
                    'allow' : r'^http://scc.pku.edu.cn/zpxx/zphd/index[0-9]*\.htm$',
                    'process_links' : 'process_links',
                    'check_url' : True,
                   },
                   {
                    'allow' : r'^http://scc.pku.edu.cn/zpxx/zphd/[0-9]+\.htm$',
                    'process_links' : 'process_links',
                    'check_url' : False,
                    'link_type' : LinkType.LEAF
                   },
               ]


class RenMinSpider(CareerSpider):

    name = 'renmin'
    itemloader_class = RenMinItemLoader
    sourcelinkprocessor_class = RenMinSourceLinkProcessor
    scriptprocessor_class = RenMinScriptProcessor

    item_regexs = [re.compile(r'^http://career.ruc.edu.cn/article_show2\.asp\?id=[0-9]+$')]
    def __init__(self, name=None, **kwarg):
        super(RenMinSpider, self).__init__(name, **kwarg)

    def start_requests(self):
        links = service.get_links(self.get_domain(), 0)
        time_str1 = '%s-%s' % (time.localtime().tm_year, time.localtime().tm_mon)
        time_str2 = '%s-%s' % (time.localtime().tm_year, time.localtime().tm_mon + 1)
        links.extend(['http://career.ruc.edu.cn/index.asp?date=%s' % time_str1,
                      'http://career.ruc.edu.cn/index.asp?date=%s' % time_str2])
        for link in links:
            yield self._create_request(link)

    def get_callback(self, link):
        return self.parse_item if _matches(link, self.item_regexs) else self.parse

    def get_rule_list(self):
        return [
                   {
                    'allow' : r'^http://career.ruc.edu.cn/news\.asp\?date=[0-9]{4}/[0-9]{2}/[0-9]{2}$',
                    'process_links' : 'process_links',
                    'check_url' : True,
                   },
                   {
                    'allow' : r'^http://career.ruc.edu.cn/article_show2\.asp\?id=[0-9]+$',
                    'process_links' : 'process_links',
                    'check_url' : False,
                    'link_type' : LinkType.LEAF
                   },
               ]
