import pandas as pd
import os
from IPython.display import display

class PandasBasics:
    def show_series(self):
        series = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
        print("Содержимое Series:")
        display(series)
        print("Доступ по .loc['b']:", series.loc['b'])
        print("Доступ по .iloc[2]:", series.iloc[2])

    def show_dataframe(self):
        data = {
            "Имя": ["Аня", "Борис", "Вика"],
            "Возраст": [20, 21, 19]
        }
        df = pd.DataFrame(data)
        print("Содержимое DataFrame:")
        display(df)


class DataInfo(PandasBasics):
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def dataframe_info(self):
        print("Информация о DataFrame:")
        print(self.df.info())


class BaseAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def preprocess(self):
        numeric_cols = ['screen_time_min', 'interactions']
        for col in numeric_cols:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        self.df.dropna(subset=numeric_cols, inplace=True)

    def get_average_by_condition(self, condition_col, target_col, condition='max'):
        if condition == 'max':
            extreme_value = self.df[condition_col].max()
        else:
            extreme_value = self.df[condition_col].min()
        subset = self.df[self.df[condition_col] == extreme_value]
        return subset[target_col].mean()


class InteractionScreenTimeAnalyzer(BaseAnalyzer):
    def analyze_ratio(self):
        self.preprocess()
        max_avg = self.get_average_by_condition('interactions', 'screen_time_min', condition='max')
        min_avg = self.get_average_by_condition('interactions', 'screen_time_min', condition='min')
        if min_avg == 0:
            return float('inf')
        return round(max_avg / min_avg, 2)


class ProductivityScreenTimeAnalyzer(BaseAnalyzer):
    def analyze_productivity_gap(self):
        self.preprocess()
        self.df['is_productive'] = self.df['is_productive'].astype(bool)
        prod_avg = self.df[self.df['is_productive']]['screen_time_min'].mean()
        nonprod_avg = self.df[~self.df['is_productive']]['screen_time_min'].mean()
        return round(prod_avg - nonprod_avg, 2)


def task6():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "screen_time_app_usage_dataset.csv")
    df = pd.read_csv(file_path)

    basics = DataInfo(df)
    basics.show_series()
    basics.show_dataframe()
    basics.dataframe_info()

    analyzer = InteractionScreenTimeAnalyzer(df)
    print("\n\nВо сколько раз больше экранное время у самых активных пользователей:", analyzer.analyze_ratio())

    productivity_analyzer = ProductivityScreenTimeAnalyzer(df)
    print("Разница в среднем экранном времени между продуктивными и непродуктивными:",
          productivity_analyzer.analyze_productivity_gap())

