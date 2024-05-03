"""Controllers for the visualizer's UI"""
import tkinter as tk
import threading


class Controller:
    def __init__(self, ui, logic):
        self.main = ui
        self.logic = logic
        self.get_combobox_values()
        self.get_default_graphs()
        self.bind_components()

    def bind_components(self):
        self.main.comboboxes[0].bind("<<ComboboxSelected>>",
                                     self.get_valid_destination)
        self.main.comboboxes[1].bind("<<ComboboxSelected>>",
                                     self.update_dist_graph)
        self.main.comboboxes[2].bind("<<ComboboxSelected>>",
                                     self.get_price_analysis)

    def get_combobox_values(self):
        self.main.comboboxes[0]["values"] = self.logic.get_airport_names()
        self.main.comboboxes[0].current(newindex=0)
        self.main.comboboxes[1]["values"] =\
            self.logic.get_dest_airports("Delhi")
        self.main.comboboxes[1].current(newindex=0)
        self.main.comboboxes[2]["values"] = self.logic.get_flight_codes()

    def get_valid_destination(self, event):
        src = event.widget.get()
        self.main.comboboxes[1]["values"] = self.logic.get_dest_airports(src)
        self.main.comboboxes[1].delete(0, "end")
        self.main.comboboxes[2].delete(0, "end")
        self.main.comboboxes[2].config(state="disabled")

    def get_default_graphs(self):
        for graphs in self.main.graphs:
            self.logic.attach(graphs)
        self.logic.notify()

    def update_dist_graph(self, event):
        if event.widget.get() != "":
            src = self.main.comboboxes[0].get()
            self.main.comboboxes[2].config(state="active")
            self.main.comboboxes[2].delete(0, "end")
            update_thread = threading.Thread(target=self.logic.pair_city(src, event.widget.get()))
            update_thread.start()

    def get_price_analysis(self, event):
        for i in range(3):
            if self.main.comboboxes[i].get() == "":
                return
        flight = event.widget.get()
        self.main.price_analysis.delete(1.0, "end")
        self.main.price_analysis.insert(tk.END,
                                        self.logic.generate_price_analysis(flight))

