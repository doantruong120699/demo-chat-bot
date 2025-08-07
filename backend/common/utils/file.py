import logging

logger = logging.getLogger(__name__)


def read_content_file_from_path(path):
    try:
        file_taken = open(path)
        content = file_taken.read()
        file_taken.close()
        return content
    except FileNotFoundError:
        logger.error(f"ERROR: file not found")
        return ""
