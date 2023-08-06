from .mlmodel import MLModel
from .plot import Plot
from .request import Request


class Execution:

    def __init__(self, experiment_id=None, experiment_type=None, request: Request = None):
        self.experiment_id = experiment_id

        # Experiment Type = "function" or "anomaly_detection"
        self.experiment_type = experiment_type

        # Execution = "wizard" automl or "simulate" execute trained wizatads
        self.execution_type = "wizard"

        self.request = request
        self.dataframe = None
        self.models = []
        self.anomalies = []
        self.plots = []

        self.result_dataframe = None

    def append_plot(self, figure, name="Unkwown"):
        plot = Plot(name)
        plot.experiment_id = self.experiment_id
        plot.figure = figure
        self.plots.append(plot)
        return plot

    def append_model(self, trained_model, input_columns, output_columns=None, has_anomalies=False, scaler=None):
        ml_model = MLModel()

        ml_model.trained_model = trained_model
        ml_model.scaler = scaler

        ml_model.input_columns = input_columns
        ml_model.output_columns = output_columns

        ml_model.has_anomalies = has_anomalies

        self.models.append(ml_model)
        return ml_model
