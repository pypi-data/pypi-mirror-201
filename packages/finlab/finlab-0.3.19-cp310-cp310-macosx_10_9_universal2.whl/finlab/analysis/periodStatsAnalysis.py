import numpy as np
from finlab.analysis import Analysis

class PeriodStatsAnalysis(Analysis):

    def __init__(self):

        def safe_division(n, d):
            return n / d if d else 0

        calc_cagr = (
            lambda s: (s.iloc[-1] / s.iloc[0]) ** safe_division(365, (s.index[-1] - s.index[0]).days) - 1 
            if len(s) > 1 else 0)

        def calc_calmar_ratio(pct):
            s = pct.add(1).cumprod().iloc[1:]
            return safe_division(calc_cagr(s), abs(s.calc_max_drawdown()))

        self.metrics = [
                ("calmar_ratio", calc_calmar_ratio),
                ('sortino_ratio', lambda s: safe_division(s.mean(), s[s < 0].std())
                    * (safe_division(len(s), (s.index[-1] - s.index[0]).days) * 365) ** 0.5),
                ('sharpe_ratio', lambda s: safe_division(s.mean(), s.std())
                    * (safe_division(len(s), (s.index[-1] - s.index[0]).days) * 365) ** 0.5),
                ('profit_factor', lambda s: safe_division((s > 0).sum(), (s < 0).sum())),
                ('tail_ratio', lambda s: -safe_division(s.quantile(0.95), (s.quantile(0.05)))),
                ('return', lambda s: calc_cagr(s.add(1).cumprod())),
                ('volatility', lambda s: s.std() * np.sqrt(safe_division(len(s), (s.index[-1] - s.index[0]).days) * 365)),
                ]

    def calc_stats(self, series):

        ########################################
        # calculate yearly metric performance
        ########################################
        pct = series.pct_change()

        def eval_f(m, s):
            if isinstance(m, str):
                return getattr(s, m)()
            else:
                return m[1](s)


        yearly = {}

        for m in self.metrics:

            name = m if isinstance(m, str) else m[0]
            s = pct.groupby(pct.index.year).apply(lambda s: eval_f(m, s))
            yearly[name] = s.values.tolist()

        yearly['year'] = s.index.values.tolist()

        ########################################
        # calculate recent days performance
        ########################################
        recent_days = [20, 60, 120, 252, 756]
        recent = {}
        for m in self.metrics:
            name = m if isinstance(m, str) else m[0]
            recent[name] = []
            for d in recent_days:
                recent[name].append(eval_f(m, pct.iloc[-d:]))

        recent['days'] = recent_days

        ########################################
        # calculate overall performance
        ########################################
        overall_daily = {}
        overall_monthly = {}
        overall_yearly = {}

        pct_m = series.resample('M').last().dropna().pct_change().iloc[1:]
        pct_y = series.resample('Y').last().dropna().pct_change().iloc[1:]

        for m in self.metrics:
            name = m if isinstance(m, str) else m[0]
            overall_daily[name] = eval_f(m, pct)
            overall_monthly[name] = eval_f(m, pct_m) if len(pct_m) > 1 else 0
            overall_yearly[name] = eval_f(m, pct_y) if len(pct_y) > 1 else 0

        return {'yearly': yearly, 
                'recent': recent, 
                'overall_daily': overall_daily, 
                'overall_monthly': overall_monthly, 
                'overall_yearly': overall_yearly}

    def analyze(self, report):

        ret = {}
        ret['strategy'] = self.calc_stats(report.daily_creturn)
        ret['benchmark'] = self.calc_stats(report.daily_benchmark)

        return ret

