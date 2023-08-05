

intro_text = '欢迎使用TopFintech数据API。所有数据由人工智能程序收集、整理、计算，仅供个人参考学习。申请免费账户：添加微信公众号TFquant,对话栏输入"新用户"。新手请查阅用户手册：http://www.topfintech.org/TF_API。屏蔽本登录提示: self.__init__(slient=True)'
att_text = 'att\n 简介: 数据标签即用于描述、指定某一集合数据的简称，例如"close", "vol", "turnover". 数据标签常作为参数用于TopFintech数据获取函数。查阅具体支持的标签名录及说明,可通过self.get_menu({数据函数命令}_att)了解, 多个数据标签可以列表格式输入'
usage_text = 'usage\n简介: 用于记录用户数据用量单位。一个单位等于一个表格单元。例如用户获得一个len=10的list数据，用量为10，一个4*4的pd.DataFrame表格则用量为16。用量到达限制可能无法继续获取数据，用量一般每日清零。'
date_range_text = 'date_range\n简介: 交易日序列指一个有序(从早到近期)的交易日日期集合，例如["2021-11-23","2021-11-24", ...... "2021-11-30"]. TopFintech 服务器根据 start_date, end_date, sample_size 三个参数生产交易日序列. 用户一般只需要提供其中两个参数值.例如，end_date = "2021-11-30", sample_size = 10,组合表示 以"2021-11-30"日为结束日，往前10个交易日的序列; start_date = "2021-05- 01", end_date="2021-10-01" 表示包含在两个日期间的交易日序列, 在这种情况下sample_size 参数输入将被忽略.'
code_text = 'code\n简介:TopFintech服务器接受的证券代码格式一般为 "{官方交易代码}.{后缀}"，例如: "000001.SZ"。股票、ETF代码后缀包括:SH,SZ,BJ(证券挂牌市场),中国市场指数后缀为"CNi",ETF期权后缀".CNo", 可转债后缀".SZb" 或 ".SHb"。'
login_text = '\n简介: 用户登录函数，函数向用户服务器请求分配数据服务器，须提供合法的TopFintech用户名、数据密码(获取账户:http://www.topfintech.org/user_management)\n参数: acct - 用户名,必填;pw - 数据密码,必填\n 登录信息或错误提示'
get_menu_text = 'get_menu\n简介:函数用于获取使用说明文本; 输入数据函数命令作为关键字, 可得关于该函数的说明文本\n参数：keyword - 说明文本关键字, 例如, 数据函数名, 参数等，必填; printout - 默认True,直接打印文本, 选False返回文本,选填\n返回：None or 说明文本'
get_tick_text = 'get_tick\n简介: 函数提供个股、ETF、ETF期权、可转债历史交易日日内跳价数据\n参数：code - 证券代码,必填,详阅self.get_menu("code"), date - 日期,格式yyyy-mm-dd,必填; timeout - 等待服务器返回数据的最长时秒, 默认200秒\n返回：时间序列表格, 其中volume_I跳价成交量单位为手，amt_I跳价成交额单位为千, dir_I = 0,1,-1 分别为中性，买入，卖出交易.'
get_hf5_text =  'get_hf5\n简介: 函数提供个股、ETF、ETF期权、可转债历史日内5档报价行情数据\n参数：code - 证券代码,必填,详阅self.get_menu("code"), date - 日期,格式yyyy-mm-dd,必填; timeout - 等待服务器返回数据的最长时秒, 默认200秒\n返回：时间序列表格, 其中volume_I累计成交量，单位为手，amt_I累计成交额,5档行情单量size单位为手，open_I当日开盘价, pre_close昨收'
get_min_text = 'get_min\n简介: 函数提供个股、ETF历史日内 n分钟 OHLC行情数据\n参数：code - 证券代码,必填，详阅self.get_menu("code"), date - 日期,格式yyyy-mm-dd,必填, freq - 数据频率,默认1分钟,可选1-60分钟; timeout - 等待服务器返回数据的最长时秒, 默认200秒;add2context - bool, 选填,是否把结果保存到context默认 False\n返回：时间序列表格, 其中vol_min时间段成交量，单位为手,amount_min时间段成交额,单位为千, 日间累计净买额单位为千'
get_1d_text = 'get_1d\n简介: 函数提供标的集合数据,即以列表、字典、文本等集合数据格式呈现的，不含日期index序列的,关于各种代码,标的说明信息的数据。\n参数：att - 数据标签,必填. 了解函数目前支持的数据标签目录，见self.get_menu("get_1d_att"); timeout – 等待服务器返回数据的最长时秒, 默认 200 秒\n返回:集合数据\n更新周期:每个交易日'
get_daily_text = 'get_daily\n简介: 函数提供股票、ETF、指数等标的物日线相关数据\n参数：code - 证券代码,必填，详阅self.menu("code");name: daily数据名称,默认"daily",见 self.menu("get_daily_name"); start_date/end_date/sample_size - 交易日序列参数，选填，详见self.menu("date_range"); adj_price - 返回前复权(q), 后复权(h), 或按指定日期中间复权的价格, 注意, 复权价根据日分红再投资收益值进行反向推导,默认不作复权处理;add2context - bool, 选填,是否把结果保存到context默认 False; timeout - 等待服务器返回数据的最长时秒, 默认200秒\n返回：None(add2context=True),时间序列表格日线数据,报错信息'
get_hist_share_text = 'get_hist_share\n简介: 函数提供上市公司各类股本历史变动明细\n参数：code - 证券代码,必填，timeout - 等待服务器返回数据的最长时秒, 默认200秒; translate,是否返回中文数据标签,选填,默认False\n返回：时间序列表格日线数据,报错信息'
#get_daily_pro_text = 'get_daily_pro\n简介: 函数提供股票、ETF、指数，日线扩展数据，对比于get_daily函数, get_daily_pro 可供用户自行设定返回表格数据中的标签变量,了解目前支持的日线数据标签见self.get_menu("get_daily_pro_att") \n参数：code - 证券代码,必填，详阅self.get_menu("code"); start_date/end_date/sample_size - 交易日序列参数，必填，详见self.get_menu("date_range"); att, 必填, 详见self.get_menu("att");add2context – bool, 选填,是否把结果保存到context默认 False; timeout - 等待服务器返回数据的最长时秒, 默认200秒\n返回：None(add2context=True),时间序列表格日线数据,报错信息'
get_stock_fs_text = 'get_stock_fs\n简介: 提供上市公司财务报表汇中表格数据，具体数据说明参考get_menu(get_stock_fs_name)\n参数：name - 财务报表类别,必填，必须为以下其中一项：资产报表 balance,损益表 income,现金流量表 cashflow ;code - 证券代码,必填 start_year - 查询数据起始年.必填,格式yyyy; timeout - 等待服务器返回数据的最长时秒, 默认200秒; translate,是否返回中文数据标签,选填,默认False\n 返回：时间序列表格日线数据,报错信息'
get_HSGT_text = 'get_HSGT\n简介: 函数用于沪深港通类数据接口\n参数：name: HSGT数据名称,start_date/end_date/sample_size - 交易日序列参数，选填, timeout - 等待服务器返回数据的最长时秒, 默认200秒\n返回：pd.DataFrame数据表单,报错文本'
get_econ_text = 'get_econ\n简介: 函数用于获取经济数据接口\n参数：name: econ数据名称,start_date/end_date/sample_size - 交易日序列参数，选填, timeout - 等待服务器返回数据的最长时秒, 默认200秒\n返回：pd.DataFrame数据表单'
context = 'context\n简介: 缓存数据库,为用户回测程序提供模拟实盘数据,可直接访问self.context, 复合dictionary格式,首层子目录由目前支持的数据频率分类.'
add_context = 'add_context\n简介: 函数用于添加用于回测的标的代码至相关context数据空间\n参数：freq:数据频率-daily/tick/min,必填,code:标的代码集合,必填,返回：None或报错str'
save_context = 'save_context\n简介: 函数用于保存context数据至本地\n参数：dir_path: 本地目录路径,必填,freq:需保存的数据频率,选填,默认=None保存所有频率数据,code: 需保存的标的代码,选填,默认=None 保存所有标的,file_format,存储文件格式,选填,默认=pic,即pickle文件格式,另可选csv文件格式'
load_context = 'load_context\n简介: 函数用于读取本地离线数据至context目录\n参数：dir_path: 本地数据目录路径,需与用于save_context的目录一致,必填,freq:需保存的数据频率,选填,默认=None尝试读取所有频率数据,code: 需读取的标的代码,选填,默认=None 尝试读取所有标的,file_format,读取那种文件格式的数据,选填,默认=pic,即pickle文件格式,另可选csv文件格式'
islogin = 'islogin\n简介 函数返回登录状态,True表示已成功登录数据服务器False表示未成功登录'
get_btdata_text ="get_btdata\n简介:函数用于下载补充回测时间轴内context数据\n参数：trade_func:数据频率-daily/tick/min,必填;code:标的代码集合,选填,默认包含所有在self.context[freq]下的标的代码; start_date,回测时间轴起始日,格式yyyy-mm-dd,必填;end_date,回测时间轴结束日,格式yyyy-mm-dd,必填;overwrite,是否覆盖context目录下已存在的数据点,选填,默认=False,即已存在的数据点不会被覆盖,将节省API网络资源和下载时间"
run_bt_text = "run_bt\n简介:函数根据用户交易函数对context数据进行实盘回测运算,运算结果直接添加至context\n参数：trade_func:用户编写的交易函数,详见self.get_menu('trade_func'), 必填;freq:数据频率-daily/tick/min,必填; start_time,回测时间轴起始日,,必填;end_date,回测时间轴结束日,格式yyyy-mm-dd,必填;code_base: 回测程序包含的标的代码集合,选填,默认包含所有在self.context[freq]下的标的代码; trade_cost_rate: 模拟实盘交易费率,选填,默认每笔交易金额的万分之一,最低消费1分;thread_pool: 运算线程数目, 当标的合集包含多个标的证券时, 可使用多线程尝试提高运行速度, 默认使用单线程, 返回: None,报错文本"
cal_portf_text ="cal_portf\n简介: 函数计算回测策略综合收益并生成报表, 使用前必须确保针对所有的标的回测计算已经完成并写入self.context\n参数：freq: 分析对象的数据频率-daily/tick/min,必填; init_fund: 模拟实盘投资的起始资本额,默认100万,选填; margin_cost: 当模拟实盘账户现金不足是, 融资利率, 不设融资上限, 用户需自行监控爆仓的情况; ss_cost: 融券利率, 不设融券障碍, 用户需按实际情况设定障碍; ON_rate: 账户中现金的隔夜回报年化利率,返回: 如有错误返回错误报告文本否则返回每日组合收益表单, 综合收益统计表单, 两个表单以tuple格式返回, 其中收益统计表单各项指标说明如下: total_trading_points交易点总数,active_rate信号输出率,即有信号的交易日占比, ave_t_cash平均持有现金数额(每个交易节点),ave_t_asset平均持有交易标的价值数额, init_pvalue起始资产额度, end_pvalue回测期末资产额度, max_pvalue回测期组合资产额最大值, min_pvalue回测期组合资产额最小值, total_trade_cost总交易费用, total_int_paid融资利率费用, overall_return期末综合回报率(非年化), ave_t_return平均每个交易节点收益率(非年化), std_t_return 交易节点收益协方差, MDD最大回撤, sharpe_ratio夏普比率"
trade_func_text = "trade_func\n简介: 用户根据回测框架编写的交易函数, 回测程序在每一个交易点(如,日线,分钟线,tick跳价), 将发生在该节点时间戳前的context数据作为信息集供与交易函数, 该设计模拟投资者在实盘中的交易决策.\n 对交易函数框架要求如下: 1.必须包含context参数并置于首位,用户可添加其他自定义参数; 2.必须以文本格式返回符合规范的交易信号; 3.下单交易信号以 dirction@price表示,其中dirction代表买卖方向,用'B'表示买入,'S'表示卖出,price即信号买入/卖出价,例: B@3.31, 表示以3.31元买入, 注意买卖信号同样代表交易结果, 用户需考虑撮合机制并在交易函数中协调实现; 4. 交易函数返回'0'表示无交易,并下单清空持有仓位, 'HB'/'HS' 分别表示继续持有多头或空头仓位至下一个交易点\n 工作原理: 用户自定交易函数一般套用于回测函数trade_func位置. 回测函数模拟实盘时间流, 将每个交易点对应的context信息集, 即模拟环境下投资者能得到的市场数据, 作为参数向trade_func推送并得到相应的交易信号, 回测程序将根据该交易信号计算收益."
event_study_text = 'event_study\n简介: 事件研究框架函数, 程序根据用户提供的事件定义函数, 对context数据进行筛选,对符合条件的交易点进行标签以及数据筛查.\n参数：target:指定的context数据(例:daily,tick), event_func:用户编写的事件函数(详见self.menu("event_func"),event_name: 事件标签名, start_time,回测时间轴起点,选填,默认为None,表示使用context数据最早时间点, end_time,回测时间轴终点,选填,默认为None,表示使用context数据的最后时间点;code_base: 回测程序包含的标的代码集合'
event_func_text = "event_func\n简介:用户指定的事件函数须符合以下基本要求: 1.以t日可用context数据作为基础参数, 2. 返回一组元组数据, 其中首位为二维代码 1/0用于表示是否赋予event标签,次位返回 None 或与该event相关的用于后期统计的数据"



menu_basic_cn = {'intro':intro_text,
                 'code':code_text,
                 'att':att_text,
                 'usage':usage_text,
                 'context':context,
                 'date_range':date_range_text,
                 'code':code_text,
                 'login':login_text,
                 'get_menu':get_menu_text,
                 'get_1d':get_1d_text,           
                 'get_daily':get_daily_text,
             #    'get_daily_pro':get_daily_pro_text,      
                 'get_tick':get_tick_text,
                 'get_hf5':get_hf5_text,
                 'get_min': get_min_text,
                 'get_HSGT':get_HSGT_text,
                 'get_econ': get_econ_text,
                 'add_context':add_context,
                 'save_context':save_context,
                 'load_context':load_context,
                 'islogin':islogin,
                 'get_btdata':get_btdata_text,
                 'run_bt':run_bt_text,
                 'cal_portf': cal_portf_text,
                 "trade_func":trade_func_text,
                 "event_study":event_study_text,
                 "event_func":event_func_text,
                 "get_stock_fs":get_stock_fs_text,
                 "get_hist_share":get_hist_share_text
                 }
