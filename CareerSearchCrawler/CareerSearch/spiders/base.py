#-*- coding:utf-8 -*-
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule
from scrapy.contrib.loader import XPathItemLoader
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from CareerSearch.spiders.linkextractor import SgmlLinkExtractor2
from CareerSearch.utils import log_error
from CareerSearch.db import career
from CareerSearch.gen.ttypes import Status, LinkStatus, LinkType, Link
from CareerSearch import service

_compiled_rules = {}


class CareerSpider(CrawlSpider):

    #TODO: for now we treat all these as errors
    handle_httpstatus_list = [403, 404, 500]
    name = ''
    itemloader_class = XPathItemLoader
    scriptprocessor_class = None
    sourcelinkprocessor_class = None
    sourcefilterprocessor_class = None
    redirectprocessor_class = None

    def __init__(self, name=None, **kwarg):
        super(CareerSpider, self).__init__(name, **kwarg)

    def start_requests(self):
#        links = service.get_links(self.get_domain(), 0)
        links = ['http://career.ruc.edu.cn/']
#        http://scc.pku.edu.cn/zpxx/zphd/34590.htm
        for link in links:
            yield self._create_request(link)

    def _create_request(self, link):
        meta = {
                'domain' : self.get_domain(),
                'rules' : self.get_rule_list(),
#                'dont_redirect' : True,
                }
        callback = self.get_callback(link)
        return Request(url=link, callback=callback, meta=meta)

    def get_callback(self, link):
        '''
        Override this method to assign callback function to request.
        '''
        return self.parse

    def _process_response(self, response, source, type):
        '''
        Returns True if response can be further processed otherwise False.
        '''
        url = response.request.url
        if self.sourcefilterprocessor_class:
            processor = self.sourcefilterprocessor_class()
            url = processor.process(self, url)

        if url is None:
            service.report_status([LinkStatus(url, source, Status.FAIL, type)])
            return False

        if self.sourcelinkprocessor_class:
            processor = self.sourcelinkprocessor_class()
            url = processor.process(url)

        if url is None:
            service.report_status([LinkStatus(url, source, Status.FAIL, type)])
            return False

        if response.status == 200:
            service.report_status([LinkStatus(url, source, Status.SUCCEED, type)])
            return True
        else:
            service.report_status([LinkStatus(url, source, Status.FAIL, type)])
            return False

    def parse(self, response):
        meta = response.request.meta
        source = meta['domain']
        all_link = []
        url = response.request.url
        if not self._process_response(response, source, LinkType.CATELOG):
            return

        rule_dicts = meta['rules']
        rules = self._get_rules(source, rule_dicts)

        for rule in rules:
            links = [l for l in rule.link_extractor.extract_links(response)]
            if links and rule.process_links:
                links = rule.process_links(links)

            for link in links:
                if link not in all_link:
                    all_link.append(link)

        if all_link:
            service.report_status([LinkStatus(link.url, source, Status.FOUND, rule.link_type) for link in all_link])
            service.report_status([LinkStatus(url, source, Status.SUCCEED, LinkType.CATELOG, len(all_link))])

    def parse_item(self, response):
        meta = response.request.meta
        source = meta['domain']
        url = response.request.url
        if self.sourcelinkprocessor_class:
            processor = self.sourcelinkprocessor_class()
            url = processor.process(url)

        if not self._process_response(response, source, LinkType.LEAF):
            service.report_status([LinkStatus(meta['redirect_urls'][0], source, Status.FAIL, type)])
            career.remove_item(url, source)
            return

        if not self.itemloader_class:
            return

        try:
            selector = HtmlXPathSelector(response)
            loader = self.itemloader_class(selector)
            loader.add_value('source', source)
            loader.add_value('source_link', url)
        except Exception, e:
            service.report_status([LinkStatus(url, source, Status.FAIL, LinkType.UNKNOWN)])
            print e, url
            log_error(url)

        try:
            item = loader.load_item()
            if (self.is_item_valid(item)):
                return item
            else:
                career.remove_item(url, source)
        except Exception, e:
            log_error(e)

    def is_item_valid(self, item, level=0):
        '''
        At least source and source link are present, so an item is valid only it has more attributes loaded.
        '''
        if level == 0:
            return True
            if len(item._values) <= 2:
                return False

        if level == 1:
            return True
            #check item count
            if len(item._values) < 9:
                career.report_link(item['source'], 'mass_null', item['source_link'])
                return False

            #check key item
#            if not item.has_key('name') or not item.has_key('version') or not item.has_key('download_link'):
            if not item.has_key('name') or not item.has_key('version') or not item.has_key('download_link'):
                career.report_link(item['source'], 'missing_key', item['source_link'])
                return False

            # check image and icon, just warning, so not return False
            if not item.has_key('images') or item['images'] == '':
                career.report_link(item['source'], 'missing_image', item['source_link'])
            if not item.has_key('icon_link') or item['icon_link'] == '':
                career.report_link(item['source'], 'missing_icon', item['source_link'])

        return True

    def process_links(self, links):
        '''
        This is a default link processing implementation.
        '''
        if self.scriptprocessor_class:
            processor = self.scriptprocessor_class()
            links = processor.process(links)

        return links

    def get_rule_list(self):
        '''
        Override this method to provide a list of rules to extract links.
        '''
        return []

    def get_domain(self):
        '''
        Override this method to custom the value of domain, by default is spider's name.
        '''
        return self.name

    def _compile_rule(self, rule_dict):
        extractor = SgmlLinkExtractor2(allow=rule_dict['allow'], check_url=rule_dict.get('check_url', True))
        rule = Rule(extractor)

        def get_method(method):
            if callable(method):
                return method
            elif isinstance(method, basestring):
                return getattr(self, method, None)
            else:
                return None

        rule.process_links = get_method(rule_dict.get('process_links'))

        #set default link type to leaf
        rule.link_type = rule_dict.get('link_type', '')

        return rule

    def _get_rules(self, domain, rule_dicts):
        rules = None
        if domain in _compiled_rules:
            rules = _compiled_rules[domain]
        else:
            rules = []
            for rule_dict in rule_dicts:
                rule = self._compile_rule(rule_dict)
                if rule:
                    rules.append(rule)
            _compiled_rules[domain] = rules
        return rules

