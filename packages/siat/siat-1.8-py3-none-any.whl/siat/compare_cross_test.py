# -*- coding: utf-8 -*-

import os; os.chdir("S:/siat")
from siat import *

#==============================================================================
if __name__=='__main__':
    ticker='600519.SS'
    start='2023-1-1'
    end='2023-4-4'
    info_types=['Close','Volume']
    
    #获取股票价格
    df1=fetch_price_stock(ticker,start,end)
    
    #获取指数价格
    mktidx='000300.SS'
    df1i=fetch_price_stock(mktidx,start,end)
    
    #获取ETF价格
    etf='512690.SS'
    df1e=fetch_price_stock(etf,start,end)
    
    #获取REiTs基金价格
    reits='180801.SZ'
    df1r=fetch_price_stock(reits,start,end)
    
    
if __name__=='__main__':
    Market={'Market':('China','000300.SS','白酒组合1号')}
    Stocks ={'600519.SS':.5,
             '000858.SZ':.3,
             '000596.SZ':.1,
             '000568.SZ':.1}
    portfolio=dict(Market,**Stocks)
    
    start='2023-1-1'
    end='2023-4-4'
    
    #获取投资组合价格
    df2=fetch_price_stock_portfolio(portfolio,start,end)

if __name__=='__main__':
    ticker='850831'
    
    start='2023-1-1'
    end='2023-4-4'
    info_types=['Close','Volume']
    
    #获取申万指数价格
    df3=fetch_price_swindex(ticker,start,end)

#多种证券价格组合
dflist=[df1,df1i,df1e,df1r,df2,df3]

#比较收益与风险指标
cmc1=compare_msecurity_cross(dflist,
                           measure='Exp Ret%',
                           start=start,end=end)

cmc2=compare_msecurity_cross(dflist,
                           measure='Annual Ret%',
                           start=start,end=end)

#比较夏普指标
rar3=rar_ratio_rolling_df(df3,ratio_name='sharpe',window=240)

cmc3=compare_mrar_cross(dflist,rar_name='sharpe',start=start,end=end,window=240)

cmc4=compare_mrar_cross(dflist,rar_name='sortino',start=start,end=end,window=240)

cmc4=compare_mrar_cross(dflist,rar_name='alpha',start=start,end=end,window=240)
#==============================================================================
