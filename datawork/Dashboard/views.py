from django.shortcuts import render

from django.shortcuts import render, render_to_response
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import components
import math

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import _pickle as cPickle
from os.path import dirname, join




def data(request):

    df = pd.read_csv(open(join(dirname(__file__), '/home/jose/Escritorio/nyc-jobs.csv')))
   
    print(df['Work Location'].dtype)


    x= df['Salary Range From']
    y= df['Salary Range To']
    ciudad=df['Work Location']
    title = 'y = f(x)'

    
    plot = figure(title= title , 
    x_axis_label= 'X-Axis', 
    y_axis_label= 'Y-Axis', 
    plot_width =1000,
    plot_height =600)

    plot.scatter(x, y, legend= 'f(x)', line_width = 2)
    #Store components 
    script, div = components(plot)
    return render_to_response( 'indexPrueba.html', {'script' : script , 'div' : div} )

def homeCompany1(request):
    df = pd.read_csv(open(join(dirname(__file__), '/home/jose/Escritorio/nyc-jobs.csv')))
    posts = list(set(df['Work Location']))
    profesion = list(set(df['Business Title']))
    return render_to_response('home-company1.html',{'posts':posts, 'profesion':profesion})


