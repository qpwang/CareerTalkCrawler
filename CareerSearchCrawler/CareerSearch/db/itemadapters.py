#-*- coding:utf-8 -*-
import re
import time
import hashlib
from datetime import datetime
from CareerSearch.utils import get_epoch_datetime
from BeautifulSoup import BeautifulSoup


class CareerItemAdapterFactory(object):

    @staticmethod
    def get_itemadapter(source=None):

        if source == TsingHuaItemAdapter.source:
            return TsingHuaItemAdapter()
        elif source == PekingItemAdapter.source:
            return PekingItemAdapter()
        elif source == RenMinItemAdapter.source:
            return RenMinItemAdapter()
        elif source == BITItemAdapter.source:
            return BITItemAdapter()

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
            item['content'] = _adapt_content_str(item.get('content'))
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
        if item.has_key('detail'):
            self._get_detail_info(item)
        if item.has_key('post_time'):
            item['post_time'] = self._get_post_time(item['post_time'])
        if item.has_key('content'):
            item['content'] = _adapt_content_str(item['content'])
        del item['detail']

        return item

    def _get_detail_info(self, item):
        infos = item['detail'].replace(u'\uff1a', ':').split(u'\n')
        for info in infos:
            if u'\u65f6\u95f4:' in info.replace(' ', '') and not item.has_key('begin_time'):
                item['begin_time'], item['end_time'] = self._get_begin_time(info.strip())
            elif u'\u5730\u70b9:' in info.replace(' ', '') and not item.has_key('address'):
                item['address'] = self._get_address(info.strip())

    def _get_address(self, address):
        return _adapt_colon_str(address, 1)

    def _get_begin_time(self, begin_time):
        begin_time = begin_time.replace(u'\xd0', '-').replace(' ', '')
        pattern = '([\\d]{4})?.?([\\d]{1,2}).([\\d]{1,2})[^0-9]*([\\d]{1,2}):([\\d]{2})(\-([\\d]{1,2}):([\\d]{2}))?'
        p = re.compile(pattern)
        r = p.search(begin_time)
        if r:
            year, month, day, hour, minute, has_end_time, end_hour, end_minute = r.groups()
            if not year:
                year = time.localtime().tm_year
            if u'\u665a' in begin_time or u'\u4e0b\u5348' in begin_time:
                if int(hour) < 12:
                    hour = int(hour) + 12

        begin_time = _adapt_datetime_str("%s-%s-%s %s:%s" % (year, month, day, hour, minute))
        end_time = 0
        if has_end_time:
            end_time = _adapt_datetime_str("%s-%s-%s %s:%s" % (year, month, day, end_hour, end_minute))
        return begin_time, end_time

    def _get_post_time(self, post_time):
        return _adapt_date_str(post_time)


class RenMinItemAdapter(CareerItemAdapter):

    source = 'renmin'

    def adapt(self, item):
        super(RenMinItemAdapter, self).adapt(item)
        if item.has_key('address'):
            item['address'] = self._get_address(item['address'])
        if item.has_key('begin_time'):
            item['begin_time'], item['end_time'] = self._get_begin_time(item['begin_time'])
        if item.has_key('content'):
            item['content'] = _adapt_content_str(item['content'])

        item['post_time'] = 0

        return item

    def _get_address(self, address):
        return _adapt_colon_str(address, 1)

    def _get_begin_time(self, begin_time):
        begin_time = begin_time.replace(u'\uff1a', ':').replace(u'\xd0', '-').replace(' ', '').replace(u'\xa0', '')
        pattern = '([\\d]{4})?.?([\\d]{1,2}).([\\d]{1,2})[^0-9]*([\\d]{1,2}):([\\d]{2})(\-([\\d]{1,2}):([\\d]{2}))?'
        p = re.compile(pattern)
        r = p.search(begin_time)
        if r:
            year, month, day, hour, minute, has_end_time, end_hour, end_minute = r.groups()
            if not year:
                year = time.localtime().tm_year
            if u'\u665a' in begin_time or u'\u4e0b\u5348' in begin_time:
                if int(hour) < 12:
                    hour = int(hour) + 12

        begin_time = _adapt_datetime_str("%s-%s-%s %s:%s" % (year, month, day, hour, minute))
        end_time = 0
        if has_end_time:
            end_time = _adapt_datetime_str("%s-%s-%s %s:%s" % (year, month, day, end_hour, end_minute))
        return begin_time, end_time


class BITItemAdapter(CareerItemAdapter):

    source = 'bit'

    def adapt(self, item):
        super(BITItemAdapter, self).adapt(item)
        if item.has_key('address'):
            item['address'] = self._get_address(item['address'])
        if item.has_key('begin_time'):
            item['begin_time'] = self._get_time(item['begin_time'])
        if item.has_key('end_time'):
            item['end_time'] = self._get_time(item['end_time'])
        if item.has_key('post_time'):
            item['post_time'] = self._get_time(item['post_time'].split('\r')[0])
        if item.has_key('content'):
            item['content'] = _adapt_content_str(item['content'])

        return item

    def _get_address(self, address):
        return _adapt_colon_str(address, 1)

    def _get_time(self, time_str):
        time_str = _adapt_colon_str(time_str, 1)
        time_str = _adapt_datetime_str(time_str)
        return time_str


def _adapt_content_str(content):
    soup = BeautifulSoup(content)
    for tag in soup():
        for attribute in ['style', 'class', 'lang']:
            del tag[attribute]
    return str(soup)


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

