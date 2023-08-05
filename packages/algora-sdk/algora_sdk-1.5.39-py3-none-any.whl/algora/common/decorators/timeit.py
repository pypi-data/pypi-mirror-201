import time
import logging

logger = logging.getLogger(__name__)


def timeit(fxn):
    def timed(*args, **kwargs):
        start = time.time()
        result = fxn(*args, **kwargs)
        end = time.time()

        logger.debug(
            f"func:{fxn.__name__} args:[{args}, {kwargs}] took: {end - start} sec"
        )
        return result

    return timed
