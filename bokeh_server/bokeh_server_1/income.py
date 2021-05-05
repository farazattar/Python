import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable

def income_tab(data):
    d = data.groupby('label')['income'].describe()
    d['mean'] = d['mean'].round(1)
    d['std'] = d['std'].round(1)
    d = d.reset_index()

    c = ColumnDataSource(d)
    Bitcoin_income_table = DataTable(
        source=c,
        columns=[
            TableColumn(field='label', title='نام باج افزار'),
            TableColumn(field='count', title='تعداد تکرار'),
            TableColumn(field='mean', title='میانگین درآمد'),
            TableColumn(field='std', title='انحراف استاندارد درآمد'),
            TableColumn(field='min', title='کمینه‌ی درآمد'),
            TableColumn(field='25%', title='۲۵٪'),
            TableColumn(field='50%', title='۵۰٪'),
            TableColumn(field='75%', title='۷۵٪'),
            TableColumn(field='max', title='بیشنیه‌ی درآمد'),

        ],
        width=1500
    )
    tab = Panel(child=Bitcoin_income_table, title='اطلاعات درآمد')
    return tab