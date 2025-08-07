import logging

logger = logging.getLogger(__name__)


def retry(times, exceptions):
    def decorator(func):
        def newfn(*args, **kwargs):
            logger.debug("Retries decorator start")
            attempt = 0
            while attempt < times:
                logger.debug("Retries attempt::: %s", attempt)
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    attempt += 1

            logger.debug("Retries decorator end")
            return func(*args, **kwargs)

        return newfn

    return decorator
