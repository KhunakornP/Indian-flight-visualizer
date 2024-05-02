import abc
from visualizer_ui import Observer
import pandas as pd


class LogicSubject(abc.ABC):
    @abc.abstractmethod
    def attach(self, observer):
        """Attach an observer to the model"""
        raise NotImplementedError

    @abc.abstractmethod
    def detach(self, observer):
        """Detach an observer from the model"""
        raise NotImplementedError

    @abc.abstractmethod
    def notify(self):
        """Notify graphs about changes in the data set"""
        raise NotImplementedError


class DataframeLogic(LogicSubject):
    def __init__(self, df):
        self._observers: list[Observer] = []
        self.orig_df = df
        self.cur_df = self.orig_df.copy()
        self.pair_city("Delhi", "Mumbai")

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observers in self._observers:
            observers.update(self)

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

    def get_flight_info(self, flight_code):
        df = self.orig_df[self.orig_df["flight"] == flight_code]
        flight = df.iloc[0]
        airline = flight.airline
        stops = flight.stops
        start = flight.arrival_time
        end = flight.departure_time
        return airline, stops, start, end

    def generate_price_analysis(self, flight_code):
        airline, stops, start, end = self.get_flight_info(flight_code)
        airline = self.get_airline_analysis(airline)
        stop = self.get_stop_analysis(stops)
        time = self.get_time_analysis(start, end)
        analysis = (f"Flight {flight_code} is {flight_code} baht cheaper than "
                    f"other similar flights\nThe price of the flight is "
                    f"influenced by the following factors:\n")
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
        sorted_df = self.cur_df[self.cur_df.departure_time == dep_time]
        price_median = sorted_df.price.median()
        time_median = sorted_df.groupby("arrival_time").price.median()
        time_med_price = time_median[end_time]
        if time_med_price < price_median:
            percent = ((price_median-time_med_price)/price_median)*100
            return (f"A flight from {dep_time} to {end_time} on average "
                    f"decreases\nprices by {percent:.0f} percent compared to "
                    f"similar flights.\n")
        percent = ((time_med_price-price_median) / price_median) * 100
        return (f"A flight from {dep_time} to {end_time} on average "
                f"decreases\nprices by {percent:.0f} percent compared to "
                f"similar flights.\n")

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
        return cities.tolist()

    def get_flight_codes(self):
        """
        Gets all available flights from the current dataframe

        :return: A list of flight codes from the current dataframe
        """
        return self.cur_df.flight.tolist()


if __name__ == "__main__":
    test = DataframeLogic(pd.read_csv("Indian Airlines.csv"))
    test.pair_city("Delhi", "Mumbai")
    print(test.cur_df.head().source_city)
    print(test.cur_df.head().destination_city)
    print(test.get_stop_analysis(2))
    print(test.get_flight_info("SG-8709"))
    print(test.generate_price_analysis("SG-8709"))
