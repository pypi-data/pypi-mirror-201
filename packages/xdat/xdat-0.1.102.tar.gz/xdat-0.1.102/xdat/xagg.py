import numpy as np


class _Agg:
    def __init__(self, col_name):
        self.col_name = col_name

    def _get_func(self):
        raise NotImplemented

    def _test(self, a):
        return self._get_func()(a)

    def as_tuple(self):
        func = self._get_func()
        return self.col_name, func


class _AggMultiCol:
    def __init__(self, *col_names, **kwargs):
        self.col_names = list(col_names)
        self.kwargs = kwargs

    def calc_func(self, df, **kwargs):
        raise NotImplemented


class Count(_Agg):
    def __init__(self):
        super().__init__(None)

    def _get_func(self):
        return lambda a: np.sum(~np.isnan(a))


class Min(_Agg):
    def _get_func(self):
        return np.nanmin


class Max(_Agg):
    def _get_func(self):
        return np.nanmax


class Mean(_Agg):
    def _get_func(self):
        return np.nanmean


class Median(_Agg):
    def _get_func(self):
        return np.nanmedian


class Std(_Agg):
    def _get_func(self):
        return np.nanstd


class Sum(_Agg):
    def _get_func(self):
        return lambda a: np.sum(~np.isnan(a)) * np.nanmean(a)   # np.nansum returns zero instead of NaN


class Any(_Agg):
    def _get_func(self):
        def func(a):
            aa = np.array(a[~np.isnan(a)])
            if len(aa):
                return aa[0]
            return np.NaN

        return func


class UniqueVals(_Agg):
    def _get_func(self):
        def func(a):
            aa = a[~np.isnan(a)]
            if len(aa):
                return np.unique(aa).tolist()
            return []

        return func


class CountUnique(_Agg):
    def _get_func(self):
        def func(a):
            try:
                aa = a[~np.isnan(a)]
            except TypeError:
                aa = a[~a.isna()]

            if len(aa):
                return len(np.unique(aa))
            return 0

        return func


class Lambda(_Agg):
    def __init__(self, col_name, func):
        super().__init__(col_name)
        self.func = func

    def _get_func(self):
        return self.func


class WMean(_AggMultiCol):
    def __init__(self, col_name, weight_col=None):
        assert weight_col, 'must specify weight column'
        super().__init__(col_name, weight_col)
        self.main_col = col_name
        self.weight_col = weight_col

    def calc_func(self, df, **kwargs):
        indices = ~np.isnan(df[self.main_col]) & ~np.isnan(df[self.weight_col])
        try:
            return np.average(df[self.main_col][indices], weights=df[self.weight_col][indices])
        except ZeroDivisionError:
            return np.NaN


class LambdaMultiCol(_AggMultiCol):
    def __init__(self, col_name, func):
        raise NotImplemented

