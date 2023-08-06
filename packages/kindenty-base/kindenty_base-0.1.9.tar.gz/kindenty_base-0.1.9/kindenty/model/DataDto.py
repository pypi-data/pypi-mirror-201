from kindenty.base.BaseModel import BaseModel, ListType

from kindenty.model.DatabaseModel import Account


class AccountTradeLogDto(BaseModel):
    __slots__ = (
        'account', 'accountType', 'id', 'strategyId', 'type', 'status', 'price', 'power', 'avgPrice', 'orderCount',
        'time',
        'tradeTime', 'orderNo', 'buyCount', 'buyId')


class PriceDto(BaseModel):
    __slots__ = ('price', 'power')


class OrderBaseDto(BaseModel):
    __slots__ = ('buyPrice', 'buyCount', 'power', 'logId')


class SharesDto(BaseModel):
    __slots__ = (
        'fallX', 'buyN', 'growthRatio', 'buyM', 'buyCountQ', 'riseY', 'incrementA', 'sinkDayW', 'price', 'spRatio',
        'spTimes', 'intervalRatio', 'maxSell', 'volatility', 'sharesCode', 'intervalRatioX', 'intervalRatioY',
        'finalPrice', 'priceInterval', 'correctRatioN')


class SharesDto130(BaseModel):
    __slots__ = (
        'fallX', 'buyN', 'growthRatio', 'buyM', 'riseY', 'maxPrice', 'curPrice', 'sharesCode', 'maxSell')


class SharesDto140(BaseModel):
    __slots__ = (
        'riseY', 'sellN', 'sharesCode', 'price', 'total', 'curPower', 'growthRatio', 'maxSell')


class StrategyDto(BaseModel):
    __slots__ = ('version', 'operation', 'accounts', 'strategies', 'name', 'sharesCodes', 'sellStatus')

    accounts = ListType(Account)
    strategies = ListType(SharesDto)


class SubmitOrderDto(BaseModel):
    __slots__ = ('accountType', 'account', 'sharesCode', 'tradeSide', 'priceType', 'priceValue', 'buyCount', 'logId')


class CancelOrderDto(BaseModel):
    __slots__ = ('accountType', 'account', 'orderNo', 'logId')


class RealMarketData(BaseModel):
    __slots__ = (
        'stopMark', 'symbol', 'highPrice', 'lastPrice', 'time', 'perAssurescaleValue', 'openPrice', 'preClosePrice',
        'assureEnbuyBalance', 'upperLimit', 'lowerLimit', 'change', 'bailBalance')


class YieldDataDto(BaseModel):
    __slots__ = ('sharesCode', 'buyAmount', 'sellAmount')


class AssistDto(BaseModel):
    __slots__ = ('sharesCode', 'balance', 'enableCount', 'buyAmount', 'buyCount', 'sellAmount', 'sellCount')


class UserInvestmentDto(BaseModel):
    __slots__ = ('id', 'time', 'userName', 'amount', 'shares', 'netValue')


class InvestmentYeildDetailDto(BaseModel):
    __slots__ = ('time', 'amount', 'shares', 'buyNetValue', 'yieldRate', 'profit')


class UserAccountInfo(BaseModel):
    __slots__ = ('userName', 'totalAssets', 'totalShares', 'totalProfit', 'yieldRate')


class SellStatusDto(BaseModel):
    __slots__ = ('sharesCode', 'startCount', 'stopCount', 'version')
