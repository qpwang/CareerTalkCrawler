from platform import node
from scrapy.settings.default_settings import COOKIES_ENABLED

if node() in ['ubuntu', 'localhost']:
    from settings_dev import *
elif node() in ['ct-182-140-141-11.ctappstore', ]:
    from settings_prod import *
else:
    raise Exception("node:%s isn't properly configured for development or production usage." % node())


BOT_NAME = 'CareerSearch'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['CareerSearch.spiders.impl']
NEWSPIDER_MODULE = 'CareerSearch.spiders'

DEFAULT_ITEM_CLASS = 'CareerSearch.items.AppItem'
USER_AGENT = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.354.0 Safari/533.3'

ITEM_PIPELINES = ['CareerSearch.pipeline.CareerItemAdapterPipeline',
                  'CareerSearch.pipeline.CareerItemStorePipeline',
                  #'CareerSearch.pipeline.CareerItemQueueImagePipeline'
                  ]

EXTENSIONS = {'scrapy.webservice.WebService': None,
              'scrapy.telnet.TelnetConsole': None, }

DOWNLOADER_MIDDLEWARES = {'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': None, }

#DOWNLOAD_DELAY = 3

SPIDER_MIDDLEWARES = {
    'CareerSearch.middleware.HttpErrorMiddleware': 700,
    'scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware': None, }

DATA_DIR = '/tmp'

LOG_ENABLED = True
LOG_LEVEL = 'ERROR'
LOG_FILE = 'log.txt'

DEFAULT_REQUEST_HEADERS = {'Accept-Language': 'en'}

TELNETCONSOLE_ENABLED = True

COOKIES_ENABLED = True
