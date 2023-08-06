import matplotlib.pyplot as plt
import pandas as pd
from typing import List
from alphalens.tears import GridFigure

from alphalens import plotting
from alphalens import performance as perf
from alphalens import utils
import alphalens
from finlab.ml.feature import combine

# fix error orginal code: http://quantopian.github.io/
@plotting.customize
def create_turnover_tear_sheet(factor_data, turnover_periods=None):

    if turnover_periods is None:
        input_periods = utils.get_forward_returns_columns(
            factor_data.columns, require_exact_day_multiple=True,
        ).to_numpy()
        turnover_periods = utils.timedelta_strings_to_integers(input_periods)
    else:
        turnover_periods = utils.timedelta_strings_to_integers(
            turnover_periods,
        )

    quantile_factor = factor_data["factor_quantile"]

    quantile_turnover = {
        p: pd.concat(
            [
                perf.quantile_turnover(quantile_factor, q, p)
                for q in quantile_factor.sort_values().unique().tolist()
            ],
            axis=1,
        )
        for p in turnover_periods
    }

    autocorrelation = pd.concat(
        [
            perf.factor_rank_autocorrelation(factor_data, period)
            for period in turnover_periods
        ],
        axis=1,
    )

    plotting.plot_turnover_table(autocorrelation, quantile_turnover)

    fr_cols = len(turnover_periods)
    columns_wide = 1
    rows_when_wide = ((fr_cols - 1) // 1) + 1
    vertical_sections = fr_cols + 3 * rows_when_wide + 2 * fr_cols
    gf = GridFigure(rows=vertical_sections, cols=columns_wide)

    for period in turnover_periods:
        if quantile_turnover[period].isnull().all().all():
            continue
        plotting.plot_top_bottom_quantile_turnover(
            quantile_turnover[period], period=period, ax=gf.next_row()
        )

    for period in autocorrelation:
        if autocorrelation[period].isnull().all():
            continue
        plotting.plot_factor_rank_auto_correlation(
            autocorrelation[period], period=period, ax=gf.next_row()
        )

    plt.show()
    gf.close()

alphalens.tears.create_turnover_tear_sheet = create_turnover_tear_sheet

def create_factor_data(factor:pd.DataFrame, adj_close:pd.DataFrame, days:List[int]=[1,5,10]):

    '''create factor data, which contains future return
    Args:
        factor (pd.DataFrame): factor data where index is datetime and columns is asset id
        adj_close (pd.DataFrame): adj close where index is datetime and columns is asset id
        days (List[int]): future return considered
    Return:
        Analytic plots and tables

    Examples:
        ```
        import alphalens
        from finlab import data
        from finlab.ml.alphalens import create_factor_data

        factor = data.get('price_earning_ratio:股價淨值比')
        adj_close = data.get('etl:adj_close')

        factor_data = create_factor_data(factor, adj_close)

        alphalens.tears.create_full_tear_sheet(factor_data.dropna(), long_short=False,
                                               group_neutral=False, by_group=False)

        ```

    '''



    adj_close = adj_close.loc[factor.index[0]:factor.index[-1]]
    factor = factor.reindex(adj_close.index, method='ffill').loc[factor.index[0]:factor.index[-1]]

    sids = adj_close.columns.intersection(factor.columns)
    adj_close = adj_close[sids]
    factor = factor[sids]

    ret = {}
    ret['factor'] = factor
    ret['factor_quantile'] = (factor.rank(axis=1, pct=True) // 0.2)

    days = [1, 5, 10]
    for d in days:
        ret[f"{d}D"] = adj_close.shift(-d-1) / adj_close.shift(-1) - 1

    ret = combine(ret)
    ret.index = ret.index.rename(['date', 'asset'])
    return ret

