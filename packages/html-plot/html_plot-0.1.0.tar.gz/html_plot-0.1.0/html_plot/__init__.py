"""
Functions for rendering Matplotlib plots as HTML objects in Jupyter
"""

from box import Box
import numpy as np
import io
import base64
import mimetypes
import matplotlib as mpl
import matplotlib.pyplot as plt
import IPython.display

def get_dim(plot):
    """
    Return a structure with the dimensions of the plot
    """
    return Box(
        dpi = plot.get_dpi(),
        # Use np.array to make `figsize` easily adjustable with expressions such as `2 * plot_dim.figsize``
        figsize = np.array([plot.get_figwidth(), plot.get_figheight()]),
    )

def fig(**fig_kwargs):
    """
    Create a Figure without using Pyplot, because we don't want to display it directly
    """
    return mpl.figure.Figure(**fig_kwargs)

def ax(title = None, **fig_kwargs):
    """
    Create a Figure with a subplot and return its ax
    """
    return fig(**fig_kwargs).add_subplot(title = title)

def html_str(fig_or_ax = None, format = "svg"):
    """
    Create an HTML version of the plot in the specified format
    """
    if fig_or_ax is None:
        _fig = plt
        _axs = [plt.gca()]
    elif issubclass(type(fig_or_ax), mpl.figure.Figure):
        _fig = fig_or_ax
        _axs = _fig.get_axes()
    elif issubclass(type(fig_or_ax), mpl.axes.Axes):
        _fig = fig_or_ax.get_figure()
        _axs = [fig_or_ax]
    elif issubclass(type(fig_or_ax), mpl.axes.Axes):
        _fig = fig_or_ax[0].get_figure()
        _axs = fig_or_ax
    else:
        raise TypeError("fig_or_ax has a wrong type")
    filename = '--'.join([ax.get_title() for ax in _axs]).replace(' ', '_')
    tmpfile = io.BytesIO()
    _fig.savefig(tmpfile, format=format, bbox_inches='tight')
    mimetype = mimetypes.types_map.get(f".{format}", "")
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    return (
        f'<a download="{filename}.{format}" href="data:{mimetype};base64,{encoded}">'
            f'<img src="data:{mimetype};base64,{encoded}">'
        '</a>'
    )

def HTML(*args, **kwargs):
    """
    Create an HTML object with the plot
    """
    return IPython.display.HTML(html_str(*args, **kwargs))

def display(*args, **kwargs):
    """
    Display the HTML plot
    """
    return IPython.display.display(HTML(*args, **kwargs))
