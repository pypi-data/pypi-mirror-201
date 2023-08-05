from kindenty.base.BaseModel import BaseModel
from kindenty.base.OrmField import IDField, StringField, FloatField, IntField, DateTimeField, BooleanField, \
    DateTimeMilliField, BigStrField, BigIntField


class Account(BaseModel):
    __table__ = 'account'
    id = IDField('id')
    category = StringField('category')
    account = StringField('account')
    accountType = StringField('account_type')
    balance = FloatField('balance')
    priority = StringField('priority')


class AccountPosition(BaseModel):
    __table__ = 'account_position'
    id = IDField('id')
    accountId = IntField('account_id')
    sharesCode = StringField('shares_code')
    enableCount = IntField('enable_count')


class RevokeOrderLog(BaseModel):
    __table__ = 'revoke_order_log'
    id = IDField('id')
    orderNo = StringField('order_no')
    time = DateTimeField('time')
    status = BooleanField('status')


class SharesQuotation(BaseModel):
    __table__ = 'shares_quotation'
    id = IDField('id')
    sharesCode = StringField('shares_code')
    lastPrice = FloatField('last_price')
    highPrice = FloatField('high_price')
    openPrice = FloatField('open_price')
    preClosePrice = FloatField('pre_close_price')
    time = StringField('time')
    createTime = DateTimeMilliField('create_time')


class SharesQuotationHistory(BaseModel):
    __table__ = 'shares_quotation_history'
    id = IDField('id')
    sharesCode = StringField('shares_code')
    lastPrice = FloatField('last_price')
    highPrice = FloatField('high_price')
    openPrice = FloatField('open_price')
    preClosePrice = FloatField('pre_close_price')
    time = StringField('time')
    createTime = DateTimeMilliField('create_time')


class Strategy(BaseModel):
    __table__ = 'strategy'
    id = IDField('id')
    name = StringField('name')
    accountId = IntField('account_id')
    sharesCode = StringField('shares_code')
    createTime = DateTimeField('create_time')
    json = BigStrField('json')
    version = StringField('version')
    enable = BooleanField('enable')
    stopTime = DateTimeField('stop_time')
    enableSell = IntField('enable_sell')


class TradeLog(BaseModel):
    __table__ = 'trade_log'
    id = IDField('id')
    strategyId = IntField('strategy_id')
    type = StringField('type')
    status = IntField('status')
    price = FloatField('price')
    power = IntField('power')
    avgPrice = FloatField('avg_price')
    orderCount = IntField('order_count')
    time = DateTimeField('time')
    tradeTime = DateTimeField('trade_time')
    orderNo = StringField('order_no')
    buyCount = IntField('buy_count')
    buyId = IntField('buy_id')


class TradeLogTest(BaseModel):
    __table__ = 'trade_log_test'
    id = IDField('id')
    strategyId = IntField('strategy_id')
    type = StringField('type')
    status = IntField('status')
    price = FloatField('price')
    power = IntField('power')
    avgPrice = FloatField('avg_price')
    orderCount = IntField('order_count')
    time = DateTimeField('time')
    tradeTime = DateTimeField('trade_time')
    orderNo = StringField('order_no')
    buyCount = IntField('buy_count')
    buyId = IntField('buy_id')
    groupId = IntField('group_id')


class YieldLog(BaseModel):
    __table__ = 'yield_log'
    id = IDField('id')
    sharesCode = StringField('shares_code')
    rate = FloatField('rate')
    groupId = IntField('group_id')


class OpenTradeLog(BaseModel):
    __table__ = 'open_trade_log'
    id = IDField('id')
    strategyId = IntField('strategy_id')
    date = StringField('date')
    logId = IntField('log_id')


class WorkerRegister(BaseModel):
    __table__ = 'worker_register'
    id = IDField('id')
    workerKey = StringField('worker_key')
    heartTime = DateTimeField('heart_time')


class HistoryData(BaseModel):
    __table__ = 'history_data'
    id = IDField('id')
    sharesCode = StringField('shares_code')
    date = StringField('date')
    time = StringField('time')
    open = FloatField('open')
    high = FloatField('high')
    low = FloatField('low')
    close = FloatField('close')
    preClose = FloatField('pre_close')
    volume = BigIntField('volume')
    turnover = BigIntField('turnover')
    dayVolume = BigIntField('day_volume')


class AccountAssetsLog(BaseModel):
    __table__ = 'account_assets_log'
    id = IDField('id')
    accountId = IntField('account_id')
    date = StringField('date')
    assets = FloatField('assets')
    shares = FloatField('shares')
    netValue = FloatField('net_value')
    preNetValue = FloatField('pre_net_value')


class ContrastLineData(BaseModel):
    __table__ = 'contrast_line_data'
    id = IDField('id')
    sharesCode = StringField('shares_code')
    date = StringField('date')
    close = FloatField('close')
    preClose = FloatField('pre_close')


class LoginUser(BaseModel):
    __table__ = 'login_user'
    id = IDField('id')
    loginName = StringField('login_name')
    pwd = StringField('pwd')
    userName = StringField('user_name')
    enable = IntField('enable')
    loginCount = IntField('login_count')
    updatePwd = IntField('update_pwd')
    createTime = DateTimeField('create_time')


class UserInvestmentLog(BaseModel):
    __table__ = 'user_investment_log'
    id = IDField('id')
    accountId = IntField('account_id')
    userId = IntField('user_id')
    assetsLogId = IntField('assets_log_id')
    transferAmount = FloatField('transfer_amount')
    shares = FloatField('shares')
    buyNetValue = FloatField('buy_net_value')
    time = DateTimeField('time')
