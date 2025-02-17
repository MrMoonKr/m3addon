import sys
import os
import logging
import importlib.util


is_blender = importlib.util.find_spec('bpy') is not None


def create_logger():
    """
        전역 로그 객체 반환

        Returns:
            Logger: 전역 로그 객체
    """
    m3log = logging.getLogger('m3addon')
    m3log.setLevel(logging.DEBUG)
    form = logging.Formatter(
        fmt='%(asctime)-15s,%(msecs)-3d %(levelname)-6s %(filename)s:%(lineno)s %(message)s'
    )

    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(form)
    m3log.addHandler(console_handler)

    fname = os.path.join(os.path.dirname(__file__), 'logs', 'output.log')
    if is_blender:
        try:
            os.makedirs(os.path.dirname(fname), exist_ok=True)
            file_handler = logging.FileHandler(fname, mode='w')
            m3log.addHandler(file_handler)
        except PermissionError:
            pass

    return m3log


mlog = create_logger()
"""
    전역 로그 객체
"""
