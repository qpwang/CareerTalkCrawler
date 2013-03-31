import MySQLdb
import string
from scheduler import prepare_link_item, get_last_crawl_limit, get_priority_limit
from settings import DB_CONFIG

_link_table = 'links'
_DEFAULT_LINK_BATCH_SIZE = 30

class MySQLdbWrapper:

    conn = None

    def connect(self):
        self.conn = MySQLdb.connect(DB_CONFIG['host'], DB_CONFIG['user'], DB_CONFIG['password'], DB_CONFIG['db'])
        self.conn.set_character_set('utf8')

    def cursor(self):
        try:
            if not self.conn:
                self.connect()
            return self.conn.cursor()
        except MySQLdb.OperationalError:
            self.connect()
            return self.conn.cursor()

_db = MySQLdbWrapper()


def get_links(source, pendings):
    size_limit = max(_DEFAULT_LINK_BATCH_SIZE - pendings, 0)
    if size_limit == 0:
        return None

    try:
        cursor = _db.cursor()

        crawl_limit = str(get_last_crawl_limit())
        priority_limit = get_priority_limit()

        #remove the distributed links(last_crawl=2) avoid duplicate
        sql = 'SELECT link,id FROM ' + _link_table + ' WHERE source = %s AND last_crawl < %s AND last_crawl <> 2 AND priority <= %s ORDER BY ABS(priority) ASC, last_crawl ASC limit %s'
        cursor.execute(sql, (source, crawl_limit, priority_limit, size_limit))
        result = cursor.fetchall()
        id_set = [str(tup[1]) for tup in result]
        #update last_crawl to 2 (2: the distributed links)
        if id_set:
            update_sql = 'UPDATE ' + _link_table + ' SET last_crawl = %s WHERE id in (%s)' % ('2', ','.join(id_set))
            cursor.execute(update_sql)
        _db.conn.commit()
        return result
    except MySQLdb.Error, e:
        print e
    finally:
        cursor.close()


def update_links(status_list):
    try:
        cursor = _db.cursor()

        for item in status_list:
            insert_item = prepare_link_item(item, cursor, True)
            update_item = prepare_link_item(item, cursor, False)

            sql = 'INSERT INTO ' + _link_table + '(' + string.join(insert_item.keys(), ',') + \
                  ') values (' + string.join(['%s'] * len(insert_item.keys()), ',') + \
                  ') ON DUPLICATE KEY UPDATE ' + string.join([key + '=%s' for key in update_item.keys() if update_item[key]], ',')
            values = [insert_item[key] for key in insert_item.keys()] + [update_item[key] for key in update_item.keys() if update_item[key]]

            cursor.execute(sql, tuple(values))
            _db.conn.commit()

    except MySQLdb.Error, e:
        print e
    finally:
        cursor.close()
