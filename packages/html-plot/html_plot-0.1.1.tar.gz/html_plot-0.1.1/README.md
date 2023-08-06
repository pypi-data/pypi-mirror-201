This package can be used to render Matplotlib plots as HTML objects in
Jupyter, so that they can be placed in HTML tables, downloaded on click,
and more.

## Examples
```python
import pandas as pd
my_plot = pd.DataFrame([[1,2,3],[4,5,6]]).plot()
```

### Simple usage
```python
html_plot.display(my_plot)
```

### Advanced usage
#### Adjust Figure and Axes (e.g. figsize, title)
```python
plot_dim = html_plot.get_dim(my_plot.get_figure())
plot_dim.figsize *= 1.5
ax = html_plot.ax("This is my plot", **plot_dim)
my_html_plot = pd.DataFrame([[1,2,3],[4,5,6]]).plot(ax=ax)
```

#### Output HTML string
```python
html_str = html_plot.html_str(my_html_plot)
print(html_str)
```

#### Output an `IPython.display.HTML` object
```python
import IPython.display
html_obj = html_plot.HTML(my_html_plot)
IPython.display.display(html_obj)
```

#### Display the object using a wrapper for `IPython.display.display()`
```python
html_plot.display(my_html_plot)
```
