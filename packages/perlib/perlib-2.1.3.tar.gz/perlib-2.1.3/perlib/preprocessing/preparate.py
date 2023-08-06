import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter
import statsmodels.api as sm
from sklearn.preprocessing import MinMaxScaler,StandardScaler,MaxAbsScaler, RobustScaler
from statsmodels.tsa.stattools import adfuller as ADF
from sklearn.model_selection import train_test_split
#import pymrmr
from sklearn.feature_selection import f_regression
import math
import operator
import sqlite3
from ._utils.dataframe import read_pandas

columnsDate = ["Time","TIME","time","Datetime","datetime","DATETİME","TARİH",
                       "Tarih","tarih","timestamp","TIMESTAMP","Timestamp","date","Date","DATE"]

class dataPrepration:

    def __init__(self):
        self.dataFrame = False
        self.col       = False
        #self.dataFrame = self.__datatimeinsert()
        #self.dataFrame = self.insertFirstcolumn(col=self.col)

    def read_data(self, path,delimiter=None) -> pd.DataFrame:
        dataFrame = read_pandas(path,delimiter=delimiter)
        return dataFrame
#
    def load_sql( self,query:str,path:str):
        con = sqlite3.connect(path)
        dataFrame = pd.read_sql(query,con=con)
        return dataFrame

    def _date_check(self,dataFrame : pd.DataFrame):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        if dataFrame.index.name in columnsDate:
            dataFrame = dataFrame.reset_index()
            dcol = list(set(dataFrame.columns.tolist()).intersection(columnsDate))[0]
            dataFrame[dcol] = pd.to_datetime(dataFrame[dcol])
        elif len(list(set(dataFrame.columns.tolist()).intersection(columnsDate))) > 0:
            dcol = list(set(dataFrame.columns.tolist()).intersection(columnsDate))[0]
            dataFrame[dcol] = pd.to_datetime(dataFrame[dcol])

        return dataFrame,dcol

    def _datatimeinsert(self, dataFrame:pd.DataFrame ) -> pd.DataFrame:
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")
        dataFrame,dcol = self._date_check()
        try:
            dataFrame[dcol] = dataFrame[dcol].astype('datetime64[ns]')
            dataFrame.index = dataFrame[dcol]
            del dataFrame[dcol]
        except: pass
        return dataFrame

    def _insertFirstcolumn(self , col : str , dataFrame : pd.DataFrame):

        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        dataFrame = dataFrame.sort_index()
        first_column = dataFrame.pop(col)
        dataFrame.insert(0, col, first_column)
        return dataFrame

    def trainingFordate_range(self, dt1 : str, dt2 : str, dataFrame : pd.DataFrame):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")
        try:
            dataFrame = self._datatimeinsert().sort_index()
        except:pass
        return dataFrame[(dataFrame.index > dt1) & (dataFrame.index < dt2)]


    def train_test_split(self, dataFrame : pd.DataFrame, target=None, test_size=None, tX=None, tY=None,
                         train_size=None,
                         random_state=None,
                         shuffle=True,
                         stratify=None,
                         ):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")
        try:
            Y = dataFrame.loc[:, [target]].values
            X = dataFrame.loc[:, dataFrame.columns != target].values
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, train_size=train_size,
                                                                random_state=random_state, shuffle=shuffle,
                                                                stratify=stratify)
        except:
            X_train, X_test, y_train, y_test = train_test_split(tX, tY, test_size=test_size, train_size=train_size,
                                                                random_state=random_state, shuffle=shuffle,
                                                                stratify=stratify)

        print("X_train shape :", X_train.shape)
        print("X_test shape  :", X_test.shape)
        print("Y_train shape :", y_train.shape)
        print("Y test shape  :", y_test.shape)
        return X_train, X_test, y_train, y_test

    def clean_dataset(self,df:pd.DataFrame):
        assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
        df.dropna(inplace=True)
        indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
        return df[indices_to_keep].astype(np.float64)

    def split( X_data , y_data , test_split : int  ):
        # Splitting the data into train and test
        X_train= X_data[:-test_split]
        X_test= X_data[-test_split:]
        y_train=y_data[:-test_split]
        y_test=y_data[-test_split:]

        print("X_train shape :", X_train.shape)
        print("X_test shape  :", X_test.shape)
        print("Y_train shape :", y_train.shape)
        print("Y test shape  :", y_test.shape)

        return X_train , X_test , y_train , y_test

    def diff( self , col : str  ,dataFrame : pd.DataFrame) :
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")
        values = dataFrame[col].diff()
        return values

    def gauss_Filter(self, dataFrame : pd.DataFrame, col : str, sigma =0.3, ):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")
        values = pd.Series(gaussian_filter(dataFrame[col], sigma=sigma),
                                                           index=dataFrame.index).astype(float)
        return values

    def moving_average(self,dataFrame : pd.DataFrame, col : str, window : int =3):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")
        values = dataFrame[col].rolling(window=window).mean().dropna()
        return values

    def exponential_Smoothing(self, col : str, dataFrame : pd.DataFrame):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        values = sm.tsa.ExponentialSmoothing(dataFrame[col],
                                                                 trend='add',
                                                                 seasonal_periods=4).fit().fittedvalues.shift(1)
        return values

    def rolling_mean_diff(self,dataFrame : pd.DataFrame, col : str, window : int =3 ):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        rolling_mean = dataFrame.rolling(window=window).mean()
        values = rolling_mean[col] - rolling_mean[col].shift().dropna()
        return values

    def circ(self,dataFrame : pd.DataFrame,dateColumn : str):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        hours_in_week = 7 * 24
        #dataFrame,dcol            = self._date_check()
        dataFrame[dateColumn] = pd.to_datetime(dataFrame[dateColumn])
        dataFrame['CircHourX']    = dataFrame[dateColumn].apply(lambda x: np.cos(x.hour / 24 * 2 * np.pi))
        dataFrame['CircHourY']    = dataFrame[dateColumn].apply(lambda x: np.sin(x.hour / 24 * 2 * np.pi))
        dataFrame['CircWeekdayX'] = dataFrame[dateColumn].apply(lambda x: np.cos(x.weekday() * 24 + x.hour / hours_in_week * 2 * np.pi))
        dataFrame['CircWeekdayY'] = dataFrame[dateColumn].apply(lambda x: np.sin(x.weekday() * 24 + x.hour / hours_in_week * 2 * np.pi))
        dataFrame['CircDayX']     = dataFrame[dateColumn].apply(lambda x: np.cos(x.day * 24 + x.hour / x.daysinmonth * 2 * np.pi))
        dataFrame['CircDayY']     = dataFrame[dateColumn].apply(lambda x: np.sin(x.day * 24 + x.hour / x.daysinmonth * 2 * np.pi))
        dataFrame['CircMonthX']   = dataFrame[dateColumn].apply(lambda x: np.cos(x.dayofyear / 365 * 2 * np.pi))
        dataFrame['CircMonthY']   = dataFrame[dateColumn].apply(lambda x: np.sin(x.dayofyear / 365 * 2 * np.pi))
        dataFrame = dataFrame.set_index(dateColumn)
        return dataFrame

    def generate_time_lags(self,dataFrame : pd.DataFrame, col : str, n_lags : int = False, th : float=False, firstN : int =False):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        def glag(df, columns, n_lags: int):
            df_L = df.copy()
            df_L = df_L[[columns]]
            for n in range(1, n_lags + 1):
                df_L[f"lag{n}"] = df_L[columns].shift(n)
            return pd.concat([df, df_L.iloc[:, 1:]], axis=1).dropna()

        dict_ = {'Lag': [],
                 'Autocor': []}

        for lag in range(1, int(np.sqrt(dataFrame.shape[0]))):
            shift = dataFrame[col].autocorr(lag)
            dict_['Lag'].append(lag)
            dict_['Autocor'].append(shift)
        autocorr_df = pd.DataFrame(dict_)
        autocorr_df = autocorr_df.sort_values("Autocor", ascending=False).reset_index(drop=True)

        if bool(n_lags) is True:
            return glag(dataFrame, col, n_lags).dropna()

        elif bool(th) is True:
            autocorr_df = autocorr_df[autocorr_df.Autocor > th]
            if autocorr_df.__len__() > 0:
                lags = ["lag" + str(x) for x in autocorr_df.Lag.tolist()]
                df_c = dataFrame.copy()
                df_c = glag(df_c, col, autocorr_df.Lag.max())
                return pd.concat([dataFrame, df_c.loc[:, lags]], axis=1).dropna()
            else:
                raise ValueError(f'No value above {th} was found.')

        elif bool(firstN) is True:
            autocorr_df = autocorr_df[:firstN]
            lags = ["lag" + str(x) for x in autocorr_df.Lag.tolist()]
            df_c = dataFrame.copy()
            df_c = glag(df_c, col, autocorr_df.Lag.max())
            return pd.concat([dataFrame, df_c.loc[:, lags]], axis=1).dropna()
        else:
            pass

    def adf_test(self, dataFrame : pd.DataFrame, columns : list =[]):

        if len(columns) == 0:
            raise  TypeError("adf_test() missing 1 required positional argument: columns")

        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        dataFrame = dataFrame.dropna()
        for col in columns:
            print(f'Augmented Dickey-Fuller Test: {col}')
            result = ADF(dataFrame[col], autolag='AIC')

            labels = ['ADF test statistic', 'p-value', '# lags used', '# observations']
            out = pd.Series(result[0:4], index=labels)

            for key, val in result[4].items():
                out[f'critical value ({key})'] = val
            print(out.to_string())

            if result[1] <= 0.05:
                print("Strong evidence against the null hypothesis")
                print("Reject the null hypothesis")
                print("Data has no unit root and is stationary")
            else:
                print("Weak evidence against the null hypothesis")
                print("Fail to reject the null hypothesis"),
                print("Data has a unit root and is non-stationary")

    def date_transform(self,dateColumn : str , dataFrame : pd.DataFrame):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        #dataFrame, dcol = self._date_check(dataFrame=dataFrame)

        if bool(dataFrame.index.name):
            dataFrame = dataFrame.reset_index()
        dataFrame[dateColumn] = pd.to_datetime(dataFrame[dateColumn],dayfirst=True)
        dataFrame['Year']       = dataFrame[dateColumn].dt.year
        dataFrame['Month']      = dataFrame[dateColumn].dt.month
        dataFrame['Day']        = dataFrame[dateColumn].dt.day
        dataFrame['WeekofYear'] = dataFrame[dateColumn].dt.weekofyear
        dataFrame['DayofWeek']  = dataFrame[dateColumn].dt.weekday
        dataFrame['Hour']       = dataFrame[dateColumn].dt.hour
        try:
            dataFrame[dateColumn] = dataFrame[dateColumn].astype('datetime64[ns]')
            dataFrame.index = dataFrame[dateColumn]
            del dataFrame[dateColumn]
        except:
            pass

        return dataFrame

    #def mRMR(self, dataFrame = None, method="MIQ", n_features=3):
#
    #    """
    #    First parameter is a pandas DataFrame (http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) containing the input dataset, discretised as defined in the original paper (for ref. see http://home.penglab.com/proj/mRMR/). The rows of the dataset are the different samples. The first column is the classification (target) variable for each sample. The remaining columns are the different variables (features) which may be selected by the algorithm. (see “Sample Data Sets” at http://home.penglab.com/proj/mRMR/ to download sample dataset to test this algorithm). IMPORTANT: the column names (feature names) should be of type string;
    #    Second parameter is a string which defines the internal Feature Selection method to use (defined in the original paper): possible values are “MIQ” or “MID”;
    #    Third parameter is an integer which defines the number of features that should be selected by the algorithm.
#
    #    """
    #    if isinstance(dataFrame, pd.DataFrame):
    #        self.dataFrame = dataFrame
    #    return pymrmr.mRMR(self.dataFrame, method, n_features)

    def likelihood(self, targetcol : str, dataFrame : pd.DataFrame, n_features:int = 4):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        columns = []
        for col in dataFrame.columns:
            for col2 in columnsDate:
                if col.endswith(col2) or col.startswith(col2):
                    columns.append(col)
        dataFrame = dataFrame.drop(columns=columns, axis=1)
        from ..forecaster import preprocess
        columns = dataFrame.columns
        dataFrame = preprocess.encode_cat(dataFrame=dataFrame)

        remove_column = []
        for col in columns:
            column = dataFrame.loc[:, dataFrame.columns.str.startswith(col)].select_dtypes(
                "object").columns.tolist()
            if len(column) != 0:
                remove_column.extend(column)
        dataFrame = dataFrame.drop(remove_column, axis=1)
        dataFrame = preprocess.auto(dataFrame=dataFrame)
        Xn = dataFrame.loc[:,dataFrame.columns != targetcol].values
        yn = dataFrame.loc[:,dataFrame.columns == targetcol].values
        scX = MinMaxScaler(feature_range=(0, 1))
        scY = MinMaxScaler(feature_range=(0, 1))
        X = scX.fit_transform(Xn)
        y = scY.fit_transform(yn.reshape(-1, 1))
        X_train, X_test, y_train, y_test = self.train_test_split(dataFrame=dataFrame,tX=X, tY=y, test_size=24, random_state=42)
        f_val, p_val = f_regression(X_train, y_train)
        f_val_dict = {}
        p_val_dict = {}
        for i in range(len(f_val)):
            if math.isnan(f_val[i]):
                f_val[i] = 0.0
            f_val_dict[i] = f_val[i]
            if math.isnan(p_val[i]):
                p_val[i] = 0.0
            p_val_dict[i] = p_val[i]

        sorted_f = sorted(f_val_dict.items(), key=operator.itemgetter(1), reverse=True)
        sorted_p = sorted(p_val_dict.items(), key=operator.itemgetter(1), reverse=True)

        feature_indexs = []

        for i in range(0, n_features):
            feature_indexs.append(sorted_f[i][0])

        return dataFrame.iloc[:, 1:].iloc[:, feature_indexs].columns.tolist()

    def plb( self, col : str,  period : int , timelag : int,dataFrame:pd.DataFrame ):

        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        """
        df      : DataFrame
        col     : Columns
        period  : Period Number
        timelag : Lookback

        """
        dict = {"Values": [],
                "lag": []}
        for i in range(1, period + 1):
            dict["Values"].append(np.tile(dataFrame[:-timelag].iloc[-i * timelag][col], (dataFrame.shape[0], 1))[0])
            dict["lag"].append(i)
        data_l = pd.DataFrame(dict["Values"]).T
        data_l.columns = dict["lag"]
        dataFrame = pd.concat([dataFrame, data_l], axis=1)
        dataFrame.loc[:, dict["lag"]] = dataFrame.loc[:, dict["lag"]].ffill()
        return dataFrame

    def normalizeZeroValues(self,columns : str ,dataFrame : pd.DataFrame):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")


        columnsDate = ['Year', 'Month', 'Day', 'WeekofYear', 'DayofWeek', 'Hour', columns]
        for col in dataFrame.loc[:, (dataFrame == 0).any()].columns.tolist():
            if col not in columnsDate:
                dataFrame.loc[dataFrame[col] < 1, col] = np.nan
                dataFrame = dataFrame.groupby(dataFrame.index.date).transform(lambda x: x.fillna(x.mean()))
        return dataFrame


    def get_scaler(self,scaler):
        scalers = {
            "minmax": MinMaxScaler,
            "standard": StandardScaler,
            "maxabs": MaxAbsScaler,
            "robust": RobustScaler,
        }
        return scalers.get(scaler.lower())()

    def inf_clean(self,dataFrame = None):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")
        return dataFrame.replace([np.inf, -np.inf], 0, inplace=True)


    def multivariate_data_create_dataset(self, dataset, target, start = 0 , window = 24, horizon = 1,end=None):
        X = []
        y = []
        start = start + window
        if end is None:
            end = len(dataset) - horizon
        for i in range(start, end):
            indices = range(i - window, i)
            X.append(dataset[indices])
            indicey = range(i + 1, i + 1 + horizon)
            y.append(target[indicey])
        X_data,y_data =  np.array(X), np.array(y)
        print('trainX shape == {}.'.format(X_data.shape))
        print('trainY shape == {}.'.format(y_data.shape))

        return X_data, y_data

    def unvariate_data_create_dataset(self, dataset, start=0, window = 24, horizon = 1,end = None):
        dataX = []
        dataY = []

        start = start + window
        if end is None:
          end = len(dataset) - horizon
        for i in range(start, end):
          indicesx = range(i-window, i)
          dataX.append(np.reshape(dataset[indicesx], (window, 1)))
          indicesy = range(i,i+horizon)
          dataY.append(dataset[indicesy])

        return np.array(dataX), np.array(dataY)


