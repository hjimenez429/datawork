from django.http import HttpResponse
from django.template.loader import get_template
from matplotlib import pylab
from pylab import *
from io import *
from io import StringIO
from PIL import *
import PIL
import PIL.Image
import io
import base64
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import _pickle as cPickle
from os.path import dirname, join

from django.shortcuts import render, render_to_response

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from math import pi
from bokeh.transform import cumsum
from bokeh.palettes import Category20c

from .forms import userform

from django.shortcuts import render, redirect

from bokeh.core.properties import value
from django.http import JsonResponse
from bokeh.models import (CategoricalColorMapper, HoverTool,
						  ColumnDataSource, Panel,
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis, Select)






def index(request):
    t = get_template('home-company.html')
    html = t.render()
    return HttpResponse(html)

def login(request):

    user_forms = userform()


    if request.method == "POST":
        df = pd.read_csv(open(join(dirname(__file__), '/home/jose/Escritorio/usuarios.csv')))
        print()

        name = request.POST.get('name')
        password = request.POST.get('password')

        valor = df.loc[(df['username'] == name) & (df['passw'] ==password)].count()

        valor1 = valor['username']
        if valor1>=1:
            return redirect('home-person/')
        else:
            return redirect('home-company/')
        #return redirect('result-company/')






    return render(request,'login.html',{'form':user_forms})

def homeCompany(request):
    df = pd.read_csv(open(join(dirname(__file__),'nyc-jobs.csv')))
    posts = list(set(df['Business Title']))
    profesion=list(set(df['Job Category']))
    pais = list(set(df['Work Location']))
    return render_to_response('home-company.html', {'posts': posts,
                              'profesion':profesion, 'pais':pais})

def homePerson(request):
    df = pd.read_csv(open(join(dirname(__file__), 'nyc-jobs.csv')))
    posts = list(set(df['Business Title']))
    profesion = list(set(df['Job Category']))
    pais = list(set(df['Work Location']))
    return render_to_response('home-person.html', {'posts': posts,
                                                    'profesion': profesion, 'pais': pais})


def resultCompany(request):
    df = pd.read_csv(open(join(dirname(__file__), 'nyc-jobs.csv')))

    # Cantidad de ofertas laborales por la semana 1.
    mask1 = (df['Posting Date'] >= '2018-10-01') & (df['Posting Date'] <= '2018-10-07')
    interno1 =(df['Posting Date'] >= '2018-10-01') & (df['Posting Date'] <= '2018-10-07') &(df['Posting Type']=='Internal')
    externo1 = (df['Posting Date'] >= '2018-10-01') & (df['Posting Date'] <= '2018-10-07') & (
                df['Posting Type'] == 'External')
    pr0 = df.loc[mask1].count()
    pr1 = df.loc[interno1].count()
    pr2 = df.loc[externo1].count()
    week1 = pr0['Posting Date']
    week1I = pr1['Posting Type']
    week1E = pr2['Posting Type']


    # Cantidad de ofertas laborales por la semana 2.
    mask2 = (df['Posting Date'] >= '2018-10-08') & (df['Posting Date'] <= '2018-10-14')
    interno2 = (df['Posting Date'] >= '2018-10-08') & (df['Posting Date'] <= '2018-10-14') & (
                df['Posting Type'] == 'Internal')
    externo2 = (df['Posting Date'] >= '2018-10-08') & (df['Posting Date'] <= '2018-10-14') & (
            df['Posting Type'] == 'External')
    pr0 = df.loc[mask2].count()
    pr1 = df.loc[interno2].count()
    pr2 = df.loc[externo2].count()
    week2 = pr0['Posting Date']
    week2I = pr1['Posting Type']
    week2E = pr2['Posting Type']

    # Cantidad de ofertas laborales por la semana 3.
    mask3 = (df['Posting Date'] >= '2018-10-15') & (df['Posting Date'] <= '2018-10-21')
    interno2 = (df['Posting Date'] >= '2018-10-15') & (df['Posting Date'] <= '2018-10-21') & (
            df['Posting Type'] == 'Internal')
    externo2 = (df['Posting Date'] >= '2018-10-15') & (df['Posting Date'] <= '2018-10-21') & (
            df['Posting Type'] == 'External')
    pr0 = df.loc[mask2].count()
    pr1 = df.loc[interno2].count()
    pr2 = df.loc[externo2].count()
    week3 = pr0['Posting Date']
    week3I = pr1['Posting Type']
    week3E = pr2['Posting Type']

    # Cantidad de ofertas laborales por la semana 4.
    mask4 = (df['Posting Date'] >= '2018-10-21') & (df['Posting Date'] <= '2018-10-31')
    interno2 = (df['Posting Date'] >= '2018-10-15') & (df['Posting Date'] <= '2018-10-21') & (
            df['Posting Type'] == 'Internal')
    externo2 = (df['Posting Date'] >= '2018-10-15') & (df['Posting Date'] <= '2018-10-21') & (
            df['Posting Type'] == 'External')
    pr0 = df.loc[mask2].count()
    pr1 = df.loc[interno2].count()
    pr2 = df.loc[externo2].count()
    week4 = pr0['Posting Date']
    week4I = pr1['Posting Type']
    week4E = pr2['Posting Type']

    #Cantidad de empleos por ciudad
    z = df['Work Location']
    df.groupby('Job ID')[['Posting Date']].size()
    x = list(set(df['Work Location']))
    x=x[:10]
    y = z.value_counts().values.tolist()
    people = list(set(df['Work Location']))
    y_pos = z.value_counts().values.tolist()

    #Cantidad de empleos por agencias
    z_agencias = df['Agency']
    x_agencias = list(set(df['Agency']))
    x_agencias = x_agencias[:10]
    y_agencias = z_agencias.value_counts().values.tolist()
    #x_agencias = list(set(df['Agency']))
    y_agencias = z.value_counts().values.tolist()
    y_agencias = y_agencias[:10]

    # Empleos con mayor oferta
    z6 = df['Civil Service Title']
    x6 = list(set(df['Civil Service Title']))
    x6 = x6[:10]
    y6 = z6.value_counts().values.tolist()
    # x_agencias = list(set(df['Agency']))
    y6 = z6.value_counts().values.tolist()
    y6 = y6[:10]

    # Ofertas de medio / tiempo completo
    z7 = df['Full-Time/Part-Time indicator']
    x7 = list(set(df['Full-Time/Part-Time indicator']))
    y7 = z7.value_counts().values.tolist()
    # x_agencias = list(set(df['Agency']))
    y7 = z7.value_counts().values.tolist()

    # Ofertas internas/externas
    z8 = df['Posting Type']
    x8 = list(set(df['Posting Type']))
    y8 = z8.value_counts().values.tolist()
    y8 = z8.value_counts().values.tolist()

    title = 'Offers x city'

    plot = figure(
        title=title,
        x_axis_label='City',
        x_range=x,
        y_axis_label='Offer amount',
        sizing_mode="scale_width",
        plot_width=950,
        plot_height=400)

    plot.line(x, y, legend='Amount', line_width=2, color='#6FB543')
    plot.line(x, y, legend='Amount', line_width=2, color='#6FB543')
    script, div = components(plot)


    x = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    y = [week1, week2, week3, week4]

    ty = [week1I, week2I, week3I, week4I]

    tx = [week1E, week1E, week1E, week1E]

    title = 'Offers x week'

    source = ColumnDataSource(data=dict(x=x, y=y, ty=ty))

    plot2 = figure(x_range=x, plot_height=200, plot_width=300, title="", toolbar_location=None,
                   sizing_mode="scale_width")
    plot2.vbar(x='x', top='y', source=source, width=0.2, color="#1F9245", line_color='red', legend=('Ofertas Totales'))
    plot2.vbar(x='x', top='ty', source=source, width=0.2, color="#6FB543", line_color='black', legend='Ofertas Inters')

    script2, div2 = components(plot2)

    x3 = x8
    y3 = y8
    title = 'Internal / External Jobs'

    plot3 = figure(
        title=title,
        x_range=x3,
        plot_width=400,
        sizing_mode="scale_width",
        plot_height=400)

    plot3.vbar(x3, top=y3, legend='Amount', width=0.9, color='#6FB543')
    script3, div3 = components(plot3)

    muestra = zip(people, y_pos)
    muestra1 = zip(x,y)
    muestra2 = zip(x_agencias,y_agencias)
    muestra3 = zip(x6,y6)
    muestra4 = zip(x7, y7)



    title = 'Laboral Time'


    x2 = dict((k,t) for k,t in muestra2)
    x3 = dict((i,j) for i,j in muestra3)
    x5 = dict((i, j) for i, j in muestra4)


    data = pd.Series(x2).reset_index(name='value').rename(columns={'index': 'jornada'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['color'] = Category20c[len(x2)]

    plot4 = figure(
        sizing_mode="scale_width",
    plot_height = 400, plot_width=400, title = "Jornada Laboral", toolbar_location = None,
    tools = "hover", tooltips = "@jornada: @value", x_range = (-0.5, 1.0))

    #plot4.vbar(x4, top=y4, legend='Amount', width=0.9, color='#6FB543')

    plot4.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='jornada', source=data)
    plot4.axis.axis_label = None
    plot4.axis.visible = False
    plot4.grid.grid_line_color = None
    script4, div4 = components(plot4)

    #Grafica cantidad de empleo por agencia
    data = pd.Series(x2).reset_index(name='value').rename(columns={'index': 'jornada'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['color'] = Category20c[len(x2)]

    plot5 = figure(
        sizing_mode="scale_width",
        plot_height=400, plot_width=600, title="Jornada Laboral", toolbar_location=None,
        tools="hover", tooltips="@jornada: @value", x_range=(-0.5, 1.0))

    # plot4.vbar(x4, top=y4, legend='Amount', width=0.9, color='#6FB543')

    plot5.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='jornada', source=data)
    plot5.axis.axis_label = None
    plot5.axis.visible = False
    plot5.grid.grid_line_color = None
    script5, div5 = components(plot5)

    #Empleos con mayor oferta
    data = pd.Series(x3).reset_index(name='value').rename(columns={'index': 'jornada'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['color'] = Category20c[len(x3)]

    plot6 = figure(
        sizing_mode="scale_width",
        plot_height=400, plot_width=600, title="Jornada Laboral", toolbar_location=None,
        tools="hover", tooltips="@jornada: @value", x_range=(-0.5, 1.0))

    # plot4.vbar(x4, top=y4, legend='Amount', width=0.9, color='#6FB543')

    plot6.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='jornada', source=data)
    plot6.axis.axis_label = None
    plot6.axis.visible = False
    plot6.grid.grid_line_color = None
    script6, div6 = components(plot6)

    # Empleos con mayor oferta
    data = pd.Series(x5).reset_index(name='value').rename(columns={'index': 'jornada'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['color'] = Category20c[len(x5)]

    plot7 = figure(
        sizing_mode="scale_width",
        plot_height=400, plot_width=600, title="Jornada Laboral", toolbar_location=None,
        tools="hover", tooltips="@jornada: @value", x_range=(-0.5, 1.0))

    # plot4.vbar(x4, top=y4, legend='Amount', width=0.9, color='#6FB543')

    plot7.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='jornada', source=data)
    plot7.axis.axis_label = None
    plot7.axis.visible = False
    plot7.grid.grid_line_color = None
    script7, div7 = components(plot7)

    return render_to_response(
        'result-company.html',
        {'script1': script, 'fig1': div,
         'script2': script2, 'fig2': div2,
         'script3': script3, 'fig3': div3,
         'script4': script4, 'fig4': div4,
         'script5': script5, 'fig5' : div5,
         'script6': script6, 'fig6': div6,
         'script7': script7, 'fig7': div7,
         'muestra':muestra, 'muestra1':muestra1}
    )

def resultPerson(request):
    np.random.seed(19680801)

    plt.rcdefaults()
    fig, ax = plt.subplots()

    # Example data
    df = pd.read_csv(open(join(dirname(__file__), 'nyc-jobs.csv')))

    # Cantidad de ofertas laborales por la semana 1.
    mask1 = (df['Posting Date'] >= '2018-10-01') & (df['Posting Date'] <= '2018-10-07')
    interno1 = (df['Posting Date'] >= '2018-10-01') & (df['Posting Date'] <= '2018-10-07') & (
                df['Posting Type'] == 'Internal')
    externo1 = (df['Posting Date'] >= '2018-10-01') & (df['Posting Date'] <= '2018-10-07') & (
            df['Posting Type'] == 'External')
    pr0 = df.loc[mask1].count()
    pr1 = df.loc[interno1].count()
    pr2 = df.loc[externo1].count()
    week1 = pr0['Posting Date']
    week1I = pr1['Posting Type']
    week1E = pr2['Posting Type']

    # Cantidad de ofertas laborales por la semana 2.
    mask2 = (df['Posting Date'] >= '2018-10-08') & (df['Posting Date'] <= '2018-10-14')
    interno2 = (df['Posting Date'] >= '2018-10-08') & (df['Posting Date'] <= '2018-10-14') & (
            df['Posting Type'] == 'Internal')
    externo2 = (df['Posting Date'] >= '2018-10-08') & (df['Posting Date'] <= '2018-10-14') & (
            df['Posting Type'] == 'External')
    pr0 = df.loc[mask2].count()
    pr1 = df.loc[interno2].count()
    pr2 = df.loc[externo2].count()
    week2 = pr0['Posting Date']
    week2I = pr1['Posting Type']
    week2E = pr2['Posting Type']

    # Cantidad de ofertas laborales por la semana 3.
    mask3 = (df['Posting Date'] >= '2018-10-15') & (df['Posting Date'] <= '2018-10-21')
    interno2 = (df['Posting Date'] >= '2018-10-15') & (df['Posting Date'] <= '2018-10-21') & (
            df['Posting Type'] == 'Internal')
    externo2 = (df['Posting Date'] >= '2018-10-15') & (df['Posting Date'] <= '2018-10-21') & (
            df['Posting Type'] == 'External')
    pr0 = df.loc[mask2].count()
    pr1 = df.loc[interno2].count()
    pr2 = df.loc[externo2].count()
    week3 = pr0['Posting Date']
    week3I = pr1['Posting Type']
    week3E = pr2['Posting Type']

    # Cantidad de ofertas laborales por la semana 4.
    mask4 = (df['Posting Date'] >= '2018-10-21') & (df['Posting Date'] <= '2018-10-31')
    interno2 = (df['Posting Date'] >= '2018-10-15') & (df['Posting Date'] <= '2018-10-21') & (
            df['Posting Type'] == 'Internal')
    externo2 = (df['Posting Date'] >= '2018-10-15') & (df['Posting Date'] <= '2018-10-21') & (
            df['Posting Type'] == 'External')
    pr0 = df.loc[mask2].count()
    pr1 = df.loc[interno2].count()
    pr2 = df.loc[externo2].count()
    week4 = pr0['Posting Date']
    week4I = pr1['Posting Type']
    week4E = pr2['Posting Type']

    # Cantidad de empleos por ciudad
    z = df['Work Location']
    df.groupby('Job ID')[['Posting Date']].size()
    x = list(set(df['Work Location']))
    x = x[:10]
    y = z.value_counts().values.tolist()
    people = list(set(df['Work Location']))
    y_pos = z.value_counts().values.tolist()

    # Cantidad de empleos por agencias
    z_agencias = df['Agency']
    x_agencias = list(set(df['Agency']))
    x_agencias = x_agencias[:10]
    y_agencias = z_agencias.value_counts().values.tolist()
    # x_agencias = list(set(df['Agency']))
    y_agencias = z.value_counts().values.tolist()
    y_agencias = y_agencias[:10]

    # Empleos con mayor oferta
    z6 = df['Civil Service Title']
    x6 = list(set(df['Civil Service Title']))
    x6 = x6[:10]
    y6 = z6.value_counts().values.tolist()
    # x_agencias = list(set(df['Agency']))
    y6 = z6.value_counts().values.tolist()
    y6 = y6[:10]

    # Ofertas de medio / tiempo completo
    z7 = df['Full-Time/Part-Time indicator']
    x7 = list(set(df['Full-Time/Part-Time indicator']))
    y7 = z7.value_counts().values.tolist()
    # x_agencias = list(set(df['Agency']))
    y7 = z7.value_counts().values.tolist()

    # Ofertas internas/externas
    z8 = df['Posting Type']
    x8 = list(set(df['Posting Type']))
    y8 = z8.value_counts().values.tolist()
    y8 = z8.value_counts().values.tolist()

    title = 'Offers x city'

    plot = figure(
        title=title,
        x_axis_label='City',
        x_range=x,
        y_axis_label='Offer amount',
        sizing_mode="scale_width",
        plot_width=950,
        plot_height=400)

    plot.line(x, y, legend='Amount', line_width=2, color='#6FB543')
    plot.line(x, y, legend='Amount', line_width=2, color='#6FB543')
    script, div = components(plot)

    x = ['Week 1', 'Week 2', 'Week 3','Week 4']
    y = [week1,week2, week3, week4]


    ty = [week1I, week2I, week3I,week4I]

    tx = [week1E, week1E, week1E, week1E]



    title = 'Offers x week'


    source = ColumnDataSource(data=dict(x=x, y=y, ty=ty))

    plot2 = figure(x_range=x, plot_height=200, plot_width=300, title="", toolbar_location=None, sizing_mode="scale_width")
    plot2.vbar(x='x', top='y', source=source, width=0.2, color="#1F9245", line_color='red', legend=('Ofertas Totales'))
    plot2.vbar(x='x', top='ty', source=source, width=0.2, color="#6FB543", line_color='black', legend='Ofertas Inters')

    script2, div2 = components(plot2)

    x3 = x8
    y3 = y8
    title = 'Internal / External Jobs'

    plot3 = figure(
        title=title,
        sizing_mode="scale_width",
        x_range=x3,
        plot_width=400,
        plot_height=400)

    plot3.vbar(x3, top=y3, legend='Amount', width=0.9, color='#6FB543')
    script3, div3 = components(plot3)

    muestra = zip(people, y_pos)
    muestra1 = zip(x, y)
    muestra2 = zip(x_agencias, y_agencias)
    muestra3 = zip(x6, y6)
    muestra4 = zip(x7, y7)

    title = 'Laboral Time'

    x2 = dict((k, t) for k, t in muestra2)
    x3 = dict((i, j) for i, j in muestra3)
    x5 = dict((i, j) for i, j in muestra4)

    data = pd.Series(x2).reset_index(name='value').rename(columns={'index': 'jornada'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['color'] = Category20c[len(x2)]

    plot4 = figure(
        sizing_mode="scale_width",
        plot_height=400, plot_width=400, title="Jornada Laboral", toolbar_location=None,
        tools="hover", tooltips="@jornada: @value", x_range=(-0.5, 1.0))

    # plot4.vbar(x4, top=y4, legend='Amount', width=0.9, color='#6FB543')

    plot4.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='jornada', source=data)
    plot4.axis.axis_label = None
    plot4.axis.visible = False
    plot4.grid.grid_line_color = None
    script4, div4 = components(plot4)

    # Grafica cantidad de empleo por agencia
    data = pd.Series(x2).reset_index(name='value').rename(columns={'index': 'jornada'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['color'] = Category20c[len(x2)]

    plot5 = figure(
        sizing_mode="scale_width",
        plot_height=400, plot_width=600, title="Jornada Laboral", toolbar_location=None,
        tools="hover", tooltips="@jornada: @value", x_range=(-0.5, 1.0))

    # plot4.vbar(x4, top=y4, legend='Amount', width=0.9, color='#6FB543')

    plot5.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='jornada', source=data)
    plot5.axis.axis_label = None
    plot5.axis.visible = False
    plot5.grid.grid_line_color = None
    script5, div5 = components(plot5)

    # Empleos con mayor oferta
    data = pd.Series(x3).reset_index(name='value').rename(columns={'index': 'jornada'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['color'] = Category20c[len(x3)]

    plot6 = figure(
        sizing_mode="scale_width",
        plot_height=400, plot_width=600, title="Jornada Laboral", toolbar_location=None,
        tools="hover", tooltips="@jornada: @value", x_range=(-0.5, 1.0))

    # plot4.vbar(x4, top=y4, legend='Amount', width=0.9, color='#6FB543')

    plot6.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='jornada', source=data)
    plot6.axis.axis_label = None
    plot6.axis.visible = False
    plot6.grid.grid_line_color = None
    script6, div6 = components(plot6)

    # Empleos con mayor oferta
    data = pd.Series(x5).reset_index(name='value').rename(columns={'index': 'jornada'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['color'] = Category20c[len(x5)]

    plot7 = figure(
        sizing_mode="scale_width",
        plot_height=400, plot_width=600, title="Jornada Laboral", toolbar_location=None,
        tools="hover", tooltips="@jornada: @value", x_range=(-0.5, 1.0))

    # plot4.vbar(x4, top=y4, legend='Amount', width=0.9, color='#6FB543')

    plot7.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='jornada', source=data)
    plot7.axis.axis_label = None
    plot7.axis.visible = False
    plot7.grid.grid_line_color = None
    script7, div7 = components(plot7)

    return render_to_response(
        'result-person.html',
        {'script1': script, 'fig1': div,
         'script2': script2, 'fig2': div2,
         'script3': script3, 'fig3': div3,
         'script4': script4, 'fig4': div4,
         'script5': script5, 'fig5': div5,
         'script6': script6, 'fig6': div6,
         'script7': script7, 'fig7': div7,
         'muestra': muestra, 'muestra1': muestra1}
    )
def updateDashboard(request,a,b):

    df = pd.read_csv(open(join(dirname(__file__), 'nyc-jobs.csv')), sep=',',header=None)
    df.columns = ['job_id', 'agency', 'posting_type', 'n_of_positions', 'business_title',
                  'civil_service_title', 'title_code_no', 'level', 'job_category', 'journal',
                  'salary_range_from', 'salary_range_to', 'salary_frecuence', 'work_location',
                  'division', 'job_description', 'minimum_qual_requirements', 'preferred_skills',
                  'additional_information', 'to_apply', 'hours_shift', 'work_location', 'recruitment_contact',
                  'residency_requirement', 'posting_date', 'post_until', 'posting_updated', 'process_date']

    axis_map = {
        "Tipo de oferta": "posting_type",
        "Agencia": "agency"
    }

    posting_map = {
        "External", "Internal"
    }

    lang = {"External": "Externas", "Internal": "Internas"}

    # Create Input controls
    #posting_type = Select(title="Tipo de oferta", options=sorted(posting_map), value="Internal")
    #amount = Slider(title="Cantidad de Agencias", value=3, start=1, end=10, step=1)
    y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="Cantidad de ofertas")
    x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Agencia")

    x = df['agency'].value_counts().index.tolist()
    y = df['agency'].value_counts().tolist()
    x = x[:b]
    y = y[:b]

    ty = df['agency'].value_counts().tolist()
    ty = ty[:b]
    source = ColumnDataSource(data=dict(x=x, y=y, ty=ty))

    p = figure(x_range=x, plot_height=200, plot_width=400, title="", toolbar_location=None, sizing_mode="scale_width")
    p.vbar(x='x', top='ty', source=source, width=0.2, color="#1F9245", line_color='red', legend=('Ofertas Totales'))
    p.vbar(x='x', top='y', source=source, width=0.2, color="#6FB543", line_color='black', legend='Ofertas ' + lang[a])

    # curdoc().clear()
    # show(p)

    def select_offers():
        selected = df[
            (df['posting_type'] == a)
        ]

        return selected

    def total_offers():
        return df

    def update():
        df2 = select_offers()
        dft = total_offers()

        x = df2['agency'].value_counts().index.tolist()
        y = df2['agency'].value_counts().tolist()
        x = x[:b]
        y = y[:b]

        ty = dft['agency'].value_counts().tolist()
        ty = ty[:b]
        print(y)
        print(ty)

        p.xaxis.axis_label = x_axis.value
        p.yaxis.axis_label = y_axis.value
        p.x_range.factors = x
        p.title.text = 'Cantidad de agencias: %d' % b + '.  Tipo de oferta: ' + a
        source.data = dict(
            x=x,
            y=y,
            ty=ty,
        )

    update()
    update()

    s3, d3 = components(p)

    return JsonResponse({'udD': d3, 'udS': s3})