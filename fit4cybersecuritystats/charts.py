#! /usr/bin/env python
from math import pi

import pandas as pd
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum


def survey_per_company_sector_chart(stats):
    data = (
        pd.Series(stats).reset_index(name="value").rename(columns={"index": "sector"})
    )
    data["angle"] = data["value"] / data["value"].sum() * 2 * pi
    try:
        data["color"] = Category20c[len(stats)]
    except KeyError:
        # if length is < 3
        data["color"] = ("#3182bd", "#6baed6", "#9ecae1")[: len(stats)]

    plot = figure(
        height=800,
        width=1200,
        title="Pie Chart",
        toolbar_location=None,
        tools="hover",
        tooltips="@sector: @value",
        x_range=(-0.5, 1.0),
    )

    plot.wedge(
        x=0,
        y=1,
        radius=0.4,
        start_angle=cumsum("angle", include_zero=True),
        end_angle=cumsum("angle"),
        line_color="white",
        fill_color="color",
        legend_field="sector",
        source=data,
    )

    plot.axis.axis_label = None
    plot.axis.visible = False
    plot.grid.grid_line_color = None
    plot.background_fill_color = None
    plot.border_fill_color = None
    # export_png(plot, filename="plot.png")
    # show(plot)
    return plot
