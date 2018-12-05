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
            return redirect('result-company/')
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
    t = get_template('home-person.html')
    html = t.render()
    return HttpResponse(html)

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
    pr = df.loc[mask3].count()
    week3 = pr['Posting Date']

    # Cantidad de ofertas laborales por la semana 4.
    mask4 = (df['Posting Date'] >= '2018-10-21') & (df['Posting Date'] <= '2018-10-31')

    pr = df.loc[mask4].count()
    interno = pr['Posting Type']
    #print(interno)
    week4 = pr['Posting Date']

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
        plot_width=950,
        plot_height=400)

    plot.line(x, y, legend='Amount', line_width=2, color='#6FB543')
    plot.line(x, y, legend='Amount', line_width=2, color='#6FB543')
    script, div = components(plot)

    x = ['Week 1','Internal Week 1','External Week 1' ,'Week 2','Internal Week 2','External Week 2', 'Week 3', 'Week 4']
    y= [week1,week1I,week1E ,week2,week2I,week2E,week3, week4]

    x0 = ['Week 1', 'Internal Week 1', 'External Week 1', 'Week 2', 'Week 3', 'Week 4']
    y0 = [week1, week1I, week1E, week2, week3, week4]

    #y2 = [100, 200, 205, 204]
    title = 'Offers x week'

    plot2 = figure(
        title=title,
        x_axis_label='Week',
        x_range=x,
        y_axis_label='Offer amount',
        plot_width=950,
        plot_height=400)

    plot2.vbar(x, top=y, legend='Amount', width=0.9, color='#6FB543')

    script2, div2 = components(plot2)

    x3 = x8
    y3 = y8
    title = 'Internal / External Jobs'

    plot3 = figure(
        title=title,
        x_range=x3,
        plot_width=400,
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
    pr = df.loc[mask3].count()
    week3 = pr['Posting Date']

    # Cantidad de ofertas laborales por la semana 4.
    mask4 = (df['Posting Date'] >= '2018-10-21') & (df['Posting Date'] <= '2018-10-31')

    pr = df.loc[mask4].count()
    interno = pr['Posting Type']
    # print(interno)
    week4 = pr['Posting Date']

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
        plot_width=950,
        plot_height=400)

    plot.line(x, y, legend='Amount', line_width=2, color='#6FB543')
    plot.line(x, y, legend='Amount', line_width=2, color='#6FB543')
    script, div = components(plot)

    x = ['Week 1', 'Internal Week 1', 'External Week 1', 'Week 2', 'Internal Week 2', 'External Week 2', 'Week 3',
         'Week 4']
    y = [week1, week1I, week1E, week2, week2I, week2E, week3, week4]

    x0 = ['Week 1', 'Internal Week 1', 'External Week 1', 'Week 2', 'Week 3', 'Week 4']
    y0 = [week1, week1I, week1E, week2, week3, week4]

    # y2 = [100, 200, 205, 204]
    title = 'Offers x week'

    plot2 = figure(
        title=title,
        x_axis_label='Week',
        x_range=x,
        y_axis_label='Offer amount',
        plot_width=950,
        plot_height=400)

    plot2.vbar(x, top=y, legend='Amount', width=0.9, color='#6FB543')

    script2, div2 = components(plot2)

    x3 = x8
    y3 = y8
    title = 'Internal / External Jobs'

    plot3 = figure(
        title=title,
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
