from platform import node

if node() in ['ubuntu', 'localhost']:
    from settings_dev import *
elif node() in ['ct-182-140-141-11.ctappstore', ]:
    from settings_prod import *
else:
    raise Exception("node:%s isn't properly configured for development or production usage." % node())
