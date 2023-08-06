import bqplot as bq
from ipywidgets import widgets
import numpy as np
from time import sleep
from BNumMet import Random


class RandomVisualizer:
    def __init__(self, randGenerator=Random.genrand):
        """
        Initializes the RandomVisualizer class.

        Parameters
        ----------
        randGenerator : RandomGenerator
            The random generator to use. It is a function that does not take any parameters and returns a random number between 0 and 1.
        """
        self.randGenerator = randGenerator
        self.generatedNumbers = []
        self.currentValue = 0
        self.iterations = 100
        self.currentIteration = 0
        self.inside_circle = 0

    def initialize_components(self):
        """
        Initializes the components of the visualizer.
        """
        # Figure 1: Circle inside a square of side 1 centered at the origin
        # =================================================================================================
        self.figure1 = bq.Figure(title="Montecarlo's method")

        self.x_sc = bq.LinearScale()  # x scale
        self.y_sc = bq.LinearScale()  # y scale
        ax_x = bq.Axis(scale=self.x_sc, grid_lines="solid", label="X")
        ax_y = bq.Axis(
            scale=self.y_sc,
            orientation="vertical",
            grid_lines="solid",
            label="Y",
        )
        # Set up the plot figure
        self.figure1 = bq.Figure(
            marks=[],  # marks
            axes=[ax_x, ax_y],  # axes
            title="Montecarlo's Method",  # title
        )

        # Draw the square
        self.square = bq.Lines(
            x=[0, 1, 1, 0, 0],
            y=[0, 0, 1, 1, 0],
            scales={"x": self.x_sc, "y": self.y_sc},
            colors=["black"],
        )
        self.figure1.marks = [self.square]
        # Draw the full circle centered at (0.5, 0.5) with radius 0.5
        x = np.linspace(0, 1, 1000)
        y = np.sqrt(1 / 4 - (x - 0.5) ** 2)
        y = np.concatenate((y, -y))  # y
        y += 0.5
        x = np.concatenate((x, (x[::-1])))  # x

        self.circle = bq.Lines(
            x=x, y=y, scales={"x": self.x_sc, "y": self.y_sc}, colors=["red"]
        )
        self.figure1.marks = [self.square, self.circle]

        # Prepare the figure for the points
        self.points = bq.Scatter(
            x=[],
            y=[],
            scales={"x": self.x_sc, "y": self.y_sc},
            colors=["blue"],
            default_size=5,
        )
        self.figure1.marks = [self.square, self.circle, self.points]

        # Figure 2: (Current value and Pi) vs. (Number of iterations)
        # =================================================================================================
        self.figure2 = bq.Figure(title="Convergence of Pi", legend_location="top-right")
        self.x_sc2 = bq.LinearScale()  # x scale
        self.y_sc2 = bq.LinearScale()  # y scale
        ax_x2 = bq.Axis(
            scale=self.x_sc2, grid_lines="solid", label="Number of iterations"
        )
        ax_y2 = bq.Axis(
            scale=self.y_sc2,
            orientation="vertical",
            grid_lines="solid",
            label="Value",
        )

        self.x_sc2.min = 0
        self.x_sc2.max = self.iterations  # Number of iterations **

        # Set up the plot figure
        self.figure2 = bq.Figure(
            marks=[],  # marks
            axes=[ax_x2, ax_y2],  # axes
            title="Convergence of Pi",  # title
        )  # this will change as the algorithm runs

        # Draw the line of Pi
        x = np.linspace(0, self.iterations, 1000)
        y = np.full(1000, np.pi)
        self.piLine = bq.Lines(
            x=x,
            y=y,
            scales={"x": self.x_sc2, "y": self.y_sc2},
            colors=["red"],
            labels=["Pi"],
            display_legend=True,
        )
        self.figure2.marks = [self.piLine]

        # Prepare the figure for the current value update
        self.currentValueLine = bq.Lines(
            x=[],
            y=[],
            scales={"x": self.x_sc2, "y": self.y_sc2},
            colors=["blue"],
            labels=["Current Value"],
            display_legend=True,
        )
        self.figure2.marks = [self.piLine, self.currentValueLine]

        # Widget: Number of Points to generate
        # =================================================================================================
        self.iterationsWidget = widgets.BoundedIntText(
            value=self.iterations,
            min=1,
            max=1000,
            description="Iterations:",
            disabled=False,
        )

        # Widget: Button for running the algorithm
        # =================================================================================================
        self.runButton = widgets.Button(
            description="Run",
            disabled=False,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            tooltip="Run",
            icon="check",  # (FontAwesome names without the `fa-` prefix)
        )
        # Observer: Button for running the algorithm
        self.runButton.on_click(self.play_montecarlo)

        # Widget: Grid
        # =================================================================================================
        self.grid = widgets.GridspecLayout(4, 4)
        self.grid[0:2, 0:2] = self.figure1
        self.grid[2:4, 0:4] = self.figure2
        self.grid[0:1, 2:4] = self.iterationsWidget
        self.grid[1:2, 2:4] = self.runButton

    def number_of_iterations(self):
        """
        Updates the number of iterations. This is called when the user plays the animation. It configures the x axis of the second figure. and the number of iterations of the algorithm.
        """
        self.iterations = self.iterationsWidget.value
        self.x_sc2.max = self.iterations
        self.piLine.x = np.linspace(0, self.iterations, 1000)

    def play_montecarlo(self, b):
        """
        Plays the montecarlo algorithm.
        """
        self.number_of_iterations()
        self.currentIteration = 0
        self.generatedNumbers = []
        self.currentValue = 0
        self.inside_circle = 0
        self.points.x = []
        self.points.y = []
        self.currentValueLine.x = []
        self.currentValueLine.y = []

        self.runButton.disabled = True

        for self.currentIteration in range(self.iterations):
            newX = self.randGenerator()
            newY = self.randGenerator()
            self.generatedNumbers.append([newX, newY])
            with self.points.hold_sync():  # Animation for the points
                self.points.x = [x[0] for x in self.generatedNumbers]
                self.points.y = [x[1] for x in self.generatedNumbers]
            if ((newX - 0.5) ** 2 + (newY - 0.5) ** 2) <= 0.25:
                self.inside_circle += 1
            # sleep(0.0001)
            self.currentValue = 4 * self.inside_circle / len(self.generatedNumbers)

            with self.currentValueLine.hold_sync():  # Animation for the current value
                self.currentValueLine.x = [x for x in self.currentValueLine.x] + [
                    self.currentIteration
                ]
                self.currentValueLine.y = [y for y in self.currentValueLine.y] + [
                    self.currentValue
                ]

        self.runButton.disabled = False

    def run(self):
        """
        Runs the visualizer.
        """
        self.initialize_components()
        return self.grid
