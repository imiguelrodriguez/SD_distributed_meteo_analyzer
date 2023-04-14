import tkinter
import tkinter as tk
from tkinter import *
import datetime as dt
from tkinter import ttk

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas


class Table:
    def __init__(self, root, headers, data):
        self.root = root
        self.reWrite(root, headers, data)
        j = 0
        for header in headers:
            e = Entry(root, width=20, fg='black',
                      font=('Arial', 18, 'bold'), background='grey')
            e.configure(state='normal')
            e.grid(row=0, column=j)
            e.insert(END, header)
            e.configure(state='disabled', disabledbackground="gray", disabledforeground="black")
            j += 1

    def reWrite(self, root, headers, data):
        for i in range(1, len(data) + 1):
            for j in range(len(headers)):
                e = Entry(root, width=20, fg='blue',
                          font=('Arial', 16, 'bold'))
                e.configure(state='normal')
                e.grid(row=i, column=j)
                e.insert(END, data[i - 1][j])
                if j != 0:
                    e.configure(state='disabled', disabledbackground="white",
                                disabledforeground=self.getColor(j, data[i - 1][j]))
                else:
                    e.configure(state='disabled', disabledbackground="white",
                                disabledforeground="black")

    def getColor(self, index, value):
        value = float(value)
        if index == 1:
            if value < 0.25:
                return "red"
            elif value < 0.5:
                return "orange"
            elif value < 0.75:
                return "gold2"
            else:
                return "green"
        else:
            if value < 0.25:
                return "green"
            elif value < 0.5:
                return "gold2"
            elif value < 0.75:
                return "orange"
            else:
                return "red"


class TerminalWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Terminal window")
        self.minsize(400, 400)
        self._titleLabel = Label(self, text="Meteo data real time plotting", font=("Arial", 20, "bold"))
        self._titleLabel.pack(anchor="n", padx=10, pady=10)
        self._controller = None
        self._figure = plt.figure()
        self._canvas = FigureCanvas(self._figure)
        self._toolbar = NavigationToolbar2Tk(self._canvas, self, pack_toolbar=False)
        self._toolbar.update()
        self._canvas.get_tk_widget().pack(anchor="center", padx=10, pady=10)
        self._toolbar.pack(anchor="center", padx=10, pady=10)
        self._wWAverage = 0.0
        self._hWAverage = 0.0
        self._wPAverage = 0.0
        self._hPAverage = 0.0
        self._wWMax = 0.0
        self._wPMax = 0.0
        self._hWMax = 0.0
        self._hPMax = 0.0
        self._wWMin = float("inf")
        self._wPMin = float("inf")
        self._hWMin = float("inf")
        self._hPMin = float("inf")
        self._x_date = []
        self._y_pollution = []
        self._y_wellness = []

        self._headers = ["Statistics", "Wellness", "Pollution"]
        data = [["Window Average", self._wWAverage, self._wPAverage],
                ["Historical Average", self._hWAverage, self._hPAverage],
                ["Window Maximum", self._wWMax, self._wPMax],
                ["Historical Maximum", self._hWMax, self._hPMax],
                ["Window Minimum", self._wWMin, self._wPMin],
                ["Historical Minimum", self._hWMin, self._hPMin]]
        self._frame = tk.Frame(self)
        self._frame.pack(anchor="s", padx=10, pady=10)
        self._table = Table(self._frame, self._headers, data)


    def updateTable(self):
        self._wWAverage = round(sum(self._y_wellness) / len(self._y_wellness), 2)
        self._hWAverage = round((self._wWAverage + self._hWAverage) / 2, 2)
        self._wPAverage = round(sum(self._y_pollution) / len(self._y_pollution), 2)
        self._hPAverage = round((self._wPAverage + self._hPAverage) / 2, 2)
        self._wWMax = round(max(self._y_wellness), 2)
        self._wPMax = round(max(self._y_pollution), 2)
        self._hWMax = round(max(self._wWMax, self._hWMax), 2)
        self._hPMax = round(max(self._wPMax, self._hPMax), 2)
        self._wWMin = round(min(self._y_wellness), 2)
        self._wPMin = round(min(self._y_pollution), 2)
        self._hWMin = round(min(self._wWMin, self._hWMin), 2)
        self._hPMin = round(min(self._wPMin, self._hPMin), 2)
        data = [["Window Average", self._wWAverage, self._wPAverage],
                ["Historical Average", self._hWAverage, self._hPAverage],
                ["Window Maximum", self._wWMax, self._wPMax],
                ["Historical Maximum", self._hWMax, self._hPMax],
                ["Window Minimum", self._wWMin, self._wPMin],
                ["Historical Minimum", self._hWMin, self._hPMin]]
        self._table.reWrite(self._frame, self._headers, data)

    def plot(self):
        # Create figure for plotting
        self._figure.clear()
        ax = self._figure.add_subplot(1, 1, 1)

        # This function is called periodically from FuncAnimation
        def animate(i, x_d, y_well, y_poll):
            result = self._controller.getResult()
            x_d.append(result.datetime)
            y_well.append(result.wellness)
            y_poll.append(result.pollution)
            # Limit x and y lists to 20 items
            x_d = x_d[-20:]
            y_well = y_well[-20:]
            y_poll = y_poll[-20:]

            self.updateTable()
            # Draw x and y lists
            ax.clear()
            ax.plot(x_d, y_well, label="Wellness index")
            ax.plot(x_d, y_poll, label="Pollution index")

            # Format plot
            plt.xticks(rotation=45, ha='right')
            plt.subplots_adjust(bottom=0.30)
            plt.title('Wellness and Pollution indexes')
            plt.xlabel('Date')
            plt.ylabel('Index')
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.22),
                       shadow=True, ncol=2)


        # Set up plot to call animate() function periodically
        ani = animation.FuncAnimation(self._figure, animate, fargs=(self._x_date, self._y_wellness, self._y_pollution),
                                      interval=3000, cache_frame_data=False)

        self._canvas.draw()

    def setController(self, controller):
        self._controller = controller
