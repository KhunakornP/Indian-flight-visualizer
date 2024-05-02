"""Controllers for the visualizer's UI"""
import tkinter as tk


class Controller:
    def __init__(self, ui, logic):
        self.main = ui
        self.logic = logic
        self.get_combobox_values()
        self.bind_components()

    def bind_components(self):
        for i in range(3):
            self.main.comboboxes[i].bind("<<ComboboxSelected>>",
                                         self.get_price_analysis)

    def get_combobox_values(self):
        for i in range(2):
            self.main.comboboxes[i]["values"] = self.logic.get_airport_names()
            self.main.comboboxes[i].current(newindex=i)
        self.main.comboboxes[2]["values"] = self.logic.get_flight_codes()

    def get_price_analysis(self, event):
        for i in range(3):
            if self.main.comboboxes[i].get() == "":
                return
        flight = self.main.comboboxes[2].get()
        self.main.price_analysis.insert(tk.END,
                                        self.logic.generate_price_analysis(flight))

