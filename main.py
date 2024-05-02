import pandas as pd
from visualizer_ui import VisualizerUI
from model_logic import DataframeLogic
from controllers import Controller


orig_df = pd.read_csv("Indian Airlines.csv")
model = DataframeLogic(orig_df)
ui = VisualizerUI()
controller = Controller(ui, model)
controller.main.run()