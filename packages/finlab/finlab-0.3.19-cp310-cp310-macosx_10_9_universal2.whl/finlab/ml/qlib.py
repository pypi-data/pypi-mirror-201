from finlab import ml
import abc
from pathlib import Path
from typing import Iterable, List, Union
from functools import partial
from concurrent.futures import ProcessPoolExecutor

import datetime
import numpy as np
import pandas as pd
from tqdm import tqdm
# from loguru import logger
import logging as logger

import qlib
from qlib import config
from qlib.data import D
from qlib.data.dataset import DatasetH
from qlib.data.dataset.loader import DataLoader
from qlib.data.dataset.handler import DataHandlerLP
from qlib.contrib.data.handler import Alpha158, Alpha360
from qlib.utils import fname_to_code, code_to_fname, init_instance_by_config


class DumpDataBase:
    INSTRUMENTS_START_FIELD = "start_datetime"
    INSTRUMENTS_END_FIELD = "end_datetime"
    CALENDARS_DIR_NAME = "calendars"
    FEATURES_DIR_NAME = "features"
    INSTRUMENTS_DIR_NAME = "instruments"
    DUMP_FILE_SUFFIX = ".bin"
    DAILY_FORMAT = "%Y-%m-%d"
    HIGH_FREQ_FORMAT = "%Y-%m-%d %H:%M:%S"
    INSTRUMENTS_SEP = "\t"
    INSTRUMENTS_FILE_NAME = "all.txt"

    UPDATE_MODE = "update"
    ALL_MODE = "all"

    def __init__(
        self,
        csv_path: str,
        qlib_dir: str,
        backup_dir: str = None,
        freq: str = "day",
        max_workers: int = 16,
        date_field_name: str = "date",
        file_suffix: str = ".csv",
        symbol_field_name: str = "symbol",
        exclude_fields: str = "",
        include_fields: str = "",
        limit_nums: int = None,
    ):
        csv_path = Path(csv_path).expanduser()
        if isinstance(include_fields, str):
            include_fields = include_fields.split(",")
        self._include_fields = tuple(filter(lambda x: len(x) > 0, map(str.strip, include_fields)))
        self.file_suffix = file_suffix
        self.symbol_field_name = symbol_field_name
        self.csv_files = sorted(csv_path.glob(f"*{self.file_suffix}") if csv_path.is_dir() else [csv_path])
        if limit_nums is not None:
            self.csv_files = self.csv_files[: int(limit_nums)]
        self.qlib_dir = Path(qlib_dir).expanduser()
        self.backup_dir = backup_dir if backup_dir is None else Path(backup_dir).expanduser()

        self.freq = freq
        self.calendar_format = self.DAILY_FORMAT if self.freq == "day" else self.HIGH_FREQ_FORMAT

        self.works = max_workers
        self.date_field_name = date_field_name

        self._calendars_dir = self.qlib_dir.joinpath(self.CALENDARS_DIR_NAME)
        self._features_dir = self.qlib_dir.joinpath(self.FEATURES_DIR_NAME)
        self._instruments_dir = self.qlib_dir.joinpath(self.INSTRUMENTS_DIR_NAME)

        self._calendars_list = []

        self._mode = self.ALL_MODE
        self._kwargs = {}

    def _format_datetime(self, datetime_d):
        datetime_d = pd.Timestamp(datetime_d)
        return datetime_d.strftime(self.calendar_format)

    def _get_date(
        self, file_or_df, *, is_begin_end: bool = False, as_set: bool = False
    ) -> Iterable[pd.Timestamp]:
        if not isinstance(file_or_df, pd.DataFrame):
            df = self._get_source_data(file_or_df)
        else:
            df = file_or_df
        if df.empty or self.date_field_name not in df.columns.tolist():
            _calendars = pd.Series(dtype=np.float32)
        else:
            _calendars = df[self.date_field_name]

        if is_begin_end and as_set:
            return (_calendars.min(), _calendars.max()), set(_calendars)
        elif is_begin_end:
            return _calendars.min(), _calendars.max()
        elif as_set:
            return set(_calendars)
        else:
            return _calendars.tolist()

    def _get_source_data(self, file_path: Path) -> pd.DataFrame:
        df = pd.read_csv(str(file_path.resolve()), low_memory=False)
        df[self.date_field_name] = df[self.date_field_name].astype(str).astype(np.datetime64)
        # df.drop_duplicates([self.date_field_name], inplace=True)
        return df

    def get_symbol_from_file(self, file_path: Path) -> str:
        return fname_to_code(file_path.name[: -len(self.file_suffix)].strip().lower())

    def get_dump_fields(self, df_columns: Iterable[str]) -> Iterable[str]:
        return (self._include_fields)

    @staticmethod
    def _read_calendars(calendar_path: Path) -> List[pd.Timestamp]:
        return sorted(
            map(
                pd.Timestamp,
                pd.read_csv(calendar_path, header=None).loc[:, 0].tolist(),
            )
        )

    def _read_instruments(self, instrument_path: Path) -> pd.DataFrame:
        df = pd.read_csv(
            instrument_path,
            sep=self.INSTRUMENTS_SEP,
            names=[
                self.symbol_field_name,
                self.INSTRUMENTS_START_FIELD,
                self.INSTRUMENTS_END_FIELD,
            ],
        )

        return df

    def save_calendars(self, calendars_data: list):
        self._calendars_dir.mkdir(parents=True, exist_ok=True)
        calendars_path = str(self._calendars_dir.joinpath(f"{self.freq}.txt").expanduser().resolve())
        result_calendars_list = list(map(lambda x: self._format_datetime(x), calendars_data))
        np.savetxt(calendars_path, result_calendars_list, fmt="%s", encoding="utf-8")

    def save_instruments(self, instruments_data: Union[list, pd.DataFrame]):
        self._instruments_dir.mkdir(parents=True, exist_ok=True)
        instruments_path = str(self._instruments_dir.joinpath(self.INSTRUMENTS_FILE_NAME).resolve())
        if isinstance(instruments_data, pd.DataFrame):
            _df_fields = [self.symbol_field_name, self.INSTRUMENTS_START_FIELD, self.INSTRUMENTS_END_FIELD]
            instruments_data = instruments_data.loc[:, _df_fields]
            instruments_data[self.symbol_field_name] = instruments_data[self.symbol_field_name].apply(
                lambda x: fname_to_code(x.lower()).upper()
            )
            instruments_data.to_csv(instruments_path, header=False, sep=self.INSTRUMENTS_SEP, index=False)
        else:
            np.savetxt(instruments_path, instruments_data, fmt="%s", encoding="utf-8")

    def data_merge_calendar(self, df: pd.DataFrame, calendars_list: List[pd.Timestamp]) -> pd.DataFrame:
        # calendars
        calendars_df = pd.DataFrame(data=calendars_list, columns=[self.date_field_name])
        calendars_df[self.date_field_name] = calendars_df[self.date_field_name].astype(np.datetime64)
        cal_df = calendars_df[
            (calendars_df[self.date_field_name] >= df[self.date_field_name].min())
            & (calendars_df[self.date_field_name] <= df[self.date_field_name].max())
        ]
        # align index
        cal_df.set_index(self.date_field_name, inplace=True)
        df.set_index(self.date_field_name, inplace=True)
        r_df = df.reindex(cal_df.index)
        return r_df

    @staticmethod
    def get_datetime_index(df: pd.DataFrame, calendar_list: List[pd.Timestamp]) -> int:
        return calendar_list.index(df.index.min())

    def _data_to_bin(self, df: pd.DataFrame, calendar_list: List[pd.Timestamp], features_dir: Path):
        if df.empty:
            logger.warning(f"{features_dir.name} data is None or empty")
            return
        if not calendar_list:
            logger.warning("calendar_list is empty")
            return
        # align index
        _df = self.data_merge_calendar(df, calendar_list)
        if _df.empty:
            logger.warning(f"{features_dir.name} data is not in calendars")
            return
        # used when creating a bin file
        date_index = self.get_datetime_index(_df, calendar_list)
        for field in self.get_dump_fields(_df.columns):
            bin_path = features_dir.joinpath(f"{field.lower()}.{self.freq}{self.DUMP_FILE_SUFFIX}")
            if field not in _df.columns:
                continue
            if bin_path.exists() and self._mode == self.UPDATE_MODE:
                # update
                with bin_path.open("ab") as fp:
                    np.array(_df[field]).astype("<f").tofile(fp)
            else:
                # append; self._mode == self.ALL_MODE or not bin_path.exists()
                np.hstack([date_index, _df[field]]).astype("<f").tofile(str(bin_path.resolve()))

    def _dump_bin(self, file_or_data, calendar_list: List[pd.Timestamp]):
        if not calendar_list:
            logger.warning("calendar_list is empty")
            return
        if isinstance(file_or_data, pd.DataFrame):
            if file_or_data.empty:
                return
            code = fname_to_code(str(file_or_data.iloc[0][self.symbol_field_name]).lower())
            df = file_or_data
        elif isinstance(file_or_data, Path):
            code = self.get_symbol_from_file(file_or_data)
            df = self._get_source_data(file_or_data)
        else:
            raise ValueError(f"not support {type(file_or_data)}")
        if df is None or df.empty:
            logger.warning(f"{code} data is None or empty")
            return

        # try to remove dup rows or it will cause exception when reindex.
        df = df.drop_duplicates(self.date_field_name)

        # features save dir
        features_dir = self._features_dir.joinpath(code_to_fname(code).lower())
        features_dir.mkdir(parents=True, exist_ok=True)
        self._data_to_bin(df, calendar_list, features_dir)

    @abc.abstractmethod
    def dump(self):
        raise NotImplementedError("dump not implemented!")

    def __call__(self, *args, **kwargs):
        self.dump()

class DumpDataAll(DumpDataBase):
    def _get_all_date(self):
        logger.info("start get all date......")
        all_datetime = set()
        date_range_list = []
        _fun = partial(self._get_date, as_set=True, is_begin_end=True)
        with tqdm(total=len(self.csv_files)) as p_bar:
            with ProcessPoolExecutor(max_workers=self.works) as executor:
                for file_path, ((_begin_time, _end_time), _set_calendars) in zip(
                    self.csv_files, executor.map(_fun, self.csv_files)
                ):
                    all_datetime = all_datetime | _set_calendars
                    if isinstance(_begin_time, pd.Timestamp) and isinstance(_end_time, pd.Timestamp):
                        _begin_time = self._format_datetime(_begin_time)
                        _end_time = self._format_datetime(_end_time)
                        symbol = self.get_symbol_from_file(file_path)
                        _inst_fields = [symbol.upper(), _begin_time, _end_time]
                        date_range_list.append(f"{self.INSTRUMENTS_SEP.join(_inst_fields)}")
                    p_bar.update()
        self._kwargs["all_datetime_set"] = all_datetime
        self._kwargs["date_range_list"] = date_range_list
        logger.info("end of get all date.\n")

    def _dump_calendars(self):
        logger.info("start dump calendars......")
        self._calendars_list = sorted(map(pd.Timestamp, self._kwargs["all_datetime_set"]))
        self.save_calendars(self._calendars_list)
        logger.info("end of calendars dump.\n")

    def _dump_instruments(self):
        logger.info("start dump instruments......")
        self.save_instruments(self._kwargs["date_range_list"])
        logger.info("end of instruments dump.\n")

    def _dump_features(self):
        logger.info("start dump features......")
        _dump_func = partial(self._dump_bin, calendar_list=self._calendars_list)
        with tqdm(total=len(self.csv_files)) as p_bar:
            with ProcessPoolExecutor(max_workers=self.works) as executor:
                for _ in executor.map(_dump_func, self.csv_files):
                    p_bar.update()

        logger.info("end of features dump.\n")

    def dump(self):
        self._get_all_date()
        self._dump_calendars()
        self._dump_instruments()
        self._dump_features()

def get_region(market):
    return ml.get_market().__class__.__name__.replace('MarketInfo', '').lower()

def dump(freq='day'):
    """產生Qlib 於台股的資料庫
    Example:
        ```py
        import qlib
        import finlab.ml.qlib as q

        q.dump() # generate tw stock database
        q.init() # initiate tw stock to perform machine leraning tasks (similar to qlib.init)

        import qlib
        # qlib functions and operations
        ```
    """
    
    market = ml.get_market()
    region = get_region(market)

    csv_path = f'~/.qlib/csv_data/{region}_data'
    qlib_dir = f'~/.qlib/qlib_data/{region}_data'
    include_fields = "open,close,high,low,volume,factor"

    if not Path(csv_path).expanduser().exists():
        Path(csv_path).expanduser().mkdir(parents=True)
    if not Path(qlib_dir).expanduser().exists():
        Path(qlib_dir).expanduser().mkdir(parents=True)

    c = market.get_price('close', adj=False)
    ac = market.get_price('close', adj=True)
    o = market.get_price('open', adj=False)
    h = market.get_price('high', adj=False)
    l = market.get_price('low', adj=False)
    v = market.get_price('volume', adj=False)

    assert c is not None
    assert ac is not None
    assert o is not None
    assert h is not None
    assert l is not None
    assert v is not None

    for s in c.columns:
        pd.DataFrame({
            'date':c.index.values,
            'volume': v[s].values,
            'high': h[s].values,
            'low': l[s].values,
            'close': c[s].values,
            'open': o[s].values,
            'factor': ac[s].values / c[s].values,
            'symbol': s
            }).to_csv(Path(csv_path).expanduser() / f"{s}.csv")

    dumper = DumpDataAll(csv_path, qlib_dir, include_fields=include_fields, freq=freq)
    dumper()

def init():
    """Qlib 初始化 (類似於台股版 qlib.init() 但更簡單易用)
    Example:
        ```py
        import qlib
        import finlab.ml.qlib as q

        q.dump() # generate tw stock database
        q.init() # initiate tw stock to perform machine leraning tasks (similar to qlib.init)

        import qlib
        # qlib functions and operations
        ```
    """
    region = get_region(ml.get_market())
    config._default_region_config[region] = \
            dict(trade_unit=1000, limit_threshold=0.1, deal_price='close')

    qlib.init(provider_uri=f'~/.qlib/qlib_data/{region}_data', 
              region=region)

def alpha(handler='Alpha158', **kwargs):

    """產生 Qlib 的特徵
    Args:
        handler (str): 預設為 'alpha158' 也可以設定成 'Alpha360'
    Example:
        ```py
        import finlab.ml.qlib as q
        features = q.alpha('Alpha158')
        ```
    """

    init()

    if handler == 'Alpha158':
        h = Alpha158(instruments=D.instruments(market='all'), **kwargs)
    elif handler == 'Alpha360':
        h = Alpha360(instruments=D.instruments(market='all'), **kwargs)
    else:
        raise Exception(f"Handler {handler} not supported.")

    alpha = h.fetch(col_set="feature")
    return alpha.dropna(how='all', axis=1)


class CustomDataLoader(DataLoader):
    def __init__(self, d):
        self.d = d
        
    def load(self, instruments, start_time=None, end_time=None) -> pd.DataFrame:
        t = self.d.index.get_level_values('datetime')

        selected = t.notna()
        if start_time:
            selected &= t > start_time
        if end_time:
            selected &= t < end_time
        if instruments:
            ins = self.d.index.get_level_values('instrument')
            selected &= ins.isin(instruments) 

        return self.d.loc[selected]

class WrapperModel():

    def __init__(self, model_config, train_valid_split=0.8, purge_days=1):
        self.model = init_instance_by_config(model_config)
        self.train_valid_split = train_valid_split
        self.purge_days = purge_days
        self.params = {
                'model_config': model_config,
                'train_valid_split': train_valid_split,
                'purge_days': purge_days
                }

    def get_params(self, deep=True):
        return self.params.copy()

    def fit(self, X_train, y_train, **fit_params):

        d = pd.concat([
            X_train, 
            y_train.to_frame(name='LABEL0')],
            axis=1, keys=['feature', 'label'])\
            .dropna().sort_index()
        
        tmin = X_train.index.get_level_values('datetime').min()
        tmax = X_train.index.get_level_values('datetime').max()

        tsplit = (tmax - tmin) * self.train_valid_split + tmin

        segments = dict(
            train=(tmin, tsplit),
            valid=(tsplit + datetime.timedelta(days=self.purge_days), tmax)
        )

        dl = CustomDataLoader(d)
        dh = DatasetH(handler=DataHandlerLP(data_loader=dl), segments=segments)
        self.model.fit(dh, **fit_params)

    def predict(self, X_test):

        x = X_test.copy()
        x.columns = pd.MultiIndex.from_tuples([('feature', x) for x in x.columns])

        dl = CustomDataLoader(x)

        tmin = x.index.get_level_values('datetime').min()
        tmax = x.index.get_level_values('datetime').max()

        segments = {
            'test': (tmin, tmax)
        }
        
        dh = DatasetH(handler=DataHandlerLP(data_loader=dl), segments=segments)
        return self.model.predict(dh)
