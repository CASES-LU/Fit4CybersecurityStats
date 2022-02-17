#! /usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2 import Environment, PackageLoader
from bokeh.resources import JSResources, CSSResources
from bokeh.embed import file_html

from instance.production import INSTANCES
from fit4cybersecuritystats.fetchers import survey_per_company_sector
from fit4cybersecuritystats.charts import survey_per_company_sector_chart


env = Environment(loader=PackageLoader("fit4cybersecuritystats"))

OUTPUT_PATH = "./stats-chart.html"

if __name__ == "__main__":
    # Point of entry in execution mode
    # grab the static resources
    js_resources = JSResources(mode="inline", minified=True, components=["bokeh"])
    css_resources = CSSResources(mode="inline", minified=True, components=["bokeh"])
    plots = []
    for instance in INSTANCES:
        stats_data = survey_per_company_sector(instance)
        plots.append(survey_per_company_sector_chart(stats_data))

    # html = file_html(plots, (js_resources, css_resources), "Fit4CyberSecurity")
    renderJS = True
    template = env.get_template("html/index.html")
    html = file_html(
        plots,
        (js_resources, css_resources),
        template=template,
        template_variables={
            'js_data': js_resources.render_js() if renderJS else '',
            'text_heading': "<h1>Fit4Cybersecurity</h1>",
            'text_download': "",
            'text_footing': "",
        }
    )

    # print(html)
    with open(OUTPUT_PATH, 'w') as f:
        f.write(str(html))
    print("HTML page written in {}.".format(OUTPUT_PATH))
