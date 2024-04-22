import pandas as pd


class DataframeLogic:
    def __init__(self):
        self.orig_df = pd.read_csv("Indian Airlines.csv")
        self.cur_df = self.orig_df.copy()

    def group_by(self, parameter, value):
        pass

    def pair_city(self, a, b):
        pass

    def generate_price_analysis(self):
        pass

