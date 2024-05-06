import abc
from visualizer_ui import Observer
import pandas as pd
import os


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
    _observers: list[Observer] = []
    def __init__(self, df):
        self.state = 1
        self.orig_df = df
        self.cur_df = self.orig_df.copy()
        self.eco = None
        self.business = None
        self.pair = ("Delhi", "Mumbai")
        self.graph_type = "Histogram"
        self.arguments = {}
        self.pair_city("Delhi", "Mumbai")

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observers in self._observers:
            observers.update_graph(self)

    def get_availability(self):
        self.state = 2
        self.graph_type = "Availability"
        self.notify()

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
        self.pair = (source, end)
        self.eco = self.cur_df[self.cur_df["class"] == "Economy"]
        self.business = self.cur_df[self.cur_df["class"] == "Business"]
        self.notify()

    def get_flight_info(self, flight_code):
        df = self.orig_df[self.orig_df["flight"] == flight_code]
        if len(df) == 0:
            return None, None, None, None, None, None, None
        flight = df.iloc[0]
        airline = flight.airline
        stops = flight.stops
        start = flight.departure_time
        end = flight.arrival_time
        price = flight.price
        f_class = flight["class"]
        duration = flight.duration
        if f_class == "Economy":
            self.cur_df = self.eco
        else:
            self.cur_df = self.business
        return airline, stops, start, end, price, duration, f_class

    def generate_price_analysis(self, flight_code):
        (airline, stops, start, end,
         price, dur, f_class) = self.get_flight_info(flight_code)
        if airline is None:
            return f"Flight not found"
        airline = self.get_airline_analysis(airline)
        stop = self.get_stop_analysis(stops)
        time = self.get_time_analysis(start, end)
        price_avg = self.cur_df.price.mean()
        duration = self.get_average_cost_per_dist(dur)
        timeframe = f'{start} to {end}'
        statistic = (f"Flight:{flight_code:30}  Stops: {stops} stop(s)\n"
                     f"Time :{timeframe:28}Price: {price} rupees\n"
                     f"Duration : {str(dur) + ' hours':26}Class: {f_class}\n"
                     f"The average cost of a flight from {self.pair[0]} to "
                     f"{self.pair[1]}\nis {price_avg:.2f} rupees\n")
        if price < price_avg:
            dif = price_avg - price
            analysis = (f"\nFlight {flight_code} is {dif:.02f} rupee cheaper "
                        f"than the average\ncost of flights from "
                        f"{self.pair[0]} to {self.pair[1]}.\nThe price of the "
                        f"flight is influenced by the following factors:\n")
        else:
            dif = price - price_avg
            analysis = (f"\nFlight {flight_code} is {dif:.2f} rupee more "
                        f"expensive\nthan the average cost of flights from "
                        f"{self.pair[0]} to {self.pair[1]}.\nThe price "
                        f"of the flight is influenced by the following "
                        f"factors:\n")
        analysis += f"\nDuration: " + duration
        analysis += f"\nAirline: " + airline
        analysis += f"\nNumber of stops: " + stop
        analysis += f"\nTime of day: " + time
        statistic += analysis
        return statistic

    def get_airline_analysis(self, airline):
        price_median = self.cur_df.price.mean()
        airline_median = self.cur_df.groupby("airline").price.mean()
        airline_med_price = airline_median[airline]
        if airline_med_price < price_median:
            percent = ((price_median-airline_med_price)/price_median)*100
            return (f"{airline} on average provides {percent:.0f} percent "
                    f"cheaper \nflights compared to similar flights"
                    f" from other airlines.\n")
        percent = ((airline_med_price-price_median) / price_median) * 100
        return (f"{airline} on average provides {percent:.0f} percent\n"
                f"more expensive flights compared to similar flights.\n")

    def get_stop_analysis(self, stops):
        price_median = self.cur_df.price.mean()
        stop_median = self.cur_df.groupby("stops").price.mean()
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
        price_median = sorted_df.price.mean()
        time_median = sorted_df.groupby("arrival_time").price.mean()
        time_med_price = time_median[end_time]
        if time_med_price < price_median:
            percent = ((price_median-time_med_price)/price_median)*100
            return (f"A flight from {dep_time} to {end_time} on average\n"
                    f"decreases prices by {percent:.0f} percent compared to "
                    f"similar flights.\n")
        percent = ((time_med_price-price_median) / price_median) * 100
        return (f"A flight from {dep_time} to {end_time} on average\n"
                f"decreases prices by {percent:.0f} percent compared to "
                f"similar flights.\n")

    def get_average_cost_per_dist(self, duration):
        time = int(duration)
        df = self.orig_df[self.orig_df["class"] == 'Economy']
        sorted_df = df[(df.duration >= time) &
                       (df.duration < time + 1)]
        med_price = sorted_df.price.mean()
        return (f"A flight with a duration of {duration} hours\n"
                f"on average costs {med_price:.2f} rupees\n")

    def get_data_summary(self, page):
        pass

    def get_airport_names(self):
        """
        Gets all available airport names in the dataframe

        :return: A list of airport names in the dataframe
        """
        cities = self.orig_df.source_city.unique()
        return cities.tolist()

    def get_dest_airports(self, start):
        cities = self.orig_df[self.orig_df.source_city == start]
        return cities.destination_city.unique().tolist()

    def get_flight_codes(self):
        """
        Gets all available flights from the current dataframe

        :return: A list of flight codes from the current dataframe
        """
        return self.cur_df.flight.unique().tolist()


if __name__ == "__main__":
    test = DataframeLogic(pd.read_csv(os.path.join(os.getcwd(), "Datasets",
                                       "Indian Airlines.csv")))
    test.pair_city("Delhi", "Mumbai")
    print(test.cur_df.head().source_city)
    print(test.cur_df.head().destination_city)
    print(test.get_stop_analysis(2))
    print(test.get_flight_info("AI-803"))
    print(test.generate_price_analysis("AI-803"))
    print(test.get_average_cost_per_dist(24))
    test.get_availability()
    print(test.cur_df["Afternoon"])