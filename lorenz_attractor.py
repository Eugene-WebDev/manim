from manim import *
from manim import ThreeDScene, ThreeDAxes, MathTex, VMobject, VGroup, Dot, TracedPath, Scene, Create, ORIGIN, DEGREES, BLUE, PI, GREEN, YELLOW, ORANGE, PURPLE, BLUE_E, BLUE_A, DOWN, UL, Write, linear, color_gradient, RED
from scipy.integrate import solve_ivp
import numpy as np

# Define the Lorenz system of differential equations
def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):
    x, y, z = state  # Unpack the state vector into x, y, z
    dxdt = sigma * (y - x)  # Compute the derivative of x
    dydt = x * (rho - z) - y  # Compute the derivative of y
    dzdt = x * y - beta * z  # Compute the derivative of z
    return [dxdt, dydt, dzdt]  # Return the derivatives as a list

# Function to compute solution points for an ODE
def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
        function,  # The ODE function to solve
        t_span=(0, time),  # Time span for the solution
        y0=state0,  # Initial state
        t_eval=np.arange(0, time, dt)  # Time points at which to store the solution
    )
    return solution.y.T  # Return the transposed solution array

# Define a class for visualizing the Lorenz attractor
class LorenzAttractor(ThreeDScene):
    def construct(self):
        # Set up 3D axes with specified ranges and color
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),  # X-axis range from -50 to 50 with tick marks every 5 units
            y_range=(-50, 50, 5),  # Y-axis range from -50 to 50 with tick marks every 5 units
            z_range=(0, 50, 5),    # Z-axis range from 0 to 50 with tick marks every 5 units
            axis_config={"color": GREY},  # Set the color of the axes to blue
        )

        # Move the axes to the origin of the scene
        axes.move_to(ORIGIN)

        # Set the initial camera orientation with specific angles
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)

        # Add the axes to the scene
        self.add(axes)

        # Define the equations
        """equations = MathTex(
            r"\sigma", r"\rho", r"\beta",
            tex_to_color_map={r"\sigma": YELLOW, r"\rho": ORANGE, r"\beta": PURPLE},
            font_size=40
        )"""
        eq1 = MathTex(r"\frac{dx}{dt} = \sigma \left( y - x \right)", font_size=15)
        eq2 = MathTex(r"\frac{dy}{dt} = x \left( \rho - z \right) - y", font_size=15)
        eq3 = MathTex(r"\frac{dz}{dt} = xy - \beta z", font_size=15)

        equations = VGroup(eq1, eq2, eq3)


        equations.arrange(DOWN)
        equations.to_corner(UL)
        equations.set_stroke(width=1)
        # Add the equation as a fixed object in the frame
        self.add_fixed_in_frame_mobjects(equations)

        # Define parameters for the Lorenz system solutions
        epsilon = 1e-5  # Small perturbation for initial conditions
        evolution_time = 30  # Total time for the system evolution
        n_points = 10  # Number of initial states to simulate
        states = [
            [10, 10, 10 + n * epsilon]  # Initial states with slight variations in z
            for n in range(n_points)
        ]
        colors = color_gradient([BLUE_E, BLUE_A], len(states))  # Generate a gradient of colors

        # Create curves for the Lorenz attractor
        curves = VGroup()
        for state, color in zip(states, colors * 10):  # Repeat colors to match the number of states
            points = ode_solution_points(lorenz_system, state, evolution_time)  # Compute solution points
            # Ensure points are in the correct shape
            if points.shape[1] != 3:
                raise ValueError("Points should have three columns for x, y, z coordinates.")
            # Create a smooth curve from the solution points
            curve = VMobject().set_points_smoothly([axes.c2p(x, y, z) for x, y, z in points])
            curve.set_stroke(color, 1, opacity=0.5)  # Set the stroke color and opacity of the curve
            curves.add(curve)  # Add the curve to the group

        # Ensure curves is not empty and contains valid VMobjects
        if curves:
            valid_curves = [curve for curve in curves if isinstance(curve, VMobject)]
            if not valid_curves:
                raise ValueError("No valid VMobjects found in curves.")
            
            # Move the camera before playing animations
            self.move_camera(theta=PI/2, run_time=10)  # Camera movement

            self.play(
                *(
                    Create(curve, rate_func=linear)  # Use a smooth rate function for smoother animation
                    for curve in valid_curves
                ),
                Write(equations),  # Animate the writing of the equation
                run_time=evolution_time/2
            )
        else:
            raise ValueError("Curves is empty or contains invalid elements.")

        # Create dots to move along the trajectories of the curves
        dots = VGroup(
            *[Dot(color=color, radius=0.1).set_opacity(0.8) for color in colors * 10]
        )

        # Define an updater function to move dots along the curves
        def update_dots(dots, curves=curves):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())  # Move each dot to the end of its corresponding curve

        dots.add_updater(update_dots)  # Add the updater to the dots

        # Create traced paths for the dots to leave trails
        tails = VGroup(
            *[
                TracedPath(dot.get_center, stroke_color=dot.get_color(), stroke_width=1)
                for dot in dots
            ]
        )

        self.add(dots)  # Add the dots to the scene
        self.add(tails)  # Add the tails to the scene
        curves.set_opacity(0)  # Make the curves invisible
        self.move_camera(theta=PI/4, run_time=10)  # Camera movement


        # Fade out all tails except the last one
        for tail in tails[:-1]:
            tail.add_updater(lambda m: m.set_opacity(0.5))  # Adjust opacity dynamically

        # Ensure the last tail remains fully visible
        tails[-1].set_opacity(1)

        self.wait(2)  # Add a wait time to ensure the scene is fully rendered

        # Optionally, you can add a final wait to keep the scene visible
        self.wait(2)  # Additional wait time to keep the scene visible at the end

# Define an empty scene class for the end screen
class EndScreen(Scene):
    pass

if __name__ == "__main__":
    import os
    import platform
    import subprocess

    # Render the scene
    os.system("manim -pqh lorenz_attractor.py LorenzAttractor")

    # Automatically open the rendered video file
    video_path = "media/videos/lorenz_attractor/480p15/LorenzAttractor.mp4"
    if platform.system() == "Windows":
        os.startfile(video_path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", video_path])
    else:  # Linux
        subprocess.call(["xdg-open", video_path])
