"""Controllers for the visualizer's UI"""
import tkinter as tk
import threading
from tkinter import messagebox
import abc


class Controller:
    """A controller for the Visualizer UI"""
    def __init__(self, ui, logic):
        self.main = ui
        self.logic = logic
        self.valid_airports = self.logic.get_airport_names()
        self.states = [AvailabilityState(self), DayState(self),
                       FrequencyState(self), AirlineState(self),
                       CorrelationState(self)]
        self.current_state = self.states[0]
        self.get_combobox_values()
        self.get_default_graphs()
        self.bind_components()

    def bind_components(self):
        """Binds the widgets to their respective handlers"""
        self.main.notebook.bind("<<NotebookTabChanged>>", self.tab_load_graph)
        self.main.comboboxes[0].bind("<<ComboboxSelected>>",
                                     self.get_valid_destination)
        self.main.comboboxes[1].bind("<<ComboboxSelected>>",
                                     self.update_dist_graph)
        self.main.comboboxes[2].bind("<<ComboboxSelected>>",
                                     self.get_price_analysis)
        self.main.comboboxes[2].bind("<Return>", self.get_price_analysis)
        self.main.button.bind("<ButtonRelease>", self.generate_graph)
        self.main.mode.configure(command=self.set_attribute_tab)
        self.main.comboboxes[4].bind("<<ComboboxSelected>>",
                                     self.temp_get_combobox_values)
        self.main.prev_button.bind("<ButtonRelease>", self.prev_summary_page)
        self.main.next_button.bind("<ButtonRelease>", self.next_summary_page)
        self.main.comboboxes[6].bind("<<ComboboxSelected>>",
                                     self.get_summary_graph)

    def get_combobox_values(self):
        self.main.comboboxes[0]["values"] = self.logic.get_airport_names()
        self.main.comboboxes[0].current(newindex=0)
        self.main.comboboxes[1]["values"] =\
            self.logic.get_dest_airports("Delhi")
        self.main.comboboxes[1].current(newindex=0)
        self.main.comboboxes[2]["values"] = self.logic.get_flight_codes()
        for i in range(3,5):
            self.main.comboboxes[i]["values"] = self.valid_airports

    def prev_summary_page(self, event):
        """
        event handler for getting the previous page of the summary.
        """
        self.logic.lower_index()
        self.main.text_boxes[2].config(state="normal")
        self.main.text_boxes[2].delete(1.0, "end")
        self.main.text_boxes[2].insert(
            tk.END, self.logic.get_summary_text())
        self.main.text_boxes[2].config(state="disabled")
        self.logic.get_summary_graph()

    def next_summary_page(self, event):
        """
        event handler for getting the next page of the summary.
        """
        self.logic.increase_index()
        self.main.text_boxes[2].config(state="normal")
        self.main.text_boxes[2].delete(1.0, "end")
        self.main.text_boxes[2].insert(
            tk.END, self.logic.get_summary_text())
        self.main.text_boxes[2].config(state="disabled")
        self.logic.get_summary_graph()

    def get_summary_graph(self, event):
        """
        event handler for notifying graphs in the summary page.
        """
        self.logic.get_summary_graph(event.widget.current())

    def get_valid_destination(self, event):
        """
        event handler for updating valid destinations.
        """
        src = event.widget.get()
        if src not in self.valid_airports:
            self.raise_invalid_message("Invalid airport")
            return
        index = self.main.comboboxes.index(event.widget)
        if index == 0:
            self.main.comboboxes[1]["values"] = (
                self.logic.get_dest_airports(src))
            self.main.comboboxes[1].delete(0, "end")
            self.main.comboboxes[2].delete(0, "end")
            self.main.comboboxes[2].config(state="disabled")
        elif index == 3:
            self.main.comboboxes[4]["values"] = (
                self.logic.get_dest_airports(src))
            self.main.comboboxes[4].delete(0, "end")

    def get_default_graphs(self):
        """
        gets the default graphs on startup.
        """
        for graphs in self.main.graphs:
            self.logic.attach(graphs)
        self.logic.notify()

    def update_dist_graph(self, event):
        """event handler for updating the flight search page's graph."""
        if event.widget.get() != "":
            src = self.main.comboboxes[0].get()
            if src not in self.valid_airports:
                self.raise_invalid_message("Invalid airport")
                return
            self.main.comboboxes[2].config(state="active")
            self.main.comboboxes[2].delete(0, "end")
            update_thread = threading.Thread(target=self.logic.get_price_graph(
                src, event.widget.get()))
            update_thread.start()
            self.main.comboboxes[2]["values"] = self.logic.get_flight_codes()

    def get_price_analysis(self, event):
        """event handler for getting the flight search's textbox."""
        for i in range(3):
            if self.main.comboboxes[i].get() == "":
                return
        flight = event.widget.get()
        self.main.text_boxes[0].config(state="normal")
        self.main.text_boxes[0].delete(1.0, "end")
        self.main.text_boxes[0].insert(tk.END,
                                    self.logic.generate_price_analysis(flight))
        self.main.text_boxes[0].config(state="disabled")

    def raise_invalid_message(self, msg):
        """
        Raises an error message.

        :param msg: A string to send a message to the user
        """
        for i in range(1):
            self.main.comboboxes[i].delete(0, "end")
        tk.messagebox.showerror("Value error",
                                message=msg)

    def tab_load_graph(self, event):
        """event handler for switching notebook tabs"""
        if event.widget.index("current") == 0:
            self.logic.state = 1
            self.logic.pair_city("Delhi", "Mumbai")
        elif event.widget.index("current") == 1:
            self.logic.state = 2
            self.main.mode.children["!radiobutton"].invoke()
            self.logic.get_availability()
        elif event.widget.index("current") == 2:
            self.logic.state = 3
            self.logic.get_summary_graph()
            self.main.text_boxes[2].insert(
                tk.END, self.logic.get_summary_text())

    def set_attribute_tab(self):
        """
        event handler for setting the attributes tab in the flight planner
        page.
        """
        self.current_state = self.states[self.main.mode.var.get()]
        self.current_state.set_components()

    def generate_graph(self, event):
        """event handler for generating graphs in the flight planner page"""
        self.current_state = self.states[self.main.mode.var.get()]
        self.current_state.get_graph()

    def temp_get_combobox_values(self, event):
        """
        event handler for updating combobox values in the flight planner page.
        """
        self.current_state = self.states[self.main.mode.var.get()]
        self.current_state.update_component_values()


class ControllerState(abc.ABC):
    """Defines the behavior of the controller depending on its state"""
    @abc.abstractmethod
    def set_components(self):
        """
        Set up the widgets to the right of the flight planner page depending.
        on the controller's mode. This is an abstract method.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_graph(self):
        """
        Gets the graph corresponding to the controller's mode.
        This is an abstract method.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update_component_values(self):
        """
        Updates combobox values depending on the controllers mode.
        This is an abstract method.
        """
        raise NotImplementedError


class AvailabilityState(ControllerState):
    """The Availability state of the controller"""
    def __init__(self, controller):
        self.controller = controller

    def set_components(self):
        """Refer to ControllerState.set_components"""
        self.controller.main.type["state"] = "disabled"
        self.controller.main.labels[0]["text"] = "From:"
        self.controller.main.labels[1]["text"] = "To:"
        for i in range(3, 5):
            self.controller.main.comboboxes[i]["values"] = (
                self.controller.valid_airports)
            self.controller.main.comboboxes[i].delete(0, "end")
        self.controller.main.comboboxes[5].config(state="disabled")

    def get_graph(self):
        src = self.controller.main.comboboxes[3].get()
        end = self.controller.main.comboboxes[4].get()
        update_thread = threading.Thread(
            target=self.controller.logic.pair_city(src, end))
        update_thread.start()
        self.controller.logic.get_availability()
        self.controller.main.text_boxes[1].config(state="normal")
        self.controller.main.text_boxes[1].delete(1.0, "end")
        self.controller.main.text_boxes[1].insert(
            tk.END, self.controller.logic.describe_statistics())
        self.controller.main.text_boxes[1].config(state="disabled")

    def update_component_values(self):
        """Refer to ControllerState.update_component_values"""


class DayState(ControllerState):
    """The days_left state of the controller"""
    def __init__(self, controler):
        self.controller = controler

    def set_components(self):
        """Refer to ControllerState.set_components"""
        self.controller.main.type["state"] = "disabled"
        self.controller.main.labels[0]["text"] = "From:"
        self.controller.main.comboboxes[3].delete(0, "end")
        for i in range(3, 5):
            self.controller.main.comboboxes[i]["values"] = (
                self.controller.valid_airports)
            self.controller.main.comboboxes[i].delete(0, "end")
        self.controller.main.labels[1]["text"] = "To:"
        self.controller.main.comboboxes[4].delete(0, "end")
        self.controller.main.labels[2]["text"] = "Flight code"
        self.controller.main.comboboxes[5].config(state="enabled")
        self.controller.main.comboboxes[5].delete(0, "end")

    def get_graph(self):
        """Refer to ControllerState.get_graph"""
        flight = self.controller.main.comboboxes[5].get()
        self.controller.logic.get_day_plot(flight)
        self.controller.main.text_boxes[1].config(state="normal")
        self.controller.main.text_boxes[1].delete(1.0, "end")
        self.controller.main.text_boxes[1].insert(
            tk.END, self.controller.logic.describe_statistics(flight, 2))
        self.controller.main.text_boxes[1].config(state="disabled")

    def update_component_values(self):
        """Refer to ControllerState.update_component_values"""
        src = self.controller.main.comboboxes[3].get()
        end = self.controller.main.comboboxes[4].get()
        self.controller.logic.graph_type = "Scatter"
        self.controller.logic.pair_city(src, end)
        self.controller.main.comboboxes[5]["values"] = (
            self.controller.logic.get_flight_codes())


class FrequencyState(ControllerState):
    """The frequency state of the controller"""
    def __init__(self, controller):
        self.controller = controller

    def set_components(self):
        """Refer to ControllerState.set_components"""
        self.controller.main.type["state"] = "disabled"
        self.controller.main.labels[0]["text"] = "x axis:"
        self.controller.main.comboboxes[3]["values"] = (
            self.controller.logic.get_countable_attributes())
        self.controller.main.comboboxes[3].delete(0, "end")
        self.controller.main.labels[1]["text"] = "y axis:"
        self.controller.main.comboboxes[4]["values"] = ["Frequency"]
        self.controller.main.comboboxes[4].current(newindex=0)
        self.controller.main.comboboxes[5].delete(0, "end")
        self.controller.main.comboboxes[5].config(state="disabled")
        self.controller.main.type["state"] = "active"
        self.controller.main.type.children["!radiobutton"].invoke()
        self.controller.main.type.set_button(2, "state", "disabled")

    def get_graph(self):
        """Refer to ControllerState.get_graph"""
        var = self.controller.main.comboboxes[3].get()
        if var not in self.controller.main.comboboxes[3]["values"]:
            self.controller.raise_invalid_message("Invalid attribute")
            return
        graph = self.controller.main.type.var.get()
        self.controller.logic.get_frequency_plot(var, graph)
        self.controller.main.text_boxes[1].config(state="normal")
        self.controller.main.text_boxes[1].delete(1.0, "end")
        self.controller.main.text_boxes[1].insert(
            tk.END, self.controller.logic.describe_statistics(mode=3))
        self.controller.main.text_boxes[1].config(state="disabled")

    def update_component_values(self):
        """Refer to ControllerState.update_component_values"""


class AirlineState(ControllerState):
    """The by airline state of the controller"""
    def __init__(self, controller):
        self.controller = controller

    def set_components(self):
        """Refer to ControllerState.set_components"""
        self.controller.main.type["state"] = "disabled"
        self.controller.main.labels[0]["text"] = "x axis:"
        self.controller.main.comboboxes[3]["values"] = ["Airline"]
        self.controller.main.comboboxes[3].current(newindex=0)
        self.controller.main.labels[1]["text"] = "y axis:"
        self.controller.main.comboboxes[4].delete(0, "end")
        self.controller.main.comboboxes[4]["values"] =\
            self.controller.logic.get_flight_class()
        self.controller.main.comboboxes[5].delete(0, "end")
        self.controller.main.comboboxes[5].config(state="disabled")

    def get_graph(self):
        """Refer to ControllerState.get_graph"""
        tier = self.controller.main.comboboxes[4].get()
        self.controller.logic.get_airline_graph(tier)
        self.controller.main.text_boxes[1].config(state="normal")
        self.controller.main.text_boxes[1].delete(1.0, "end")
        if tier == "Economy":
            self.controller.main.text_boxes[1].insert(
                tk.END, self.controller.logic.describe_statistics(mode=4))
        elif tier == "Business":
            self.controller.main.text_boxes[1].insert(
                tk.END, self.controller.logic.describe_statistics(mode=5))
        self.controller.main.text_boxes[1].config(state="disabled")

    def update_component_values(self):
        """Refer to ControllerState.update_component_values"""


class CorrelationState(ControllerState):
    """The correlation state of the controller"""
    def __init__(self, controller):
        self.controller = controller

    def set_components(self):
        """Refer to ControllerState.set_components"""
        self.controller.main.labels[0]["text"] = "x axis:"
        self.controller.main.comboboxes[3].delete(0, "end")
        self.controller.main.labels[1]["text"] = "y axis:"
        self.controller.main.comboboxes[4].delete(0, "end")
        self.controller.main.labels[2]["text"] = "Group by"
        for i in range(3, 5):
            self.controller.main.comboboxes[i]["values"] = (
                self.controller.logic.get_numerical_attributes()
            )
        self.controller.main.comboboxes[5].delete(0, "end")
        self.controller.main.comboboxes[5].config(state="disabled")
        self.controller.main.type["state"] = "active"
        self.controller.main.type.set_button(1, "state", "disabled")
        self.controller.main.type.children["!radiobutton2"].invoke()
        self.controller.main.type.set_button(3, "state", "disabled")

    def get_graph(self):
        """Refer to ControllerState.get_graph"""
        var1 = self.controller.main.comboboxes[3].get()
        var2 = self.controller.main.comboboxes[4].get()
        if var1 not in self.controller.main.comboboxes[3]["values"]:
            self.controller.raise_invalid_message("Invalid attribute")
        if var2 not in self.controller.main.comboboxes[4]["values"]:
            self.controller.raise_invalid_message("Invalid attribute")
        self.controller.logic.get_correlation_graph(var1, var2)
        self.controller.main.text_boxes[1].config(state="normal")
        self.controller.main.text_boxes[1].delete(1.0, "end")
        self.controller.main.text_boxes[1].insert(
            tk.END, self.controller.logic.describe_statistics(mode=6))
        self.controller.main.text_boxes[1].config(state="disabled")

    def update_component_values(self):
        """Refer to ControllerState.update_component_values"""
