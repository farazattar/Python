import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable
from bokeh.plotting import figure

def barchart_tab(data):
    d = data.groupby('label')['income'].describe()
    d['mean'] = d['mean'].round(1)
    d['std'] = d['std'].round(1)
    d = d.reset_index()
    Ransomware_lables = d['label'].tolist()
    Counts = d['count'].tolist()
    p = figure(x_range=Ransomware_lables, title="باج افزارها")
    p.vbar(x=Ransomware_lables, top=Counts)
    tab = Panel(child=p, title='نمودار میله ای')
    return tab