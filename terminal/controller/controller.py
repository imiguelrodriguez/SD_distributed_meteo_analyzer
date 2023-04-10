
class Controller:
    def __init__(self, view, model):
        self._model = model
        self._view = view

    def getResult(self):
        return self._model.resultsQueue.get(block=True)

    def initPlot(self):
        self._view.plot()

    def runWindow(self):
        self._view.mainloop()
