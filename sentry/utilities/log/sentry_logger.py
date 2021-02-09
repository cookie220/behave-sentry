import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def logging_decorator(fn):
    def func(*args, **kwargs):
        logger.info('function name is %s and input parameters is : (%s, %s)', args, kwargs)
        return fn(*args, **kwargs)

    return func

