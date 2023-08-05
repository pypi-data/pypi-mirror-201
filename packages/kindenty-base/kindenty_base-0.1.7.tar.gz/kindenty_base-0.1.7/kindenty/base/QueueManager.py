import queue
from multiprocessing.managers import BaseManager

from kindenty.base.ExceptionModel import ArgsException


class Data:
    keys = []
    values = []

    def put(self, k, v):
        self.keys.append(k)
        self.values.append(v)

    def get(self, k):
        if not isinstance(k, (str, int)):
            raise ArgsException('参数错误')
        if isinstance(k, str):
            i = self.keys.index(k)
            return self.values[i]
        if isinstance(k, int):
            return self.values[k]

    def remove(self, k):
        i = self.keys.index(k)
        self.values.pop(i)
        self.keys.remove(k)

    def keys(self):
        return self.keys

    def values(self):
        return self.values


class Master(BaseManager):
    workerRegisterListQueue = queue.Queue()
    realMarketDataQueue = {}
    finishSharesCodeQueue = queue.Queue()
    submitOrderQueue = queue.Queue()
    cancelOrderQueue = queue.Queue()
    testMainOrderQueue = queue.Queue()
    sharesSubscribeQueue = queue.Queue()
    unSharesSubscribeQueue = queue.Queue()

    def __init__(self, ip: bytes = b'127.0.0.1', port: int = 5000, password: bytes = b'123456'):
        Master.register('getSubmitOrder', callable=getSubmitOrderQueue)
        Master.register('getCancelOrder', callable=getCancelOrderQueue)
        Master.register('getRealMarketData', callable=getRealMarketDataQueue)
        Master.register('workerRegisterList', callable=getWorkerRegisterList)
        Master.register('getFinishSharesCode', callable=getFinishSharesCodeQueue)
        Master.register('realMarketData', callable=getRealMarketData)
        Master.register('getTestMainOrder', callable=getTestMainOrderQueue)
        Master.register('getSharesSubscribe', callable=getSharesSubscribeQueue)
        Master.register('getUnSharesSubscribe', callable=getUnSharesSubscribeQueue)
        self.registerRealMarket = dict()
        super().__init__(address=(ip, port), authkey=password)

    def getRegisterRealMarketQueue(self, key):
        if key not in Master.realMarketDataQueue.keys():
            queue = self.getRealMarketData(key)
            self.registerRealMarket[key] = queue
        return self.registerRealMarket.get(key)


def getTestMainOrderQueue():
    return Master.testMainOrderQueue


def getRealMarketData():
    return Master.realMarketDataQueue


def getRealMarketDataQueue(sharesCode):
    if sharesCode not in Master.realMarketDataQueue.keys():
        Master.realMarketDataQueue[sharesCode] = queue.Queue()
    return Master.realMarketDataQueue[sharesCode]


def getFinishSharesCodeQueue():
    return Master.finishSharesCodeQueue


def getWorkerRegisterList():
    return Master.workerRegisterListQueue


def getSubmitOrderQueue():
    return Master.submitOrderQueue


def getCancelOrderQueue():
    return Master.cancelOrderQueue


def getSharesSubscribeQueue():
    return Master.sharesSubscribeQueue


def getUnSharesSubscribeQueue():
    return Master.unSharesSubscribeQueue


class Worker(BaseManager):
    def __init__(self, ip: bytes = b'127.0.0.1', port: int = 5000, password: bytes = b'123456'):
        Worker.register('getSubmitOrder')
        Worker.register('getRealMarketData')
        Worker.register('getCancelOrder')
        Worker.register('workerRegisterList')
        Worker.register('getFinishSharesCode')
        Worker.register('getTestMainOrder')
        Worker.register('getSharesSubscribe')
        Worker.register('getUnSharesSubscribe')
        self.registerRealMarket = dict()
        super().__init__(address=(ip, port), authkey=password)

    def getRegisterRealMarketQueue(self, key):
        if key not in Master.realMarketDataQueue.keys():
            queue = self.getRealMarketData(key)
            self.registerRealMarket[key] = queue
        return self.registerRealMarket.get(key)
