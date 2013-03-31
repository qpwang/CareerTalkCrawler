from CareerSearch.settings import DB_CONFIG, QUEUE_CONFIG
from CareerSearch.db import career

career.config(DB_CONFIG['host'], DB_CONFIG['user'], DB_CONFIG['password'], DB_CONFIG['db'])

career.init_queue(QUEUE_CONFIG['host'], QUEUE_CONFIG['port'], QUEUE_CONFIG['password'])
