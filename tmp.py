def check_spider_middleware(method):
    @functools.wraps(method)
    def wrapper(self, request, spider):
        msg = '%%s %s middleware step' % (self.__class__.__name__,)
        if self.__class__ in spider.middleware:
            spider.log(msg % 'executing', level=log.DEBUG)
            return method(self, request, spider)
        else:
            spider.log(msg % 'skipping', level=log.DEBUG)
            return None

    return wrapper

print 'test'
