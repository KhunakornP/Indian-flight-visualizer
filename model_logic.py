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
        self.title = ""
        self.graph_type = "Histogram"
        self.arguments = {}
        self.index = 0
        self.pair_city("Delhi", "Mumbai")

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observers in self._observers:
            observers.update_graph(self)

    def increase_index(self):
        if self.index < 2:
            self.index += 1

    def lower_index(self):
        if self.index > 0:
            self.index -= 1

    def get_summary_text(self):
        if self.index == 0:
            return ("from the graph we can see that flights with only 1 "
                    "stops\nare more expensive on average than flights with 0 "
                    "or 2+ stops\n"
                    "Air asia on average provides the cheapest flights and\n"
                    "Vistara on average provides the most expensive flights.\n"
                    )
        elif self.index == 1:
            return ("from the plot we can see that there is a big jump in "
                    "price between booking the flight 20 days and 10 days\n"
                    "before the flight date. So when booking a flight it is\n"
                    "recommended to book the flight at least 16 days in "
                    "advance\nfor the best prices.\n"
                    "The correlation Coefficient between price and no. of "
                    "days is\n-0.55 which means that the more days between "
                    "booking the flight and departure date.\n The cheaper "
                    "the ticket price will become\n")
        elif self.index == 2:
            return ("From the graph we can see that the cheapest time "
                    "interval\n on average for ticket price are flights "
                    "from late night to\nearly morning followed by night to"
                    " late night and both\nlate night to late night and "
                    "early morning to early morning\nthe most expensive "
                    "flights are flights which have long durations\n(eg. early"
                    " morning to late night). Flights that depart during\n"
                    "morning on average have the highest cost with an average "
                    "cost\nof 7119.02 rupees and flights that depart duning "
                    "late night\non average have the cheapest cost with an "
                    "average cost \nof 4784.70 rupees")

    def get_summary_graph(self, index=-1):
        self.state = 3
        current = self.index
        if index in range(4):
            self.index = index
        self.notify()
        self.index = current

    def describe_statistics(self,flight="", mode=1):
        if mode == 1:
            string = self.cur_df.groupby(
                "departure_time").flight.count().to_string()
            string = string.splitlines()
            if len(string) < 2:
                return "No Departure data"
            string[0] = string[0] + " number of departures"
            description = ""
            # I really should have used a monospaced font
            padding = ["    ", "           ", "   ",
                       "              ",
                       "         ","             ","                  "]
            count = 0
            for strings in string:
                split = strings.split(maxsplit=1)
                description += split[0] + padding[count] + split[1]+"\n"
                count += 1
            return description
        elif mode == 2:
            eco = self.eco[self.eco.flight == flight]
            business = self.business[self.business.flight == flight]
            eco_values = list(eco["price"].describe().values)
            bus_values = list(business["price"].describe().values)
            description = (f"Economy class price statistics:\n"
                           f"Mean: {eco_values[1]:.2f} rupees\n"
                           f"Min: {eco_values[3]:.2f} rupees\n"
                           f"Max: {eco_values[-1]:.2f} rupees\n"
                           f"\nBusiness class price statistics:\n"
                           f"Mean: {bus_values[1]:.2f} rupees\n"
                           f"Min: {bus_values[3]:.2f} rupees\n"
                           f"Max: {bus_values[-1]:.2f} rupees")
            return description
        elif mode == 3:
            return "No statistics available"
        elif mode == 4:
            df = self.orig_df[self.orig_df["class"] == "Economy"]
            airlines = df.airline.unique().tolist()
            description = f"Economy class price statistics:\n"
            for airline in airlines:
                cur_df = df[df.airline == airline]
                values = list(cur_df["price"].describe().values)
                describe = (f"\n*Price statistics for {airline}*\n"
                            f"Mean: {values[1]:.2f} rupees\n"
                            f"Min: {values[3]:.2f} rupees\n"
                            f"Max: {values[-1]:.2f} rupees\n")
                description += describe
            return description
        elif mode == 5:
            df = self.orig_df[self.orig_df["class"] == "Business"]
            airlines = df.airline.unique().tolist()
            description = f"Business class price statistics:\n"
            for airline in airlines:
                cur_df = df[df.airline == airline]
                values = list(cur_df["price"].describe().values)
                describe = (f"\n*Price statistics for {airline}*\n"
                            f"Mean: {values[1]:.2f} rupees\n"
                            f"Min: {values[3]:.2f} rupees\n"
                            f"Max: {values[-1]:.2f} rupees\n")
                description += describe
            return description
        elif mode == 6:
            cor = self.orig_df[self.pair[0]].corr(self.orig_df[self.pair[1]])
            description = (f"{self.pair[0]} and {self.pair[1]} has a\n"
                           f"correlation coefficient of {cor:.2f}\n")
            if cor < 0:
                relation = "negative"
            else:
                relation = "positive"
            if abs(cor) < 0.2:
                modifier = "very weak/negligible"
            elif abs(cor) < 0.4:
                modifier = "weak"
            elif abs(cor) < 0.6:
                modifier = "moderate"
            elif abs(cor) < 0.8:
                modifier = "strong"
            else:
                modifier = "Very strong"
            if cor == 1:
                desc_relation = "because they are the same attribute"
            else:
                desc_relation = (f"which is considered to be a {modifier} "
                                 f"{relation} relation")
            return description + desc_relation



    def get_correlation_graph(self, var1, var2):
        self.state = 2
        self.cur_df = self.orig_df.copy()
        self.graph_type = "Scatter"
        self.pair = (var1, var2)
        self.title = f"Scatter plot of {var1} and {var2}"
        self.arguments = {"x":var1, "y":var2}
        self.notify()

    def get_availability(self):
        self.state = 2
        self.graph_type = "Count"
        src = self.pair[0] if self.pair[0] else "nowhere"
        end = self.pair[1] if self.pair[1] else "nowhere"
        self.title = (f"Flight availability from {src} to "
                      f"{end}")
        self.arguments = {"x":"departure_time", "hue":"arrival_time"}
        self.notify()

    def get_airline_graph(self, tier):
        self.cur_df = self.orig_df.copy()
        self.cur_df = self.cur_df[self.cur_df["class"] == tier]
        self.title = (f"{tier if tier else 'Unknown class'}"
                      f" ticket Price distribution grouped by airlines")
        self.arguments = {"x":"airline", "y":"price", "showfliers":False}
        self.graph_type = "Box"
        self.notify()

    def get_day_plot(self, flight_code):
        self.pair_city(self.pair[0], self.pair[1])
        self.cur_df = self.cur_df[self.cur_df.flight == flight_code]
        self.state = 2
        self.graph_type = "Scatter"
        self.arguments = {"x":"days_left", "y":"price", "hue":"class"}
        self.title = (f"Scatter plot of price and days booked before flight of"
                      f" flight {flight_code if flight_code else 'not found'}")
        self.notify()

    def get_frequency_plot(self, attribute, graph=1):
        self.state = 2
        self.cur_df = self.orig_df.copy()
        if graph < 2:
            self.arguments = {"x":attribute}
            self.title = f"Histogram of {attribute}"
            self.graph_type = "Count"
            if attribute in ["duration", "days_left"]:
                self.arguments["binwidth"] = 2
                self.graph_type = "Histogram"
        elif graph == 2:
            if attribute in ["duration", "days_left"]:
                self.title = f"Histogram of {attribute}"
                self.arguments = {"x": attribute, "binwidth": 2}
                self.graph_type = "Histogram"
                self.notify()
                return
            self.cur_df = self.cur_df.groupby(attribute).count()
            self.arguments = {"labels":self.cur_df.index.to_list(),
                              "x":self.cur_df.columns[1]}
            self.title = (f"Distribution of {attribute} from total number of "
                          f"{attribute}")
            self.graph_type = "Pie"
        self.notify()

    def get_price_graph(self, source, end):
        self.pair_city(source, end)
        self.notify()

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

    def get_countable_attributes(self):
        return [x for x in list(self.orig_df.columns) if x not in ["flight",
                                                                   "price"]]

    def get_all_attributes(self):
        return self.orig_df.columns.to_list()

    def get_flight_class(self):
        return self.orig_df["class"].unique().tolist()

    def get_numerical_attributes(self):
        return self.orig_df.select_dtypes(include=["int64",
                                                   "float64"]).columns.tolist()


if __name__ == "__main__":
    test = DataframeLogic(pd.read_csv(os.path.join(os.getcwd(), "Datasets",
                                       "Indian Airlines.csv")))

    df = test.orig_df
    df = df[df["class"] == "Economy"]
    print(df["price"].corr(df["days_left"]))
    df = test.orig_df
    df = df[df["class"] == "Business"]
    print(df["price"].corr(df["days_left"]))
