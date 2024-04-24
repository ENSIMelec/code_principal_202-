import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Asserv import Asserv  # assuming the class is imported from another file
import numpy as np
import sys

# Parse the command-line argument
try:
    graph_config = int(sys.argv[1])  # Expecting an integer argument
except (IndexError, ValueError):
    print("Please provide a valid integer argument for the graph configuration.")
    sys.exit(1)

# Initialize the Asserv class
asserv = Asserv()

# Define plot configurations
plots_config = {
    0: {"label": ("Angle Mesuré","Angle PID","Commande Angle"), "getters": ("get_angle", "get_output_pid_angle","get_cmd_angle"), "ylabel": "Angle"},
    1: {"label": ("Distance Mesuré","Distance PID","Commande Distance"), "getters":("get_distance", "get_output_pid_distance", "get_cmd_distance"), "ylabel": "Distance"},
    2: {"label": "Motor Data", "getters": ("get_vitesse_g", "get_output_pid_vitesse_g", "get_cmd_vitesse_g", "get_vitesse_d", "get_output_pid_vitesse_d", "get_cmd_vitesse_d"), "ylabel": "Commanded Speed Right/Left"}
}

# Check if the configuration is valid
if graph_config not in plots_config:
    print("Invalid configuration. Please choose a valid option (0-2).")
    sys.exit(1)

# Setup matplotlib figure and axes
fig, ax = plt.subplots()
config = plots_config[graph_config]
fig.suptitle(config["ylabel"])

# Initialize line objects for the selected graph
line1, = ax.plot([], [], 'r-', label=f"{config['label'][0]}")
line2, = ax.plot([], [], 'b-', label=f"{config['label'][1]}")
line3, = ax.plot([], [], 'g-', label=f"{config['label'][2]}")
ax.set_xlabel("Time (s)")
ax.set_ylabel(config["ylabel"])
ax.legend()

# Data cache for x-axis and y-axis values
xdata, ydata1, ydata2, ydata3 = [], [], [], []

def init():
    ax.set_xlim(0, 100)
    ax.set_ylim(-1000, 1000)  # Adjust this range based on expected data range
    return line1, line2, line3

def update(frame):
    xdata.append(frame)
    ydata1.append(getattr(asserv, config["getters"][0])())
    ydata2.append(getattr(asserv, config["getters"][1])())
    ydata3.append(getattr(asserv, config["getters"][2])())
    
    line1.set_data(xdata, ydata1)
    line2.set_data(xdata, ydata2)
    line3.set_data(xdata, ydata3)

    # Scroll graph if necessary
    if len(xdata) > 100:
        ax.set_xlim(xdata[-100], xdata[-1])

    return line1, line2, line3

ani = FuncAnimation(fig, update, frames=np.arange(0, 2000), init_func=init, blit=True)

plt.show()
