#-*- coding:utf-8 -*-
import re
import hashlib
from datetime import datetime
from CareerSearch.utils import get_epoch_datetime
from BeautifulSoup import BeautifulSoup


class CareerItemAdapterFactory(object):

    @staticmethod
    def get_itemadapter(source=None):

        if source == TsingHuaItemAdapter.source:
            return TsingHuaItemAdapter()

        return None


class CareerItemAdapter(object):

    def adapt(self, item):
        if item.has_key('content') and len(item['content']) > 0:
            item['content_md5'] = self._get_content_md5(str([item['content']]))

    def _get_content_md5(self, content):
        content_md5 = hashlib.md5(content).hexdigest()
        return content_md5


class TsingHuaItemAdapter(CareerItemAdapter):

    source = 'tsinghua'

    def adapt(self, item):
        super(self.__class__, self).adapt(item)
        if item.has_key('address'):
            item['address'] = item['address'].strip()
        if item.has_key('begin_time'):
            item['begin_time'] = _adapt_datetime_str(item.get('begin_time').replace(u'\xa0\xa0', ' '))
        if item.has_key('post_time'):
            item['post_time'] = self._get_post_time(item.get('post_time'))
        else:
            item['post_time'] = get_epoch_datetime()
        if item.has_key('content'):
            item['content'] = self._get_content(item.get('content'))
        item['end_time'] = 0
        return item

    def _get_post_time(self, post_time):
        post_time = post_time.split(u'\uff1a')[1].split(u'\u3011')[0].strip()
        return _adapt_date_str(post_time)

    def _get_content(self, content):
        soup = BeautifulSoup(content)
        for tag in soup():
            for attribute in []:
                del tag[attribute]
        return str(soup)


class PekingItemAdapter(CareerItemAdapter):

    source = 'peking'

    def adapt(self, item):
        super(PekingItemAdapter, self).adapt(item)
        if item.has_key('address'):
            item['address'] = item['address']

def _adapt_date_str(date_str):
    if not date_str:
        return None;
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return get_epoch_datetime(date)


def _adapt_datetime_str(datetime_str):
    if not datetime_str:
        return None;
    date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    return get_epoch_datetime(date)


def _adapt_colon_str(colon_str, index):
    if u'：' in colon_str:
        return colon_str.split(u'：')[index].strip()
    elif ':' in colon_str:
        return colon_str.split(':')[index].strip()
    else:
        return colon_str


def _adapt_desc_str(desc_str):
    if not desc_str:
        return None
    soup = BeautifulSoup(desc_str)
    desc = soup.getText('\n')
    desc = __strip(desc)
    desc = __removeDuplicated(desc)
    desc = __cutTail(desc)
    return desc


def __strip(desc):
        result = ''
        p1 = re.compile(r'[ ]{2,}'); p2 = re.compile(ur'[-_=　—]{3,}'); p3 = re.compile(r'[\n]{3,}')
        lines = desc.split('\n')
        lm = len(lines) - 1
        for i in range(0, lm + 1):
            line = lines[i]
            line = line.strip(u' \t\r\n　')
            line = p1.sub('', line)
            line = p2.sub('\n', line)
            if i < lm:
                line += '\n'
            result += line
        result = p3.sub('\n\n', result)
        return result.strip('\n')


def __removeDuplicated(desc):
        result = ''
        lines = desc.split('\n')
        lm = len(lines) - 1
        for i in range(0, lm + 1):
            line = lines[i]
            if i > 0 and line == lines[i - 1]:
                continue
            segs = line.split(' ')
            if len(segs) % 2 == 0:
                mid = len(segs) / 2
                seg1 = ' '.join(segs[0:mid]); seg2 = ' '.join(segs[mid:]);
                if seg1 == seg2:
                    line = seg1
            if i < lm:
                line += '\n'
            result += line
        return result


def __cutTail(desc):
        result = desc.strip('\n')
        if result[-2:] == u'\u6536\u8d77':
            result = result[:-2].strip('\n')
        if result[-12:] == u'\u8be5\u5e94\u7528\u6765\u81ea\u667a\u6c47\u4e91\u5e94\u7528\u5e02\u573a':
            result = result[:-12]
        return result.strip('\n')

