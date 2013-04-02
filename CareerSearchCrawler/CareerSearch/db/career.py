#-*- coding:utf-8 -*-
import string
import MySQLdb
from redis_queue import Queue
from CareerSearch.utils import log_error, get_epoch_datetime


_connections = {}
_conn = None
_table_dic = {}
_table = 'career_talk'
_link_monitor_table = 'link_monitor'

_queue = None
_queue_name = 'item_queue'


def config(host, user, password, db):
    global _conn
    _conn = _get_connection(host, user, password, db)


def init_queue(host, port, password):
    global _queue
    _queue = Queue(_queue_name, host=host, port=port, password=password)


def push_item_url(url):
    _queue.append(url)


def _get_connection(host, user, password, db):
    key = host
    conn = None
    if key in _connections:
        conn = _connections[key]
    else:
        conn = MySQLdb.connect(host, user, password, db)
        conn.set_character_set('utf8')
        _connections[key] = conn
    return conn


def remove_item(source_link, name):
    pass


def save_item(item, name):
    if not item:
        return
    try:
        cursor = _conn.cursor()

        #record last_crawl time
        item['add_time'] = get_epoch_datetime()
        item['update_time'] = get_epoch_datetime()

        _upsert_item(cursor, item)
        _conn.commit()
    except Exception, e:
        log_error(e)
    finally:
        cursor.close()


def _upsert_item(cursor, item):

    sql = "INSERT INTO " + _table + " (" + string.join(item.keys(), ',') + \
          ") values (" + string.join(["%s"] * len(item.keys()), ',') + \
          ") ON DUPLICATE KEY UPDATE " + string.join([key + "=%s" for key in item.keys() if item.get(key)], ',')
    values = [item.get(key) for key in item.keys()] + \
                 [item.get(key) for key in item.keys() if item.get(key)]

    cursor.execute(sql, tuple(values))


def report_link(source, catetory, link, description=''):
    try:
        cursor = _conn.cursor()

        insert_sql = "INSERT INTO %s (source, category, link, description, create_time) VALUES('%s', '%s', '%s', '%s', %s)" % \
                    (_link_monitor_table, source, catetory, link, description, get_epoch_datetime())
        cursor.execute(insert_sql)
        _conn.commit()
    except MySQLdb.Error, e:
        log_error(e)
    finally:
        cursor.close()

