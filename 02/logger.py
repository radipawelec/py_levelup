
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@log_this(logger, level=logging.INFO, format='%s: %s -> %s')
def my_func(a, b, c=None, d=False):
    return 'Wow!'