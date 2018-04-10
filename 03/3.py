import logging

def log_this(logo,level,form):
    def decorated(to_be_decorated):
        def wrapper(*args, **kwargs):
            logging.basicConfig(format="",level=level)
            s = args
            if 'd' in kwargs:
                s = s + (f'd={kwargs["d"]}',)
            if 'c' in kwargs:
                s = s + (f'c={kwargs["c"]}',)
            logo.info('logger.info('+form,to_be_decorated.__name__,s,to_be_decorated(*args, **kwargs)+")")
            return ""
        return wrapper
    return decorated
 
 
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
 
@log_this(logger, logging.INFO, '%s: %s -> %s')
def my_func(a, b, c=None, d=False):
    return 'Wow!'
my_func(1, 2, d=True)