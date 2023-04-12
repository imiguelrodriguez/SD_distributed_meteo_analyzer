import tkinter
import tkinter as tk
from tkinter import *
import datetime as dt
from tkinter import ttk

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas


class TerminalWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        def fixed_map(option):
            # Fix for setting text colour for Tkinter 8.6.9
            # From: https://core.tcl.tk/tk/info/509cafafae
            #
            # Returns the style map for 'option' with any styles starting with
            # ('!disabled', '!selected', ...) filtered out.

            # style.map() returns an empty list for missing options, so this
            # should be future-safe.
            return [elm for elm in style.map('Treeview', query_opt=option) if
                    elm[:2] != ('!disabled', '!selected')]

        style = ttk.Style()
        style.map('Treeview', foreground=fixed_map('foreground'),
                  background=fixed_map('background'))

        # Adding a title to the window
        self.wm_title("Terminal window")
        self._titleLabel = Label(self, text="Meteo data real time plotting", font=("Arial", 20, "bold"))
        self._titleLabel.grid(row=0, padx=10, pady=10)
        self._controller = None
        self._figure = plt.figure()
        self._canvas = FigureCanvas(self._figure)
        self._toolbar = NavigationToolbar2Tk(self._canvas, self, pack_toolbar=False)
        self._toolbar.grid(row=2)
        self._toolbar.update()
        self._canvas.get_tk_widget().grid(row=1)
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
        self._tree = ttk.Treeview(self)

        # Define the columns of the table
        self._tree["columns"] = ("Wellness", "Pollution")
        self._tree.tag_configure("bold", font=("Consolas", 13, "bold"))
        self._tree.tag_configure("red_text", font=("Consolas", 13, "bold"), foreground="red")
        self._tree.tag_configure("green_text", font=("Consolas", 13, "bold"), foreground="green")
        self._tree.tag_configure("orange_text", font=("Consolas", 13, "bold"), foreground="orange")
        self._tree.tag_configure("yellow_text", font=("Consolas", 13, "bold"), foreground="yellow")
        # Add headings for each column
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))
        self._tree.heading("#0", text="Statistics", anchor=tkinter.CENTER)
        self._tree.heading("Wellness", text="Wellness", anchor=tkinter.CENTER)
        self._tree.heading("Pollution", text="Pollution", anchor=tkinter.CENTER)

        # Add some data to the table
        self._tree.insert("", "end", text="Historical Average", values=(0.0, 0.0))
        self._tree.insert("", "end", text="Window Average", values=(0.0, 0.0))
        self._tree.insert("", "end", text="Historical Maximum", values=(0.0, 0.0))
        self._tree.insert("", "end", text="Window Maximum", values=(0.0, 0.0))
        self._tree.insert("", "end", text="Historical Minimum", values=(0.0, 0.0))
        self._tree.insert("", "end", text="Window Minimum", values=(0.0, 0.0))

        # Store the item identifiers in a dictionary
        self._items = {
            "Historical Average": self._tree.get_children()[0],
            "Window Average": self._tree.get_children()[1],
            "Historical Maximum": self._tree.get_children()[2],
            "Window Maximum": self._tree.get_children()[3],
            "Historical Minimum": self._tree.get_children()[4],
            "Window Minimum": self._tree.get_children()[5]
        }

        for row in self._tree.get_children():
            self._tree.item(row, tags=("bold",))
        self._tree.grid(row=1, column=1, padx=10, pady=10)

    def updateTable(self):
        self._wWAverage = round(sum(self._y_wellness) / len(self._y_wellness), 2)
        self._tree.set(self._items["Window Average"], "Wellness", self._wWAverage)
        self._tree.item(self._items["Window Average"], tag=(self.getColor("Wellness", self._wWAverage),))
        self._hWAverage = round((self._wWAverage + self._hWAverage) / 2, 2)
        self._tree.set(self._items["Historical Average"], "Wellness", self._hWAverage)
        self._wPAverage = round(sum(self._y_pollution) / len(self._y_pollution), 2)
        self._tree.set(self._items["Window Average"], "Pollution", self._wPAverage)
        self._hPAverage = round((self._wPAverage + self._hPAverage) / 2, 2)
        self._tree.set(self._items["Historical Average"], "Pollution", self._hPAverage)
        self._wWMax = round(max(self._y_wellness), 2)
        self._tree.set(self._items["Window Maximum"], "Wellness", self._wWMax)
        self._wPMax = round(max(self._y_pollution), 2)
        self._tree.set(self._items["Window Maximum"], "Pollution", self._wPMax)
        self._hWMax = round(max(self._wWMax, self._hWMax), 2)
        self._tree.set(self._items["Historical Maximum"], "Wellness", self._hWMax)
        self._hPMax = round(max(self._wPMax, self._hPMax), 2)
        self._tree.set(self._items["Historical Maximum"], "Pollution", self._hPMax)
        self._wWMin = round(min(self._y_wellness), 2)
        self._tree.set(self._items["Window Minimum"], "Wellness", self._wWMin)
        self._wPMin = round(min(self._y_pollution), 2)
        self._tree.set(self._items["Window Minimum"], "Pollution", self._wPMin)
        self._hWMin = round(min(self._wWMin, self._hWMin), 2)
        self._tree.set(self._items["Historical Minimum"], "Wellness", self._hWMin)
        self._hPMin = round(min(self._wPMin, self._hPMin), 2)
        self._tree.set(self._items["Historical Minimum"], "Pollution", self._hPMin)

    def getColor(self, index, value):
        if index == "Wellness":
            if value < 0.25:
                return "red_text"
            elif value < 0.5:
                return "orange_text"
            elif value < 0.75:
                return "yellow_text"
            else:
                return "green_text"
        else:
            if value < 0.25:
                return "green_text"
            elif value < 0.5:
                return "yellow_text"
            elif value < 0.75:
                return "orange_text"
            else:
                return "red_text"

    def plot(self):
        # Create figure for plotting
        self._figure.clear()
        ax = self._figure.add_subplot(1, 1, 1)

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
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        # Set up plot to call animate() function periodically
        ani = animation.FuncAnimation(self._figure, animate, fargs=(self._x_date, self._y_wellness, self._y_pollution),
                                      interval=3000, cache_frame_data=False)

        self._canvas.draw()

    def setController(self, controller):
        self._controller = controller
