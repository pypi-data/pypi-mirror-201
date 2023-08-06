
from kindenty.base.BaseMethod import QueryMethod, UpdateMethod, SelectMethod
from kindenty.base.DatabaseDriver import driver

from kindenty.base.ExceptionModel import ArgsException
from kindenty.base.OrmField import IDField



class DaoMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if cls.__name__ == 'BaseDao':
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, (QueryMethod, UpdateMethod, SelectMethod)):
                mappings[k] = v
        for k, v in mappings.items():
            attrs.pop(k)
            if isinstance(v, (QueryMethod, SelectMethod)):
                attrs[k] = lambda self, param={}, method=v: driver.result(driver.execute([method.sql], param), method)
            elif isinstance(v, UpdateMethod):
                attrs[k] = lambda self, param={}, sql=v.sql: driver.update(driver.execute([*sql], param))
        attrs['insert'] = lambda self, models=list: driver.update(
            driver.insert(self, driver.execute(*self.__insert__(models)), *models))
        attrs['create'] = lambda self: driver.execute(*self.__create__())
        attrs['queryAll'] = lambda self: driver.result(driver.execute(*self.__query_all__()),
                                                       QueryMethod('', self.__mode__))
        attrs['__mappings__'] = mappings

        return type.__new__(cls, name, bases, attrs)


class BaseDao(dict, metaclass=DaoMetaclass):

    def __create__(self):
        fields = []
        for k, v in self.__mode__.__mappings__.items():
            fields.append('%s %s' % (v.name, v.columnType))
        sql = 'CREATE TABLE IF NOT EXISTS %s (%s)' % (self.__mode__.__table__, ','.join(fields))
        return [sql], []

    def __insert__(self, models: list):
        if models is None or len(models) == 0:
            raise ArgsException('%s model defined error' % self.name)
        fields = []
        params = []
        args = []
        prop = []
        for k, v in self.__mode__.__mappings__.items():
            if isinstance(v, IDField):
                continue
            fields.append(v.name)
            params.append('?')
            prop.append(k)
        values = []
        for m in models:
            values.append('(%s)' % ','.join(params))
            for k, v in self.__mode__.__mappings__.items():
                if isinstance(v, IDField):
                    continue
                args.append(v.parseToValue(getattr(m, k)))
        sql = 'insert into %s (%s) values %s' % (self.__mode__.__table__, ','.join(fields), ','.join(values))
        return [sql], args

    def __query_all__(self):
        fields = []
        for k, v in self.__mode__.__mappings__.items():
            fields.append('%s as %s' % (v.name, k))
        sql = 'select %s from %s' % (','.join(fields), self.__mode__.__table__)
        return [sql], []


def transaction(fun):
    return driver.transaction(fun)
