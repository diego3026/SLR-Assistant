class AppState:

    def __init__(self):
        self.topic = ""
        self.objectives = ""
        self.notes = ""
        self.equation = ""
        self.csv_path = ""
        self.results = None
        self.listeners = []
        self.history = []
        self.model_metrics = None
        
    def subscribe(self, callback):
        self.listeners.append(callback)

    def notify(self):
        for callback in self.listeners:
            callback()

state = AppState()