import tkinter as tk
from tkinter import *
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from terminal.controller.controller import Controller


class TerminalWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Terminal window")
        self._titleLabel = Label(self, text="Meteo data real time plotting")
        self._titleLabel.grid(row=0)
        self._controller = None

        # self._figure = None
        # Create a Matplotlib canvas and embed it in the Tkinter window
        # canvas = FigureCanvasTkAgg(self._figure, master=self._window)
        # canvas.draw()
        # canvas.get_tk_widget().pack()

    def plot(self):
        # Create figure for plotting
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        x_date = []
        y_pollution = []
        y_wellness = []

        # This function is called periodically from FuncAnimation
        def animate(i, x_d, y_well, y_poll):
            result = self._controller.getResult()
            x_d.append(dt.datetime.fromtimestamp(result.datetime.ToSeconds()).strftime('%H:%M:%S'))
            y_well.append(result.wellness)
            y_poll.append(result.pollution)

            # Limit x and y lists to 20 items
            x_d = x_d[-20:]
            y_well = y_well[-20:]
            y_poll = y_poll[-20:]

            # Draw x and y lists
            ax.clear()
            ax.plot(x_d, y_well, label="Wellness index")
            ax.plot(x_d, y_poll, label="Pollution index")

            # Format plot
            plt.xticks(rotation=45, ha='right')
            plt.subplots_adjust(bottom=0.30)
            plt.title('Wellness and Pollution indexes')
            plt.xlabel('Date')

        # Set up plot to call animate() function periodically
        ani = animation.FuncAnimation(fig, animate, fargs=(x_date, y_wellness, y_pollution), interval=1000)
        plt.show()

    def setController(self, controller):
        self._controller = controller
