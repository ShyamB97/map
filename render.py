"""
Created on: 10/05/2025 21:45

Author: Shyam Bhuller

Description: Render the GPX files. Uses plotly for an easy implementation of open street map.
#? automaticaly calculate the best zoom value based on the paths?
"""
import numpy as np
import pandas as pd
import plotly.express as px

from plotly.graph_objects import Figure

from gpx import GPX


def quad_interp(x0 : float, x1 : float, y0 : float, y1 : float, step : int) -> np.ndarray:
    """ Quadratic interpolation of two 2d points.

    Args:
        x0 (float): First point x value, treated as the 1st root. 
        x1 (float): Second point x value, treated as the inflection point.
        y0 (float): First point y value, treated as the 1st root.
        y1 (float): Second point y value, treated as the inflection point.
        step (int): Number of the interpolated points generated along the quadratic.

    Returns:
        np.ndarray: y values of the quadratic curve generated from the two points.
    """
    r0 = x0 # assume this is the 1st root
    m = x1 # assume this is the maxima/minima
    ym = y1 - y0 # height of the maxima/minima, given the 1st root must have y = 0

    if r0 != m:
        a =  -ym / (m - r0)**2
        b = -2 * a * m
        c = a * m**2 + ym

        y = lambda t: a*(t**2) + b*t + c
        y_i = y0 + y(np.linspace(r0, m, step)) # offset to return to global position space
    else:
        # positions are the same, so just do linear interpolation
        y_i = np.linspace(y0, y1, step)
    return y_i


def interp(x : list | np.ndarray, y : list | np.ndarray, step : int) -> list | np.ndarray:
    """ Quadratic interpolation algorithm for an array of 2d points.

    Args:
        x (list | np.ndarray): x values of the points.
        y (list | np.ndarray): y values of the point.
        step (int): Number of interpolated points to generate BETWEEN EACH pair of points.

    Returns:
        list | np.ndarray: array of Interpolated points.
    """

    if step <= 2:
        print("Skipping interpolation, step size must be greater than 2")
        return x, y

    x_i = np.array([])
    y_i = np.array([])
    for i in range(len(x) - 1):
        xt = np.linspace(x[i], x[i + 1], step)
        if i%2 == 0:
            yt = quad_interp(x[i], x[i + 1], y[i], y[i + 1], step)
        else:
            yt = quad_interp(x[i + 1], x[i], y[i + 1], y[i], step)[::-1]
        y_i = np.concatenate((y_i, yt))
        x_i = np.concatenate((x_i, xt))

    return x_i, y_i


def render_map(gpxs : list[str]) -> Figure:
    """ Parse the gpx files and render the map.

    Args:
        gpxs (list[str]): gpx files to open.

    Returns:
        Figure: plotly figure widget.
    """

    # open the gpx files and add the paths from each route in a dataframe
    df = pd.DataFrame()
    for g in gpxs:
        gpx = GPX(g)
        for n, p in gpx.get_paths().items():
            tmp_df = pd.DataFrame(p)
            tmp_df["hike"] = n # tag each node to keep knowledge of which hike it came from.
            df = pd.concat([df, tmp_df], axis = 0)

    fig = px.line_map(df, lat="lat", lon="lon", height=800, color = "hike", color_discrete_sequence = px.colors.qualitative.Dark24, labels = "hike") # generate the lines on a open street map widget
    fig.update_traces(line={'width': 4}) # set all the line widths
    fig.update_layout(map_style="basic", map_center_lon = 0.5 * (max(df.lon) + min(df.lon)), map_center_lat = 0.5 * (max(df.lat) + min(df.lat)), map_zoom = 10, margin={"r":0,"t":0,"l":0,"b":0}) # set the style of the map, and the origin point + zoom
    return fig