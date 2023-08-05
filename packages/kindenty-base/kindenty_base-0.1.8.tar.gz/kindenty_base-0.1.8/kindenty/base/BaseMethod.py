from typing import Any


class QueryMethod:
    __slots__ = ('sql', 'result')

    def __init__(self, sql: str, result: Any):
        self.sql = sql
        self.result = result


class SelectMethod:
    __slots__ = ('sql', 'result')

    def __init__(self, sql: str, result):
        self.sql = sql
        self.result = result


class UpdateMethod:
    __slots__ = ('sql', 'params')

    def __init__(self, *sql):
        self.sql = sql
