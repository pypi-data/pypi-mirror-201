from time import ctime

from MALDIpy import __version__


def run():
    cur_time = ctime()
    text = f"""
    # MALDIpy
    
    version {__version__} ({cur_time} +0800)
    """
    print(text)
