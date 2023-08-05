"""
TFdata client package
www.topfintech.org

demo trading strategy which can be used as input for run_bt class method in tfdata package
do not use in actual trading!

context data
context data means all the available for the decision maker at time t for generating the signal,
and should be passed to the method as a pd.DataFrame


format of trade signal
each trading strategy method need to take a context data as input and return a str coded trade signal
the signal starts with a char represent the trade direction B = Buy, S=sell, 
H = holding the previous position ,followed by trading vol and then @ as the hint for limit price, 
e.g B1000@5.1 means a trading signal for buying 1000 units at a limit price of 5.1,
'HB'/'HS' means to hold the previous generated buy/sell signal
signal = '0' means to liquidate all positions. 

"""

def daily_3mom (context,p='close',q=10000):
    #p is the trade price
    #q is the trade quant
    """
    buy/sell when the last three trade days have positive/negative returns
    assume buy/sell at the last window day at market close when the investor realizes the signal at the leat minute and act on it
    the position is liquidated when the next day fail to give the same signal, in which case a reverse trade signal is given
    """
    trade = '0'
    if context.shape[0]>=3:
        if (context['pct_chg']>0).iloc[-3:].sum() == 3:
            if context['trade'].iat[-2][0] in ['B','H']:
                trade = 'HB'
            else:
                trade = "B%s@%.3f" % (q,context[p].iat[-1])
                
        elif (context['pct_chg']<0).iloc[-3:].sum() == 3:
            if context['trade'].iat[-2][0] in  ['S','H']:
                trade ='HS'
            else:
                trade = "S%s@%.3f" % (q,context[p].iat[-1])
    return trade

def daily_MA_mom(context,MA_fast='MA5',MA_slow='MA20',q=100,sig=None):
    """
    moving average base momentum strategy.
    buy when a fast MA cross a slow MA, expressed in different momentum measured as period returns
    sig measures the degree of difference in momentum between the two MA indicators
    high sig means stronger signal is required for making a trade
    """
    if MA_fast not in context.columns:
        
        return f'error: context缺失MA_fast: {MA_fast}'
    else:
        try:
            f_n = int(MA_fast[2:])
        except:
            return f'error: MA_fast标签命名不正确: {MA_fast}'
        
    if MA_slow not in context.columns:
        return f'error: context缺失MA_slow: {MA_fast}'
    else:
        try:
            s_n = int(MA_slow[2:])
        except:
            return f'error: MA_slow标签命名不正确: {MA_slow}'
    cdata = context[[MA_fast,MA_slow,'close','trade']].dropna().iloc[-s_n:]
    if cdata.shape[0]!=s_n:
        return '0' 
    
    close = cdata['close'].iat[-1]
    if (cdata['trade'].iat[-2][0] =='B' and 'S' not in cdata['trade'].iat[-3]) or cdata['trade'].iat[-2] =='HB':
        if cdata[MA_fast].iat[-1]>cdata[MA_slow].iat[-1]:
            return 'HB'
        else:
            return f'S{q}@{close}'
        
    if (cdata['trade'].iat[-2][0] =='S' and 'B' not in cdata['trade'].iat[-3]) or cdata['trade'].iat[-2] =='HS':
        if cdata[MA_fast].iat[-1]<cdata[MA_slow].iat[-1]:
            return 'HS'
        else:
            return f'B{q}@{close}'    
    
    if sig is None:
        sig = (s_n+f_n)//2
    
    if (cdata[MA_fast].iloc[:-1]>cdata[MA_slow].iloc[:-1]).sum()>=sig-1 and cdata[MA_fast].iat[-1]<=cdata[MA_slow].iat[-1]:
        return f'S{q}@{close}'
    
    if (cdata[MA_fast].iloc[:-1]<cdata[MA_slow].iloc[:-1]).sum()>=sig-1 and cdata[MA_fast].iat[-1]>=cdata[MA_slow].iat[-1]:
        return f'B{q}@{close}'  
    
    return '0'
    
def st_ETF_min_lit(context,q=5000,tick_size=0.001):
    if 'close_1min' not in context:
        return 'error: context missing close_1min'
    if (context.index[-1].hour==14 and context.index[-1].minute>=57) or (context.index[-1].hour >=15):
        return '0'    
    cdata=context[['open_1min','close_1min','trade']].dropna()
    if cdata.empty: #assume on the first trading point, two limit orders on the upper and lower steps are placed
        return 'H'
    if cdata.shape[0]==1 or cdata.index[-1].date()!=cdata.index[-2].date():
        pre_close = cdata['open_1min'].iat[0]
        close =  cdata['close_1min'].iat[0]
    else:
        close, pre_close = cdata['close_1min'].iat[-1],cdata['close_1min'].iat[-2] 
    if close>pre_close:
        return "S%s@%.3f" % (q,close)
    elif close < pre_close:
        return "B%s@%.3f" % (q,close)
    return 'H'

def st_stock_lit(context,q=5000,tick_size=0.01):
    if 'last_I' not in context:
        return 'error: context missing close_min'
    if (context.index[-1].hour==14 and context.index[-1].minute>=57) or (context.index[-1].hour >=15):
        return '0'    
    cdata=context[['last_I','trade']].dropna()
    if cdata.empty: #assume on the first trading point, two limit orders on the upper and lower steps are placed
        return 'H'
    if cdata.shape[0]>1:
        close, pre_close = cdata['last_I'].iat[-1],cdata['last_I'].iat[-2] 
    if close>pre_close:
        return "S%s@%.3f" % (q,close)
    elif close < pre_close:
        return "B%s@%.3f" % (q,close)
    return 'H'    
        
def st_tick_ETF_lit(context,q=5000,tick_size=0.001,gap=2):
    if 'last_I' not in context:
        return 'error: context missing last_I'   
    cdata=context[['last_I','trade','note']].dropna()
    if cdata.empty: #assume on the first trading point, two limit orders on the upper and lower steps are placed
        return 'H'
    if cdata.shape[0]>1:
        close, anchor = round(cdata['last_I'].iat[-1],3),round(cdata['note'].iat[-2],3)
    else:
        return '0',cdata['last_I'].iat[-1]
    if close-anchor - gap*tick_size > -0.000001:
        sq = q*(1 + round((close-anchor)/tick_size)-gap)
        return "S%s@%.3f" % (int(sq),close),close
    elif anchor - close - gap*tick_size > -0.000001:
        bq = q*(1 + round((anchor-close)/tick_size)-gap)
        return "B%s@%.3f" % (int(bq),close),close
    else:
        return 'H',anchor

def gap_event_daily(context,t=0.005):
    if 'close' not in context.columns or 'open' not in context.columns:
        return 'open/close columns not found'
    else:
        if context.shape[0] <2 :
            return 0,None
        else:
            if context["open"].iat[-1]/context["close"].iat[-2] - 1 >t:
                return 1,context[['open','close']].iloc[[-1]]
            else:
                return 0,None
                
        
    
    