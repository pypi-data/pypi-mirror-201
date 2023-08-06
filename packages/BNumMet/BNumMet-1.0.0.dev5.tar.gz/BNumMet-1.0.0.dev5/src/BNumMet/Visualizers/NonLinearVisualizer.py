import bqplot as bq
import numpy as np
from ipywidgets import widgets
from BNumMet.NonLinear import zBrentDekker


class NonLinearVisualizer:
    def __init__(
        self, fun=lambda x: (x - 1) * (x - 4) * np.exp(-x), interval=(0, 3), tol=1e-3
    ):
        # Initialize basic Parameters
        self.brentDekker = zBrentDekker(
            fun, interval, tol, iters=True, steps=True
        )  # Get the output of Brent Dekkers Alg --> (x, iters)

        # Set the input function, the interval for the function evaluation,
        # and the tolerance for the algorithm
        self.f = fun
        self.a, self.b = interval
        self.fa, self.fb = self.f(self.a), self.f(self.b)

        # Check that the function has a zero in the interval
        if self.f(self.a) * self.f(self.b) > 0:
            raise ValueError("The function has no zeros in the given interval")

        # Set the tolerance and initial values for data variables
        self.t = tol
        self.original_data = (self.a, self.b)
        self.iterations = 0

        # First Step of the Algorithm
        # ==========================================================================
        ## Section: INT
        # Set the initial values for internal variables
        self.c, self.fc, self.e = self.a, self.fa, self.b - self.a
        ## Section: EXT
        # Call the sectionEXT() function to perform the first external section of the algorithm
        self.sectionEXT()

        # Current Step Save Values
        # ==========================================================================
        # Save the current state of the algorithm in a tuple
        self.currentStep = (self.a, self.b, self.c, self.e)

        # Revert Stack
        # ==========================================================================
        # Create an empty stack to keep track of previous states of the algorithm
        self.revertStack = []

        # Draw mesh
        # ==========================================================================
        # Create a numpy array of 1000 evenly spaced values between the minimum and maximum
        # values of the function interval to use for plotting the function
        self.x = np.linspace(min(self.a, self.b), max(self.a, self.b), 1000)
        self.widen = False

    def checkBoxChanged(self, change):
        with self.Fig.hold_sync():  # Hold the figure syncronized
            self.draw_figures()  # Draw the figures

    def sectionINT(self):
        # Check if the function evaluates with the same sign on both sides of c
        if np.sign(self.fb) == np.sign(self.fc) != 0:
            # If the condition is met, update the values of c, fc and e
            self.c, self.fc, self.e = self.a, self.fa, self.b - self.a

    def sectionEXT(self):
        # Check which of the endpoints has the smaller absolute value of f
        if abs(self.fc) < abs(self.fb):
            # If the condition is met, swap the values of a, b and c with b, c and b respectively,
            # and update the values of fa, fb and fc accordingly
            self.a, self.b, self.c, self.fa, self.fb, self.fc = (
                self.b,
                self.c,
                self.b,
                self.fb,
                self.fc,
                self.fb,
            )

    def initializeComponents(self):
        # Current Solution Text
        # ==========================================================================
        # Widget for displaying current solution output
        # Current Solution: (b, f(b))
        # Iterations: N
        self.currentSolOut = widgets.Output()

        # Helper Text
        # ==========================================================================
        # Widget for displaying helper output
        # Suggestion for next step: <Bisect/IQI/Secant>
        self.helperOut = widgets.Output()  # Next Possible Step: <Bisect/IQI/None>

        # Brent-Dekker Solution
        # ==========================================================================
        # Widget for displaying Brent-Dekker solution output
        # Brent-Dekker Solution: (x^, f(x^)) in N^ iterations
        self.brentDekkerOut = widgets.HTML(
            value=f"<blockquote> Brent-Dekker Solution: <b>({self.brentDekker[0]:.4e}, {self.f(self.brentDekker[0]):.4e})</b> in <b>{self.brentDekker[1]}</b> iterations"
        )

        # Reset Button
        # ==========================================================================
        # Widget for reset button
        self.resetButton = widgets.Button(
            description="Reset",
            disabled=False,
            button_style="danger",
            tooltip="Reset",
            icon="undo",
        )
        self.resetButton.on_click(self.reset)

        # Revert Button
        # ==========================================================================
        # Widget for revert button
        self.revertButton = widgets.Button(
            description="Revert",
            disable=False,
            button_style="warning",
            tooltip="Revert",
            icon="arrow-left",
        )
        self.revertButton.on_click(self.revert)

        # FIGURE
        # ==========================================================================
        # Widget for plotting the function and its zeros
        # Set up axes and scales for the plot
        self.x_sc = bq.LinearScale()
        self.y_sc = bq.LinearScale()
        ax_x = bq.Axis(scale=self.x_sc, grid_lines="solid", label="X")
        ax_y = bq.Axis(
            scale=self.y_sc,
            orientation="vertical",
            tick_format="0.4e",
            grid_lines="solid",
            label="Y",
        )
        # Set up the plot figure
        self.Fig = bq.Figure(
            marks=[],
            axes=[ax_x, ax_y],
            title="Zeros of a Function",
        )
        # Set up the plot figure toolbar
        self.Toolbar = bq.Toolbar(figure=self.Fig)
        # Add default lines to the plot figure
        self.defaultLines()

        # FUNCTION BUTTONS
        # ==========================================================================
        # Widgets for buttons for selecting the next function to perform
        # Each button has a pointIndex attribute that is used to identify the point in the points array
        # 0: Bisect  1: Secant  2: IQI
        # Bisect Button
        self.bisectButton = widgets.Button(
            description="Bisect",
            disabled=False,
            tooltip="Bisect",
        )
        self.bisectButton.pointIndex = 0
        self.bisectButton.on_click(self.next_step)

        # Secant Button
        self.secantButton = widgets.Button(
            description="Secant",
            disabled=False,
            tooltip="Secant",
        )
        self.secantButton.pointIndex = 1
        self.secantButton.on_click(self.next_step)

        # IQI Button
        self.IQIButton = widgets.Button(
            description="IQI",
            disabled=False,
            tooltip="IQI",
        )
        self.IQIButton.pointIndex = 2
        self.IQIButton.on_click(self.next_step)

        # CHECKBOXES FOR FUNCTION BUTTONS
        # ==========================================================================
        self.bisectCheckbox = widgets.Checkbox(
            value=False,
            description="Bisect",
            disabled=False,
            indent=False,
        )
        # On change of checkbox, function checkBoxChanged
        self.bisectCheckbox.observe(self.checkBoxChanged, names="value")

        self.secantCheckbox = widgets.Checkbox(
            value=False,
            description="Secant",
            disabled=False,
            indent=False,
        )
        self.secantCheckbox.observe(self.checkBoxChanged, names="value")

        self.IQICheckbox = widgets.Checkbox(
            value=False,
            description="IQI",
            disabled=False,
            indent=False,
        )
        self.IQICheckbox.observe(self.checkBoxChanged, names="value")

        # GRID
        # ==========================================================================
        self.grid = widgets.GridspecLayout(2, 2)
        self.grid[0, 0] = widgets.VBox([self.Toolbar, self.Fig])

        # Text Outputs Group
        textGroup = widgets.VBox(
            [self.currentSolOut, self.helperOut, self.brentDekkerOut]
        )
        self.grid[1, 0] = textGroup

        # Buttons Group
        text1 = widgets.HTML(value="<b>Next Step Selector</b>")  # Next Step Selector
        text2 = widgets.HTML(value="<b>Draw Step?</b>")  # Draw Step?
        selectors = widgets.VBox(  # Next Step Selectors
            [text1, self.bisectButton, self.secantButton, self.IQIButton]
        )
        checkboxes = widgets.VBox(
            [text2, self.bisectCheckbox, self.secantCheckbox, self.IQICheckbox]
        )
        buttonsGroup = widgets.HBox([selectors, checkboxes])

        self.grid[0, 1] = buttonsGroup

        # Reset and Revert Buttons Group
        buttonsGroup2 = widgets.HBox(
            [
                self.revertButton,
                self.resetButton,
            ]
        )
        self.grid[1, 1] = buttonsGroup2

    def defaultLines(self):
        # 0. Horizontal Line f(x)=0
        self.hLine = bq.Lines(  # Horizontal Line f(x)=0
            x=self.x,
            y=[0] * len(self.x),
            scales={"x": self.x_sc, "y": self.y_sc},
            enable_move=False,
            enable_add=False,
            colors=["Black"],
        )
        # 1. Function Line f(x)
        self.functionLine = bq.Lines(  # Function Line f(x)
            x=self.x,
            y=list(map(self.f, self.x)),
            scales={"x": self.x_sc, "y": self.y_sc},
            labels=["f(x)"],
            display_legend=False,
            enable_move=False,
            enable_add=False,
            colors=["Gray"],
            line_style="dashed",
        )

    def next_step(self, b):
        """
        This function is called when a button is clicked

        Parameters
        ----------
        b : Button
            The button that was clicked

        Returns
        -------
        None.
        """

        if self.hintStep is None:
            return
        self.revertStack.append(
            [self.a, self.b, self.c, self.e, self.iterations]
        )  # Add the current state to the revert stack

        self.a = self.b  # Set a = b
        self.fa = self.fb  # Set f(a) = f(b)

        newB = self.nextPoints_addition[b.pointIndex]  # Get the next point
        self.b = (
            newB
            if abs(self.b - newB) > self.tolerance
            else self.b + np.sign(0.5 * (self.c - self.b)) * self.tolerance
        )  # If the new point is too close to the current point, move it a little bit
        self.fb = self.f(self.b)  # Set f(b) = f(newB)
        self.e = self.errs[b.pointIndex]  # Set e = error

        self.iterations += 1  # Increment the number of iterations

        # Section: Ext
        self.sectionEXT()  # Update the section
        # Section: Int
        self.sectionINT()  # Update the section

        self.one_step()  # Update the plot

    def reset(self, b):
        """
        Reset everything to the initial state, this can be understood as reverting all the steps
        """
        if len(self.revertStack) == 0:
            return

        self.a, self.b, self.c, self.e, self.iterations = self.revertStack[
            0
        ]  # Get the initial state
        self.fb = self.f(self.b)  # Set f(b) = f(newB)
        self.fa = self.f(self.a)  # Set f(a) = f(b)
        self.fc = self.f(self.c)  # Set f(c) = f(newC)

        self.revertStack = []  # Clear the revert stack
        self.one_step()  # Update the plot

    def revert(self, b):
        """
        This method reverts the last step
        """
        if len(self.revertStack) == 0:  # If there is no step to revert
            return

        (
            self.a,
            self.b,
            self.c,
            self.e,
            self.iterations,
        ) = self.revertStack.pop()  # Get the last state
        self.fb = self.f(self.b)  # Set f(b) = f(newB)
        self.fa = self.f(self.a)  # Set f(a) = f(b)
        self.fc = self.f(self.c)  # Set f(c) = f(newC)

        self.one_step()  # Update the plot

    def one_step(self):
        """
        This method is called when a step is made
        """
        with self.grid.hold_sync():  # Hold the grid syncronized
            self.brent_dekker_Step()  # Update the Brent-Dekker step
            self.IQIButton.disabled = (
                self.nextPoints_addition[2] is None
            )  # Disable the IQI button if the IQI point is None
            self.IQICheckbox.disabled = (
                self.nextPoints_addition[2] is None
            )  # Disable the IQI checkbox if the IQI point is None

            self.update_ouputs()  # Update the outputs
            with self.Fig.hold_sync():  # Hold the figure syncronized
                self.draw_figures()  # Draw the figures
            # self.drawFigures()

    def draw_figures(self):
        """
        This method draws the figures
        1. The function
        2. Dot for the current solution
        3. The next step suggestions
        4. if checkboxes are checked, the steps are drawn
        """

        def draw_point(point, value, color, label, marker, legend=True):
            return bq.Scatter(
                x=[point],
                y=[value],
                scales={"x": self.x_sc, "y": self.y_sc},
                colors=[color],
                default_size=100,
                stroke="black",
                display_legend=legend,
                labels=[label],
                marker=marker,
            )  # Draw a point

        def secant_draw():
            # Draws a line on whole self.x range with the secant equation on the points (b, fb) and (self.nextPoints_addition[1], self.f(self.nextPoints_addition[1]))
            secant = bq.Lines(
                x=self.x,
                y=[
                    self.fb + (self.fa - self.fb) / (self.a - self.b) * (x - self.b)
                    for x in self.x
                ],
                scales={"x": self.x_sc, "y": self.y_sc},
                colors=["red"],
                display_legend=True,
                labels=["Secant Line"],
                line_style="dashed",
            )  # Draw a line
            return secant

        def bisect_draw(m, minY, maxY):
            # m = (a + b) / 2
            # draw a vertical line at m
            bisect = bq.Lines(
                x=[m, m],
                y=[minY, maxY],
                scales={"x": self.x_sc, "y": self.y_sc},
                colors=["green"],
                display_legend=True,
                labels=["Bisect Line"],
                line_style="dashed",
            )  # Draw a line
            return bisect

        def iqi_draw(a, b, c, minY, maxY):
            # draw a vertical line at m
            interpolY = [self.f(a), self.f(b), self.f(c)]  # [f(a), f(b), f(c)]
            interpolX = [a, b, c]  # [a, b, c]
            yMesh = np.linspace(minY, maxY, 1000)
            # Lagrange interpolation with (Y,X)
            q_y = (  # Lagrange interpolation
                lambda y: ((y - interpolY[1]) * (y - interpolY[2]))
                / ((interpolY[0] - interpolY[1]) * (interpolY[0] - interpolY[2]))
                * interpolX[0]
                + ((y - interpolY[0]) * (y - interpolY[2]))
                / ((interpolY[1] - interpolY[0]) * (interpolY[1] - interpolY[2]))
                * interpolX[1]
                + ((y - interpolY[0]) * (y - interpolY[1]))
                / ((interpolY[2] - interpolY[0]) * (interpolY[2] - interpolY[1]))
                * interpolX[2]
            )
            xMesh = q_y(yMesh)  # Get the x values for the y values
            xMesh = np.where(
                (xMesh < self.x[0]) | (xMesh > self.x[-1]), np.nan, xMesh
            )  # Set the x values outside the range to nan
            IQILine = bq.Lines(  # Draw a line
                x=xMesh,
                y=yMesh,
                scales={"x": self.x_sc, "y": self.y_sc},
                colors=["blue"],
                display_legend=True,
                labels=["IQI Line"],
                line_style="dashed",
            )
            return IQILine

        points2check = [  # Points to check
            self.a,
            self.b,
            self.c,
            self.nextPoints_addition[0],
            self.nextPoints_addition[1],
        ] + (
            []
            if self.nextPoints_addition[2] is None
            else [
                self.nextPoints_addition[2]
            ]  # If the IQI point is None, add it to the list
        )

        if self.hintStep is None:  # If the hint step is None
            self.Fig.marks = [
                self.hLine,
                self.functionLine,
            ]  # Set the marks to the function and the horizontal line
            return

        minMax = [
            min(points2check),
            max(points2check),
        ]  # Get the min and max of the points to check

        if minMax[0] < min(self.original_data) or minMax[1] > max(
            self.original_data
        ):  # If the min or max of the points to check is outside the range of the original data
            self.x = np.linspace(  # Set the x values to the min and max of the points to check
                min(min(self.original_data), minMax[0]),
                max(max(self.original_data), minMax[1]),
                1000,
            )
            self.defaultLines()  # Set the default lines
            self.widen = True  # Set widen to True
        elif self.widen:  # If widen is True
            self.x = np.linspace(
                min(self.original_data), max(self.original_data), 1000
            )  # Set the x values to the min and max of the original data
            self.defaultLines()  # Set the default lines
            self.widen = False  # Set widen to False

        marks2plot = [
            self.hLine,
            self.functionLine,
        ]  # Set the marks to the function and the horizontal line

        # 1. The Current Points (a,b,c)
        marks2plot.append(
            draw_point(
                self.a, self.fa, "red", "a", "circle", legend=False
            )  # Draw a point
        )
        marks2plot.append(
            draw_point(
                self.b,
                self.fb,
                "Black",
                "Current Solution",
                "cross",
                legend=True,  # Draw a point
            )
        )
        marks2plot.append(
            draw_point(
                self.c, self.fc, "green", "c", "circle", legend=False
            )  # Draw a point
        )

        # 2. The next step suggestions
        marks2plot.append(  # Bisect
            draw_point(
                self.nextPoints_addition[0],
                0,
                "green",
                "Bisection",
                "rectangle",
            )
        )
        marks2plot.append(
            draw_point(  # Secant
                self.nextPoints_addition[1],
                0,
                "red",
                "Secant",
                "triangle-up",
            )
        )
        if self.nextPoints_addition[2] is not None:
            marks2plot.append(
                draw_point(  # IQI
                    self.nextPoints_addition[2],
                    0,
                    "blue",
                    "IQI",
                    "triangle-down",
                )
            )

        # FIX THE VIEW
        self.x_sc.min = minMax[
            0
        ]  # Set the x scale min to the min of the points to check
        self.x_sc.max = minMax[
            1
        ]  # Set the x scale max to the max of the points to check

        self.y_sc.min = min(
            self.f(minMax[0]), self.f(minMax[1])
        )  # Set the y scale min to the min of the function of the min and max of the points to check
        self.y_sc.max = max(
            self.f(minMax[0]), self.f(minMax[1])
        )  # Set the y scale max to the max of the function of the min and max of the points to check

        fX = list(map(self.f, self.x))  # Get the function values for the x values
        yminMax = (min(fX), max(fX))  # Get the min and max of the function values

        # 3. The steps
        if self.secantCheckbox.value:  # If the secant checkbox is checked
            marks2plot.append(secant_draw())  # Draw the secant line

        if self.bisectCheckbox.value:  # If the bisect checkbox is checked
            marks2plot.append(  # Draw the bisect line
                bisect_draw(
                    self.nextPoints_addition[0], yminMax[0], yminMax[1]
                )  # Draw the bisect line
            )
        if (
            self.IQICheckbox.value and self.nextPoints_addition[2] is not None
        ):  # If the IQI checkbox is checked and the IQI point is not None
            marks2plot.append(
                iqi_draw(self.a, self.b, self.c, yminMax[0], yminMax[1])
            )  # Draw the IQI line

        self.Fig.marks = marks2plot  # Set the marks to the marks to plot

    def update_ouputs(self):
        """
        This method updates the outputs of the app
            > current solution
            > helper text
        The next step must be calculated before calling this method
        """
        self.currentSolOut.clear_output()  # Clear the current solution output
        self.helperOut.clear_output()  # Clear the helper output

        with self.currentSolOut:  # Print the current solution
            print(
                f"Current Solution: ({self.b:.4e}, {self.f(self.b):.4e})"
            )  # Print the current solution
            print(f"Iterations: {self.iterations}")  # Print the iterations
        with self.helperOut:  # Print the helper text
            print(  # Print the helper text
                f"Next Step suggestion: {self.hintStep if self.hintStep is not None else 'FINISHED'}"
            )

    def run(self):
        """
        This method sets up everything and runs the app

        Returns
        -------
        Widgets.GridBox
            The GridBox containing all the widgets
        """
        self.initializeComponents()  # Initialize the components
        self.one_step()  # Run one step

        return self.grid

    def brent_dekker_Step(self):
        """
        This method imitates the Brent-Dekker in one step, instead of giving the result point, this method returns the 3 available points for the next step as well as the next possible step

        Returns
        -------
        - next_step: str
            The next possible step
        - nextPoints_addition: list
            The 3 available quantity to add to b for the next step (midpoint, secant, IQI)
        - errs: list
            The errors of the 3 available points for the next step
        """
        self.tolerance = 2 * np.finfo(float).eps * abs(self.b) + self.t
        ## Midpoint error
        m = 0.5 * (self.c - self.b)

        if abs(m) <= self.tolerance or self.f(self.b) == 0 or self.f(self.a) == 0:
            self.hintStep = None
            self.nextPoints_addition = [None, None, None]
            self.errs = [None, None, None]
            self.update_ouputs()
            return

        next_step = None
        nextPoints_addition = [None, None, None]
        errs = [None, None, None]

        nextPoints_addition[0] = self.b + m  # Always exists
        errs[0] = m  # Always exists

        # See if Bisection is possible
        # CHECK abs(self.e) < self.tolerance or abs(self.fa) <= abs(self.fb) in the original code
        # Here we do nothing because it is the midpoint - only thing next_step is Bisection (which will be default if secant/iqi fails)

        s = self.fb / self.fa
        pqPair = None
        if self.a == self.c:
            # Linear Interpolation (Secant)
            p1 = 2 * m * s
            q1 = 1 - s

        else:
            # Linear Interpolation (Secant)
            p1 = self.fb * (self.b - self.a)
            q1 = self.fb - self.fa

            # Inverse Quadratic Interpolation (IQI)
            q = self.fa / self.fc
            r = self.fb / self.fc
            p2 = s * (2 * m * q * (q - r) - (self.b - self.a) * (r - 1))
            q2 = (q - 1) * (r - 1) * (s - 1)

            # Correct signs of IQI
            if p2 > 0:
                q2 = -q2
            else:
                p2 = -p2

            pqPair = (p2, q2)

        if p1 > 0:
            q1 = -q1
        else:
            p1 = -p1

        # Store e-Values for next step
        errs[1] = abs(p1 / q1)  # Secant always exists
        errs[2] = (
            None if pqPair is None else abs(pqPair[0] / pqPair[1])
        )  # IQI may not exist if a==c if it does, it is stored in pqPair

        # Store next points (Quantity to add) for next step
        nextPoints_addition[1] = self.b + p1 / q1  # Secant always exists
        nextPoints_addition[2] = (
            None if pqPair is None else self.b + pqPair[0] / pqPair[1]
        )  # IQI may not exist if a==c if it does, it is stored in pqPair
        pqPair = (
            (p1, q1) if pqPair is None else pqPair
        )  # If IQI does not exist, use Secant instead (pqPair is None if IQI does not exist), otherwise use IQI (pqPair is not None if IQI exists)

        # Choose the best interpolation
        if 2 * pqPair[0] < 3 * m * pqPair[1] - abs(
            self.tolerance * pqPair[1]
        ) and pqPair[0] < abs(0.5 * self.e * pqPair[1]):
            next_step = "IQI" if self.a != self.c else "Secant"
        else:
            next_step = "Bisection"

        self.hintStep = next_step
        self.nextPoints_addition = nextPoints_addition
        self.errs = errs

        return next_step, nextPoints_addition, errs
