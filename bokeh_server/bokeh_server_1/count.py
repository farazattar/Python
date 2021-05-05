import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable

def count_tab(data):
    d = data.groupby('label')['count'].describe()
    d['mean'] = d['mean'].round(1)
    d['std'] = d['std'].round(1)
    d = d.reset_index()

    c = ColumnDataSource(d)
    Bitcoin_count_table = DataTable(
        source=c,
        columns=[
            TableColumn(field='label', title='نام باج افزار'),
            TableColumn(field='count', title='تعداد تکرار'),
            TableColumn(field='mean', title='میانگین'),
            TableColumn(field='std', title='انحراف استاندارد'),
            TableColumn(field='min', title='کمینه‌'),
            TableColumn(field='25%', title='۲۵٪'),
            TableColumn(field='50%', title='۵۰٪'),
            TableColumn(field='75%', title='۷۵٪'),
            TableColumn(field='max', title='بیشنیه'),

        ],
        width=1500
    )
    tab = Panel(child=Bitcoin_count_table, title='اطلاعات مربوط به شمار')
    return tab