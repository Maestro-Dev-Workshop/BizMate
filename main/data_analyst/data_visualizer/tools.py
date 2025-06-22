import matplotlib.pyplot as plt
from typing import Any
from pathlib import Path

# Helper functions
def create_figure_and_subplots(
    num_rows: int,
    num_cols: int,
    vertical_size: float,
    horizontal_size: float,
    fig_name: str):
  """
  Creates a figure and subplots.

  Args:
    num_rows: The number of rows in the subplot grid.
    num_cols: The number of columns in the subplot grid.
    vertical_size: The vertical size of the figure in inches.
    horizontal_size: The horizontal size of the figure in inches.
    fig_name: The name of the figure.

  Returns:
    A tuple containing the matplotlib figure and subplots(axes) objects.
  """
  print(f" - Function Call: create_figure_and_subplots({num_rows}, {num_cols}, {vertical_size}, {horizontal_size}, {fig_name})")
  fig, axes = plt.subplots(num_rows, num_cols, figsize=(horizontal_size, vertical_size));
  # fig.suptitle(fig_name);
  return fig, axes;

def generate_bar_chart(
    ax: Any,
    categories: list[str],
    values: list[float],
    orientation: str,
    width: str,
    bottom: str,
    colors: str):
  """
  Generates a bar chart.

  Args:
    ax: The matplotlib axes object to plot the chart on.
    categories: The list of categories or x-coordinates of the bars.
    values: The list of heights of the bars (i.e., values).
    orientation: The orientation of the chart (either 'horizontal' or 'vertical').
    width: The width of the bars. Pass 'None' to use default value.
    bottom: The vertical baseline of the bars. Pass 'None' to use default value.
    colors: The colors of the bars in hexadecimal format. Either a single color for all bars passed as a string, or a list of colours for the different bars passed as a single string with colors separated by ",". Pass 'None' to use default value.

  Returns:
    The axis with the chart plotted on it.
  """
  print(f" - Function Call: generate_bar_chart({categories}, {values}, {orientation}, {width}, {bottom}, {colors})")

  if colors:
    colors = colors.split(",")
    if len(colors) == 1:
      colors = colors[0]
  if not width:
    width = 0.8
  else:
    width = float(width)
  if not bottom:
    bottom = 0
  else:
    bottom = float(bottom)

  print(categories)
  print(values)
  print(width)
  print(bottom)
  print(colors)
  ax = ax
  if orientation == "horizontal":
    ax.barh(y=categories, width=values, height=width, left=bottom, color=colors)
  else:
    ax.bar(x=categories, height=values, width=width, bottom=bottom, color=colors)
  return ax

def generate_line_chart(
    ax: Any,
    x_values: list,
    y_values: list[float],
    label: str,
    line_style: str,
    marker: str,
    color: str,
    x_lim: list[float],
    y_lim: list[float]
    ):
  """
  Generates a line chart.

  Args:
    ax: The matplotlib axes object to plot the chart on.
    x_values: The list of X-axis data (can be dates, numbers, categories).
    y_values: The list of Y-axis data (numerical values).
    label: Label for the legend.
    line_style: The style of the line (e.g. 'solid', 'dashed', 'dotted', 'dashdot', e.t.c). Pass 'None' to use default value.
    marker: The marker to use (e.g. 'o', '^', 's', 'x', e.t.c). Pass 'None' to use default value.
    color: The color of the line in hexadecimal format. Pass 'None' to use default value.
    x_lim: The bounds of the x-axis in the format [<left_bound>, <right_bound>]. Pass 'None' to use default value.
    y_lim: The bounds of the y-axis in the format [<top_bound>, <bottom_bound>]. Pass 'None' to use default value.

  Returns:
    The axis with the chart plotted on it.
  """
  print(f" - Function Call: generate_line_chart({x_values}, {y_values}, {label}, {line_style}, {marker}, {color})")
  ax.plot(x_values, y_values, label=label, linestyle=line_style, marker=marker, color=color)
  if x_lim:
    ax.set_xlim(x_lim)
  if y_lim:
    ax.set_ylim(y_lim)
  return ax

def generate_scatter_chart(
    ax: Any,
    x_coordinates: list[float],
    y_coordinates: list[float],
    sizes: list,
    marker: str,
    colors: str,
    color_map: str,
    color_map_min: float,
    color_map_max: float,
    alpha: float,
    x_lim: list[float],
    y_lim: list[float],
    ):
  """
  Generates a scatter chart.

  Args:
    ax: The matplotlib axes object to plot the chart on.
    x_coordinates: The list of x coordinates of the points to plot.
    y_coordinates: The list of y coordinates of the points to plot.
    sizes: The list of sizes of the points. Pass 'None' to use default value.
    marker: The marker to use (e.g. 'o', '^', 's', 'x', e.t.c). Pass 'None' to use default value.
    colors: The colors of the points in hexadecimal format. Either a single color for all points passed as a string, or a list of colours for the different points passed as a single string with colors separated by ",". Pass 'None' to use default value.
    color_map: The color map to use. Pass 'None' to use default value.
    color_map_min: The minimum value of the color map. Pass 'None' to use default value.
    color_map_max: The maximum value of the color map. Pass 'None' to use default value.
    alpha: The transparency of the points. Pass 'None' to use default value.
    x_lim: The bounds of the x-axis in the format [<left_bound>, <right_bound>]. Pass 'None' to use default value.
    y_lim: The bounds of the y-axis in the format [<top_bound>, <bottom_bound>]. Pass 'None' to use default value.

  Returns:
    The axis with the chart plotted on it.
  """
  print(f" - Function Call: generate_scatter_chart({x_coordinates}, {y_coordinates}, {sizes}, {marker}, {colors}, {color_map}, {color_map_min}, {color_map_max}, {alpha})")
  if colors:
    colors = colors.split(",")
    if len(colors) == 1:
      colors = colors[0]
  ax.scatter(x_coordinates, y_coordinates, s=sizes, marker=marker, c=colors, cmap=color_map, vmin=color_map_min, vmax=color_map_max, alpha=alpha)
  if x_lim:
    ax.set_xlim(x_lim)
  if y_lim:
    ax.set_ylim(y_lim)
  return ax

def generate_pie_chart(
    ax: Any,
    values: list[float],
    labels: list,
    explode: list,
    colors: str,
    ):
  """
  Generates a pie chart.

  Args:
    ax: The matplotlib axes object to plot the chart on.
    values: The list of values to plot.
    labels: The list of labels for each slice.
    explode: List to "explode" (offset) slices (e.g., [0, 0.1, 0, 0]). Pass 'None' to use default value.
    colors: The colors of the slices in hexadecimal format. Either a single color for all slices passed as a string, or a list of colours for the different slices passed as a single string with colors separated by ",". Pass 'None' to use default value.

  Returns:
    The axis with the chart plotted on it.
  """
  print(f" - Function Call: generate_pie_chart({values}, {labels}, {explode}, {colors})")
  if colors:
    colors = colors.split(",")
    if len(colors) == 1:
      colors = colors[0]
  ax.pie(values, labels=labels, explode=explode, colors=colors)
  return ax

def annotate_chart(
    ax: Any,
    x_label: str,
    y_label: str,
    title: str,
    use_legend: bool,
    legend_loc: str,
    legend_title: str):
  """
  Adds labels and a title to a chart.

  Args:
    ax: The matplotlib axes object whose chart is to be labelled.
    x_label: The label for the x-axis. Pass 'None' to use default value.
    y_label: The label for the y-axis. Pass 'None' to use default value.
    title: The title of the chart.
    use_legend: Whether to use a legend. True or False.
    legend_loc: The location of the legend (e.g. 'upper left', 'upper right', 'lower left', 'lower right', e.t.c).
    legend_title: The title of the legend.

  Returns:
    The axis with the chart labelled.
  """
  print(f" - Function Call: annotate_chart({x_label}, {y_label}, {title}, {use_legend}, {legend_loc}, {legend_title})")
  if x_label:
    ax.set_xlabel(x_label)
  if y_label:
    ax.set_ylabel(y_label)
  ax.set_title(title)
  if use_legend:
    ax.legend(loc=legend_loc, title=legend_title)
  return ax

def save_visual(fig: Any, business_id: str, file_name: str):
  """
  Saves a figure as an image.

  Args:
    fig: The matplotlib figure object to save.
    business_id: The ID of the business.
    file_name: The name of the file to save the image as.

  Returns:
    The path to the saved image.
  """
  print(f" - Function Call: save_visual({fig})")
  file_name = file_name if file_name.endswith(".png") else f"{file_name}.png"
  file_path = Path("main", "visuals", business_id, file_name)
  print(file_path.exists(),file_path.resolve())
  fig.savefig(file_path)
  return file_path.__str__()


# Main tools
def create_and_save_bar_chart(
    categories: list[str],
    values: list[float],
    orientation: str,
    width: str,
    bottom: str,
    colors: str,
    fig_horizontal_size: float,
    fig_vertical_size: float,
    x_label: str,
    y_label: str,
    title: str,
    use_legend: bool,
    legend_loc: str,
    legend_title: str,
    business_id: str,
    file_name: str):
  """
  Creates a bar chart and saves it as an image.

  Args:
    categories: The list of categories or x-coordinates of the bars.
    values: The list of heights of the bars (i.e., values).
    orientation: The orientation of the chart (either 'horizontal' or 'vertical'). Horizontal should be the preferred orientation.
    width: The width of the bars. Pass 'None' to use default value.
    bottom: The vertical baseline of the bars. Pass 'None' to use default value.
    colors: The colors of the bars in hexadecimal format. Either a single color for all bars passed as a string, or a list of colours for the different bars passed as a single string with colors separated by ",". Pass 'None' to use default value.
    fig_horizontal_size: The horizontal size of the figure in inches.
    fig_vertical_size: The vertical size of the figure in inches.
    x_label: The label for the x-axis.
    y_label: The label for the y-axis.
    title: The title of the chart.
    use_legend: Whether to use a legend. True or False.
    legend_loc: The location of the legend (e.g. 'upper left', 'upper right', 'lower left', 'lower right', e.t.c).
    legend_title: The title of the legend.
    business_id: The ID of the business.
    file_name: The name of the file to save the image as.

  Returns:
    The path to the saved image.
  """
  try:
    fig, ax = create_figure_and_subplots(1, 1, fig_vertical_size, fig_horizontal_size, "Test")
    ax = generate_bar_chart(ax, categories, values, orientation, width, bottom, colors)
    ax = annotate_chart(ax, x_label, y_label, title, use_legend, legend_loc, legend_title)
    return save_visual(fig, business_id, file_name)
  except Exception as e:
    print(e)
    return f"Error: {e}"

def create_and_save_line_chart(
    x_values: list[str],
    y_values: list[float],
    label: str,
    line_style: str,
    marker: str,
    color: str,
    x_lim: list[float],
    y_lim: list[float],
    fig_horizontal_size: float,
    fig_vertical_size: float,
    x_label: str,
    y_label: str,
    title: str,
    use_legend: bool,
    legend_loc: str,
    legend_title: str,
    business_id: str,
    file_name: str):
  """
  Creates a line chart and saves it as an image.

  Args:
    x_values: The list of X-axis data (can be dates, numbers, categories).
    y_values: The list of Y-axis data (numerical values).
    label: Label for the legend.
    line_style: The style of the line (e.g. 'solid', 'dashed', 'dotted', 'dashdot', e.t.c).
    marker: The marker to use (e.g. 'o', '^', 's', 'x', e.t.c).
    color: The color of the line in hexadecimal format. Pass 'None' to use default value.
    x_lim: The bounds of the x-axis in the format [<left_bound>, <right_bound>]. Pass 'None' to use default value.
    y_lim: The bounds of the y-axis in the format [<top_bound>, <bottom_bound>]. Pass 'None' to use default value.
    fig_horizontal_size: The horizontal size of the figure in inches.
    fig_vertical_size: The vertical size of the figure in inches.
    x_label: The label for the x-axis. Pass 'None' to use default value.
    y_label: The label for the y-axis. Pass 'None' to use default value.
    title: The title of the chart.
    use_legend: Whether to use a legend. True or False.
    legend_loc: The location of the legend (e.g. 'upper left', 'upper right', 'lower left', 'lower right', e.t.c).
    legend_title: The title of the legend.
    business_id: The ID of the business.
    file_name: The name of the file to save the image as.

  Returns:
    The path to the saved image.
  """
  try:
    fig, ax = create_figure_and_subplots(1, 1, fig_vertical_size, fig_horizontal_size, "Test")
    ax = generate_line_chart(ax, x_values, y_values, label, line_style, marker, color, x_lim, y_lim)
    ax = annotate_chart(ax, x_label, y_label, title, use_legend, legend_loc, legend_title)
    return save_visual(fig, business_id, file_name)
  except Exception as e:
    return f"Error: {e}"

def create_and_save_scatter_chart(
    x_coordinates: list[float],
    y_coordinates: list[float],
    sizes: list[float],
    marker: str,
    colors: str,
    color_map: str,
    color_map_min: float,
    color_map_max: float,
    alpha: float,
    x_lim: list[float],
    y_lim: list[float],
    fig_horizontal_size: float,
    fig_vertical_size: float,
    x_label: str,
    y_label: str,
    title: str,
    use_legend: bool,
    legend_loc: str,
    legend_title: str,
    business_id: str,
    file_name: str):
  """
  Creates a scatter chart and saves it as an image.

  Args:
    x_coordinates: The list of x coordinates of the points to plot.
    y_coordinates: The list of y coordinates of the points to plot.
    sizes: The list of sizes of the points. Pass 'None' to use default value.
    marker: The marker to use (e.g. 'o', '^', 's', 'x', e.t.c). Pass 'None' to use default value.
    colors: The colors of the points in hexadecimal format. Either a single color for all points passed as a string, or a list of colours for the different points
    color_map: The color map to use. Pass 'None' to use default value.
    color_map_min: The minimum value of the color map. Pass 'None' to use default value.
    color_map_max: The maximum value of the color map. Pass 'None' to use default
    alpha: The transparency of the points. Pass 'None' to use default value.
    x_lim: The bounds of the x-axis in the format [<left_bound>, <right_bound>]. Pass 'None' to use default value.
    y_lim: The bounds of the y-axis in the format [<top_bound>, <bottom_bound>]. Pass 'None' to use default value.
    fig_horizontal_size: The horizontal size of the figure in inches.
    fig_vertical_size: The vertical size of the figure in inches.
    x_label: The label for the x-axis.
    y_label: The label for the y-axis.
    title: The title of the chart.
    use_legend: Whether to use a legend. True or False.
    legend_loc: The location of the legend (e.g. 'upper left', 'upper right', 'lower left', 'lower right', e.t.c).
    legend_title: The title of the legend.
    business_id: The ID of the business.
    file_name: The name of the file to save the image as.

  Returns:
    The path to the saved image.
  """
  try:
    fig, ax = create_figure_and_subplots(1, 1, fig_vertical_size, fig_horizontal_size, "Test")
    ax = generate_scatter_chart(ax, x_coordinates, y_coordinates, sizes, marker, colors, color_map, color_map_min, color_map_max, alpha, x_lim, y_lim)
    ax = annotate_chart(ax, x_label, y_label, title, use_legend, legend_loc, legend_title)
    return save_visual(fig, business_id, file_name)
  except Exception as e:
    return f"Error: {e}"

def create_and_save_pie_chart(
    values: list[float],
    labels: list[str],
    explode: list[float],
    colors: str,
    fig_horizontal_size: float,
    fig_vertical_size: float,
    title: str,
    use_legend: bool,
    legend_loc: str,
    legend_title: str,
    business_id: str,
    file_name: str):
  """
  Creates a pie chart and saves it as an image.

  Args:
    values: The list of values to plot.
    labels: The list of labels for each slice.
    explode: List to "explode" (offset) slices, explode values can range from 0.0 to 1.0. Pass 'None' to use default value.
    colors: The colors of the slices in hexadecimal format. Either a single color for all slices passed as a string, or a list of colours for the different slices.
    fig_horizontal_size: The horizontal size of the figure in inches.
    fig_vertical_size: The vertical size of the figure in inches.
    title: The title of the chart.
    use_legend: Whether to use a legend. True or False.
    legend_loc: The location of the legend (e.g. 'upper left', 'upper right', 'lower left', 'lower right', e.t.c).
    legend_title: The title of the legend.
    business_id: The ID of the business.
    file_name: The name of the file to save the image as.

  Returns:
    The path to the saved image.
  """
  try:
    fig, ax = create_figure_and_subplots(1, 1, fig_vertical_size, fig_horizontal_size, "Test")
    ax = generate_pie_chart(ax, values, labels, explode, colors)
    ax = annotate_chart(ax, None, None, title, use_legend, legend_loc, legend_title)
    return save_visual(fig, business_id, file_name)
  except Exception as e:
    return f"Error: {e}"