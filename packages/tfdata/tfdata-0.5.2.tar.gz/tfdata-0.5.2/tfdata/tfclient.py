"""
TFdata client package
www.topfintech.org

TFdata client package manages the communicaton between TFdata servers and user-side client application.
User acct and user_pw are required for communicating with the data server. Check www.topfintech.org for details
"""

__author__ = "DrEdw  (ed@topfintech.org)"
__copyright__ = "Copyright (c) 2020-2021 ed@topfintech.org by the MIT license"
__license__ = "MIT"
__verson__ = '0.5.2'

from tfdata.menu_text.menu_text0 import menu_basic_cn
from tfdata.menu_text.att_list import *
from tfdata.utils.network_utils import tryrq  
from tfdata.utils.comm_utils import timenow,pro_ts,get_codetype
import pandas as pd
import numpy as np
import requests
from tdautils import tradedate_A
import threading
from tfdata.test_stra import daily_3mom,daily_MA_mom,st_ETF_min_lit,st_tick_ETF_lit,gap_event_daily


class TFclient():
    def __init__ (self,access_key='',slient=False,offline_path=None,auto_login=True,offline_dir=None):
        if access_key=='':
            raise ValueError ('需提供用户密匙,搜索添加微信公众号TFquant,对话栏输入"入会"可免费申请')
        else:
            if len(access_key)!= 96:
                raise ValueError ('请提供正确的数据密匙,如忘记数据密匙,请加微信公众号TFquant,输入"重置密匙"')
            else:
                self.__akey=access_key
        self.slient = slient
        self.__version = __verson__ 
        self.__access_key = access_key
        self.__offline_path = offline_path #this is used to saved data-specified offline data
        self.__ds_url = None
        self.__uid = None
        self.__login_time = None
        self.__notebook=None #do not modidy the use of these variables of server may refuse to respond
        self.__menu = menu_basic_cn #user menu
        self.__att_menu = {'get_1d_att':get_1d_att,'get_tick_att':get_tick_att,'get_hf5_att':get_hf5_att,\
                           'get_HSGT_name':get_HSGT_name,'get_econ_name':get_econ_name,'get_daily_name':get_daily_name,\
                               'get_stock_fs_name':get_stock_fs_name,\
                                   'get_hist_share_att':get_hist_share_att}
        self.report_usage=False #if True, program will print out data usage after successful request
        self.__current_usage=0 #store usage only in current instance
        self.__offline_dir = None
        self.context = {'tick':{},'daily':{},'min':{},"econ":{},"val":{},"fs":{},"HSGT":{},"mszy":{}}
        
        if not self.slient:
            print (menu_basic_cn['intro'])
        if auto_login:
            lo = self.login()
            if isinstance(lo,str):
                print (lo)            
    
    
    def __init_doc(self):
        """
        initilize document dictionary for users
        
        """
        self._doc = {}
        self._doc['get_1d']="获取列表数据，列表数据指用户指定的非时间序列集合，例如所有A股代码，今日IPO股票代码等。\
            函数要求输入单个数据特征，返回列表、字典或错误说明文本。\
                具体支持的数据特征可通过 self.menu['1d']查看。函数支持timeout可选参数，用于设定等待服务器返回数据最长时间。"
    @property
    def akey(self):
        return self.__access_key
    
    @property
    def notebook(self): 
        return self.__notebook
    
    @property
    def version(self):
        return self.__version
    
    @property
    def menu(self):
        return self.__menu
    
    @property
    def att_menu(self):
        return self.__att_menu

    @property
    def acct_info(self):
        return [self.__acct,self.__pw]
    
    @property
    def current_usage(self):
        return self.__current_usage

    def _check_date(self,start_date=None,end_date=None,sample_size=None,max_size=7000):
        if start_date is not None:
            try:
                start_date = pro_ts(pd.Timestamp(start_date))
            except Exception as e:
                return f'起始日输入错误：{e}'

        if end_date is not None:
            try:
                end_date = pro_ts(pd.Timestamp(end_date))
            except Exception as e:
                return f'结束日输入错误：{e}'
            
        if sample_size is not None:
            if not isinstance(sample_size,int) or sample_size <0:
                return 'sample_size输入错误'
            else:
                if sample_size>max_size:
                    sample_size=max_size
        if pd.Timestamp(start_date)>pd.Timestamp(end_date):
            return '结束日早于起始日'
        
    def __send_akey(self,server_url=None):
        """
        send akey to public server for validation and receive the assigned data server ip
        """
        if server_url is None:
            server_url = 'http://www.topfintech.org:80/clientupdate'
        re = tryrq(url = server_url,retry=1,timeout=30,wait=1,request_type='post',
                   data={'akey':self.__akey})

        if isinstance(re,str):
            return f'服务器不接受用户登录请求:{re}'
        else:
            if isinstance(re,requests.models.Response):
                try:
                    if re.status_code==200:
                        try:
                            redict = re.json()
                        except:
                            return f'服务器返回错误信息: {re.text}'
                        self.__notebook = redict
                        if 'version' in redict.keys() and redict['version'] != self.version: 
                            print (f'TFclient更新版本{redict["version"]}已经发布，请通过pip update TFclient升级，继续使用旧版本可能产生各种错误！')
                        if 'mes' in redict.keys():
                            print (f'重要提示:{redict["mes"]}')
                        if 'uid' in redict.keys():
                            self.__uid = redict['uid']
                        self.__ds_url = redict['ds_url']
                    else:
                        return f'服务器错误代码{re.status_code}'
                except Exception as e:
                    return f'连接数据服务器失败:{e}'
            else:
                return  f'连接数据服务器失败 bad request:{str(re)}'
    
    def _request(self,arg,timeout=200):
        arg.update({'uid':self.__uid,'akey':self.__akey})
        re = tryrq(url = self.__ds_url+'/datarequest',retry=1,timeout=timeout,wait=1,request_type='post',json=arg)
        self.temp=re
        if isinstance(re,str):
            return f'数据服务器不接受数据请求:{re}'
        else:
            try:
                js = re.json()
            except Exception as e:
                try:
                    return re.text
                except:
                    return f'数据服务器不接受数据请求:{e}'
            if 'data' in js.keys():
                if isinstance(js['data'],list) or (isinstance(js['data'],str) and "{" not in js['data'] and "}" not in js['data']):
                    self.__current_usage+=1
                    return js['data']
                else:
                    try:
                        df = pd.read_json(js['data'])
                        if df.empty:
                            raise ValueError()
                    except:
                        return '数据服务器返回JSON格式不正确'
                    if 'time' in df.columns:
                        df.set_index('time',drop=True,inplace=True)
                    self.__current_usage+= int(js['usage'])    
                    return df.replace('ND',np.NaN)
            else:
                '返回数据为空'
        
        
    def login(self):
        """
        send login request to public server
        
        Returns
        ------- 用户未登录
        None or error str message
        """
        dre = self.__send_akey() #this connect to main web portal for a dataAPI server assignment 
        if dre is not None:
            return dre
        if self.__ds_url is None:
            return '数据服务器缺失,请稍后再试'
        else:
            re = tryrq(url = self.__ds_url+'/userlogin',retry=1,timeout=30,wait=1,request_type='post',data={'akey':self.akey,'uid':self.__uid})
            if isinstance(re,str):
                return f'数据服务器不接受登录请求：{re}'
            else:
                if isinstance(re,requests.exceptions.ConnectionError):
                    return '数据服务器无响应'
                else:
                    self.temp = re
                    if re.status_code==200:
                        if re.text[:2]=='欢迎':
                            if not self.slient:
                                print (re.text)
                            self.__login_time = timenow()
                        else:
                            return re.text
                    else:
                       return '数据服务器不接受登录'
    
    def save_context(self,dir_path,freq=None,code=None,file_format='pic'):
        """
        write context data to local file.user may use this interface to save data to local after download
        local folder pemission issues should be handled by users
        
        Parameters
        ----------
        dir_path :str
        folder dir path for keeping data. structure design: dir_path/freq_name/code_name
        user only need to specify dir_path
        
        freq: optional,None or str, the default option is to write all freq in context to file
        
        code: optional,None or str, the default option is to write all code under each freq in context to file
        
        file_format,optional,str, the file_format for storing each code file. only support pic or csv file for now
        
        Returns
        -------
        None or error str message
        
        """ 
        
        for f in self.context.keys():
            if freq is not None and freq!= f:
                continue
            for c in self.context[f].keys():
                if code is not None and c!=code:
                    continue
                try:
                    if file_format=='pic':
                        self.context[f][c].to_pickle(dir_path+f'/{f}/{c}.pic')
                    elif file_format=='csv':
                        self.context[f][c].to_csv(dir_path+f'/{f}/{c}.csv')
                    else:
                        return '保存格式目前只支持pickle或csv格式'
                except Exception as e:
                    return f'保存context目录下{f}/{c}出错{e},检查项目目录是否权限错误'
        
    def add_context(self,freq,code):
        """
        context is the dictionary folder self.context;
        data are assoicated with code(stock,etf,futures etc.); 
        context keep all code data grouped under different frequency(freq) types;
        the struture of the context folder is therefore like this: self.context = {freq0:{code:data,code:data},freq1:{code:data,code:data}....};
        user may use this interface to add a list of code under a freq type to the context;
        once the codes are added, further data retriving and backtest actions may be performed based on those added codes
        
        Parameters
        ----------
        
        freq: required, str, name of the freq type, e.g. daily,min,tick,check user manual for details
        
        code: required,str/list, code assoicated with stock, ETF, options, etc.

        Returns
        -------
        None 
        
        """         
        if not isinstance(code,list):
            code = [code]
        if freq not in self.context:
            self.context[freq] = {}
        for c in code:
            if c not in self.context[freq].keys():
                self.context[freq][c]=pd.DataFrame()
    
    def load_context(self,dir_path,freq=None,code=None,file_format='pic'):
        """
        load context data from local file.
        The default optoins will try to load all local data associated with added freq and code in context
        
        Parameters
        ----------
        dir_path :str
        folder dir path for keeping data. structure design: dir_path/freq_name/code_name
        user only need to specify dir_path
        
        freq: optional,None or str, the default option is to try loading all added freq in context
        
        code: optional,None or str, the default option is to try loading all added code in context
        
        file_format,optional,str, the file_format for storing each code file. only support pic or csv file for now
        
        Returns
        -------
        a report dictionary that highlight errors assoicated with all added code or error str message
        an empty report dictionary means all data for the added codes have been successfully readed from files
        
        """ 
        
        if freq is None:
            freq_list = list(self.context.keys())
        else:
            if not isinstance(freq,list):
                freq_list = [freq]
            else:
                freq_list=freq
        if code is not None:
            if not isinstance(code,list):
                code = [code]
        report = {}
        for f in freq_list:
            report[f] = {}
            for c in list(self.context[f].keys()):
                if code is not None and c not in code:
                    continue
                else:
                    try:
                        if file_format=='pic':
                            file_path = f'{dir_path}/{f}/{c}.pic'
                            self.context[f][c] = pd.read_pickle(file_path)
                        elif file_format=='csv':
                            file_path = f'{dir_path}/{f}/{c}.csv'
                            self.context[f][c] = pd.read_csv(file_path)
                        else:
                            return '保存格式目前只支持pickle或csv格式'
                    except Exception as e:
                        report[f][c] = str(e)
        return report
                    
    def islogin(self):
        """
        return local login state of the client, the server-side state may not be the same
        """
        if self.__akey is not None and self.__login_time is not None and self.__uid is not None:
            return True
        else:
            return False
    
    def get_menu(self,keyword=None,printout=True):
        """
        return user menu subtext assoicated with a keyword
        Parameters
        ----------
        keyword : optional,str
        a search keyword for the request text in user manual
        if the default value None is provided, return self.__menu
        
        printout: optional,bool,when True menu text is not returned but printed out
        
        Returns
        -------
        requested text or error str message
        
        """ 
        rt = None
        
        if keyword is None:
            return self.__menu
        else:
            if keyword in self.__menu.keys():
                rt = self.__menu[keyword]             
            elif keyword in self.__att_menu:
                rt = self.__att_menu[keyword]   
            else:
                def dse(di,kw,re={},st=''):
                    for k in di.keys():
                        if k == kw:
                            if st=='':
                                re[k] = di[k]
                            else:
                                re[st+'->'+k] = di[k]
                        else:
                            if isinstance(di[k],dict):
                                if st=='':
                                    re.update(dse(di[k],kw,re,k))
                                else:
                                    re.update(dse(di[k],kw,re,st+'->'+k))
                    return re
                
                cw = dse(self.att_menu,keyword)
                if len(cw)>0:
                    rt = cw
        if rt is None:
            return f'暂无关于{keyword}的用户手册说明'
        else:
            if printout:
                print (rt)
            else:
                return rt
    
    def _get_hf(self,code,hf_type,date,timeout=200):
        """
        provide intraday data

        Parameters
        ----------
        code : str
            valid postfix code 
        date: str
             only one request per date,user may need to make mutiple request for a series of dates
        timeout: int
            wait time for return from data API before timeout break             
        Returns
             a pd.DataFrame or error str
        """        
        if hf_type not in ['hf_tick','hf5','hf_min']:
            return '非法参数'
        if '.' not in code:
            return '请输入正确的带后缀代码'
        code_type = get_codetype(code)
        if code_type not in ['ETF_CN','stock_A','ETFO_CN','CB_CN']:
            return '暂不提供该类别代码日内数据'
        try:
            date = pro_ts(pd.Timestamp(date))
        except:
            return '日期格式不正确'
        
        arg = {'rt':hf_type,'code':code,'date':date,'at':code_type}  
        rre = self._request(arg,timeout=timeout)
        return rre
        """
        re = tryrq(url = self.__ds_url+'/datarequest',retry=1,timeout=timeout,wait=1,request_type='post',json=arg)
        self.temp=re
        if isinstance(re,str):
            return f'服务器不接受数据请求:{re}'
        else:
            if re.status_code==200:
                try:
                    js = re.json()
                    self.__current_usage += int(js['usage'])
                    if self.report_usage:
                        print (f"数据用量: {js['usage']}")
                except:
                    return f'数据服务器返回错误信息:{re.text}'
                try:
                    df = pd.read_json(js['data']).set_index('time')
                    df.index = pd.DatetimeIndex(df.index)
                except Exception as e:
                    return f'无法读取数据服务器返回JSON表格:{e}'
                return df
        """
        
    def get_tick(self,code,date,add2context=False):
        """
        provide intraday tick(summary of trades in every 3 second) data
        check self._get_hf for detail
        
        """   
        if not self.islogin():
            return '未登录数据服务器,请先用self.login()登录'
        df =  self._get_hf(code=code,date=date,hf_type='hf_tick')   
        if isinstance(df,str):
            return df
        else:
            try:
                df.index = pd.DatetimeIndex(df.index)
            except:
                pass
            if add2context:
                if code in self.context['tick'] and not self.context['tick'][code].empty:
                    if date not in pro_ts(self.context['tick'][code].index):
                        self.context['tick'][code] = pd.concat([self.context['tick'][code],df],axis=0)
                        self.context['tick'][code].sort_index(inplace=True)
                else:
                    self.context['tick'][code] = df
            else:
                return df
    
    def get_min(self,code,date,freq='1min',add2context=False):
        """
        gen intraday min_by_min data by using tick data
        
        check self._get_hf for detail
        
        
        """  
        if freq[-3:] !='min':
            return 'freq参数输入错误，必须采用分钟参数，例如 5min,不超过60分钟'
        else:
            try:
                minint = int(freq[:-3])
            except:
                return 'freq参数输入错误，必须采用分钟参数，例如 5min,不超过60分钟'
            if minint>60:
                return 'freq参数输入错误，必须采用分钟参数，例如 5min,不超过60分钟'
            
        tickdf = self.get_tick(code=code,date=date,add2context=False)
        if isinstance(tickdf,str):
            return tickdf
        else:
            last_pre = tickdf['last_I'].loc[:f"{date} 09:29:59"]
            vol_pre= tickdf['volume_I'].loc[:f"{date} 09:29:59"].sum()
            amt_pre =tickdf['amt_I'].loc[:f"{date} 09:29:59"].sum()
            if pd.Timestamp(f"{date} 09:30:00") not in tickdf.index:
                tickdf.loc[pd.Timestamp(f"{date} 09:30:00")] = np.NaN
            ohlc = tickdf['last_I'].loc[f"{date} 09:30:00":].resample(freq,origin='start',label='right',closed='right').ohlc()
            ohlc = pd.concat([ohlc.loc[f"{date} 09:30:00":f"{date} 11:30:00"],ohlc.loc[f"{date} 13:00:00":f"{date} 15:00:00"]],axis=0)
            if not last_pre.dropna().empty:
                pre_last = last_pre.dropna().iloc[-1]
            else:
                pre_last = None
            ohlc[f'close_{freq}'] = ohlc['close'].fillna(method='ffill')
            ohlc[f'open_{freq}'] = ohlc[f'close_{freq}'].shift(1)
            ohlc[f'low_{freq}'] = ohlc['low'].fillna(ohlc[f'close_{freq}'])
            ohlc[f'high_{freq}'] = ohlc['high'].fillna(ohlc[f'close_{freq}'])
            ohlc[f'vol_{freq}'] = tickdf['volume_I'].loc[f"{date} 09:30:00":].resample(freq,origin='start',label='right',closed='right').sum().fillna(0)
            ohlc[f'amount_{freq}'] = tickdf['amt_I'].loc[f"{date} 09:30:00":].resample(freq,origin='start',label='right',closed='right').sum().fillna(0)
            ohlc.drop(['open','high','low','close'],axis=1,inplace=True)
            ohlc = ohlc.loc[f"{date} 09:30:00":]
            if pre_last is not None:
                ohlc[f'open_{freq}'].iat[0] = pre_last
                ohlc[f'vol_{freq}'].iat[0] += vol_pre
                ohlc[f'amount_{freq}'].iat[0] += amt_pre
            ohlc[f'vol_{freq}'] = ohlc[f'vol_{freq}'].astype(int)
        if add2context:
            if freq not in self.context:
                self.context[freq] = {}
            if code in self.context[freq] and not self.context[freq][code].empty:
                if date not in pro_ts(self.context[freq][code].index):
                    self.context[freq][code] = pd.concat([self.context[freq][code],ohlc],axis=0)
                    self.context[freq][code].sort_index(inplace=True) 
            else:
                self.context[freq][code] = ohlc
        else:
            return ohlc
        
    def get_hf5(self,code,date):
        """
        provide intraday hf5, ie. level 1 quote data
        check self._get_hf for detail
        """   
        if not self.islogin():
            return '未登录数据服务器,请先用self.login()登录'        
        return self._get_hf(code=code,date=date,hf_type='hf5')           

    def get_1d(self,att,timeout=200):
        """
        1d data are list or dictionary data without the the time index and columns

        Parameters
        ----------
        att : str,default is None
             name of the attribute data under request. Available att name may be found in self.menu
        timeout: int
             request timeout setting
        Returns
             request result dict
        """
        if not self.islogin():
            return '未登录数据服务器,请先用self.login()登录'            
        if att not in self.get_menu('get_1d_att',printout=False).keys():
            return f'目前不支持1D数据标签{att},请查阅用户手册'
        arg = {'rt':'1d','att':att}
        rre = self._request(arg,timeout=timeout)
        return rre


    def get_hist_share(self,code,timeout=200,translate=False):
        """
        Request share change data 
        
        Parameters
        ----------
        code : str
            valid postfix code
        timeout: int
            wait time for return from data API before timeout break
        translate: bool
            whether translate columns labels into Chinese

        """          
        if not isinstance(code,str) or ('.SH' not in code and '.SZ' not in code and 'BJ' not in code):
            return 'code 参数输入错误'
        arg = {'rt':'sharebase','code':code}    
        rre = self._request(arg,timeout=timeout)
        if isinstance(rre,str):
            return rre
        else:
            if translate:
                return rre.rename(columns=get_hist_share_att)
            else:
                return rre

    def get_stock_fs(self,name,code,start_year,timeout=200,translate=False):
        """
        Request financial report data 
        
        Parameters
        ----------
        name : str
            data name, 'balance,income,or cashflow'
        code: str
            stock code for the request
        start_year: int
            all statment data since the start year will be in the request
        timeout: int
            wait time for return from data API before timeout break
        return
            dataframe or error str

        """          
        if not isinstance(name,str) or name not in get_stock_fs_name:
            return 'name必须是balance资产报表, income收入报表,或cashflow现金流报表'
        if not isinstance(code,str) or ('.SH' not in code and '.SZ' not in code):
            return 'code 参数输入错误'
        if not isinstance(start_year,int):
            return 'start_year输入错误'
        arg = {'rt':'fs','name':name,'start_year':start_year,'code':code}    
        rre = self._request(arg,timeout=timeout)
        if isinstance(rre,str):
            return rre
        else:
            if 'time' in rre.columns:
                rre.set_index('time',drop=True,inplace=True)    
            if translate:
                rre = rre.rename(columns=get_stock_fs_name[name])
            return rre           


    def get_econ(self,name,start_date=None,end_date=None,sample_size=10,timeout=200):
        """
        Parameters
        ----------
        name : str
            data name
        arg : dict
            supported arg passed to the API. This depends on the name of data under request
        Returns
        -------
        pd.DataFrame 
        or
        error string

        """          
        if name not in get_econ_name.keys():
            return '不支持{name}的cbdata数据查询,请查阅self.get_menu("get_econ_name")'
        else:
            ccd = self._check_date(start_date=start_date,end_date=end_date,sample_size=sample_size,max_size=5000)
            if isinstance(ccd,str):
                return ccd
            arg={"start_date":start_date,"end_date":end_date,"sample_size":sample_size,'rt':'econ_data'}
            if 'att' in arg:
                att_list = list(get_econ_name[name].keys())
                att_list.remove('arg说明')
                if isinstance(arg['att'],list):
                    for a in arg['att']:
                        if a not in att_list:
                            return f'不支持数据标签{a},请查阅self.get_menu("get_econ_name")'
                else:
                    return 'arg中att参数必须以list格式输入'
            if name == 'rrp':
                if 'freq' not in arg.keys():
                    return 'datacb rrp 央行逆回购数据要求提供freq (1d,1w,1m) 参数'                        
            arg['name'] = name
            rre = self._request(arg,timeout=timeout)
            return rre        

    def get_HSGT(self,name,code=None,start_date=None,end_date=None,sample_size=None,timeout=200):
        """
        Parameters
        ----------
        name : str
            data name
        arg : dict
            supported arg passed to the API. This depends on the name of data under request
        Returns
        -------
        pd.DataFrame 
        or
        error string
        """          
        if name not in get_HSGT_name.keys():
            return '不支持{name}的HSGT数据查询,请查阅self.get_menu("get_HSGT_name")'
        else:
            ccd = self._check_date(start_date=start_date,end_date=end_date,sample_size=sample_size,max_size=3000)
            if isinstance(ccd,str):
                return ccd
            arg={"start_date":start_date,"end_date":end_date,"sample_size":sample_size,'rt':f'HGT_{name}'}
            rre = self._request(arg,timeout=timeout)
            return rre

    def get_daily(self,code,name='daily',start_date=None,end_date=None,sample_size=None,timeout=200,adj_price=None,add2context=False,translate=False):
        """
        Parameters
        ----------
        code : str
            valid postfix code, if a non-postfix code is provided the system may try to match 
        att_group: str
            name of daily data group under request
        start_date : str, optional,default is None
            required format yyyy-mm-dd, if it is None, start_date will be auto-filled on server site, the particular value is case-specific
        end_date : str, optional,default is None
            required format yyyy-mm-dd, if it is None, end_date will be auto-filled on server site, the particular value is case-specific
        sample_size, inttf
            when either start_date or end_date is None but not both, sample_size specify the length of the resulting time index
        timeout: int
            wait time for return from data API before timeout break
        adj_price: None or str
            specify the adjustment scheme for OHLC price, q - backward adjusted, h - forward adjusted, or point-adjusted if a date text is provided
        add2context: bool
            specifiy whether returning data will be used to upgrade local context database
        trasnalte: bool
            rename and translate the return dataframe's columns into Chinese
        Returns
            None if add2context=True 
            else 
            pd.DataFrame of daily OHLC price,vol,amount assoicted with the input code 
            or
            error string

        """  
        if not self.islogin():
            return '未登录数据服务器,请先用self.login()登录'        
        ct = get_codetype(code)
        if ct =='NA':
            return '代码格式不正确，请查阅"self.get_menu("code")'
        if name not in ['daily','valuation','ms']:
            return f'不支持的daily数据name：{name}'
        else:
            if name in ['valuation','ms'] and ct != 'stock_A':
                return f'{name}组日线数据仅限于股票'
            else:
                rt = f'{name}_att'
        
        if ct in ['stock_A','ETF_CN'] and name == 'daily':
            if adj_price is not None:
                if adj_price not in ['q','h']:
                    try:
                        adjdate = pd.Timestamp(adj_price)
                    except:
                        return 'adj_price参数输入错误: q - 前复权, h - 后复权, or 提供日期进行点复权'
            
            
        arg = {'code':code,'uid':self.__uid,'akey':self.__akey,'rt':rt,'start_date':start_date,'end_date':end_date,'sample_size':sample_size}
        df = self._request(arg,timeout=timeout)            
        if isinstance(df,str):
            return df
        
        if name == 'daily' and ct in ['stock_A','ETF_CN'] and adj_price is not None:
            if code[0] in ['1','5'] and ('SH' in code or 'SZ' in code):
                rsize = 3
            else:
                rsize = 2
                
            df['pindex'] = np.NaN
            df["pindex"].iat[0] = 1
            df['close'] = df['close'].replace(0,np.NaN)
            
            for i in range(1, df.shape[0]):
                t = df.index[i]
                tl = df.index[i-1]
                if pd.isnull(df.at[t,'close']) or pd.isnull(df.at[t,'pct_chg']):
                    df.at[t,'pindex'] = df.at[tl,'pindex']
                else:
                    if 'pre_close' in df.columns and not pd.isnull(df.at[t,'pre_close']):
                        df.at[t,'pindex'] = df.at[tl,'pindex']*(df.at[t,'close']/df.at[t,'pre_close'])
                    else:
                        df.at[t,'pindex'] = df.at[tl,'pindex']*(1+df.at[t,'pct_chg']/100)
            df['pindex'] = round(df['pindex'],10)
            if adj_price == 'q':
                for i in range(2,df.shape[0]+1):
                    df.loc[df.index[-i],['open','high','low','close']] = round(df.loc[df.index[-i+1],['open','high','low','close']]*(df.at[df.index[-i],'pindex']/df.at[df.index[-i+1],'pindex']),rsize)
            elif adj_price == 'h':
                for i in range(1,df.shape[0]):
                    df.loc[df.index[i],['open','high','low','close']] = round(df.loc[df.index[i-1],['open','high','low','close']]*(df.at[df.index[i],'pindex']/df.at[df.index[i-1],'pindex']),rsize)            
            else:
                try:
                    adate = pd.Timestamp(adj_price)
                except:
                    adate = None
                if adate is not None and adate in df.index:
                    loc = df.index.get_loc(adate)
                    for i in range(1,loc+1):
                        df.loc[df.index[loc-i],['open','high','low','close']] = round(df.loc[df.index[loc-i+1],['open','high','low','close']]*(df.at[df.index[loc-i],'pindex']/df.at[df.index[loc-i+1],'pindex']),rsize)             
                    for i in range(1,df.shape[0]-loc):
                        df.loc[df.index[loc+i],['open','high','low','close']] = round(df.loc[df.index[loc+i-1],['open','high','low','close']]*(df.at[df.index[loc+i],'pindex']/df.at[df.index[loc+i-1],'pindex']),rsize)
            df.drop('pindex',axis=1)
        
        if translate:
            df.rename(columns=get_daily_name[name],inplace=True)
        if add2context:
            for att in df.columns:
                self.__add2context(code,freq='daily',att_series=df[att])
        else:
            return df

    def __add2context(self,code,freq,att_series):
        if code not in self.context[freq]:
            self.context[freq][code] = pd.DataFrame(att_series)
        else:
            if att_series.name in self.context[freq][code].columns:
                self.context[freq][code] = self.context[freq][code].reindex(self.context[freq][code].index.union(att_series.index))
                self.context[freq][code].update(pd.DataFrame(att_series))
            else:
                self.context[freq][code] = pd.concat([self.context[freq][code],pd.DataFrame(att_series)],axis=1)
    
    
    def run_bt(self,trade_func,freq,start_date,end_date,code_base=None,trade_cost_rate=0.0001,thread_pool=1):
        """
        this performs back-testing experience using cache data from self.get_btdata. trade_func will apply
        on each freq-based trade point with buying or selling decision. final returns are reported to user
    
        Parameters
        ----------
        trade_func: TYPE func,take each trade point data as arg and return signal_based str code for sell,station,buy decisions
        start_date : TYPE str
        end_date : TYPE str
        code_base: Type None or list of code, code that will be included in applying the trade_func in each t, None means all codes available in the self.bt_cache are included
        """
        if freq not in self.context:
            return "未发现self.context中存在回测数据"
        
        if start_date is not None:
            try:
                start_date = pro_ts(pd.Timestamp(start_date))
            except Exception as e:
                return f'起始日输入错误：{e}'

        if end_date is not None:
            try:
                end_date = pro_ts(pd.Timestamp(end_date))
            except Exception as e:
                return f'结束日输入错误：{e}'
        ta= tradedate_A()
        
        try:
            dl = ta.gen_dtindex(start_date=start_date,end_date=end_date)
        except Exception as e:
            return f'请输入正确的start_date,end_date参数 {e}'
        
        cfolder = self.context[freq]
        if code_base is None:
            code_base=list(cfolder.keys())
            if len(code_base)==0:
                return '无任何可用的code base数据'
        else:
            if not isinstance(code_base,list):
                return 'code_base参数输入不正确'
            else:
                ecb = set(code_base) - set(cfolder.keys())
                if len(ecb)>0:
                    print (f"部分code_base代码未有context数据:{ecb}")
                    code_base  = list(set(code_base) - ecb)
        note = {}
        def btc(c):
            if cfolder[c].empty:
                note[c] = 'NoData'
                return
            if freq == 'tick' or freq[-3:] == 'min':
                dindex = cfolder[c].loc[pro_ts(dl[0]):pro_ts(dl[-1])].index
                if len(dindex)==0:
                    note[c] ='NoData'
                    return
            else:
                dindex = dl
                
            cfolder[c]['trade'] = '0'
            cfolder[c]['note'] = ''
            for di in range(len(dindex)):
                if dindex[di] not in cfolder[c].index:
                    continue
                else:
                    ire = trade_func(cfolder[c].loc[:dindex[di]])
                    if isinstance(ire,tuple):
                        cfolder[c].loc[dindex[di],['trade','note']] = ire
                    else:
                        cfolder[c].at[dindex[di],'trade'] = ire
            cfolder[c]['hold_vol'] = 0
            cfolder[c]['profit_I'] = 0
            cfolder[c]['trade_cost'] = 0
            cfolder[c]['money_flow'] = 0
            cfolder[c]['value'] = 0
            if freq =='daily':
                cs = cfolder[c]['close']
            elif freq[-3:]=='min':
                cs = cfolder[c][f'close_{freq}']
            elif freq=='tick':
                cs = cfolder[c]['last_I']
            
            for i in range(cfolder[c].shape[0]):
                sig = cfolder[c]['trade'].iat[i]
                close= float(cs.iat[i])
                
                if i !=0:
                    q_lag = cfolder[c]['hold_vol'].iat[i-1]
                    pre_close = float(cs.iat[i-1])
                else:
                    q_lag = 0
                    pre_close = np.NaN
                    
                cfolder[c]['hold_vol'].iat[i] = q_lag
                
                if i!=0 and sig =='0': #return vol to 0
                    if q_lag >0:
                        cfolder[c]['trade'].iat[i] = sig = "S%s@%.4f" % (abs(q_lag),close)
                    elif q_lag <0:
                        cfolder[c]['trade'].iat[i] = sig = "B%s@%.4f" % (abs(q_lag),close)
                    else:
                        continue
                else:
                    if i==0 and sig=='0':
                        continue
                
                if q_lag != 0:
                    cfolder[c]['profit_I'].iat[i] = q_lag*(close-pre_close)  #work either ways for q< or >0
                
                
                if sig[0] !='H':
                    try:
                        q = float(sig[1:sig.index("@")])
                        p = float(sig[sig.index("@")+1:])
                        if q ==0 or p ==0:
                            raise ValueError()
                    except:
                        note[c] = f'错误trade signal格式:{sig}'    
                        continue
                else:
                    cfolder[c]['value'].iat[i] = cfolder[c]['hold_vol'].iat[i]*close
                    continue

                if sig[0] == 'B':
                    cfolder[c]['money_flow'].iat[i] = -p*q
                    cfolder[c]['hold_vol'].iat[i] += q
                elif sig[0] == 'S':
                    cfolder[c]['money_flow'].iat[i] = p*q
                    cfolder[c]['hold_vol'].iat[i] -= q 
                  
                cfolder[c]['trade_cost'].iat[i]  = max(round(p*q*trade_cost_rate,2),0.01)
                if cfolder[c]['hold_vol'].iat[i]!=0:
                    cfolder[c]['value'].iat[i] = cfolder[c]['hold_vol'].iat[i]*close
        
        if thread_pool>1:
            tl = []
            for c in code_base:
                tt = threading.Thread(target=btc,args=[c])
                tt.start()
                tl.append(tt)
            for t in tl:
                t.join()
        else:
            for c in code_base:
                btc(c)
                
        return note
   
            
    def cal_portf(self,freq,init_fund=1000000,margin_cost=0.05,ss_cost=0.08,ON_rate=0,code_base=None):
        """
        provide portfolio return summary on current back-testing results that are already written to context
        i.e. code-to-code back-testing results must have already been calculated and saved to self.context 
        
        freq : str
            data frequency type that is consistent with self.context keys
        margin_cost : float
            the margin account annualized interest rate when there is not enough cash to carry on the simulation
        ON_rate : float
            the annualized over night return for cash
        Returns:
            tuple containing two dataframe of reports, error str
    
        """        
        if freq not in self.context:
            return f'未发现相关回测数据 freq = {freq}'
        ipdf = self.context[freq]
        pfdf_index = None
        for c in ipdf:
            if code_base is not None:
                if c not in code_base:
                    continue
            if ipdf[c].empty or 'trade' not in ipdf[c].columns:
                continue
            if pfdf_index is None:
                pfdf_index = ipdf[c][['trade', 'hold_vol', 'profit_I', 'trade_cost',
                'money_flow', 'value']].dropna().index
            else:
                pfdf_index = pfdf_index.union(ipdf[c].index)
                
        pfdf = pd.DataFrame(index=pfdf_index,columns =['cash','asset_value','total_value','profit'])
        report = pd.Series(index=['total_trading_points','active_rate','ave_t_cash','ave_t_asset',\
                                  'init_pvalue','end_pvalue','max_pvalue','min_pvalue','total_trade_cost',\
                                      'total_int_paid','overall_return','ave_t_return','std_t_return',\
                                          'MDD','sharpe_ratio'],dtype=object)

        if pfdf.empty:
            return '所有标的context数据为空或未完成回测计算'
            
        pfdf['cash'].iat[0] = init_fund
        pfdf['asset_value'] = 0 
        pfdf['active'] = 0
        pfdf['trade_cost'] = 0
        pfdf['trade_code'] = ''
        pfdf['profit'] = 0
        pfdf['on_interest'] = 0
        
        for i in range(pfdf.shape[0]):
            if i!=0:
                if freq=='daily':
                    t_days = (pfdf_index[i] - pfdf_index[i-1]).days
                    if pfdf['cash'].iat[i-1]<0:
                        on_interest = -pfdf['cash'].iat[i-1]*(margin_cost/365)*t_days
                    else:
                        on_interest = pfdf['cash'].iat[i-1]*(ON_rate/365)*t_days
                    pfdf['cash'].iat[i] = pfdf['cash'].iat[i-1] + on_interest
                    pfdf['on_interest'].iat[i] = on_interest
                else:
                    pfdf['cash'].iat[i] = pfdf['cash'].iat[i-1]
            
                
            t = pfdf_index[i]
            for c in ipdf:
                if ipdf[c].empty or t not in ipdf[c].index:
                    continue
                pfdf.at[t,'trade_cost'] += ipdf[c].at[t,'trade_cost']
                pfdf.at[t,'cash'] += ipdf[c].at[t,'money_flow'] - ipdf[c].at[t,'trade_cost']
                pfdf.at[t,'asset_value'] += ipdf[c].at[t,'value']
                pfdf.at[t,'profit'] += ipdf[c].at[t,'profit_I'] - ipdf[c].at[t,'trade_cost']
                if ipdf[c].at[t,'trade'][0] not in ['0']: 
                    pfdf.at[t,'active']+=1
                    pfdf.at[t,'trade_code'] += c+','
                    
            if pfdf.at[t,'trade_code']!='':
                pfdf.at[t,'trade_code'] = pfdf.at[t,'trade_code'][:-1]
                
        pfdf['total_value'] = pfdf['cash'] + pfdf['asset_value']
        
        report.at['total_trading_points'] = pfdf.shape[0]
        try:
            report.at['active_rate'] = round(100*pfdf[pfdf['active']>=1].shape[0]/report.at['total_trading_points'],2)
        except:
            report.at['active_rate']=np.NaN
        report.at['ave_t_cash'] = pfdf['cash'].mean()
        report.at['ave_t_asset'] = pfdf['asset_value'].mean()
        report.at['init_pvalue'] = pfdf['total_value'].iat[0]
        report.at['end_pvalue'] = pfdf['total_value'].iat[-1]
        report.at['max_pvalue'] = pfdf['total_value'].max()
        report.at['min_pvalue'] = pfdf['total_value'].min()
        report.at['total_trade_cost'] = pfdf['trade_cost'].sum()
        report.at['total_int_paid'] = pfdf['on_interest'].sum()
        try:
            report.at['overall_return'] = round(100*(report.at['end_pvalue']/report.at['init_pvalue']-1),2)
        except:
            report.at['overall_return']  = np.NaN
        report.at['ave_t_return'] = pfdf['profit'].mean()
        report.at['std_t_return'] = pfdf['profit'].std()
        try:
            report.at['MDD'] = round(100*(report.at['min_pvalue'] - report.at['max_pvalue'])/report.at['max_pvalue'],2)
        except:
            report.at['MDD']=np.NaN
        try:
            report.at['sharpe_ratio'] = report.at['overall_return']/report.at['std_t_return']
        except:
            report.at['sharpe_ratio'] = np.NaN
        return pfdf,report
    
    def get_btdata(self,freq,start_date,end_date,code=None,overwrite=False):
        """
        request missing data from API based on user defined data requirment
        Parameters
        ----------
        freq : str
            data frequency type that is consistent with self.context keys
        att : str or list of str att name 
            if a str of a attribute is provide - > return a time series or a list of str attribute -> return a time series dataframe
        start_date : str
            required format yyyy-mm-dd, the start date of the back-testing period, will be auto offset if it is not a trading day
        end_date : str
            required format yyyy-mm-dd,the end date of the back-testing period, will be auto offset if it is not a trading day
            when either start_date or end_date is None but not both, sample_size specify the length of the resulting time index
        code : str,optional
            valid postfix code, if code is None, all added context under self.context[freq] will be included 
        overwrite: bool,optional
            only request missing data from API if overwrite=False
        Returns:
            None, error str message
    
        """
        if freq not in self.context:
            self.context[freq] = {}
        cfolder = self.context[freq]
        
        if start_date is not None:
            try:
                start_date = pro_ts(pd.Timestamp(start_date))
            except Exception as e:
                return f'起始日输入错误：{e}'

        if end_date is not None:
            try:
                end_date = pro_ts(pd.Timestamp(end_date))
            except Exception as e:
                return f'结束日输入错误：{e}'
            
        ta= tradedate_A()
        try:
            dl = ta.gen_dtindex(start_date=start_date,end_date=end_date)
        except Exception as e:
            return f'请输入正确的start_date,end_date参数 {e}'
        if code is None:
            cl=list(cfolder.keys())
        else:
            if isinstance(code,str):
                cl= [code]
            for c in cl:
                if c not in cfolder.keys():
                    return f'code={c}未添加至context'

        for c in cl:
            if cfolder[c].empty:
                cdl = []
            else:
                cdl = pro_ts(cfolder[c].index)
                
            if freq=='tick':
                for d in dl:
                    strd = pro_ts(d)
                    if overwrite or strd not in cdl:
                        cdata = self.get_tick(code=c,date=strd,add2context=True)
                        
            elif freq[-3:] == 'min':
                try:
                    mnum =int(freq[:-3])
                except:
                    return 'min-freq输入格式错误'
                for d in dl:
                    strd = pro_ts(d)
                    if overwrite or strd not in cdl:
                        cdata = self.get_min(code=c,date=strd,freq=freq,add2context=True)  
                
            elif freq=='daily':
                if overwrite or cfolder[c].empty or pro_ts(dl[0]) not in cdl or pro_ts(dl[-1]) not in cdl:
                    cdata = self.get_daily(code=c,start_date=pro_ts(dl[0]),end_date=pro_ts(dl[-1])).dropna(how='any')
                    if cdata.empty:
                        cdata ='NoData'
                    if isinstance(cdata,pd.DataFrame):
                        cfolder[c] = pd.concat([cfolder[c],cdata],axis=0).reset_index().drop_duplicates(subset=['index']).set_index("index")
                    else:
                        print (f'回测数据缺失:code ={c} sdate={dl[0]},edate={dl[-1]},reason={cdata}')

    def event_study(self,target,event_func,event_name,code_list=None,start_time=None,end_time=None):
        """
        this performs event_study on given targeted context data.event_func is used to check whether a given 
        data point should be labeled as an event, post-event performance statistics is calculated based on labeled events

        Parameters
        ----------
        target: Type str, data target in self.context
        event_func: TYPE func,take each trade point data as arg and return an indicator of 0/1 to label an event
        event_name: Type str, label name for the event
        start_time : optional, the default setting -- None -- uses the start of the local data dataFrame index. user input time str format: yyyy-mm-dd hh:mm:ss
        end_date : optional, the default setting  -- None -- uses the end of the local data dataFrame index. user input time str format: yyyy-mm-dd hh:mm:ss
        code_base: Type None or list of code, code that will be included in applying the trade_func in each t, None means all codes available in the self.bt_cache are included
        """        
        if target not in self.context:
            return 'targeted data not in context'
        else:
            event_df = pd.DataFrame()
            cdata = self.context[target]
            if code_list is None:
                cl = list(cdata.keys())
            else:
                cl = code_list
            for c in cl:
                if c not in cdata:
                    print (f'{c} not in context[{target}]')
                    continue
                else:
                    try:
                        scdata = cdata[c].loc[start_time:end_time]
                    except Exception as e:
                        print (f's/end time wrong format {start_time} {end_time}: {e}')
                        continue
                    cdata[c][f'event_{event_name}'] = 0
                    for i in range(scdata.shape[0]):
                        fre = event_func(cdata[c].iloc[:i+1])
                        cdata[c].at[scdata.index[i],f'event_{event_name}'] = fre[0]
                        if fre[1] is not None:
                            event_df = pd.concat([event_df,fre[1]])
            return event_df    
        
    def get_daily_pro(self,code,att,start_date=None,end_date=None,sample_size=None,timeout=200,add2context=False):
        """
        This API is still under development
        Parameters
        ----------
        code : str
            valid postfix code, if a non-postfix code is provided the system may try to match 
        start_date : str, optional,default is None
            required format yyyy-mm-dd, if it is None, start_date will be auto-filled on server site, the particular value is case-specific
        end_date : str, optional,default is None
            required format yyyy-mm-dd, if it is None, end_date will be auto-filled on server site, the particular value is case-specific
        sample_size, int
            when either start_date or end_date is None but not both, sample_size specify the length of the resulting time index
        timeout: int
            wait time for return from data API before timeout break
        Returns
            None if add2context=True 
            else 
            pd.DataFrame
            or
            error string
        """
        if not self.islogin():
            return '未登录数据服务器,请先用self.login()登录'        
        df = self._get_tstable(code=code,att=att,start_date=start_date,end_date=end_date,sample_size=sample_size,timeout=timeout)
        if add2context:
            for att in df.columns:
                self.__add2context(code,freq='daily',att_series=df[att])
        else:
            return df        
