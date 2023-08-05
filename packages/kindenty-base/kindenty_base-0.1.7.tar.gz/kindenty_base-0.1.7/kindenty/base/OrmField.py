from decimal import Decimal
from kindenty.databaseConfig import type

from kindenty.base.DatabaseType import DatabaseType
from datetime import datetime
import time


class Field(object):

    def __init__(self, name, column_type, objFun, valueFun=None):
        self.name = name
        self.columnType = column_type
        self.parseToObj = objFun
        if valueFun is None:
            valueFun = objFun
        self.parseToValue = valueFun

    def __str__(self):
        return '<%s:%s-%s>' % (self.__class__.__name__, self.name, self.columnType)


class IDField(Field):

    def __init__(self, name):
        super(IDField, self).__init__(name, '%s NOT NULL PRIMARY KEY %s ' % (
            type.value.int, 'AUTO_INCREMENT' if type == DatabaseType.mysql else 'AUTOINCREMENT'),
                                      lambda x: int(x))


class StringField(Field):

    def __init__(self, name, len: int = 100):
        super(StringField, self).__init__(name, '%s(%d)' % (type.value.str, len),
                                          lambda x: str(x) if x is not None else None)


class EnumField(Field):
    def __init__(self, name):
        super(EnumField, self).__init__(name, type.value.str, lambda x: str(x) if x is not None else None)


class IntField(Field):

    def __init__(self, name):
        super(IntField, self).__init__(name, type.value.int, lambda x: int(x) if x is not None else None)


class BigIntField(Field):

    def __init__(self, name):
        super(BigIntField, self).__init__(name, type.value.bigint, lambda x: int(x) if x is not None else None)


class FloatField(Field):

    def __init__(self, name):
        super(FloatField, self).__init__(name, type.value.float,
                                         lambda x: Decimal(str(x)).quantize(Decimal('0.000000')) if x is not None else None,
                                         lambda x: float(x.quantize(Decimal('0.000000'))) if x is not None else None)


class BooleanField(Field):

    def __init__(self, name):
        super(BooleanField, self).__init__(name, type.value.boolean, lambda x: int(x) if x is not None else None)


class DateTimeField(Field):

    def __init__(self, name):
        super(DateTimeField, self).__init__(name, type.value.datetime,
                                            lambda x: datetime.strptime(x,
                                                                        '%Y-%m-%d %H:%M:%S') if x is not None else None,
                                            lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if x is not None else None)
class DateTimeMilliField(Field):

    def __init__(self, name):
        super(DateTimeMilliField, self).__init__(name, type.value.datetime,
                                            lambda x: datetime.strptime(x,
                                                                        '%Y-%m-%d %H:%M:%S.%f') if x is not None else None,
                                            lambda x: x.strftime('%Y-%m-%d %H:%M:%S.%f') if x is not None else None)


class BigStrField(Field):

    def __init__(self, name):
        super(BigStrField, self).__init__(name, type.value.bigStr, lambda x: str(x) if x is not None else None)


if __name__ == '__main__':
    # print(time.time().strftime('%Y-%m-%d %H:%M:%S'))
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(None)))
