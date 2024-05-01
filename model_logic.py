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

    def generate_price_analysis(self, flight_code, airline, stops, start, end):
        airline = self.get_airline_analysis(airline)
        stop = self.get_stop_analysis(stops)
        time = self.get_time_analysis(start, end)
        analysis = (f"Flight {flight_code} is {'x'} baht cheaper than other "
                    f"similar flights\nThe price of the flight is influenced "
                    f"by the following factors:\n")
        analysis += f"Airline: " + airline
        analysis += f"Number of stops: " + stop
        analysis += f"Time of day: " + time
        return analysis

    def get_airline_analysis(self, airline):
        price_median = self.cur_df.price.median()
        airline_median = self.cur_df.groupby("airline").price.median()
        airline_med_price = airline_median[airline]
        if airline_med_price < price_median:
            percent = ((price_median-airline_med_price)/price_median)*100
            return (f"{airline} on average provides {percent:.0f} percent "
                    f"cheaper \nflights compared to similar flights.\n")
        percent = ((airline_med_price-price_median) / price_median) * 100
        return (f"{airline} on average provides {percent:.0f} percent\n"
                f"more expensive flights compared to similar flights.\n")

    def get_stop_analysis(self, stops):
        price_median = self.cur_df.price.median()
        stop_median = self.cur_df.groupby("stops").price.median()
        stop_med_price = stop_median[stops]
        if stop_med_price < price_median:
            percent = ((price_median-stop_med_price)/price_median)*100
            return (f"A flight with {stops} stop(s) on average decreases\n"
                    f"prices by {percent:.0f} percent compared to "
                    f"similar flights.\n")
        percent = ((stop_med_price-price_median) / price_median) * 100
        return (f"A flight with {stops} stop(s) on average increases\n"
                f"prices by {percent:.0f} percent compared to "
                f"similar flights.\n")

    def get_time_analysis(self, dep_time, end_time):
        return "To be added"

    def get_data_summary(self, page):
        pass

    def update_graph(self):
        pass

    def get_airport_names(self):
        """
        Gets all available airport names in the dataframe

        :return: A list of airport names in the dataframe
        """
        cities = self.orig_df.source_city.unique()
        return cities

    def get_flight_codes(self):
        """
        Gets all available flights from the current dataframe

        :return: A list of flight codes from the current dataframe
        """
        return self.cur_df.flight


if __name__ == "__main__":
    test = DataframeLogic()
    test.pair_city("Delhi", "Mumbai")
    print(test.cur_df.head().source_city)
    print(test.cur_df.head().destination_city)
    print(test.get_airport_names())
    print(test.get_flight_codes())
    print(test.get_stop_analysis(2))
    print(test.generate_price_analysis("A", "AirAsia", 1,"A","b"))
