"""Controllers for the visualizer's UI"""
import tkinter as tk
from tkinter import messagebox
import threading


class Controller:
    def __init__(self, ui, logic):
        self.main = ui
        self.logic = logic
        self.valid_airports = self.logic.get_airport_names()
        self.get_combobox_values()
        self.get_default_graphs()
        self.bind_components()

    def bind_components(self):
        self.main.notebook.bind("<<NotebookTabChanged>>", self.tab_load_graph)
        self.main.comboboxes[0].bind("<<ComboboxSelected>>",
                                     self.get_valid_destination)
        self.main.comboboxes[1].bind("<<ComboboxSelected>>",
                                     self.update_dist_graph)
        self.main.comboboxes[2].bind("<<ComboboxSelected>>",
                                     self.get_price_analysis)
        self.main.comboboxes[2].bind("<Return>", self.get_price_analysis)
        self.main.button.bind("<Button>", self.generate_graph)
        self.main.mode.configure(command=self.set_attribute_tab)
        self.main.comboboxes[4].bind("<<ComboboxSelected>>",
                                     self.temp_get_flight_codes)

    def get_combobox_values(self):
        self.main.comboboxes[0]["values"] = self.logic.get_airport_names()
        self.main.comboboxes[0].current(newindex=0)
        self.main.comboboxes[1]["values"] =\
            self.logic.get_dest_airports("Delhi")
        self.main.comboboxes[1].current(newindex=0)
        self.main.comboboxes[2]["values"] = self.logic.get_flight_codes()
        for i in range(3,5):
            self.main.comboboxes[i]["values"] = self.valid_airports

    def get_valid_destination(self, event):
        src = event.widget.get()
        if src not in self.valid_airports:
            self.raise_invalid_airport()
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
        for graphs in self.main.graphs:
            self.logic.attach(graphs)
        self.logic.notify()

    def update_dist_graph(self, event):
        if event.widget.get() != "":
            src = self.main.comboboxes[0].get()
            if src not in self.valid_airports:
                self.raise_invalid_airport()
                return
            self.main.comboboxes[2].config(state="active")
            self.main.comboboxes[2].delete(0, "end")
            update_thread = threading.Thread(target=self.logic.get_price_graph(
                src, event.widget.get()))
            update_thread.start()
            self.main.comboboxes[2]["values"] = self.logic.get_flight_codes()

    def get_price_analysis(self, event):
        for i in range(3):
            if self.main.comboboxes[i].get() == "":
                return
        flight = event.widget.get()
        self.main.price_analysis.config(state="normal")
        self.main.price_analysis.delete(1.0, "end")
        self.main.price_analysis.insert(tk.END,
                                        self.logic.generate_price_analysis(flight))
        self.main.price_analysis.config(state="disabled")

    def raise_invalid_airport(self):
        for i in range(1):
            self.main.comboboxes[i].delete(0, "end")
        tk.messagebox.showerror("Value error",
                                message="Invalid airport")

    def tab_load_graph(self, event):
        if event.widget.index("current") == 0:
            self.logic.state = 1
            update_thread = threading.Thread(target=self.logic.pair_city,
                                             args=("Delhi", "Mumbai"))
            update_thread.start()
        elif event.widget.index("current") == 1:
            self.logic.state = 2
            self.main.mode.children["!radiobutton"].invoke()
            update_thread = threading.Thread(target=
                                             self.logic.get_availability)
            update_thread.start()

    def set_attribute_tab(self):
        if self.main.mode.var.get() == 0:
            self.main.type["state"] = "disabled"
            self.main.labels[0]["text"] = "From:"
            self.main.labels[1]["text"] = "To:"
            for i in range(3,5):
                self.main.comboboxes[i]["values"] = self.valid_airports
                self.main.comboboxes[i].delete(0, "end")
            self.main.comboboxes[5].config(state="disabled")
        elif self.main.mode.var.get() == 1:
            self.main.type["state"] = "disabled"
            self.main.labels[0]["text"] = "From:"
            self.main.comboboxes[3].delete(0, "end")
            self.main.labels[1]["text"] = "To:"
            self.main.comboboxes[4].delete(0, "end")
            self.main.labels[2]["text"] = "Flight code"
            self.main.comboboxes[5].config(state="enabled")
        elif self.main.mode.var.get() == 2:
            self.main.type["state"] = "disabled"
            self.main.labels[0]["text"] = "x axis:"
            self.main.comboboxes[3].delete(0, "end")
            self.main.labels[1]["text"] = "y axis:"
            self.main.comboboxes[4]["values"] = ["Frequency"]
            self.main.comboboxes[4].current(newindex=0)
            self.main.comboboxes[5].config(state="disabled")
        elif self.main.mode.var.get() == 3:
            self.main.type["state"] = "disabled"
            self.main.labels[0]["text"] = "x axis:"
            self.main.comboboxes[3]["values"] = ["Airport"]
            self.main.comboboxes[3].current(newindex=0)
            self.main.labels[1]["text"] = "y axis:"
            self.main.comboboxes[4].delete(0, "end")
            self.main.comboboxes[5].config(state="disabled")
        elif self.main.mode.var.get() == 4:
            self.main.labels[0]["text"] = "x axis:"
            self.main.comboboxes[3].delete(0, "end")
            self.main.labels[1]["text"] = "y axis:"
            self.main.comboboxes[4].delete(0, "end")
            self.main.labels[2]["text"] = "Group by"
            self.main.comboboxes[5].config(state="enabled")
            self.main.type["state"] = "active"

    def generate_graph(self, event):
        if self.main.mode.var.get() == 0:
            src = self.main.comboboxes[3].get()
            end = self.main.comboboxes[4].get()
            update_thread = threading.Thread(
                target=self.logic.pair_city(src, end))
            update_thread.start()
            self.logic.get_availability()
        elif self.main.mode.var.get() == 1:
            flight = self.main.comboboxes[5].get()
            self.logic.get_day_plot(flight)

    def temp_get_flight_codes(self, event):
        """Note don't forget to move everything to state pattern"""
        if self.main.mode.var.get() == 1:
            src = self.main.comboboxes[3].get()
            end = event.widget.get()
            self.logic.graph_type = "Scatter"
            self.logic.pair_city(src, end)
            self.main.comboboxes[5]["values"] = self.logic.get_flight_codes()
