import pandas as pd
from visualizer_ui import VisualizerUI
from model_logic import DataframeLogic
from controllers import Controller
import os


if __name__ == "__main__":
    orig_df = pd.read_csv(os.path.join(os.getcwd(), "Datasets",
                                       "Indian Airlines.csv"))
    model = DataframeLogic(orig_df)
    ui = VisualizerUI()
    controller = Controller(ui, model)
    controller.main.run()
