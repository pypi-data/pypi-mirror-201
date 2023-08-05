class ArgsException(Exception):

    def __init__(self, *args, **kw):
        super(ArgsException, self).__init__(*args, **kw)


class ModelException(Exception):

    def __init__(self, *args, **kw):
        super(ModelException, self).__init__(*args, **kw)


class ResultMultipleException(Exception):

    def __init__(self, *args, **kw):
        super(ModelException, self).__init__(*args, **kw)


class DataException(Exception):

    def __init__(self, *args, **kw):
        super(ModelException, self).__init__(*args, **kw)



