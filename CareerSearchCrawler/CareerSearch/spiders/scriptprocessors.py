from CareerSearch.spiders.sourcelinkprocessors import *


class TsingHuaScriptProcessor():

    source = 'tsinghua'

    def process(self, links):
        page_links = []
        processor = TsingHuaSourceLinkProcessor()
        for link in links:
            link.url = processor.process(link.url)
            if link.url:
                page_links.append(link)

        return page_links


class PekingScriptProcessor():

    source = 'peking'

    def process(self, links):
        page_links = []
        processor = PekingSourceLinkProcessor()
        for link in links:
            link.url = processor.process(link.url)
            if link.url:
                page_links.append(link)

        return page_links


class RenMinScriptProcessor():

    source = 'renmin'

    def process(self, links):
        page_links = []
        processor = RenMinSourceLinkProcessor()
        for link in links:
            link.url = processor.process(link.url)
            if link.url:
                page_links.append(link)

        return page_links


class BITScriptProcessor():

    source = 'bit'

    def process(self, links):
        page_links = []
        processor = BITSourceLinkProcessor()
        for link in links:
            link.url = processor.process(link.url)
            if link.url:
                page_links.append(link)

        return page_links


class BeiHangScriptProcessor():

    source = 'beihang'

    def process(self, links):
        page_links = []
        processor = BeiHangSourceLinkProcessor()
        for link in links:
            link.url = processor.process(link.url)
            if link.url:
                page_links.append(link)

        return page_links
