import pandas as pd


class DataframeLogic:
    def __init__(self):
        self.orig_df = pd.read_csv("Indian Airlines.csv")
        self.cur_df = self.orig_df.copy()

    def group_by(self, parameter, value):
        pass

    def pair_city(self, source, end):
        """
        Groups the data by city pair

        :param source: A string representing a name of airport to group
         as the starting airport
        :param end: A string representing a name of airport to group
         as the destination airport
        """
        df = self.orig_df[self.orig_df.source_city == source]
        df = df[df.destination_city == end]
        self.cur_df = df

    def generate_price_analysis(self):
        pass

    def get_data_summary(self, page):
        pass

    def update_graph(self):
        pass


if __name__ == "__main__":
    test = DataframeLogic()
    test.pair_city("Delhi", "Mumbai")
    print(test.cur_df.head().source_city)
    print(test.cur_df.head().destination_city)