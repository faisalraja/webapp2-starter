import inspect
import logging
import gevent
from peewee import SqliteDatabase
import sys
import config


def background_service():
    """Placeholder only for demo
    :return:
    """
    while 1:
        # logging.debug('Background Counter: {}'.format(ctr))
        gevent.sleep(1)


def get_db():
    """Get Application Database
    :return: DB
    """
    global DB
    if DB is None:
        DB = SqliteDatabase(config.db)

    return DB


def get_members_by_parent(module, parent):
    """Get all models that extends BaseModel
    :return:
    """
    return dict(member
                for member in inspect.getmembers(sys.modules[module if type(module) is str else module.__name__],
                                                 lambda c: inspect.isclass(c) and c.__base__ is parent))