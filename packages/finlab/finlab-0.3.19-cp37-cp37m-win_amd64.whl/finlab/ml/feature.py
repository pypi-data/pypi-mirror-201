from talib import abstract
import numpy as np
import re
import talib
import logging
from functools import lru_cache
import pandas as pd
from finlab import data
from typing import List, Protocol, Dict, Optional, Generator
import finlab.market_info
from finlab.dataframe import FinlabDataFrame
import random
import gc
from finlab import ml
from finlab.ml.utils import resampler


class IndicatorName():
  
    @staticmethod
    def encode(package_name, func, output, params):

        encoded = package_name + '.' + func + '__' + output + '__'
        for k, v in params.items():
          encoded += f'{k}__{v}__'

        return encoded
    
    @staticmethod
    def decode(encoded):
      
        tokens = encoded.split('__')
        
        func = tokens[0].split('.')[-1]
        output = tokens[1]
        params = dict(zip(tokens[2:][::2], tokens[2:][1::2]))

        return func, output, params


class TalibIndicatorFactory():

    def __init__(self, market:Optional[finlab.market_info.MarketInfo]=None):
        if market:
            self.market = market
        else:
            self.market = ml.get_market()
    @staticmethod
    def set_dynamic_types(f, params):

        ret = {}
        for k, v in params.items():
            try:
                f.set_parameters(**{k:v})

            except Exception as ex:
                s = str(ex)
                regex = re.compile(r'expected\s([a-z]*),\s')
                match = regex.search(s)
                correct_type = match.group(1)
                v = {'int':int, 'float': float}[correct_type](v)
                f.set_parameters(**{k:v})

            ret[k] = v

        return ret
  
    def calculate_indicator(self, func, output, params, adj=False):
      
        func = func.split('.')[0]

        # get ith output
        f = getattr(abstract, func)
        org_params = f.parameters
        params = self.set_dynamic_types(f, params)
        f.set_parameters(org_params)
        target_i = -1
        for i, o in enumerate(f.output_names):
            if o == output:
                target_i = i
                break

        if target_i == -1:
            raise Exception("Cannot find output names")
        
        # apply talib
        indicator = data.indicator(func, adj=adj, market=ml.get_market(), **params)

        if isinstance(indicator, tuple):
            indicator = indicator[target_i]

        # normalize result
        if func in TalibIndicatorFactory.normalized_funcs():
            indicator /= self.market.get_price('close', adj=adj)

        return indicator
    
    @staticmethod
    def all_functions():
        talib_categories = [
          'Cycle Indicators', 
          'Momentum Indicators', 
          'Overlap Studies', 
          'Price Transform', 
          'Statistic Functions', 
          'Volatility Indicators']

        talib_functions = sum([talib.get_function_groups()[c] for c in talib_categories], [])
        talib_functions = ['talib.'+f for f in talib_functions if f != 'SAREXT' and f != 'MAVP']
        return talib_functions

    @staticmethod
    @lru_cache
    def normalized_funcs():
      talib_normalized = talib.get_function_groups()['Overlap Studies']\
        + talib.get_function_groups()['Price Transform']\
        + ['APO', 'MACD', 'MACDEXT', 'MACDFIX', 'MOM', 'MINUS_DM', 'PLUS_DM', 'HT_PHASOR']
      return [t for t in talib_normalized]
    
    def generate_feature_names(self, func, lb, ub, n):

        func = func.split('.')[-1]

        if func == 'MAMA':
            return []

        f = getattr(abstract, func)
        outputs = f.output_names
        org_params = f.parameters
        params_lb = {k:v*lb for k, v in org_params.items()}
        params_ub = {k:v*ub for k, v in org_params.items()}
        
        min_value = {
          'signalperiod': 2,
          'timeperiod': 2,
          'fastperiod': 2,
          'slowperiod': 2,
          'timeperiod1': 2, 'timeperiod2': 2,
          'timeperiod3': 2,
          'fastk_period': 2, 
          'fastd_period': 2,
          'vfactor': 0,
        }

        ret = []
        for _ in range(n):

          new_params = {}
          for k, v in org_params.items():
            rvalue = np.random.random_sample(1)[0] * (params_ub[k] - params_lb[k]) + params_lb[k]
            rvalue = type(v)(rvalue)
            new_params[k] = rvalue
            
          
          if 'nbdevup' in new_params:
            new_params['nbdevup'] = 2
          if 'nbdevdn' in new_params:
            new_params['nbdevdn'] = 2
          if 'vfactor' in new_params:
            new_params['vfactor'] = float(random.uniform(0, 1))
          if 'nbdev' in new_params:
            new_params['nbdev'] = 2.5
            
          for p in new_params:
            if p in min_value and new_params[p] < min_value[p]:
              new_params[p] = min_value[p]
            
          for o in outputs:
            ret.append(IndicatorName.encode('talib', func, o, new_params))

        return list(set(ret))

class Factory(Protocol):
    def __init__(self, market:Optional[finlab.market_info.MarketInfo]) -> None:
        pass

    def all_functions(self) -> List[str]:
        return []

    def calculate_indicator(self, func, output, params) -> pd.DataFrame:
        return pd.DataFrame()

 
def ta_names(lb:int=1, ub:int=10, n:int=1, factory=None) -> List[str]:
    """
    Generate a list of technical indicator feature names.

    Args:
        lb (int): The lower bound of the multiplier of the default parameter for the technical indicators.
        ub (int): The upper bound of the multiplier of the default parameter for the technical indicators.
        n (int): The number of random samples for each technical indicator.
        factory (IndicatorFactory): A factory object to generate technical indicators.
            Defaults to TalibIndicatorFactory.

    Returns:
        List[str]: A list of technical indicator feature names.

    Example:

        ```
        import finlab.ml.feature as f


        # method 1: generate each indicator with random parameters
        features = f.ta()

        # method 2: generate specific indicator
        feature_names = ['talib.MACD__macdhist__fastperiod__52__slowperiod__212__signalperiod__75__']
        features = f.ta(feature_names, resample='W')

        # method 3: generate some indicator
        feature_names = f.ta_names()
        features = f.ta(feature_names)
        ```
    """

    if factory is None:
        factory = TalibIndicatorFactory()

    return sum([factory.generate_feature_names(f, lb, ub, n) for f in factory.all_functions()], [])


def ta(feature_names:Optional[List[str]], 
       factories=None,
       resample=None, 
       start_time=None, 
       end_time=None, 
       **kwargs) -> pd.DataFrame:
    """Calculate technical indicator values for a list of feature names.

    Args:
        feature_names (Optional[List[str]]): A list of technical indicator feature names. Defaults to None.
        factories (Optioanl[Dict[str, TalibIndicatorFactory]]): A dictionary of factories to generate technical indicators. Defaults to {"talib": TalibIndicatorFactory()}.
        resample (Optional[str]): The frequency to resample the data to. Defaults to None.
        start_time (Optional[str]): The start time of the data. Defaults to None.
        end_time (Optional[str]): The end time of the data. Defaults to None.
        **kwargs: Additional keyword arguments to pass to the resampler function.

    Returns:
        pd.DataFrame: technical indicator feature names and their corresponding values.
    """

    if factories is None:
        factories = {'talib':TalibIndicatorFactory()}

    if feature_names is None:
        feature_names = ta_names()

    test_f = resampler(TalibIndicatorFactory().calculate_indicator("RSI", 'real', {}).loc[start_time:end_time], resample, **kwargs).unstack()
    final_columns = []

    def create_features() -> Generator[np.ndarray, None, None]:

        nonlocal final_columns

        for name in feature_names:
            func, output, params = IndicatorName.decode(name)

            factory = factories[name.split('.')[0]]
            try:
                f = resampler(factory.calculate_indicator(func, output, params).loc[start_time:end_time], resample, **kwargs).unstack()
                yield np.array(f.values)
                final_columns.append(name)

            except Exception as e:
                logging.warn(e)
                # traceback.print_exc(file=sys.stdout)
                logging.warn(f"Cannot calculate indicator {name}. Skipped")
                print(func, output, params)

    values = np.fromiter(
            create_features(), 
            dtype=np.dtype((np.float64, len(test_f))))
    ret = pd.DataFrame(values.T, index=test_f.index, 
                       columns=final_columns, copy=False).swaplevel(0,1)
    ret.index.names = ['datetime', 'instrument']
    return ret



def combine(features:Dict[str, pd.DataFrame], resample=None, sample_filter=None, **kwargs):

    """The combine function takes a dictionary of features as input and combines them into a single pandas DataFrame. combine 函數接受一個特徵字典作為輸入，並將它們合併成一個 pandas DataFrame。
    Args:

        features (Dict[str, pd.DataFrame]): a dictionary of features where index is datetime and column is instrument. 一個特徵字典，其中索引為日期時間，欄位為證券代碼。
        resample (str): Optional argument to resample the data in the features. Default is None. 選擇性的參數，用於重新取樣特徵中的資料。預設為 None。
        **kwargs: Additional keyword arguments to pass to the resampler function. 傳遞給重新取樣函數 resampler 的其他關鍵字引數。

    Returns:
        A pandas DataFrame containing all the input features combined. 一個包含所有輸入特徵合併後的 pandas DataFrame。

    Examples:
        The example code shows how to use the finlab.ml.feature module to combine two sets of features, RSI and price_earning_ratio, from the finlab.data module. The f.combine function is used to combine the features, with the feature names specified as keys in a dictionary and the corresponding feature data specified as values. In this example, the 'rsi' feature is obtained by calling data.indicator('RSI'), which calculates the Relative Strength Index, and the 'pb' feature is obtained by calling data.get('price_earning_ratio:股價淨值比'), which retrieves the price-to-book ratio. The resulting features variable is a DataFrame containing both sets of features combined together.
        這個範例程式碼展示如何使用 finlab.ml.feature 模組，從 finlab.data 模組中結合兩個特徵集，RSI 和 price_earning_ratio。使用 f.combine 函數結合這些特徵，其中特徵名稱以字典的鍵形式給出，對應的特徵資料以值的形式給出。在這個範例中，'rsi' 特徵使用 data.indicator('RSI') 取得，該函數會計算相對強弱指數。'pb' 特徵使用 data.get('price_earning_ratio:股價淨值比') 取得，該函數會取得股價淨值比。最終的 features 變數是一個 DataFrame，包含這兩個特徵集的資料結合在一起。

        ``` py
        from finlab import data
        import finlab.ml.feature as f

        features = f.combine({
            'rsi': data.indicator('RSI'),
            'pb': data.get('price_earning_ratio:股價淨值比')
            })

        features.head()
        ```

        |    datetime   |            |     rsi    |     pb     |
        |---------------|------------|------------|------------|
        |   2020-01-01  |    1101    |     0      |     2      |
        |   2020-01-02  |    1102    |     100    |     3      |
        |   2020-01-03  |    1108    |     100    |     4      |

        結合其他功能產生特徵，首先，使用 data.indicator('RSI') 函數從 finlab.data 模組中計算相對強弱指數特徵，並將其以 'rsi' 為鍵值存入特徵字典。接著，使用 q.alpha('Alpha158') 函數從 finlab.ml.qlib 模組中計算 Alpha158 信號特徵，並將其以 'qlib_alpha158' 為鍵值存入特徵字典。然後，使用 f.ta(f.ta_names()) 函數結合一個包含所有 ta 名稱的特徵集，並將其以默認名稱為鍵值存入特徵字典。最後，使用 f.combine 函數將這些特徵合併成一個 pandas DataFrame。

        ``` py
        from finlab import data
        import finlab.ml.feature as f
        import finlab.ml.qlib as q

        features = f.combine({
            'rsi': data.indicator('RSI'),
            'qlib158': q.alpha('Alpha158')
            'talib': f.ta(f.ta_names()),
            })

        features.head()
        ```
    """

    if len(features) == 0:
        return pd.DataFrame()

    def resampling(df) -> pd.DataFrame:
        return resampler(df, resample, **kwargs)
    
    unstacked = {}

    union_index = None
    union_columns = None
    unstacked = {}
    concats = []

    for name, df in features.items():

        if isinstance(df.index, pd.MultiIndex):
            concats.append(df)
        else:
            if isinstance(df, FinlabDataFrame):
                df = df.index_str_to_date()

            udf = resampling(df)
            unstacked[name] = udf
            if union_index is not None:
                union_index = union_index.union(udf.index)
            else:
                union_index = udf.index
            if union_columns is not None:
                union_columns = union_columns.intersection(udf.columns)
            else:
                union_columns = udf.columns
            
    final_index = None
    for name, udf in unstacked.items():
        udf = udf\
            .reindex(index=union_index, columns=union_columns)\
            .ffill()\
            .unstack()
        unstacked[name] = udf.values

        if final_index is None:
            final_index = udf.index

    for i, c in enumerate(concats):
        c.index = c.index.set_names(['datetime', 'instrument'])
        if union_index:
            concats[i] = c[c.index.get_level_values('datetime').isin(union_index)]

    if unstacked:
        unstack_df = pd.DataFrame(unstacked, index=final_index)
        unstack_df = unstack_df.swaplevel(0, 1)
        unstack_df.index = unstack_df.index.set_names(['datetime', 'instrument'])
        concats.append(unstack_df)

    ret = pd.concat(concats, axis=1)
    ret.sort_index(inplace=True)

    if sample_filter is not None:
        if isinstance(sample_filter, FinlabDataFrame):
            sample_filter = sample_filter.index_str_to_date()
        usf = resampling(sample_filter)

        if union_index and union_columns:
            usf = usf.reindex(index=union_index, columns=union_columns)

        usf = usf.ffill()\
           .unstack()\
           .swaplevel(0, 1)\
           .reindex(ret.index).fillna(False)
        ret = ret[usf.values]

    return ret

