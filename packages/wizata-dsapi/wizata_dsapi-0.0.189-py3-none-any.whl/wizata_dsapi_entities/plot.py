import uuid


class Plot:

    def __init__(self, name="Unknown", experiment_id=None):
        self.plot_id = uuid.uuid4()
        self.name = name
        self.experiment_id = experiment_id
        self.figure = None
