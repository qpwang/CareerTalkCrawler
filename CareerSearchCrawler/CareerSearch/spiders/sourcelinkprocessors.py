import re


class TsingHuaSourceLinkProcessor():

    base_url = 'http://career.tsinghua.edu.cn/docinfo/career/jyzpxx/zphDetail_zc.jsp?id==PttrLhP'

    def process(self, link):
        if link:
            feature_pattern = re.compile(r'&pre=(.*)|&pos=(.*)|&f=(.*)')
            feature_match = feature_pattern.search(link)
            if feature_match and link.startswith(self.base_url):
                link = link.replace(feature_match.group(), '')
            return link
        return None


class PekingSourceLinkProcessor():

    base_url = 'http://scc.pku.edu.cn/zpxx/zphd'

    def process(self, link):
        return link


class RenMinSourceLinkProcessor():

    base_url = 'http://career.ruc.edu.cn/article_show2.asp?id='

    def process(self, link):
        return link


class BITSourceLinkProcessor():

    base_url = 'http://job.bit.edu.cn/job/news/jobMeetingAll.jhtml?page='

    def process(self, link):
        return link


class BeiHangSourceLinkProcessor():

    base_url = 'http://career.buaa.edu.cn/website/zphxx/'

    def process(self, link):
        return link


class USTBSourceLinkProcessor():

    base_url = 'http://job.ustb.edu.cn/accms/sites/jobc/zhaopinhuixinxi-content.jsp?contentId='

    def process(self, link):
        return link
