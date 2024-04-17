import tkinter as tk
from tkinter import ttk


class VisualizerUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Indian flight visualizer")
        self.init_notebook()

    def init_components(self):
        pass

    def init_notebook(self):
        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, expand=True, anchor=tk.N, fill="both")
        names = ["Flight search", "Flight planner", "Data summary"]
        for i in range(3):
            page = tk.Frame(notebook, width=400, height=400)
            page.pack(fill='both', expand=True)
            notebook.add(page, text=names[i])

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    f = VisualizerUI()
    f.run()