from bokeh.plotting import figure, show
month=[0, 4, 5, 8, 9, 12, 15, 18]
weight=[2.48, 6.4, 7.74, 8.8, 9.25, 9.74, 10.9, 11.4]
height=[50, 63, 68, 71, 74, 78, 81.5, 85]
head=[32, 39.5, 41.5, 43, 44, 45, 46, 46.5]
p = figure(title="Sepehr Growth Tracker", x_axis_label='month', y_axis_label='Weight/Height/Head')
p.line(month, weight, legend_label="Sepehr Wight", line_color="blue", line_width=2)
p.line(month, height, legend_label="Sepehr height", line_color="red", line_width=2)
p.line(month, head, legend_label="Sepehr head", line_color="green", line_width=2)
show(p)
