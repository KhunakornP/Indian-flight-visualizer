import abc
import threading
import tkinter as tk
from tkinter import ttk, font
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from keypad import Keypad
matplotlib.use("TkAgg")


# for testing
df = pd.read_csv("Indian Airlines.csv")


class VisualizerUI(tk.Tk):
    """UI class for the visualizer"""
    def __init__(self):
        super().__init__()
        self.title("Indian flight visualizer")
        self.comboboxes = []
        self.graphs = []
        self.price_analysis = None
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Times", size=22)
        self.init_components()

    def init_components(self):
        """Initializes the ui components"""
        self.option_add("*TCombobox*Listbox*Font", self.default_font)
        self.init_menu()
        self.init_notebook()

    def init_menu(self):
        """Initialize the top menu of the ui"""
        menu_font = self.default_font
        menu_font.configure(size=18)
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit, font=menu_font)
        menu_bar.add_cascade(label="File", menu=file_menu, font=menu_font)
        self.configure(menu=menu_bar)

    def init_notebook(self):
        """Initializes the notebook"""
        notebook = ttk.Notebook(self,width=2000, height=1000)
        notebook.pack(pady=10, expand=True, anchor=tk.N, fill="both")
        names = ["Flight search", "Flight planner", "Data summary"]
        notebook.add(self.init_flight_search(), text=names[0])
        notebook.add(self.init_flight_planner(), text=names[1])
        notebook.add(self.init_data_summary(), text=names[2])

    def init_flight_search(self):
        """Initializes the flight search page"""
        mainframe = tk.Frame(self)
        frame1 = tk.Frame(mainframe)
        frame2 = tk.Frame(mainframe)
        frame3 = tk.Frame(mainframe)
        text_label = tk.Label(frame3, text="Price analysis", anchor=tk.N)
        text_label.pack(expand=True, fill='both')
        self.price_analysis = tk.Text(frame3, font=self.default_font,
                                      width=0, height=20)
        self.price_analysis.pack(expand=True, fill="both", padx=10, pady=5)
        self.price_analysis.configure(state="disabled")
        placeholder = GraphManager(frame2)
        self.graphs.append(placeholder)
        placeholder.pack(expand=True, fill="both", anchor=tk.CENTER)
        from_label = tk.Label(frame1, text="From:")
        from_combo = ttk.Combobox(frame1,font=self.default_font)
        self.comboboxes.append(from_combo)
        to_label = tk.Label(frame1, text="To:")
        to_combo = ttk.Combobox(frame1,font=self.default_font)
        self.comboboxes.append(to_combo)
        flight_label = tk.Label(frame1, text="Flight:")
        flight_combo = ttk.Combobox(frame1,font=self.default_font)
        self.comboboxes.append(flight_combo)
        settings = {"padx":5, "pady":5, "anchor":tk.W,
                    "expand":True, "fill":"both"}
        from_label.pack(**settings)
        from_combo.pack(**settings)
        to_label.pack(**settings)
        to_combo.pack(**settings)
        flight_label.pack(**settings)
        flight_combo.pack(**settings)
        mainframe.grid_columnconfigure((0, 1, 2, 3, 4, 5),
                                       uniform="1", weight=1)
        mainframe.grid_rowconfigure((0, 1), uniform="1", weight=1)
        settings = {"padx":5, "pady":5}
        frame1.grid(row=0, column=0, sticky="nsew", rowspan=2, **settings)
        frame2.grid(row=0, column=1, sticky="nsew", rowspan=2, columnspan=3,
                    **settings)
        frame3.grid(row=0, column=4, sticky="nsew", rowspan=2, columnspan=2,
                    **settings)
        mainframe.pack(fill='both', expand=True)
        return mainframe

    def init_flight_planner(self):
        """Initializes the flight planner page"""
        mainframe = tk.Frame(self)
        frame2 = tk.Frame(mainframe)
        mode_select = Keypad(frame2, ["Availability","Days booked",
                                    "Frequency", "By airport", "By pair"],
                             label="mode:")
        type_select = Keypad(frame2, ["Distribution", "Scatter",
                                    "Histogram"], label="Type:")
        graph = GraphManager(mainframe)
        self.graphs.append(graph)
        statistic = tk.Text(frame2)
        mainframe.pack(fill="both", expand=True)
        mainframe.grid_columnconfigure((0,1,2), uniform="1", weight=1)
        mainframe.grid_rowconfigure((0,1), uniform="1", weight=1)
        settings = {"padx": 10, "pady": 5, "expand": True,
                    "fill": "both"}
        mode_select.pack(**settings, side=tk.LEFT)
        type_select.pack(**settings, side=tk.LEFT)
        statistic.pack(**settings, side=tk.LEFT)
        frame2.grid(row=0, column=0, sticky="ew", columnspan=2)
        graph.grid(row=1, column=0, sticky="ew",columnspan=2, padx=10, pady=5)
        return mainframe

    def init_data_summary(self):
        """Initializes the data summary page"""
        mainframe = tk.Frame(self)
        frame1 = tk.Frame(mainframe)
        placeholder = GraphManager(mainframe)
        self.graphs.append(placeholder)
        frame2 = tk.Frame(mainframe)
        graph_label = tk.Label(frame1, text="Graph selector:")
        graph_select = ttk.Combobox(frame1,font=self.default_font)
        self.comboboxes.append(graph_select)
        sum_label = tk.Label(frame2, text="Exploration:")
        sum_text = tk.Text(frame2)
        settings = {"padx": 10, "pady": 5, "expand": True,
                    "fill": "both"}
        graph_label.pack(**settings, anchor=tk.N)
        graph_select.pack(expand=True, fill="both", pady=150, padx=10
                          , anchor=tk.CENTER)
        sum_label.pack(**settings)
        sum_text.pack(**settings)
        frame1.pack(fill="both", expand=True, side=tk.LEFT)
        placeholder.pack(fill="both", expand=True, side=tk.LEFT)
        frame2.pack(fill="both", expand=True, side=tk.RIGHT)
        mainframe.pack(fill="both", expand=True)
        return mainframe

    def run(self):
        """Runs the app"""
        self.mainloop()


class Observer(abc.ABC):
    @abc.abstractmethod
    def update_graph(self, logic):
        """Receive an update from the model"""
        raise NotImplementedError


class GraphManager(tk.Frame, Observer):
    """A class for managing graphs"""
    def __init__(self, parent, graph_type=1):
        super().__init__(parent)
        self.type = graph_type
        self.init_components()

    def init_components(self):
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(figure=self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH,
                                         expand=True)

    def update_graph(self, logic):
        if self.type == logic.state:
            self.draw(logic)

    def draw(self, logic):
        if self.type == 1:
            self.draw_dist_plot(logic.cur_df, logic.pair)

    def draw_dist_plot(self, data, pair):
        """Draw the graph from the dataframe"""
        self.ax.clear()
        self.ax.set_title(f"price distribution of flights from {pair[0]} to {pair[1]}")
        self.ax.set_xlabel("price (rupee)")
        sns.histplot(data=data, x="price", log_scale=True,
                               hue="class", ax=self.ax)
        self.canvas.draw()


if __name__ == "__main__":
    f = VisualizerUI()
    f.run()
