import math
import pandas as pd
from finlab import data
from finlab.analysis import Analysis


class AlphaBetaAnalysis(Analysis):

    def __init__(self):
        self._result = None

    def is_market_info_supported(self, market_info):
        return 'TWMarketInfo' in str(market_info)

    @staticmethod
    def calculate_alpha_beta(creturn, benchmark):

        a = creturn
        b = benchmark

        beta = pd.DataFrame({'a': a.values, 'b': b.values}).cov().iloc[0,1] / b.var()
        alpha = ((a - b * beta).mean()+1) ** 252 - 1

        return alpha, beta

    def analyze(self, report):

        benchmark_pct = report.daily_benchmark.pct_change()
        creturn_pct = report.daily_creturn.pct_change()

        # recent metrics
        recent = {'alpha': [], 'beta': [], 'ndays': [], 'info': []}
        for n in [0, 20, 60, 120, 252]:
            a = creturn_pct.iloc[-n:]
            b = benchmark_pct.loc[a.index[0]:].reindex(a.index)
            alpha, beta = self.calculate_alpha_beta(a, b)
            recent['alpha'].append(0 if math.isnan(alpha) else alpha)
            recent['beta'].append(1 if math.isnan(beta) else beta)
            recent['ndays'].append(n)

        # yearly metrics
        yearly = {'alpha': [], 'beta': [], 'year': []}
        for year in range(creturn_pct.index[0].year, creturn_pct.index[-1].year+1):
            a = creturn_pct.loc[str(year)]
            b = benchmark_pct.loc[str(year)]
            alpha, beta = self.calculate_alpha_beta(a, b)
            yearly['alpha'].append(0 if math.isnan(alpha) else alpha)
            yearly['beta'].append(1 if math.isnan(beta) else beta)
            yearly['year'].append(year)

        # overall metrics
        alpha, beta = self.calculate_alpha_beta(creturn_pct, benchmark_pct)

        return {
            'yearly': yearly,
            'recent': recent,
            'overall': {'alpha': alpha, 'beta': beta}
        }
        

