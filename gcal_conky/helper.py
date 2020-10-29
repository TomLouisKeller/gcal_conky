import os


def get_current_location():
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_absolute_path(filename: str):
    if filename.startswith('/'):
        # print("root -> ", filename)
        return filename
    elif filename.startswith('~/'):
        # print("home -> ", filename)
        return filename
    elif filename.startswith('../'):
        # print("../ -> ", filename)
        return os.path.join(get_current_location(), filename)
    else:
        # print("relative ->  ", filename)
        return os.path.join(get_current_location(), "../", filename)


def get_logger(inpath="tmp", file_name_prefix=""):
    from datetime import datetime
    import logging
    import sys

    if file_name_prefix != "":
        file_name_prefix += "-"

    logging_path = "{path}/{prefix}{now}.log".format(path=inpath, prefix=file_name_prefix, now=str(datetime.now()))
    level = logging.DEBUG
    format = '%(asctime)s  - %(pathname)s:%(lineno)s -  %(message)s'
    # format = '%(asctime)s -  %(message)s'

    format = logging.Formatter(format)
    logger = logging.RootLogger(level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(format)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(logging_path)
    file_handler.setFormatter(format)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)

    return logger


def print_to_file(output_file_path, content: list):
    file = open(output_file_path, "w")
    for line in content:
        file.write(line + "\n")
    file.close()
