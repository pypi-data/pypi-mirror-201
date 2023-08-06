"""
Contains functions to make 2D or 3D plots for loss landscapes.

Functions
---------
plot_loss_2D
    Wrapper for making the contour plots.
make_contour_plot
    Creates a 2D-plot of the loss landscape.
"""
#                                                                       Modules
# =============================================================================
# Standard
import pickle as pik

# Third-party
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable


plt.ioff()


def plot_loss_2D(path_to_file: str, ax : plt.Axes,
                 is_log: bool = False) -> plt.Axes:
    """Wrapper for making the contour plots.
    Opens the .npz file created by the visualize function
    and creates a 2D contour plot.
    fig, ax = plt.subplots(*args) can be used to create the ax
    object.

    Parameters
    ----------
    path_to_file
        Path to the .npz file created using the visualization module.
    ax
        A matplotlib Axes object on which the plot will be made.
    is_log
        Plot the logarithmic loss landscape and trajectory.

    Returns
    -------
    ax
        Axes object with the plot.
    """

    outs = np.load(path_to_file, allow_pickle=True)
    flag = outs["b"]
    outs = outs["a"]

    if flag == 1:
        ax = make_contour_plot(ax, outs[0][0], outs[0][1], outs[0][2],
                               path_x=outs[1][0], path_y=outs[1][1],
                               is_log=is_log)
    # PCA based plots
    elif flag == 2:
        ax = make_contour_plot(ax, outs[0][0], outs[0][1], outs[0][2],
                               path_x=outs[1][0], path_y=outs[1][1],
                               labels=outs[2][0], is_log=is_log)
    #  Random filter-normalized plotting - No trajectories
    elif flag == 3:
        ax = make_contour_plot(ax, outs[0][0], outs[0][1], outs[0][2],
                               is_log=is_log)
    return ax


def make_contour_plot(ax: plt.Axes, X: np.ndarray,
                      Y: np.ndarray, Z: np.ndarray,
                      path_x: np.array = [], path_y: np.array = [],
                      labels: np.array = [],
                      is_log: bool = False) -> plt.Axes:
    """Creates a 2D-plot of the loss landscape.
    Embeds the trajectory as well.

    Parameters
    ----------
    X, Y, Z
        x,y,z-components of loss landscape as a grid.
        X and Y must both be 2D with the same shape as Z
        (e.g. created via numpy.meshgrid)
    path_(x,y,z)
        x,y-components of trajectory.
    labels
        Label used in the plot (Only for PCA).
    is_log
        Plot the logarithmic loss landscape and trajectory.

    Returns
    -------
    ax
        Axes object with the plot.
    """
    if is_log:
        scale = lambda x: np.log(x)
    else:
        scale = lambda x: x

    CS = ax.contourf(X, Y, scale(Z), 100, zorder=0, cmap='viridis')
    for c in CS.collections:
        c.set_edgecolor("face")

    # Plot trajectory as well
    if len(path_x) != 0 and len(path_y) != 0:
        NPOINTS = len(path_x)
        cmap = matplotlib.cm.get_cmap('hot')
        normalize = matplotlib.colors.Normalize(vmin=0, vmax=NPOINTS)
        colors = [cmap(normalize(value)) for value in range(NPOINTS)]
        # ax.plot(path_x, path_y, color="k",
        #         markersize=0, alpha=1, zorder=8)
        ax.scatter(path_x, path_y, color=colors[::-1],
                   edgecolor='k', alpha=1, zorder=10)
        # Start of trajectory
        ax.plot(path_x[0], path_y[0], markerfacecolor='k',
                markeredgecolor='k', marker='v',
                markersize=10, alpha=1, zorder=10)
        # End of trajectory
        ax.plot(path_x[-1], path_y[-1], markerfacecolor='r',
                markeredgecolor='r', marker='X',
                markersize=10, alpha=1, zorder=10)

    ax.tick_params(axis='x', which='both', bottom=False,
                   top=False, labelbottom=False)
    ax.tick_params(axis='y', which='both', bottom=False,
                   top=False, labelbottom=False)
    if len(labels) != 0:
        ax.set_xlabel(str(labels[0]))
        ax.set_ylabel(str(labels[1]))
    add_colorbar(CS)
    return ax


def add_colorbar(mappable):
    """Adds a colorbar to a contour plot."""
    last_axes = plt.gca()
    ax = mappable.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = fig.colorbar(mappable, cax=cax)
    plt.sca(last_axes)
    return cbar
