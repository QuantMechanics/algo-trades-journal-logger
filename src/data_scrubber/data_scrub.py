import pandas as pd
import numpy as np
from functools import wraps
import datetime


def inputvalidator(input_="ohlc"):
    def dfcheck(func):
        @wraps(func)
        def wrap(*args, **kwargs):

            args = list(args)
            i = 0 if isinstance(args[0], pd.DataFrame) else 1

            args[i] = args[i].rename(
                columns={c: c.lower() for c in args[i].columns})

            inputs = {
                "o": "open",
                "h": "high",
                "l": "low",
                "c": kwargs.get("column", "close").lower(),
                "v": "volume",
            }

            if inputs["c"] != "close":
                kwargs["column"] = inputs["c"]

            for l in input_:
                if inputs[l] not in args[i].columns:
                    raise LookupError(
                        'Must have a dataframe column named "{0}"'.format(
                            inputs[l])
                    )

            return func(*args, **kwargs)

        return wrap

    return


def apply(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


class DS:
    __version__ = "0.0.1"

    @classmethod
    @apply(inputvalidator(input_="ohlcv"))
    def clean_dataframe(cls, ohlc: pd.DataFrame) -> pd.DataFrame:
        """
        :param pd.DataFrame ohlcv: 'open, high, low, close, volume' pandas DataFrame
        :return pd.DataFrame: result is pandas.DataFrame
        """
        try:
            data = ohlc.copy(deep=True)

            if 'Unnamed: 0' in data.columns:
                del data['Unnamed: 0']

            data.rename(columns={'Open': 'open', 'High': 'high',
                                 'Low': 'low', 'Close': 'close', 'Volume': 'volume', 'Datetime': 'date'})

            if type(data.index) != pd.RangeIndex:
                data.reset_index(inplace=True)
            if 'date' in data.columns:
                data['date'] = data['date'].astype(str).str[:-6]
                data['date'] = pd.to_datetime(data['date'])

            if type(data.index) == pd.RangeIndex:
                data.set_index('date', inplace=True)

            return data
        except Exception as identifier:
            raise LookupError(identifier)

    @classmethod
    def resample_dataframe(cls, df: pd.DataFrame, time_window="15min", column="close") -> pd.DataFrame:
        """
        This function helps in resampling of the ohlc data based on time_window parameter provided
        """
        df = df.resample(time_window, closed='right', label='right').agg(
            {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
        df.dropna(inplace=True)
        return df

    @classmethod    
    def get_orb_dataframe(cls, input_data: pd.DataFrame, input_hour=9, input_minutes=15) -> pd.Series:
        """
        This function helps in giving the orb datas
        Two new columns  orb_high, orb_low shall be added in given dataframe
        """
        try:
            data = input_data.copy(deep=False)
            data.reset_index(inplace=True)
            data['onlydate'] = data['date'].dt.date
            data_high = (data[data['date'].dt.time <= datetime.time(
                hour=input_hour, minute=input_minutes)].groupby(['onlydate'])['high'].agg('max').reset_index())
            data_low = (data[data['date'].dt.time <= datetime.time(
                hour=input_hour, minute=input_minutes)].groupby(['onlydate'])['low'].agg('min').reset_index())

            data = pd.merge(data, data_high, on='onlydate', how='left')
            data = pd.merge(data, data_low, on='onlydate', how='left')
            data.rename(columns={'high_y': 'orb_high', 'low_y': 'orb_low',
                                 'high_x': 'high', 'low_x': 'low'}, inplace=True)
            del data['onlydate']
            data.set_index('date', inplace=True)
            return pd.Series(data['orb_high']), pd.Series(data['orb_low'])
        except Exception as identifier:
            print(identifier)
            return pd.Series(np.nan), pd.Series(np.nan)
        
    @classmethod
    def NPreviousDaysOHLC(cls, df: pd.DataFrame, prev_days: int = 1) -> pd.Series:
        """
        This function gives previous n days high low based on prev_days param
        dataframe should've columns ['open','high','low','close'] and datetime as index
        output: Four columns data['pOpen'],data['pHigh'],data['pLow'],data['pClose']
        """
        try:
            data = df.copy(deep=True)
            data.reset_index(inplace=True)
            data['onlydate'] = data['date'].dt.date
            data['pClose'] = 0
            data['pHigh'] = 0
            data['pLow'] = 0
            data['pOpen'] = 0

            data.set_index('date', inplace=True)
            unique_dates = sorted(data['onlydate'].unique())
            for i in range(0, len(unique_dates)):
                xdate = unique_dates[i]
                if prev_days > i:
                    data.loc[data['onlydate'] == xdate,
                             ['pOpen', 'pHigh', 'pLow', 'pClose']] = [np.nan, np.nan, np.nan, np.nan]
                else:
                    pdate = unique_dates[i-prev_days]
                    pdata = data[data['onlydate'] == pdate].iloc[-1]
                    data.loc[data['onlydate'] == xdate, [
                        'pOpen', 'pHigh', 'pLow', 'pClose']] = [pdata['open'], pdata['high'], pdata['low'], pdata['close']]
            return pd.Series(data['pOpen']), pd.Series(data['pHigh']), pd.Series(data['pLow']), pd.Series(data['pClose'])
        except Exception as identifier:
            print(identifier)
            pass