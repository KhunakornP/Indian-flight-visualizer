import tkinter as tk
from tkinter import ttk, font
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
matplotlib.use("TkAgg")


# for testing
df = pd.read_csv("Indian Airlines.csv")


class VisualizerUI(tk.Tk):
    """UI class for the visualizer"""
    def __init__(self):
        super().__init__()
        self.title("Indian flight visualizer")
        self.from_city = tk.StringVar()
        self.to_city = tk.StringVar()
        self.flight = tk.StringVar()
        self.cur_graph = tk.StringVar()
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Times", size=22)
        self.init_menu()
        self.init_notebook()

    def init_components(self):
        """Initializes the ui components"""
        pass

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
        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, expand=True, anchor=tk.N, fill="both")
        names = ["Flight search", "Flight planner", "Data summary"]
        notebook.add(self.init_flight_search(), text=names[0])
        page = tk.Frame(notebook, width=400, height=400)
        notebook.add(page, text=names[1])
        notebook.add(self.init_data_summary(), text=names[2])
        # for i in range(3):
        #     page = tk.Frame(notebook, width=400, height=400)
        #     page.pack(fill='both', expand=True)
        #     notebook.add(page, text=names[i])

    def init_flight_search(self):
        """Initializes the flight search page"""
        mainframe = tk.Frame(self)
        frame1 = tk.Frame(mainframe)
        frame2 = tk.Frame(mainframe)
        frame3 = tk.Frame(mainframe)
        text_sum = tk.Label(frame3, text="Price analysis", anchor=tk.N)
        text_sum.pack(expand=True, fill='both')
        placeholder = GraphManager(frame2, df)
        placeholder.pack(expand=True, fill="both")
        from_label = tk.Label(frame1, text="From:")
        from_combo = ttk.Combobox(frame1,font=self.default_font, textvariable=self.from_city)
        to_label = tk.Label(frame1, text="To:")
        to_combo = ttk.Combobox(frame1,font=self.default_font, textvariable=self.to_city)
        flight_label = tk.Label(frame1, text="Flight:")
        flight_combo = ttk.Combobox(frame1,font=self.default_font, textvariable=self.flight)
        settings = {"padx":10, "pady":5, "anchor":tk.W,"expand":True, "fill":"y"}
        from_label.pack(**settings)
        from_combo.pack(**settings)
        to_label.pack(**settings)
        to_combo.pack(**settings)
        flight_label.pack(**settings)
        flight_combo.pack(**settings)
        frame1.pack(fill="both", expand=True, side=tk.LEFT)
        frame2.pack(fill="both", expand=True, side=tk.LEFT)
        frame3.pack(fill="both", expand=True, side=tk.RIGHT)
        mainframe.pack(fill='both', expand=True)
        return mainframe

    def init_flight_planner(self):
        """Initializes the flight planner page"""
        pass

    def init_data_summary(self):
        """Initializes the data summary page"""
        mainframe = tk.Frame(self)
        frame1 = tk.Frame(mainframe)
        placeholder = GraphManager(mainframe, df)
        frame2 = tk.Frame(mainframe)
        graph_label = tk.Label(frame1, text="Graph selector:")
        graph_select = ttk.Combobox(frame1,font=self.default_font,
                                    textvariable=self.cur_graph)
        sum_label = tk.Label(frame2, text="Exploration:")
        sum_text = tk.Text(frame2)
        settings = {"padx": 10, "pady": 5, "expand": True,
                    "fill": "both"}
        graph_label.pack(**settings)
        graph_select.pack(**settings)
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


class GraphManager(tk.Frame):
    """A class for managing graphs"""
    def __init__(self, parent, df):
        super().__init__(parent)
        self.df = df
        self.draw()

    def draw(self):
        """Draw the graph from the dataframe"""
        fig, ax = plt.subplots(figsize=(6,6), dpi=100)
        sns.histplot(df, x="price")
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def update_graph(self, x,y):
        """Updates the graph"""
        pass

if __name__ == "__main__":
    f = VisualizerUI()
    f.run()
