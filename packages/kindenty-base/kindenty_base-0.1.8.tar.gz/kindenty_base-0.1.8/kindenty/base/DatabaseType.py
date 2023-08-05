from enum import Enum, unique

@unique
class DataType(Enum):
    int = 'INTEGER'
    text = 'TEXT'

    sqlite_str = 'CHARACTER'
    sqlite_float = 'DOUBLE'
    sqlite_date = 'CHARACTER(30)'

    mysql_str = 'VARCHAR'
    mysql_float = 'DECIMAL(18,6)'
    mysql_date = 'VARCHAR(30)'
    mysql_bigint = 'bigint'


class FieldType(object):
    __slots__ = ('str', 'int', 'float', 'boolean', 'datetime', 'bigStr','bigint')

    def __init__(self, **kw):
        self.str = kw.get('str', DataType.sqlite_str.value)
        self.int = kw.get('int', DataType.int.value)
        self.float = kw.get('float', DataType.sqlite_float.value)
        self.boolean = kw.get('boolean', DataType.int.value)
        self.datetime = kw.get('datetime', DataType.sqlite_date.value)
        self.bigStr = kw.get('bigStr', DataType.text.value)
        self.bigint = kw.get('bigint', DataType.int.value)


@unique
class DatabaseType(Enum):
    sqlite = FieldType()
    mysql = FieldType(str=DataType.mysql_str.value, int=DataType.int.value, float=DataType.mysql_float.value,
                      boolean=DataType.int.value, datetime=DataType.mysql_date.value, bigStr=DataType.text.value, bigint=DataType.mysql_bigint.value)



