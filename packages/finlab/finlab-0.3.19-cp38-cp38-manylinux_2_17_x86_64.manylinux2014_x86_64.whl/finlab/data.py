import os
import re
import time
import json
import pickle
import logging
import datetime
import numpy as np
import pandas as pd
from io import BytesIO
import finlab
from finlab.utils import check_version, requests
from finlab.market_info import TWMarketInfo, MarketInfo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CacheStorage():

    def __init__(self):
        """將歷史資料儲存於快取中
          Examples:

              欲切換成以檔案方式儲存，可以用以下之方式：

              ``` py
              from finlab import data
              data.set_storage(data.CacheStorage())
              close = data.get('price:收盤價')
              ```

              可以直接調閱快取資料：

              ``` py
              close = data._storage._cache['price:收盤價']
              ```
        """

        self._cache = {}
        self._cache_time = {}
        self._cache_expiry = {}
        self._stock_names = {}

    @staticmethod
    def now():
        return datetime.datetime.now(tz=datetime.timezone.utc)

    def set_dataframe(self, name, df, expiry=None):
        self._cache[name] = df
        self._cache_time[name] = self.now()
        self._cache_expiry[name] = expiry or self.now()

    def set_stock_names(self, stock_names):
        self._stock_names = {**self._stock_names, **stock_names}

    def get_time_created(self, name):

        if name not in self._cache or name not in self._cache_time:
            return None

        return self._cache_time[name]

    def get_time_expired(self, name):

        if name in self._cache_expiry:
            return self._cache_expiry[name]

        return None

    def get_dataframe(self, name):

        # not exists
        if name not in self._cache or name not in self._cache_time:
            return None

        return self._cache[name]

    def get_stock_names(self):
        return self._stock_names


class FileStorage():
    def __init__(self, path='finlab_db'):
        """將歷史資料儲存於檔案中
          Examples:

              欲切換成以檔案方式儲存，可以用以下之方式：

              ``` py
              from finlab import data
              data.set_storage(data.FileStorage())
              close = data.get('price:收盤價')
              ```

              可以在本地端的 `./finlab_db/price:收盤價.pickle` 中，看到下載的資料，
              可以使用 `pickle` 調閱歷史資料：
              ``` py
              import pickle
              close = pickle.load(open('finlab_db/price:收盤價.pickle', 'rb'))
              ```
        """
        self._path = path
        self._cache = {}
        self._stock_names = None
        self._expiry = {}

        if not os.path.isdir(path):
            os.mkdir(path)

        f_stock_names = os.path.join(path, 'stock_names.pkl')

        if not os.path.isfile(f_stock_names):
            with open(f_stock_names, 'wb') as f:
                pickle.dump({}, f)
        else:
            with open(f_stock_names, 'rb') as f:
                self._stock_names = pickle.load(f)

        f_expiry = os.path.join(self._path, 'expiry.pkl')

        if not os.path.isfile(f_expiry):
            with open(f_expiry, 'wb') as f:
                pickle.dump({}, f)
        else:
            with open(f_expiry, 'rb') as f:
                self._expiry = pickle.load(f)

    def set_dataframe(self, name, df, expiry=None):
        file_path = os.path.join(
            self._path, name + '.pickle').replace(':', '#')
        df.to_pickle(file_path)
        self._cache[name] = df
        self._expiry[name] = expiry or CacheStorage.now()

        with open(os.path.join(self._path, 'expiry.pkl'), 'wb') as f:
            pickle.dump(self._expiry, f)

    def get_time_created(self, name):

        # check existence
        file_path = os.path.join(
            self._path, name + '.pickle').replace(':', '#')

        if not os.path.isfile(file_path):
            return None

        return datetime.datetime.fromtimestamp(
            os.path.getmtime(file_path), tz=datetime.timezone.utc)

    def get_time_expired(self, name):

        if name in self._expiry:
            return self._expiry[name]

        return None

    def get_dataframe(self, name):

        if name in self._cache:
            return self._cache[name]

        file_path = os.path.join(
            self._path, name + '.pickle').replace(':', '#')

        if os.path.isfile(file_path):
            ret = pd.read_pickle(file_path)
            self._cache[name] = ret
            return ret

        return None

    def set_stock_names(self, stock_names):
        self._stock_names = {**self._stock_names, **stock_names}

        with open(os.path.join(self._path, 'stock_names.pkl'), 'wb') as f:
            pickle.dump(self._stock_names, f)

    def get_stock_names(self):

        if self._stock_names is not None:
            return self._stock_names

        with open(os.path.join(self._path, 'stock_names.pkl'), 'rb') as f:
            stock_names = pickle.load(f)
        self._stock_names = stock_names
        return stock_names


_storage = CacheStorage()
universe_stocks = set()


def set_storage(storage):
    """設定本地端儲存歷史資料的方式
    假設使用 `data.get` 獲取歷史資料則，在預設情況下，程式會自動在本地複製一份，以避免重複下載大量數據。
    storage 就是用來儲存歷史資料的接口。我們提供兩種 `storage` 接口，分別是 `finlab.data.CacheStorage` (預設) 以及
    `finlab.data.FileStorage`。前者是直接存在記憶體中，後者是存在檔案中。詳情請參考 `CacheStorage` 和 `FileStorage` 來獲得更詳細的資訊。
    在預設情況下，程式會自動使用 `finlab.data.CacheStorage` 來存取重複索取之歷史資料。

    Args:
        storage (data.Storage): The interface of storage

    Examples:

        欲切換成以檔案方式儲存，可以用以下之方式：

        ``` py
        from finlab import data
        data.set_storage(data.FileStorage())
        close = data.get('price:收盤價')
        ```

        可以在本地端的 `./finlab_db/price:收盤價.pickle` 中，看到下載的資料，
        可以使用 `pickle` 調閱歷史資料：
        ``` py
        import pickle
        close = pickle.load(open('finlab_db/price:收盤價.pickle', 'rb'))
        ```
    """

    global _storage
    _storage = storage


class universe():
    def __init__(self, market='ALL', category='ALL'):
        """當呼叫 `data.get` 或是 `data.indicator` 時，返回產業相關類股。

        Args:
            market (str): Universe market type. ex: `ALL`, `TSE`, `OTC`, `TSE_OTC`, `ETF`, `STOCK_FUTURE`
            category (str): Stock categories, can be either a string or a list. ex: `光電業`, `其他`, `其他電子業`, `化學工業`, `半導體`, `塑膠工業`, `存託憑證`, `建材營造`, `文化創意業`, `橡膠工業`, `水泥工業`,`汽車工業`, `油電燃氣業`, `玻璃陶瓷`, `生技醫療`, `生技醫療業`, `紡織纖維`, `航運業`, `觀光事業`, `貿易百貨`, `資訊服務業`, `農業科技`, `通信網路業`, `造紙工業`, `金融`, `鋼鐵工業`, `電器電纜`, `電子商務`, `電子通路業`, `電子零組件`, `電機機械`, `電腦及週邊`, `食品工業`

        Examples:

            想要當鋼鐵人、航海王，可以用以下方法將這些類股一次選出來
            ``` py
            with universe('TSE_OTC', ['鋼鐵工業', '航運業']):
                close_subset = data.get('price:收盤價')
                print(close_subset)
            ```

            | date       |   2002 |   2006 |   ..   |   2008 |   2009 |
            |:-----------|-------:|-------:|-------:|-------:|-------:|
            | 2007-04-23 |  39.65 |  38.3  |   ..   |   7.8  |  17.55 |
            | 2007-04-24 |  39.85 |  38.85 |   ..   |   8.34 |  17.5  |
            | 2007-04-25 |  39.25 |  38.1  |   ..   |   8.25 |  17.3  |
            | 2007-04-26 |  39    |  37.85 |   ..   |   8.2  |  17.3  |
            | 2007-04-27 |  38.2  |  37.2  |   ..   |   7.88 |  16.6  |

        """
        self._market = market
        self._category = category
        self._previous_stocks = set()

    def __enter__(self):
        global universe_stocks
        self._previous_stocks = universe_stocks
        set_universe(self._market, self._category)
        return self

    def __exit__(self, type, value, traceback):
        global universe_stocks
        universe_stocks = self._previous_stocks


def set_universe(market: str = 'ALL', category='ALL'):
    """Set subset of stock ids when retrieve data using data.get or data.indicator

    Args:
        market (str): universe market type. ex: 'ALL', 'TSE', 'OTC', 'TSE_OTC', 'ETF', 'STOCK_FUTURE'
        category (str): stock categories, can be either a string or a list. ex: '光電業', '其他', '其他電子業',
   '化學工業', '半導體', '塑膠工業', '存託憑證', '建材營造', '文化創意業', '橡膠工業', '水泥工業',
   '汽車工業', '油電燃氣業', '玻璃陶瓷', '生技醫療', '生技醫療業', '紡織纖維', '航運業', '觀光事業', '貿易百貨',
   '資訊服務業', '農業科技', '通信網路業', '造紙工業', '金融', '鋼鐵工業', '電器電纜', '電子商務',
   '電子通路業', '電子零組件', '電機機械', '電腦及週邊', '食品工業'


    """

    categories = get('security_categories')

    market_match = pd.Series(True, categories.index)

    if market == 'ALL':
        pass
    elif market == 'TSE':
        market_match = categories.market == 'sii'
    elif market == 'OTC':
        market_match = categories.market == 'otc'
    elif market == 'TSE_OTC':
        market_match = (categories.market == 'sii') | (
            categories.market == 'otc')
    elif market == 'ETF':
        market_match = categories.market == 'other_securities'
    elif market == 'STOCK_FUTURE':
        futures_and_options = get('single_stock_futures_and_equity_options_underlying')
        futures_and_options = futures_and_options[~futures_and_options['stock_id'].duplicated()]
        futures_and_options = categories.merge(futures_and_options, how='left', on='stock_id')
        market_match = futures_and_options['是否為股票期貨標的'] == 'Y'

    category_match = pd.Series(True, categories.index)

    if category == 'ALL':
        pass
    else:
        if isinstance(category, str):
            category = [category]

        matched_categories = set()
        all_categories = set(categories.category)
        for ca in category:
            matched_categories |= (
                set([c for c in all_categories if isinstance(c, str) and re.search(ca, c)]))
        category_match = categories.category.isin(matched_categories)

    global universe_stocks
    universe_stocks = set(categories.stock_id[market_match & category_match])


def get(dataset: str, save_to_storage: bool = True, force_download=False):
    """下載歷史資料

    請至[歷史資料目錄](https://ai.finlab.tw/database) 來獲得所有歷史資料的名稱，即可使用此函式來獲取歷史資料。
    假設 `save_to_storage` 為 `True` 則，程式會自動在本地複製一份，以避免重複下載大量數據。

    Args:
        dataset (str): The name of dataset.
        save_to_storage (bool): Whether to save the dataset to storage for later use.

    Returns:
        (pd.DataFrame): financial data

    Examples:

        欲下載所有上市上櫃之收盤價歷史資料，只需要使用此函式即可:

        ``` py
        from finlab import data
        close = data.get('price:收盤價')
        close
        ```

        | date       |   0015 |   0050 |   0051 |   0052 |   0053 |
        |:-----------|-------:|-------:|-------:|-------:|-------:|
        | 2007-04-23 |   9.54 |  57.85 |  32.83 |  38.4  |    nan |
        | 2007-04-24 |   9.54 |  58.1  |  32.99 |  38.65 |    nan |
        | 2007-04-25 |   9.52 |  57.6  |  32.8  |  38.59 |    nan |
        | 2007-04-26 |   9.59 |  57.7  |  32.8  |  38.6  |    nan |
        | 2007-04-27 |   9.55 |  57.5  |  32.72 |  38.4  |    nan |

    """
    check_version()

    global universe_stocks
    global _storage

    not_available_universe_stocks = [
        'benchmark_return', 'institutional_investors_trading_all_market_summary',
        'margin_balance', 'intraday_trading_stat',
        'stock_index_price', 'stock_index_vol',
        'taiex_total_index', 'broker_info',
        'rotc_monthly_revenue', 'rotc_price',
        'world_index', 'rotc_broker_trade_record',
        'us_price', 'us_sp500',
        'us_tickers', 'security_categories',
        ]

    def refine_stock_id(ret):

        if dataset.split(':')[0] in not_available_universe_stocks:
            return ret
        if ':' in dataset:
            return ret if not universe_stocks else ret[ret.columns.intersection(universe_stocks)]
        if 'stock_id' in ret.columns:
            return ret if not universe_stocks else ret.loc[ret['stock_id'].isin(universe_stocks)]

        return ret

    # not expired
    time_expired = _storage.get_time_expired(dataset)
    if time_expired and time_expired > CacheStorage.now() and not force_download:
        return refine_stock_id(_storage.get_dataframe(dataset))

    # request for auth url
    url = 'https://asia-east2-fdata-299302.cloudfunctions.net/auth_generate_data_url'
    params = {
        'api_token': finlab.get_token(),
        'bucket_name': 'finlab_tw_stock_item',
        'blob_name': dataset.replace(':', '#') + '.feather'
    }

    time_saved = _storage.get_time_created(dataset)
    if time_saved and not force_download:
        params['time_saved'] = time_saved.strftime('%Y%m%d%H%M%S')

    res = requests.post(url, params)

    try:
        url_data = res.json()
    except:
        raise Exception("Cannot get response from data server.")

    # use cache
    if 'url' in url_data and url_data['url'] == '':
        return refine_stock_id(_storage.get_dataframe(dataset))

    if 'quota' in url_data:
        logger.warning(
            f'{dataset} -- Daily data usage: {url_data["quota"]:.1f} / {url_data["limit_size"]} MB')

    if 'error' in url_data:

        if url_data['error'] in [
            'request not valid',
            'User not found',
            'api_token not valid',
                'api_token not match', ]:
            finlab.login()
            return get(dataset, save_to_storage)

        raise Exception(f"**Error: {url_data['error']}")

    assert 'url' in url_data

    res = requests.get(url_data['url'])
    df = pd.read_feather(BytesIO(res.content))

    # set date as index
    if 'date' in df:
        df.set_index('date', inplace=True)

        table_name = dataset.split(':')[0]
        if table_name in ['tw_total_pmi', 'tw_total_nmi', 'tw_industry_nmi', 'tw_industry_pmi']:
            if isinstance(df.index[0], pd.Timestamp):
                close = get('price:收盤價')
                df.index = df.index.map(
                    lambda d: d if len(close.loc[d:]) == 0 or d < close.index[0] else close.loc[d:].index[0])

        # if column is stock name
        if (df.columns.str.find(' ') != -1).all():

            # remove stock names
            df.columns = df.columns.str.split(' ').str[0]

            # combine same stock history according to sid
            check_numeric_dtype = pd.api.types.is_numeric_dtype(df.values)
            if check_numeric_dtype:
                df = df.transpose().groupby(level=0).mean().transpose()
            else:
                df = df.fillna(np.nan).transpose().groupby(
                    level=0).last().transpose()

        df = finlab.dataframe.FinlabDataFrame(df)

        if table_name in ['monthly_revenue', 'rotc_monthly_revenue']:
            df = df._index_date_to_str_month()
        elif table_name in ['financial_statement', 'fundamental_features']:
            df = df._index_date_to_str_season()
        elif table_name in ['us_fundamental']:
            df = df._index_date_to_str_season('-US')
    # save cache
    if save_to_storage:
        expiry = datetime.datetime.strptime(
                url_data['time_scheduled'], '%Y%m%d%H%M%S').replace(tzinfo=datetime.timezone.utc)\
                if 'time_scheduled' in url_data else None

        _storage.set_dataframe(dataset, df, expiry=expiry)

    return refine_stock_id(df)


def get_input_args(attr):
    input_names = attr.input_names
    refine_input_names = []
    for key, val in input_names.items():
        if 'price' in key:
            if isinstance(val, list):
                refine_input_names += val
            elif isinstance(val, str):
                refine_input_names.append(val)

    return refine_input_names

def indicator(indname, adjust_price=False, resample='D', market:MarketInfo=TWMarketInfo(), **kwargs):
    """支援 Talib 和 pandas_ta 上百種技術指標，計算 2000 檔股票、10年的所有資訊。

    在使用這個函式前，需要安裝計算技術指標的 Packages

    * [Ta-Lib](https://github.com/mrjbq7/ta-lib)
    * [Pandas-ta](https://github.com/twopirllc/pandas-ta)

    Args:
        indname (str): 指標名稱，
            以 TA-Lib 舉例，例如 SMA, STOCH, RSI 等，可以參考 [talib 文件](https://mrjbq7.github.io/ta-lib/doc_index.html)。

            以 Pandas-ta 舉例，例如 supertrend, ssf 等，可以參考 [Pandas-ta 文件](https://twopirllc.github.io/pandas-ta/#indicators-by-category)。
        adjust_price (bool): 是否使用還原股價計算。
        resample (str): 技術指標價格週期，ex: `D` 代表日線, `W` 代表週線, `M` 代表月線。
        **kwargs (dict): 技術指標的參數設定，TA-Lib 中的 RSI 為例，調整項為計算週期 `timeperiod=14`。
    建議使用者可以先參考以下範例，並且搭配 talib官方文件，就可以掌握製作技術指標的方法了。
    """
    package = None

    try:
        from talib import abstract
        import talib
        attr = getattr(abstract, indname)
        package = 'talib'
    except:
        try:
            import pandas_ta
            # test df.ta has attribute
            getattr(pd.DataFrame().ta, indname)
            attr = lambda df, **kwargs: getattr(df.ta, indname)(**kwargs)
            package = 'pandas_ta'
        except:
            raise Exception(
                "Please install TA-Lib or pandas_ta to get indicators.")

    close = market.get_price('close', adj=adjust_price)
    open_ = market.get_price('open', adj=adjust_price)
    high = market.get_price('high', adj=adjust_price)
    low = market.get_price('low', adj=adjust_price)
    volume = market.get_price('volume', adj=adjust_price)

    if resample.upper() != 'D':
        close = close.resample(resample).last()
        open_ = open_.resample(resample).first()
        high = high.resample(resample).max()
        low = low.resample(resample).min()
        volume = volume.resample(resample).sum()

    dfs = {}
    default_output_columns = None
    for key in close.columns:

        prices = {'open': open_[key].ffill(),
                  'high': high[key].ffill(),
                  'low': low[key].ffill(),
                  'close': close[key].ffill(),
                  'volume': volume[key].ffill()}

        if package == 'pandas_ta':
            prices = pd.DataFrame(prices)
            s = attr(prices, **kwargs)

        elif package == 'talib':
            abstract_input = list(attr.input_names.values())[0]
            abstract_input = get_input_args(attr)

            # quick fix talib bug
            if indname == 'OBV':
                abstract_input = ['close', 'volume']

            if indname == 'BETA':
                abstract_input = ['high', 'low']

            if isinstance(abstract_input, str):
                abstract_input = [abstract_input]
            paras = [prices[k] for k in abstract_input]
            s = attr(*paras, **kwargs)
        else:
            raise Exception("Cannot determine technical package from indname")

        if isinstance(s, list):
            s = {i: series for i, series in enumerate(s)}

        if isinstance(s, np.ndarray):
            s = {0: s}

        if isinstance(s, pd.Series):
            s = {0: s.values}

        if isinstance(s, pd.DataFrame):
            s = {i: series.values for i, series in s.items()}

        if default_output_columns is None:
            default_output_columns = list(s.keys())

        for colname, series in s.items():
            if colname not in dfs:
                dfs[colname] = {}
            dfs[colname][key] = series if isinstance(
                series, pd.Series) else series

    newdic = {}
    for key, df in dfs.items():
        newdic[key] = pd.DataFrame(df, index=close.index)

    ret = [newdic[n] for n in default_output_columns]
    ret = [d.apply(lambda s:pd.to_numeric(s, errors='coerce')) for d in ret]

    if len(ret) == 1:
        return finlab.dataframe.FinlabDataFrame(ret[0])

    return tuple([finlab.dataframe.FinlabDataFrame(df) for df in ret])


def get_strategies(api_token=None):
    """取得已上傳量化平台的策略回傳資料。

    可取得自己策略儀表板上的數據，例如每個策略的報酬率曲線、報酬率統計、夏普率、近期部位、近期換股日...，
    這些數據可以用來進行多策略彙整的應用喔！


    Args:
        api_token (str): 若未帶入finlab模組的api_token，會自動跳出[GUI](https://ai.finlab.tw/api_token/)頁面，
                         複製網頁內的api_token貼至輸入欄位即可。
    Returns:
        (dict): strategies data
    Response detail:

        ``` py
        {
          strategy1:{
            'asset_type': '',
            'drawdown_details': {
               '2015-06-04': {
                 'End': '2015-11-03',
                 'Length': 152,
                 'drawdown': -0.19879090089478024
                 },
                 ...
              },
            'fee_ratio': 0.000475,
            'last_trading_date': '2022-06-10',
            'last_updated': 'Sun, 03 Jul 2022 12:02:27 GMT',
            'ndays_return': {
              '1': -0.01132480035770611,
              '10': -0.0014737286933147464,
              '20': -0.06658015749110646,
              '5': -0.002292995729485159,
              '60': -0.010108700314771735
              },
            'next_trading_date': '2022-06-10',
            'positions': {
              '1413 宏洲': {
                'entry_date': '2022-05-10',
                'entry_price': 10.05,
                'exit_date': '',
                'next_weight': 0.1,
                'return': -0.010945273631840613,
                'status': '買進',
                'weight': 0.1479332345384493
                },
              'last_updated': 'Sun, 03 Jul 2022 12:02:27 GMT',
              'next_trading_date': '2022-06-10',
              'trade_at': 'open',
              'update_date': '2022-06-10'
              },
            'return_table': {
              '2014': {
                'Apr': 0.0,
                'Aug': 0.06315180932606546,
                'Dec': 0.0537589857541485,
                'Feb': 0.0,
                'Jan': 0.0,
                'Jul': 0.02937490104459939,
                'Jun': 0.01367930162104769,
                'Mar': 0.0,
                'May': 0.0,
                'Nov': -0.0014734320286596825,
                'Oct': -0.045082529665408266,
                'Sep': 0.04630906972509852,
                'YTD': 0.16626214846456966
                },
                ...
              },
            'returns': {
              'time': [
                '2014-06-10',
                '2014-06-11',
                '2014-06-12',
                ...
                ],
              'value': [
                100,
                99.9,
                100.2,
                ...
                ]
              },
            'stats': {
              'avg_down_month': -0.03304015302646822,
              'avg_drawdown': -0.0238021414698247,
              'avg_drawdown_days': 19.77952755905512,
              'avg_up_month': 0.05293384465715908,
              'cagr': 0.33236021285588846,
              'calmar': 1.65261094975066,
              'daily_kurt': 4.008888367138843,
              'daily_mean': 0.3090784769257415,
              'daily_sharpe': 1.747909002374217,
              'daily_skew': -0.6966018726321078,
              'daily_sortino': 2.8300677082214034,
              ...
              },
            'tax_ratio': 0.003,
            'trade_at': 'open',
            'update_date': '2022-06-10'
            },
          strategy2:{...},
          ...}
        ```
    """
    if api_token is None:
        api_token = finlab.get_token()

    request_args = {
        'api_token': api_token,
    }

    url = 'https://asia-east2-fdata-299302.cloudfunctions.net/auth_get_strategies'
    response = requests.get(url, request_args)
    status_code = response.status_code
    if status_code in [400, 401]:
        logger.error("The authentication code is wrong or the account is not existed."
                     "Please input right authentication code or register account ")
        return {}
    try:
        return json.loads(response.text)
    except:
        pass

    return response.text


def search(keyword=None, display_info=['name', 'description', 'type']):
    """查詢與取得資料庫目錄資訊。

    查詢FinLab資料庫目錄中的資料表名稱或項目欄位名稱是否包含關鍵字，方便搜尋資料庫是否存在目標資料。

    Args:
        keyword (str): 欲查詢關鍵字。
        display_info (list):指定顯示的資訊項目，預設只顯示「資料表英文代稱、資料表的中文描述、資料表欄位名稱」，若設定為None，則顯示全部資訊。

    Returns:
        (list): database information

    Response detail:
        ``` py
        [{'name': 'financial_statement',
          'description': '財報',
          'type': {'存貨': 'float-資產負債表(仟元)', '存貨_增加_減少': 'float-單季現金流量表(仟元)'}},
         {'name': 'fundamental_features',
          'description': '財務指標',
          'type': {'存貨週轉率': 'float-(%)'}},
         {'name': 'tw_total_pmi',
          'description': '台灣製造業採購經理人指數',
          'type': {'存貨': 'float', '客戶存貨': 'float'}},...]

        ```
    Examples:

        ``` py

        # 查詢各資料表的欄位名稱含有'存貨'關鍵字的相關資料表資訊
        ex1 = search_database_category(keyword='存貨')
        # 取得資料庫所有資訊
        ex2 = search_database_category(display_info=None)
        ```
    """
    if not hasattr(search, 'db_info'):
        res = requests.get('https://asia-east2-fdata-299302.cloudfunctions.net/get_data_info')
        search.db_info = json.loads(res.text)['data']

    db_info = search.db_info

    if display_info:
        db_info = [{i: table[i] for i in display_info} for table in db_info]

    result = []
    if keyword:
        result = [table for table in db_info if (re.search(keyword, table['description'], re.IGNORECASE)) or (
            re.search(keyword, table['name'], re.IGNORECASE))]
        result_tables = [table['name'] for table in result]

    def check_column_contains_keyword(table, keyword):
        table = table.copy()
        keyword_exist = {k: v for k, v in table['type'].items() if re.search(keyword, k, re.IGNORECASE)}
        if len(keyword_exist) > 0:
            table['type'] = keyword_exist
            return table

    if keyword:
        for table in db_info:
            if table['name'] not in result_tables:
                checked_table = check_column_contains_keyword(table, keyword=keyword)
            if checked_table is not None:
                result.append(checked_table)
    return result
