import time

from kindenty.base import log
from kindenty.base.BaseMethod import QueryMethod, SelectMethod
from kindenty.base.BaseModel import BaseModel
from kindenty.base.ExceptionModel import ModelException, ResultMultipleException
from kindenty.base.OrmField import IDField
from kindenty.databaseConfig import pool


class MysqlExecuteDriver:

    @staticmethod
    def insert(model, cursor, *args):
        try:
            mappings = model.__mode__.__mappings__
            idList = list(filter(lambda k: isinstance(mappings[k], IDField), mappings))
            if idList is None or len(idList) > 1:
                raise ModelException('%s model defined error' % model.name)
            idKey = idList[0]
            _id = cursor.lastrowid
            for m in args:
                setattr(m, idKey, _id)
                _id += 1
            return cursor
        except Exception as e:
            raise e

    @staticmethod
    def result(cursor, method):
        try:
            if not cursor:
                if isinstance(method, QueryMethod):
                    return []
                if isinstance(method, SelectMethod):
                    return None
            props = list(map(lambda p: p[0], cursor.description))
            rs = cursor.fetchall()

            if isinstance(method, QueryMethod):
                if len(rs) == 0:
                    return []
                if isinstance(method.result(), BaseModel):
                    return [method.result().setAttrs(props, x) for x in rs]
                else:
                    return [method.result(x[0]) for x in rs]
            if isinstance(method, SelectMethod):
                if len(rs) == 0:
                    return None
                if len(rs) > 1:
                    raise ResultMultipleException()
                if isinstance(method.result(), BaseModel):
                    return method.result().setAttrs(props, rs[0])
                else:
                    return method.result(rs[0][0])
        except Exception as e:
            raise e

    @staticmethod
    def execute(sql: list, *args):
        start = time.time()
        conn = pool.get()
        with conn.cursor() as cursor:
            log.debug('PARAMS: %s' % (str(args)))
            result = []
            try:
                for s in sql:
                    insert = False
                    if '?' in s:
                        s = s.replace('?', '%s')
                        insert = True
                    if len(args) == 1 and isinstance(args[0], dict):
                        keys = list(args[0].keys())
                        keys.sort(key=len, reverse=True)
                        for k in keys:
                            v = args[0][k]
                            if isinstance(v, (list, tuple)):
                                s = s.replace(':%s' % k, ','.join(map(lambda x: "'%s'" % x, v)))
                            else:
                                s = s.replace(':%s' % k, "%s" % v)
                    if insert:
                        cursor.execute(s, *args)
                    else:
                        cursor.execute(s)
                    result.append(cursor)
                return result[-1]
            except Exception as e:
                raise e
            finally:
                log.debug('SQL: %s , time：%s ms' % (sql, int((time.time()-start)*1000)))

    @staticmethod
    def transaction(fun):
        def wrapper(*args, **kwargs):
            try:
                conn = pool.get()
                conn.autocommit(False)
                conn.begin()
                result = fun(*args, **kwargs)
                conn.commit()
                return result
            except Exception as e:
                conn.rollback()
                raise e

        return wrapper

    @staticmethod
    def update(cursor):
        log.debug('ROWS: %d' % cursor.rowcount)
        return cursor


class SQLite3Driver:

    @staticmethod
    def insert(model, cursor, *args):
        try:
            mappings = model.__mode__.__mappings__
            idList = list(filter(lambda k: isinstance(mappings[k], IDField), mappings))
            if idList is None or len(idList) > 1:
                raise ModelException('%s model defined error' % model.name)
            idKey = idList[0]
            _id = cursor.lastrowid
            for m in args[::-1]:
                setattr(m, idKey, _id)
                _id -= 1
            return cursor
        except Exception as e:
            raise e

    @staticmethod
    def result(cursor, method):
        try:
            props = list(map(lambda p: p[0], cursor.description))
            rs = cursor.fetchall()

            if isinstance(method, QueryMethod):
                if len(rs) == 0:
                    return []
                if isinstance(method.result(), BaseModel):
                    return [method.result().setAttrs(props, x) for x in rs]
                else:
                    return [method.result(x[0]) for x in rs]
            if isinstance(method, SelectMethod):
                if len(rs) == 0:
                    return None
                if len(rs) > 1:
                    raise ResultMultipleException()
                if isinstance(method.result(), BaseModel):
                    return method.result().setAttrs(props, rs[0])
                else:
                    return method.result(rs[0][0])
        except Exception as e:
            raise e

    @staticmethod
    def execute(sql: list, *args):
        conn = pool.get()

        log.debug('SQL: %s' % sql)
        log.debug('PARAMS: %s' % (str(args)))
        result = []
        try:
            for s in sql:
                if len(args) == 1 and isinstance(args[0], dict):
                    for k, v in args[0].items():
                        if isinstance(v, (list, tuple)):
                            s = s.replace(':%s' % k, ','.join(map(lambda x: "'%s'" % x, v)))
                result.append(conn.execute(s, *args))
            return result[-1]
        except Exception as e:
            raise e

    @staticmethod
    def transaction(fun):
        def wrapper(*args, **kwargs):
            try:
                conn = pool.get()
                conn.execute('BEGIN TRANSACTION')
                result = fun(*args, **kwargs)
                conn.commit()
                return result
            except Exception as e:
                conn.rollback()
                raise e

        return wrapper

    @staticmethod
    def update(cursor):
        log.debug('ROWS: %d' % cursor.rowcount)
        return cursor


driver = MysqlExecuteDriver
