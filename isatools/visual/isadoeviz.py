from bokeh.io import output_file
from bokeh.plotting import figure, show
import json
import os
import sys

from bokeh.plotting import figure, show, output_notebook, output_file
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.tools import HoverTool
from datetime import datetime
# from bokeh.palettes import GnBu3
import pandas as ps

# arms = ["arm1", "arm2"]
# # output_file('output_file_test.html',
# #             title='Empty Bokeh Figure')
# element_type = ["screen", "treatment", "washout", "follow-up"]
# elements_per_arm = {'types': element_type,
#                     'arm1': [0,1,2,1,3],
#                     'arm2': [0,1,2,1,2,3]
#                     }


# p = figure(y_range=arms, plot_height=250, x_range=(0, 6), title="ISA Study Arms")
# # p.hbar_stack(, y='arms', height=0.9, color=GnBu3, source=ColumnDataSource(elements_per_arm),
# #              legend=["%s arms" % x for x in arms])
# p.y_range.range_padding = 0.1
# p.ygrid.grid_line_color = None
# p.legend.location = "center_left"
# show(p)
# path = "../tests/data/"
#
# try:
#     if os.path.exists(path):
#         print("it exists", path)
#     else:
#         print("could not find my path")
# except OSError as oserror:
#      print(oserror, path)

# try:
#
#     # input_isadoe = json.loads("isa-doe-arms-test.json",encoding="UTF-8")
#     with open('isa-doe-arms-test.json', 'r') as f:
#         array = json.load(f)
#
#         print(array)
#         arms = array['arms']
#         print(arms)
#
# except IOError as e:
#     print("problem reading the file:", e)
#
#
# try:
#     with open('isa-doe-arms-test.json', 'r') as f:
#         df = ps.read_json(f)
#
# except IOError as e1:
#     print("pd reading json in pandas")


output_file('GanttChart.html')

DF=ps.DataFrame(columns=['Item','Start','End','Color'])
Items=[
    ['screen','2015-7-22','2015-8-7','green'],
    ['treatment1','2015-8-10','2015-8-14','red'],
    ['washout','2015-8-17','2015-8-21','gray'],
    ['treatment2','2015-9-1','2016-6-1','orange'],
    ['follow-up','2016-1-2','2016-3-15','blue']

    ] #first items on bottom

for i,Dat in enumerate(Items[::-1]):
    DF.loc[i]=Dat

#convert strings to datetime fields:
DF['Start_dt']=ps.to_datetime(DF.Start)
DF['End_dt']=ps.to_datetime(DF.End)
#DF
G=figure(title='Project Schedule',x_axis_type='datetime',width=800,height=400,y_range=DF.Item.tolist(),
        x_range=Range1d(DF.Start_dt.min(),DF.End_dt.max()), tools='save')

hover=HoverTool(tooltips="Task: @Item<br>\
Start: @Start<br>\
End: @End")
G.add_tools(hover)

DF['ID']=DF.index+0.8
DF['ID1']=DF.index+1.2
CDS=ColumnDataSource(DF)
G.quad(left='Start_dt', right='End_dt', bottom='ID', top='ID1',source=CDS,color="Color")
#G.rect(,"Item",source=CDS)
show(G)


# # The figure will be rendered in a static HTML file called output_file_test.html
# output_file('output_file_test.html',
#             title='Empty Bokeh Figure')
#
# # Set up a generic figure() object
# fig = figure()
#
# # See what it looks like
# show(fig)

