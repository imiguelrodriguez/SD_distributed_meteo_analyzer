from concurrent import futures

import terminal.view.terminalWindow


class Controller:
    def __init__(self, model):
        self._model = model
        self._view = None

    def getResult(self):
        return self._model.resultsQueue.get(block=True)

    def initPlot(self):
        executor = futures.ThreadPoolExecutor(max_workers=5)
        executor.submit(self._view.plot)

    def runWindow(self):
        self.initPlot()
        self._view.mainloop()

    def createWindow(self):
        root = terminal.view.terminalWindow.TerminalWindow()
        self._view = root
        return root
