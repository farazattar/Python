from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
import pandas as pd
from income import income_tab
from count import count_tab
from barchart import barchart_tab

data = pd.read_csv('BitcoinHeistData.csv').dropna()
tab_income = income_tab(data)
tab_count = count_tab(data)
tab_barchart = barchart_tab(data)
tabs = Tabs(tabs=[tab_income, tab_count, tab_barchart])
curdoc().add_root(tabs)
