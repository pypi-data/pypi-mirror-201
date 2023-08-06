from kindenty.base.BaseDao import BaseDao, UpdateMethod, QueryMethod, SelectMethod, \
    transaction
from kindenty.model.DataDto import AccountTradeLogDto, RealMarketData, YieldDataDto, \
    AssistDto, UserInvestmentDto, SellStatusDto
from kindenty.model.DatabaseModel import Account, AccountPosition, RevokeOrderLog, \
    SharesQuotation, Strategy, TradeLog, OpenTradeLog, WorkerRegister, HistoryData, SharesQuotationHistory, \
    TradeLogTest, YieldLog, AccountAssetsLog, ContrastLineData, LoginUser, UserInvestmentLog


class AccountDao(BaseDao):
    __mode__ = Account

    deleteByAccount = UpdateMethod("delete from account where account=':account'")

    updateAccount = UpdateMethod(
        "update account set account_type=':accountType', category=':category',priority=':priority' where account=':account'")

    getByAccount = SelectMethod(
        "select id,account,category,account_type as accountType,balance,priority from account where account=':account' ",
        Account)

    getById = SelectMethod("select id,account,category,account_type as accountType,balance,priority from account where id=:id ",
                           Account)

    getAccountByTop1 = SelectMethod(
        "select id,category,account,account_type as accountType,balance,priority from account limit 1",
        Account)

    getAccount = SelectMethod(
        "select id,category,account,account_type as accountType,balance,priority from account where account=':account' and category=':category' and account_type=':accountType' ",
        Account)
    queryByIds = QueryMethod(
        "select id,category,account,account_type as accountType, balance,priority from account where id in (:ids) ",
        Account)

    queryCreditBySharesCode = QueryMethod("""
        select id,category,account,account_type as accountType,balance ,priority
        from account 
        where category='credit' and id in (select account_id from strategy where enable=1 and shares_code=':sharesCode')""",
                                          Account)
    updateBalance = UpdateMethod("update account set balance = ':balance' where id=:id")

    addBalance = UpdateMethod("update account set balance = balance + :balance where id=:id")

    addBalanceByStrategyId = UpdateMethod(
        "update account set balance = balance + :balance where id=(select account_id from strategy where id=:strategyId)  and exists (select id from trade_log where id=:id and status in (:status))")

    updateBalanceByTradeLog = UpdateMethod("""
        update account a,(select b.account_id,sum(a.order_count*a.price) amount from trade_log a 
                inner join strategy b on a.strategy_id=b.id where b.shares_code=':sharesCode' and a.`type`='BUY' and (status=0 or status is null or order_no is null) group by b.account_id) b
        set a.balance=a.balance+b.amount   
        where a.id=b.account_id     
    """)


class AccountPositionDao(BaseDao):
    __mode__ = AccountPosition
    # deleteAll = UpdateMethod("delete from account_position",
    #                          "DELETE FROM sqlite_sequence WHERE `name` = 'account_position'")
    deleteAll = UpdateMethod("truncate account_position")

    replaceSave = UpdateMethod("""
        replace into account_position(account_id,shares_code,enable_count)
        values(':accountId',':sharesCode',':enableCount')
    """)

    querySharesCodeByAccountId = QueryMethod(
        "select distinct  shares_code from account_position where account_id=:accountId", str)

    selectOneByAccountIdAndSharesCode = SelectMethod(
        "select id,account_id as accountId,shares_code as sharesCode,enable_count as enableCount from account_position where account_id=:accountId and shares_code=':sharesCode'",
        AccountPosition)

    updateEnableCountByAccountIdAndSharesCode = UpdateMethod(
        "update account_position set enable_count = enable_count+:num where account_id=:accountId and shares_code=':sharesCode'")

    updateEnableCountByAccountIdAndSharesCodeAndLogIdAndStatus = UpdateMethod(
        "update account_position set enable_count = enable_count+:num where account_id=:accountId and shares_code=':sharesCode' and exists (select id from trade_log where id=:id and status in (:status))")

    updateEnableCountByLogId = UpdateMethod("""
        update account_position a ,trade_log b , strategy c set enable_count = enable_count + b.order_count where a.shares_code=c.shares_code and a.account_id=c.account_id and c.id=b.strategy_id and b.`type`='BUY' and b.id = :logId
    """)

    updateEnableCountByTradeLog = UpdateMethod("""
        update account_position a ,(select b.account_id,b.shares_code,sum(a.order_count) `count` from trade_log a 
        inner join strategy b on a.strategy_id=b.id where b.shares_code=':sharesCode' and a.`type`='SELL' and (status=0 or status is null or order_no is null) group by b.account_id,b.shares_code) b
        set a.enable_count=a.enable_count+b.`count` 
        where a.account_id=b.account_id and a.shares_code=b.shares_code
    """)

    queryAssistData = SelectMethod("""
        select b.shares_code as sharesCode,a2.balance ,ap.enable_count as enableCount,
            ifnull(sum(case when a.`type`='BUY' and a.status in (0,2)  then a.order_count *a.price else 0 end),0) buyAmount,
            ifnull(sum(case when a.`type`='BUY' and a.status in (2) then a.order_count else 0 end),0) buyCount,
            ifnull(sum(case when a.`type` = 'SELL' and a.status in (2)  then  a.order_count*a.price end),0) sellAmount,
            ifnull(sum(case when a.`type`='SELL' and a.status in (0,2) then a.order_count else 0 end),0) sellCount
        from trade_log a
        inner join strategy b on a.strategy_id=b.id 
        inner join account_position ap on ap.shares_code = b.shares_code 
        inner join account a2 on a2.id = ap.account_id and a2.id = b.account_id 
        where b.shares_code=':sharesCode'
        group by b.shares_code,a2.balance ,ap.enable_count
    """, AssistDto)


class RevokeOrderLogDao(BaseDao):
    __mode__ = RevokeOrderLog
    selectOneByOrderNo = SelectMethod(
        "select id,order_no as orderNo,`time`,`status` from revoke_order_log where order_no=':orderNo' and `status` in (0,1) order by `time` desc limit 1",
        RevokeOrderLog)
    queryByOrderNo = QueryMethod(
        "select order_no from revoke_order_log where order_no in (:orderNos) and `status` in (0,1)", str)
    cleanHistoryData = UpdateMethod(
        "delete from revoke_order_log where date_format(now(),'%Y-%m-%d')>date_format(`time`,'%Y-%m-%d')")
    updateStatusByOrderNo = UpdateMethod("update revoke_order_log set `status`=:status where order_no=':orderNo'")

    deleteByOrderNo = UpdateMethod("delete from revoke_order_log where order_no = ':orderNo'")

    deleteByTodayBefore = UpdateMethod(
        "delete from revoke_order_log where date_format(now(),'%Y-%m-%d') > date_format(`time`,'%Y-%m-%d')")


class SharesQuotationDao(BaseDao):
    __mode__ = SharesQuotation

    deleteByTodayBefore = UpdateMethod(
        "delete from shares_quotation where date_format(now(),'%Y-%m-%d') > date_format(create_time,'%Y-%m-%d')")

    deleteBySharesCode = UpdateMethod("delete from shares_quotation where shares_code=':sharesCode'")

    cleanAll = UpdateMethod("delete from shares_quotation")


class SharesQuotationHistoryDao(BaseDao):
    __mode__ = SharesQuotationHistory

    insertSelect = UpdateMethod("""
        insert into shares_quotation_history(id,shares_code,last_price,high_price,open_price,pre_close_price,time,create_time) 
        select id,shares_code,last_price,high_price,open_price,pre_close_price,time,create_time 
        from shares_quotation where date_format(now(),'%Y-%m-%d') > date_format(create_time,'%Y-%m-%d')""")

    selectCount = SelectMethod(
        "select count(1) from shares_quotation_history where shares_code in (:sharesCodes) and last_price != 0 and date_format(create_time,'%Y-%m-%d') > ':startDate' and date_format(create_time,'%Y-%m-%d') <= ':endDate'", int)

    queryByLastpriceNotNone = QueryMethod("""
        select 0 as stopMark,shares_code as symbol,high_price as highPrice,last_price as lastPrice,
        date_format(create_time,'%Y-%m-%d') as time,open_price as openPrice,pre_close_price as preClosePrice
        from shares_quotation_history 
        where shares_code in (:sharesCodes) and last_price != 0 and open_price != 0 and pre_close_price != 0 and date_format(create_time,'%Y-%m-%d') > ':startDate' and date_format(create_time,'%Y-%m-%d') <= ':endDate'
        order by id limit :limit offset :offset""", RealMarketData)


class StrategyDao(BaseDao):
    __mode__ = Strategy

    enableByIds = UpdateMethod("update strategy set enable=1, stop_time=null where id in (:ids)")

    queryIdByKey = QueryMethod("""
        select max(id) from strategy where concat(account_id,',',shares_code,',',version) in (:keys)
    """, int)

    deleteBySharesCode = UpdateMethod("delete from strategy where shares_code=':sharesCode'")

    queryCountByEnableSell = QueryMethod("""
        select shares_code as sharesCode, version,sum(case when enable_sell=1 then 1 else 0 end) as startCount,sum(case when enable_sell=0 then 1 else 0 end) as stopCount
        from strategy 
        where shares_code like ':sharesCode'
        group by shares_code, version
        order by shares_code
    """, SellStatusDto)

    disable = UpdateMethod(
        "update strategy set enable=0,stop_time=date_format(now(),'%Y-%m-%d %H:%i:%S') where version=':version' and `name`=':name'")
    queryStrategyByNotSellAll = QueryMethod("""
        select a.id,a.`name`,a.account_id as accountId,a.shares_code as sharesCode,a.create_time as createTime,a.json,a.version,a.enable,a.enable_sell as enableSell
        from strategy a
        left outer join (select strategy_id,sum(`buy_count`) as ct from trade_log where `type` in ('BUY','MARGIN_BUY','DEBIT_BUY') and status in(1,2,3) group by strategy_id)  b on a.id=b.strategy_id
        left outer join (select strategy_id,sum(`buy_count`) as ct from trade_log where `type` in ('SELL','DEBIT_SELL','MARGIN_SELL') and status in(0,1,2,3) group by strategy_id)  c on a.id=c.strategy_id
        where ((b.ct-c.ct)>0 and a.enable=0) or enable=1 or (a.version='1.4' and a.enable_sell = 1)""", Strategy)

    disableByAccountIdAndSharesCodeAndVersion = UpdateMethod("""
        update strategy set enable=0,stop_time=date_format(now(),'%Y-%m-%d %H:%i:%S') 
        where concat(account_id,',',shares_code,',',version) in (:keys) and enable=1""")

    disableBySharesCode = UpdateMethod("""
        update strategy set enable=0,stop_time=date_format(now(),'%Y-%m-%d %H:%i:%S') 
        where shares_code = ':sharesCode' and enable=1 and version= ':version'
    """)

    queryBySharesCode = QueryMethod("""
        select a.id,a.`name`,a.account_id as accountId,a.shares_code as sharesCode,a.create_time as createTime,a.json,a.version,a.enable,a.enable_sell as enableSell,t.minPrice
        from strategy a
        left join (select strategy_id,min(price) as minPrice from trade_log 
                    where id not in (select buy_id from trade_log where `type` in ('SELL','DEBIT_SELL','MARGIN_SELL') and status in (0,1,2,3) and buy_id is not null)
                        and `type` in ('BUY','MARGIN_BUY','DEBIT_BUY') and status in(1,2,3) group by strategy_id) t on a.id=t.strategy_id
        left outer join (select strategy_id,sum(`buy_count`) as ct from trade_log where `type` in ('BUY','MARGIN_BUY','DEBIT_BUY') and status in(1,2,3) group by strategy_id)  b on a.id=b.strategy_id
        left outer join (select strategy_id,sum(`buy_count`) as ct from trade_log where `type` in ('SELL','DEBIT_SELL','MARGIN_SELL') and status in(0,1,2,3) group by strategy_id)  c on a.id=c.strategy_id
        where shares_code = ':sharesCode' and (((b.ct-ifnull(c.ct,0))>0 and a.enable=0) or enable=1 or (a.version='1.4' and a.enable_sell=1)) order by t.minPrice""",
                                    Strategy)

    queryBySharesCodeAndAccountId = QueryMethod("""
            select id,`name`,account_id as accountId,shares_code as sharesCode,create_time as createTime,json,version,enable,enable_sell as enableSell 
            from strategy
            where account_id=':accountId' and shares_code like ':sharesCode' and enable=1 and version=':version'
            union 
            select a.id,a.`name`,a.account_id as accountId,a.shares_code as sharesCode,a.create_time as createTime,a.json,a.version,a.enable,a.enable_sell as enableSell 
            from strategy a 
            inner join (select shares_code,max(id) id from strategy where enable=0  and version=':version' group by shares_code) s on a.shares_code = s.shares_code and a.id=s.id
            where a.account_id=':accountId' and a.shares_code like ':sharesCode' and a.shares_code  not in (select shares_code from strategy where enable=1  and version=':version')
    """, Strategy)

    getById = SelectMethod(
        "select id,`name`,account_id as accountId,shares_code as sharesCode,create_time as createTime,json,version,enable,enable_sell as enableSell from strategy where id=:id",
        Strategy)

    querySharesCodeByAccountId = QueryMethod("""
        select distinct shares_code
        from strategy
        where account_id=:accountId""", str)

    updateEnableSellBySharesCode = UpdateMethod(
        "update strategy set enable_sell=':status' where shares_code in (:sharesCodes) and version=':version'")

    updateEnableSellById = UpdateMethod(
        "update strategy set enable_sell=':status' where id=:strategyId")

    updateJsonBySharesCode = UpdateMethod("update strategy set json=':json' where shares_code=':sharesCode'")

    updateJsonById = UpdateMethod("update strategy set json=':json' where id=':id'")

    selectBySharesCodeAndEnable = QueryMethod("""
        select a.id,a.`name`,a.account_id as accountId,a.shares_code as sharesCode,a.create_time as createTime,a.json,a.version,a.enable,a.enable_sell as enableSell
        from strategy a 
        where a.shares_code=':sharesCode' and a.enable=1
    """, Strategy)

    countTodayUpdate = SelectMethod(
        "select count(1) from strategy where shares_code=':sharesCode' and version='1.2' and date_format(create_time,'%Y-%m-%d')=date_format(now(),'%Y-%m-%d')",
        int)

    selectBySharesCodeAndAccountIdAndEnable = SelectMethod("""
        select a.id,a.`name`,a.account_id as accountId,a.shares_code as sharesCode,a.create_time as createTime,a.json,a.version,a.enable,a.enable_sell as enableSell
        from strategy a 
        where a.shares_code=':sharesCode' and a.enable=:enable and a.account_id=:accountId and a.version=':version'
        order by a.id desc
        limit 1
    """, Strategy)


class OpenTradeLogDao(BaseDao):
    __mode__ = OpenTradeLog

    selectByStrategyIdAndDate = SelectMethod(
        "select id,strategy_id as strategyId,date,log_id as logId from open_trade_log where strategy_id=':strategyId' and date=':date'",
        OpenTradeLog)

    cleanAll = UpdateMethod("delete from open_trade_log")


class WorkerRegisterDao(BaseDao):
    __mode__ = WorkerRegister

    countWorker = SelectMethod(
        "select count(1) from worker_register where date_add(heart_time, interval 10 second) > now()", int)

    deleteExpire = UpdateMethod("delete from worker_register where date_add(heart_time, interval 10 second) < now()")

    updateHeartTime = UpdateMethod(
        "update worker_register set heart_time=date_format(now(),'%Y-%m-%d %H:%i:%S') where worker_key=':key'")


class TradeLogDao(BaseDao):
    __mode__ = TradeLog

    sumSellCountByStrategyId = SelectMethod("select ifnull(sum(buy_count),0) from trade_log where strategy_id=':strategyId' and `type` in ('SELL','DEBIT_SELL','MARGIN_SELL') and status in (2,3)", int)

    selectLatestByStrategyId = SelectMethod("""select id,strategy_id as strategyId,`type`,status,price,power,avg_price as avgPrice,`order_count` as orderCount,`buy_count` as buyCount,`time`,order_no as orderNo,buy_id as buyId,trade_time as tradeTime
        from trade_log
        where strategy_id=':strategyId' and `type` in ('SELL','DEBIT_SELL','MARGIN_SELL') and status in (2,3)
        order by id desc 
        limit 1
        """, TradeLog)

    selectSellCountByStrategyId = SelectMethod("""select ifnull(sum(buy_count), 0) from trade_log where strategy_id=':strategyId' and status in (2, 3) and `type` in ('SELL','DEBIT_SELL','MARGIN_SELL')""", int)

    selectOneByStrategyIdAndStatus = SelectMethod("""select id,strategy_id as strategyId,`type`,status,price,power,avg_price as avgPrice,`order_count` as orderCount,`buy_count` as buyCount,`time`,order_no as orderNo,buy_id as buyId,trade_time as tradeTime
        from trade_log
        where strategy_id=':strategyId' and `type` in ('SELL','DEBIT_SELL','MARGIN_SELL') and date_format(`time`,'%Y-%m-%d')=date_format(now(),'%Y-%m-%d') and status in (0, 1)
        limit 1
        """, TradeLog)

    selectByStrategyId = SelectMethod("""select id,strategy_id as strategyId,`type`,status,price,power,avg_price as avgPrice,`order_count` as orderCount,`buy_count` as buyCount,`time`,order_no as orderNo,buy_id as buyId,trade_time as tradeTime
        from trade_log
        where strategy_id=':strategyId' and `type` in ('BUY','MARGIN_BUY','DEBIT_BUY') and date_format(`time`,'%Y-%m-%d')=date_format(now(),'%Y-%m-%d') and status in (0, 1)
        order by id desc 
        limit 1
        """, TradeLog)

    deleteBySharesCode = UpdateMethod("delete from trade_log where strategy_id in (select id from strategy where shares_code = ':sharesCode')")

    cleanAll = UpdateMethod("delete from trade_log")

    cleanData = UpdateMethod(
        "delete from trade_log where date_format(now(),'%Y-%m-%d') > date_format(`time`,'%Y-%m-%d') and (status=0 or status is null or order_no is null)")

    cleanDataRegression = UpdateMethod(
        "delete from trade_log where  (status=0 or status is null or order_no is null) and strategy_id in (select id from strategy where shares_code = ':sharesCode')")

    queryTodayBuyLogByStrategyId = QueryMethod("""select id,strategy_id as strategyId,`type`,status,price,power,avg_price as avgPrice,`order_count` as orderCount,`buy_count` as buyCount,`time`,order_no as orderNo,buy_id as buyId,trade_time as tradeTime
        from trade_log
        where strategy_id =:id  and `type` in ('BUY','MARGIN_BUY','DEBIT_BUY') and date_format(`time`,'%Y-%m-%d')=date_format(now(),'%Y-%m-%d')
        order by `time` desc""", TradeLog)

    updateOrderNoAndStatusById = UpdateMethod(
        "update trade_log set `status`=:status where id=:id and `status` < :status",
        "update trade_log set order_no=':orderNo' where id=:id")

    getById = SelectMethod("""select id,strategy_id as strategyId,`type`,status,price,power,avg_price as avgPrice,`order_count` as orderCount,`buy_count` as buyCount,`time`,order_no as orderNo,buy_id as buyId,trade_time as tradeTime
        from trade_log
        where id=:id""", TradeLog)

    updateStatusAndBuyCountByOrderNo = UpdateMethod(
        "update trade_log set `status`=:status,buy_count=:buyCount,avg_price=:avgPrice,trade_time=':tradeTime',order_no=':orderNo' where id=:id")

    getByOrderNoAndStatus = SelectMethod("""select id,strategy_id as strategyId,`type`,status,price,power,avg_price as avgPrice,`order_count` as orderCount,`buy_count` as buyCount,`time`,order_no as orderNo,buy_id as buyId,trade_time as tradeTime
        from trade_log
        where order_no=':orderNo'""", TradeLog)

    deleteById = UpdateMethod("delete from trade_log where id=:id")

    queryByStatus = QueryMethod("""select c.account as account,c.account_type as accountType,a.id,a.strategy_id as strategyId,a.`type`,a.status,a.price,a.power,a.avg_price as avgPrice,a.`order_count` as orderCount,a.`buy_count` as buyCount,a.`time`,a.order_no as orderNo,a.buy_id as buyId,a.trade_time as tradeTime
        from trade_log a
        inner join strategy b on a.strategy_id=b.id
        inner join account c on b.account_id=c.id
        where a.status in (:status) and a.order_no is not null """, AccountTradeLogDto)

    selectOneByStrategyIdAndClosestPriceLog = QueryMethod("""select * from (
          select a.id,a.strategy_id as strategyId,a.`type`,a.status,a.price,a.power,a.avg_price as avgPrice,a.`order_count` as orderCount,a.`buy_count` as buyCount,a.`time`,a.order_no as orderNo,a.buy_id as buyId,
            (select ifnull(max(last_price),:highPrice)-:incA from shares_quotation where shares_code=b.shares_code and date_format(`create_time`,'%Y-%m-%d %H-%i-%S') >= date_format(a.`trade_time`,'%Y-%m-%d %H-%i-%S')) as highPrice
            from trade_log a
            inner join strategy b on a.strategy_id=b.id
            where a.strategy_id=:strategyId and a.`type` in ('BUY','MARGIN_BUY','DEBIT_BUY') and a.status in (2,3)
        ) c where :highPrice - :incA>=c.price and c.highPrice>=c.price
		order by c.price desc""", TradeLog)

    queryMarketableCountBySharesCode = SelectMethod("""select sum(buyCount) as `count`
        from (
        select ifnull(sum(a.buy_count),0) buyCount
        from trade_log a
        inner join strategy b on a.strategy_id=b.id
        where date_format(now(),'%Y-%m-%d')>date_format(a.`time`,'%Y-%m-%d') and a.`type` in ('BUY','MARGIN_BUY','DEBIT_BUY') and a.status in(1,2,3) and b.shares_code=':sharesCode'
        union all
        select ifnull(-sum(a.buy_count),0) buyCount
        from trade_log a
        inner join strategy b on a.strategy_id=b.id
        where a.`type` in ('SELL','DEBIT_SELL','MARGIN_SELL') and a.status in(0,1,2,3) and b.shares_code=':sharesCode'
        ) a""", int)

    queryNotSellOrderByStrategyIdAndLtCurPrice = QueryMethod("""select a.id,a.strategy_id as strategyId,a.`type`,a.status,a.price,a.power,a.avg_price as avgPrice,a.`order_count` as orderCount,a.`buy_count`-ifnull(b.buy_count,0) as buyCount,a.`time`,a.order_no as orderNo,a.buy_id as buyId
        from trade_log a
        left OUTER join (select buy_id,sum(case when status in (0,1) then order_count when status in (2,3) then buy_count end) as buy_count from trade_log where buy_id is not null and `type` in ('SELL','DEBIT_SELL','MARGIN_SELL') and status in(0,1,2,3) group by buy_id) b on a.id=b.buy_id
        where a.`type` in ('BUY','MARGIN_BUY','DEBIT_BUY') and a.status in(2,3) and a.strategy_id=':strategyId' and :curPrice>=a.avg_price and a.`buy_count`-ifnull(b.buy_count,0)>0
        order by a.avg_price""", TradeLog)

    deleteByBuyId = UpdateMethod("delete from trade_log where buy_id=:buyId")

    queryNotSellByStrategyIdAndGtCurPrice = QueryMethod("""select a.id,a.strategy_id as strategyId,a.`type`,a.status,a.price,a.power,a.avg_price as avgPrice,a.`order_count` as orderCount,a.`buy_count` as buyCount,a.`time`,a.order_no as orderNo,a.buy_id as buyId,a.trade_time as tradeTime
        from trade_log a
        where a.strategy_id in (select id from strategy where shares_code=':sharesCode' and version=':version') and  a.price >:curPrice and a.`type` in ('SELL','DEBIT_SELL','MARGIN_SELL') and a.status = 0 and a.order_no is not null and a.order_no not in (select order_no from revoke_order_log)
        order by a.price desc""", TradeLog)

    updateBuyIdById = UpdateMethod("update trade_log set buy_id = :buyId where id=:id")

    updateBuyIdIsNullByBuyId = UpdateMethod("update trade_log set buy_id = null where buy_id=:buyId")

    querySpTimes = QueryMethod("""select distinct date(`time`) as times
        from trade_log
        where date_format(now(),'%Y-%m-%d') > date_format(`time`,'%Y-%m-%d') and strategy_id=:strategyId
        order by 1 desc
        limit :spTimes""", str)

    queryCountByPriceAndDate = SelectMethod("""select count(1) as ct
        from trade_log
        where date_format(`time`,'%Y-%m-%d') in (:dates ) and price=:price and `status` in (2,3) and strategy_id=:strategyId""",
                                            int)
    statisticsRate = QueryMethod("""
        select b.shares_code as sharesCode,sum(c.buy_count*c.avg_price) buyAmount,sum(a.buy_count*a.avg_price) sellAmount
        from trade_log a 
        inner join strategy b on a.strategy_id=b.id 
        inner join trade_log c on a.buy_id=c.id and c.strategy_id = b.id 
        where b.shares_code in (:sharesCodes) and a.status = 2 and a.`type` = 'SELL'
        group by b.shares_code
    """, YieldDataDto)


class HistoryDataDao(BaseDao):
    __mode__ = HistoryData


class TradeLogTestDao(BaseDao):
    __mode__ = TradeLogTest

    insertSelectByTradeLog = UpdateMethod("""
        insert into trade_log_test(id,strategy_id,type,status,price,power,avg_price,order_count,time,trade_time,order_no,buy_count,buy_id,group_id)
        select id,strategy_id,type,status,price,power,avg_price,order_count,time,trade_time,order_no,buy_count,buy_id,:groupId 
        from trade_log 
        """)


class YieldLogDao(BaseDao):
    __mode__ = YieldLog

    selectMaxGroupId = SelectMethod("select ifnull(max(group_id),0) from yield_log", int)


class AccountAssetsLogDao(BaseDao):
    __mode__ = AccountAssetsLog

    selectCount = SelectMethod("select count(1) from account_assets_log", int)

    selectNewest = SelectMethod("""
        select id,account_id as accountId, `date` , assets, shares, net_value as netValue, pre_net_value as preNetValue
        from account_assets_log
        order by `date` desc 
        limit 1
    """, AccountAssetsLog)

    queryPageLog = QueryMethod("""
        select id,account_id as accountId, `date` , assets, shares, net_value as netValue, pre_net_value as preNetValue
        from account_assets_log
        order by `date` desc 
        limit :limit offset :offset
    """, AccountAssetsLog)

    queryLogByGtDate = QueryMethod("""
        select id,account_id as accountId, `date` , assets, shares, net_value as netValue, pre_net_value as preNetValue
        from account_assets_log
        where `date`>=':date' and `date` <= ':endDate'
        group by `date`
        order by `date`
        """, AccountAssetsLog)

    queryLogByBtDate = QueryMethod("""
        select `date`,assets, shares, net_value as netValue,pre_net_value as preNetValue
        from account_assets_log
        where `date` >= ':qStart' and `date` <= ':qEnd' 
        order by `date` desc
        """, AccountAssetsLog)

    sumShares = SelectMethod(
        "select ifnull(sum(shares),0) from account_assets_log where `date`<':date'", float)

    selectByDate = SelectMethod("""
        select id,account_id as accountId, `date` , assets, shares, net_value as netValue, pre_net_value as preNetValue
        from account_assets_log
        where `date` = ':date'
        """, AccountAssetsLog)

    selectByEtDate = SelectMethod("""
        select id,account_id as accountId, `date` , assets, shares, net_value as netValue, pre_net_value as preNetValue
        from account_assets_log
        where `date` < ':etDate' 
        order by `date` desc
        limit 1
        """, AccountAssetsLog)

    updateSharesByDate = UpdateMethod(
        "update account_assets_log set shares=:shares where `date`=':date' and account_id=:accountId")

    clearSharesByDate = UpdateMethod(
        "update account_assets_log set shares=0 where `date` in (:dates) and account_id=:accountId")

    updateAssetsAndNetValueById = UpdateMethod("update account_assets_log set assets=:assets, net_value=:netValue where id=:id")

class ContrastLineDataDao(BaseDao):
    __mode__ = ContrastLineData
    queryByDate = QueryMethod("""
        select `date`, shares_code as sharesCode , `close`, `pre_close` as preClose
        from contrast_line_data
        where `date` >= ':date'
        order by `date`
    """, ContrastLineData)

    deleteByDate = UpdateMethod(
        "delete from contrast_line_data where `date` >=':begin' and `date`<=':end' and shares_code = ':sharesCode'")

    selectMaxDate = SelectMethod("select max(`date`) from contrast_line_data where `date` >= ':date'", str)


class LoginUserDao(BaseDao):
    __mode__ = LoginUser

    selectByLoginName = SelectMethod("""
        select id, login_name as loginName, pwd, user_name as userName, enable, create_time as createTime, login_count as loginCount, update_pwd as updatePwd
        from login_user
        where login_name = ':loginName'
        """, LoginUser)

    addLoginCountByLoginName = UpdateMethod(
        "update login_user set login_count=login_count + 1 where login_name=':loginName'")

    queryByUserName = QueryMethod("""
        select id, login_name as loginName, pwd, user_name as userName, enable, create_time as createTime, login_count as loginCount, update_pwd as updatePwd
        from login_user
        where user_name like ':userName'
        """, LoginUser)

    updateEnableByLoginName = UpdateMethod("update login_user set enable=:enable where login_name=':loginName'")

    updatePwdByLoginName = UpdateMethod("update login_user set pwd=':newPwd' where login_name=':loginName'")

    updateUpdatePwdByLoginName = UpdateMethod(
        "update login_user set update_pwd=:updatePwd where login_name=':loginName'")

    queryByIds = QueryMethod("""
        select id, login_name as loginName, pwd, user_name as userName, enable, create_time as createTime, login_count as loginCount, update_pwd as updatePwd
        from login_user
        where id in (:ids)
    """, LoginUser)


class UserInvestmentLogDao(BaseDao):
    __mode__ = UserInvestmentLog

    queryLogByBtDate = QueryMethod("""
        select a.id, a.time, b.user_name as userName, TRUNCATE(a.transfer_amount,2) as amount, truncate(a.shares,2) as shares, truncate(a.buy_net_value,4) as netValue
        from user_investment_log a
        inner join login_user b on a.user_id = b.id
        where date_format(a.`time`, '%Y-%m-%d') >= ':qStart' and date_format(a.`time`, '%Y-%m-%d') <= ':qEnd' and a.account_id = :accountId and b.user_name like ':queryKey'
        order by a.`time` desc 
    """, UserInvestmentDto)

    deleteByIds = UpdateMethod("delete from user_investment_log where id in (:ids)")

    sumUserAmountByEtDate = SelectMethod("""
        select TRUNCATE(ifnull(sum(transfer_amount),0),2) from user_investment_log 
        where date_format(`time`, '%Y-%m-%d %H:%i:%S') <=':etDate' and assets_log_id is null
    """, float)

    queryLogByEtDate = QueryMethod("""
        select id, account_id as accountId, user_id as userId, assets_log_id as assetsLogId, TRUNCATE(transfer_amount,2) as transferAmount, shares, buy_net_value as buyNetValue, `time`
        from user_investment_log
        where date_format(`time`, '%Y-%m-%d %H:%i:%S') <=':etDate' and assets_log_id is null
    """, UserInvestmentLog)

    updateSharesAndNetValueByEtDate = UpdateMethod("""
        update user_investment_log set shares=:shares, buy_net_value=:netValue, assets_log_id=:assetsLogId
        where date_format(`time`, '%Y-%m-%d %H:%i:%S') <= ':etDate' and assets_log_id is null
    """)

    queryLogByUserId = QueryMethod("""
        select id, account_id as accountId, user_id as userId, assets_log_id as assetsLogId, TRUNCATE(transfer_amount,2) as transferAmount, shares, buy_net_value as buyNetValue, `time`
        from user_investment_log
        where user_id=:userId
        order by `time` desc 
    """, UserInvestmentLog)

    queryPageLogByUserId = QueryMethod("""
        select id, account_id as accountId, user_id as userId, assets_log_id as assetsLogId, TRUNCATE(transfer_amount,2) as transferAmount, shares, buy_net_value as buyNetValue, `time`
        from user_investment_log
        where user_id=:userId
        order by `time` desc 
        limit :limit offset :offset
    """, UserInvestmentLog)

    selectCountByUserId = SelectMethod("select count(1) from user_investment_log where user_id=:userId", int)

@transaction
def test():
    accounts = [AccountPosition(accountId=1, sharesCode='123444', enableCount=1),
                AccountPosition(accountId=1, sharesCode='123555', enableCount=1)]
    accPositionDao = AccountPositionDao()
    accPositionDao.create()
    accPositionDao.insert(accounts)
    scStrs = accPositionDao.querySharesCodeByAccountId({"accountId": 1})
    ac = accPositionDao.selectOneByAccountIdAndSharesCode({"accountId": 1, "sharesCode": "123555"})
    accPositionDao.updateEnableCountByAccountIdAndSharesCode({"num": 1, "accountId": 1, "sharesCode": "123555"})
    # accPositionDao.deleteAll()

    print(scStrs)


if __name__ == '__main__':
    test()
