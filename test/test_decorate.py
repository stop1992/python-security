import functools

def log(text):
    # def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print '%s %s' % (text, func.__name__)
        return func(*args, **kw)
    return wrapper
    # return decorator

@log('execute')
def now():
    print 'this is a date'

now()
print now.__name__

