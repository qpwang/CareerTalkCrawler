#-*- coding:utf-8 -*-
import re
import time
from CareerSearch import service
from CareerSearch.spiders.base import CareerSpider
from CareerSearch.spiders.itemloaders import *
from CareerSearch.spiders.scriptprocessors import *
from CareerSearch.spiders.sourcelinkprocessors import *
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


class BITSpider(CareerSpider):

    name = 'bit'
    itemloader_class = BITItemLoader
    sourcelinkprocessor_class = BITSourceLinkProcessor
    scriptprocessor_class = BITScriptProcessor

    item_regexs = [re.compile(r'^http://job.bit.edu.cn/job/news.jhtml\?action=jobMeetingInfo&jobMeetingId=[0-9]+$')]
    def __init__(self, name=None, **kwarg):
        super(BITSpider, self).__init__(name, **kwarg)

    def get_callback(self, link):
        return self.parse_item if _matches(link, self.item_regexs) else self.parse

    def get_rule_list(self):
        return [
                   {
                    'allow' : r'^http://job.bit.edu.cn/job/news/jobMeetingAll.jhtml?page=[0-9]$',
                    'process_links' : 'process_links',
                    'check_url' : True,
                   },
                   {
                    'allow' : r'^http://job.bit.edu.cn/job/news.jhtml\?action=jobMeetingInfo&jobMeetingId=[0-9]+$',
                    'process_links' : 'process_links',
                    'check_url' : False,
                    'link_type' : LinkType.LEAF
                   },
               ]


class BeiHangSpider(CareerSpider):

    name = 'beihang'
    itemloader_class = BeiHangItemLoader
    sourcelinkprocessor_class = BeiHangSourceLinkProcessor
    scriptprocessor_class = BeiHangScriptProcessor

    item_regexs = [re.compile(r'^http://career.buaa.edu.cn/website/zphxx/.*h$')]
    def __init__(self, name=None, **kwarg):
        super(BeiHangSpider, self).__init__(name, **kwarg)

    def get_callback(self, link):
        return self.parse_item if _matches(link, self.item_regexs) else self.parse

    def get_rule_list(self):
        return [
                   {
                    'allow' : r'^http://career.buaa.edu.cn/website/zphxx.h\?pageNo=[0-9]$',
                    'process_links' : 'process_links',
                    'check_url' : True,
                   },
                   {
                    'allow' : r'^http://career.buaa.edu.cn/website/zphxx/.{24}\.h$',
                    'process_links' : 'process_links',
                    'check_url' : False,
                    'link_type' : LinkType.LEAF
                   },
               ]


class USTBSpider(CareerSpider):

    name = 'ustb'
    itemloader_class = USTBItemLoader
    sourcelinkprocessor_class = USTBSourceLinkProcessor
    scriptprocessor_class = USTBScriptProcessor

    item_regexs = [re.compile(r'^http://job.ustb.edu.cn/accms/sites/jobc/zhaopinhuixinxi-content.jsp\?contentId=[0-9]+$')]
    def __init__(self, name=None, **kwarg):
        super(USTBSpider, self).__init__(name, **kwarg)

    def start_requests(self):
        links = service.get_links(self.get_domain(), 0)
        base_url = 'http://job.ustb.edu.cn/accms/sites/jobc/zhaopinhuixinxi-list.jsp?fromDate=%s&F_FL1=校内&F_FL2='
        week_day = time.localtime().tm_wday
        time_str1 = '%4d%2.2d%2.2d' % (time.localtime(time.time() - 60 * 60 * 24 * week_day).tm_year, time.localtime(time.time() - 60 * 60 * 24 * week_day).tm_mon, time.localtime(time.time() - 60 * 60 * 24 * week_day).tm_mday)
        time_str2 = '%4d%2.2d%2.2d' % (time.localtime(time.time() - 60 * 60 * 24 * (week_day - 7)).tm_year, time.localtime(time.time() - 60 * 60 * 24 * (week_day - 7)).tm_mon, time.localtime(time.time() - 60 * 60 * 24 * (week_day - 7)).tm_mday)
        time_str3 = '%4d%2.2d%2.2d' % (time.localtime(time.time() - 60 * 60 * 24 * (week_day - 14)).tm_year, time.localtime(time.time() - 60 * 60 * 24 * (week_day - 14)).tm_mon, time.localtime(time.time() - 60 * 60 * 24 * (week_day - 14)).tm_mday)
        time_str4 = '%4d%2.2d%2.2d' % (time.localtime(time.time() - 60 * 60 * 24 * (week_day - 21)).tm_year, time.localtime(time.time() - 60 * 60 * 24 * (week_day - 21)).tm_mon, time.localtime(time.time() - 60 * 60 * 24 * (week_day - 21)).tm_mday)
        links.extend([base_url % time_str1,
                      base_url % time_str2,
                      base_url % time_str3,
                      base_url % time_str4,
                      ])
        for link in links:
            yield self._create_request(link)

    def get_callback(self, link):
        return self.parse_item if _matches(link, self.item_regexs) else self.parse

    def get_rule_list(self):
        return [
                   {
                    'allow' : r'^http://job.ustb.edu.cn/accms/sites/jobc/zhaopinhuixinxi-list.jsp\?fromDate=[0-9]{8}&F_FL1=%E6%A0%A1%E5%86%85&F_FL2=$',
                    'process_links' : 'process_links',
                    'check_url' : True,
                   },
                   {
                    'allow' : r'^http://job.ustb.edu.cn/accms/sites/jobc/zhaopinhuixinxi-content.jsp\?contentId=[0-9]+$',
                    'process_links' : 'process_links',
                    'check_url' : False,
                    'link_type' : LinkType.LEAF
                   },
               ]
