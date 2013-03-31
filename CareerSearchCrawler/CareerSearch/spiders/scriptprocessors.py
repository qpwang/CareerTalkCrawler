from CareerSearch.spiders.sourcelinkprocessors import TsingHuaSourceLinkProcessor, PekingSourceLinkProcessor


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
