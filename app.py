
from random import randint
import random
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import geojson
import requests
import json
import flask
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import time
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import pandas as pd 
import os
from datetime import date


dfDataKPI = pd.read_excel('Data.xlsx',sheet_name='DataKPI')
dfDataDiccionario = pd.read_excel('Data.xlsx',sheet_name='DiccionarioCampos')
empresas = dfDataKPI['nombreempresa'].unique().tolist()

style_head_empresa = {'color':'#fff','backgroundColor':'#235795','verticalAlign': 'middle','textAlign': 'left'}
page1InfoEmpresa1 = 'Reporte de la Autoevaluación del Ecosistema Digital'
page1InfoEmpresa2 = 'Este informe comprende los siguientes puntos: '
page1InfoEmpresa3 = '1. Caracterización de su empresa'
page1InfoEmpresa4 = 'Ilustra el perfil básico de su empresa y su referente con el segmento en el que usted se desempeña, en este caso las empresas de (Programación digital).'
page1InfoEmpresa5 = '2. Resultado de la Medición del Modelo de Madurez Digital y Colaborativa reportado por empresario.'
page1InfoEmpresa6 = 'En este informe se incluye una caracterización de su empresa y los resultados obtenidos con un desglose de la puntuación de cada uno de los atributos evaluados. Hemos realizado un análisis de su nivel actual de madurez digital para cada una de estas dimensiones. Para ayudarlo a mejorar, se llevó a cabo un análisis que le permitirá cerrar las brechas en su desarrollo digital. '

ref1 = '- Neilson, G., & Mcgrath, J. (2018). Strategy + Business: Digital Champions. PWC, Autumn 2018, July 26, 2018, 20.'
ref2 = '- Hansen, M., & Birkinshaw, J. (2007). La cadena de valor de la innovación. Harvard Business Review, 85(6), 100–110.'
ref3 = '- Westerman, G. (2020). The New Elements of Digital Transformation The New Elements of Digital Transformation. MIT Sloan Management Review, 62210, 10.'
ref4 = '- Sebastian, I. M., Weill, P., & Woerner, S. L. (2020). Driving Growth in Digital Ecosystems. MIT Sloan Management Review, 62(1), 58–62.'
ref5 = '- Manyika, J., Ramaswamy, S., Khanna, S., Sarrazin, H., Pinkus, G., Sethupathy, G., & Yaffe, A. (2017). Digital America Full Report December 2015. In Mckinsey & Company (Vol. 52, Issue 29, pp. 27–30).'
ref6 = '- Westerman, G., Bonnet, D., & McAfee, A. (2014). Leading Digital: Turning Technology into Business Transformation. Harvard Business Review Press.'
ref7 = '- Rivera, J. D., Barbosa, C. R., Mónica Lorena Ortiz Medina, Salinas, I. A. N., & Viña, M. C. P. (2019). Industria 4.0 Transformacion empresarial para la reactivacion economica. In Confecámaras.'
ref8 = '- Hansen, M. (2009). Collaboration: How Leaders Avoid the Traps, Build Common Ground, and Reap Big Results (unknown ed.). Harvard Business Review Press.'
ref9 = '- Gupta, R., Mejia, C., & Kajikawa, Y. (2019). Business, innovation and digital ecosystems landscape survey and knowledge cross sharing. Technological Forecasting and Social Change, 147(July), 100–109. https://doi.org/10.1016/j.techfore.2019.07.004'
ref10 = '- Corporación Internancional de Productividad (2021). Consolidando el Ecosistema de Innovación Digital del Valle del Cauca'






external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Setup the app
# Make sure not to change this file name or the variable names below,
# the template is configured to execute 'server' on 'app.py'
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Autoevaluación Ecosistema Digital e Innovación'
app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.Hr(),
        html.Div([
            dbc.Row([
                    dbc.Col(html.H5("Selecciona una empresa:")            
                    ),
                    dbc.Col(dcc.Dropdown(
                                id='dropdown',
                                options=[{'label': val, 'value': val} for val in empresas],
                                value=empresas[0])
                                
                    ),
                    dbc.Col(dbc.Button("Imprimir reporte", outline=True, color="primary")            
                    ),
            ])
        ]),
        html.Hr(),
        html.H5(page1InfoEmpresa1,style=style_head_empresa),
        html.H5("",id='nombre-empresa'),
        html.H5("",id='nombre-empresario'),
        html.H5("",id='fecha-reporte'),
        html.P(" "),
        html.P("",id='intro-empresa'),
        html.P(" "),
        html.P(page1InfoEmpresa2),
        html.P(" "),
        html.P(page1InfoEmpresa3,style={'fontWeight':'bold'}),
        html.P(page1InfoEmpresa4),
        html.P(" "),
        html.P(page1InfoEmpresa5,style={'fontWeight':'bold'}),
        html.P(page1InfoEmpresa6),
        html.Hr(),
        dbc.Tabs(
            [
                dbc.Tab(label="Perfil", tab_id="perfil-empresa"),
                dbc.Tab(label="Caracterización", tab_id="kpis"),
                dbc.Tab(label="Madurez digital", tab_id="madurez-digital"),
                dbc.Tab(label="Estrategia digital", tab_id="estrategia-digital"),
                dbc.Tab(label="Clientes", tab_id="clientes"),
                dbc.Tab(label="Talento Humano", tab_id="talento-humano"),
                dbc.Tab(label="Tecnologia", tab_id="tecnologia"),
                dbc.Tab(label="Operaciones", tab_id="operaciones"),
                dbc.Tab(label="Innovación digital", tab_id="innovacion-digital"),
                dbc.Tab(label="Colaboración interna", tab_id="colaboracion-interna"),
                dbc.Tab(label="Colaboración externa", tab_id="colaboracion-externa"),
                dbc.Tab(label="Capacidad de generación de empleo", tab_id="capacidad-generacion-empleo"),
            ],
            id="tabs",
            active_tab="perfil-empresa",
        ),
        html.Div(id="tab-content", className="p-4"),
        html.Hr(),
        html.Div(
            [
                dbc.Button(
                    "Referencias",
                    id="collapse-button",
                    className="mb-3",
                    color="primary",
                ),
                dbc.Collapse(
                    dbc.Col(
                        [
                            html.Div(ref1),
                            html.Div(ref2),
                            html.Div(ref3),
                            html.Div(ref4),
                            html.Div(ref5),
                            html.Div(ref6),
                            html.Div(ref7),
                            html.Div(ref8),
                            html.Div(ref9),
                            html.Div(ref10),
                            html.P(" ")
                        ]
                    ),
                    id="collapse",
                ),
            ]
        ),
        html.Div("© Corporación Internacional de Productividad - CIP - 2021"),
        html.Hr(),
    ]
)


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):
    if active_tab and data is not None:
        if active_tab == "perfil-empresa":
            return processPerfilEmpresa(data["perfilempresa"])
        elif active_tab == "kpis":
            return processKPIs(data["kpis"])
        elif active_tab == "madurez-digital":
            return processMadurezDigital(data["madurezdigital"])
        elif active_tab == "estrategia-digital":
            return processMadurezDigital(data["madurezdigital"])
        elif active_tab == "clientes":
            return processMadurezDigital(data["madurezdigital"])
        elif active_tab == "talento-humano":
            return processMadurezDigital(data["madurezdigital"])
        elif active_tab == "tecnologia":
            return processMadurezDigital(data["madurezdigital"])
        elif active_tab == "operaciones":
            return processMadurezDigital(data["madurezdigital"])
        elif active_tab == "innovacion-digital":
            return processMadurezDigital(data["madurezdigital"])
        elif active_tab == "colaboracion-interna":
            return processMadurezDigital(data["madurezdigital"])
        elif active_tab == "colaboracion-externa":
            return processMadurezDigital(data["madurezdigital"])
        elif active_tab == "capacidad-generacion-empleo":
            return processMadurezDigital(data["madurezdigital"])
    return "No tab selected"


@app.callback([Output("store", "data"), 
              Output("nombre-empresa", "children"), 
              Output("nombre-empresario", "children"),
              Output("fecha-reporte", "children"),
              Output("intro-empresa", "children")],
              [Input('dropdown', "value")])
def generate_graphs(name):
    """
    This callback generates three simple graphs from random data.
    """
    print(name,type(name))
    nombre_empresario = 'Andres Castillo'
    Segmento = 'Programación'
    intro_empresa = 'Señor empresario: gracias por completar la autoevaluación de su empresa realizada en el marco del Proyecto Ecosistema de Innovación Digital del Valle del Cauca. Como quedó establecido previamente, le estamos haciendo llegar el reporte de los resultados de la autoevaluación que usted muy gentilmente diligenció. Su empresa pertenece al segmento de empresas de '+Segmento+' dentro de la cadena de producción digital del Valle del Cauca. '
    today = date.today()
    fecha_reporte = today.strftime("%d/%m/%Y")
    
    if not name:
        # generate empty graphs when app loads
        return {k: go.Figure(data=[]) for k in ["kpis","perfilempresa", "hist_1", "hist_2"]}," "

    
    perfilempresa = getKPIPerfilEmpresa(dfDataKPI,name)
    kpis = getKPIs(dfDataKPI,name)
    madurezdigital = getKPIMadurezDigital(dfDataKPI,name)

    # simulate expensive graph generation process
    time.sleep(2)

    # generate 100 multivariate normal samples
    data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 100)

    hist_1 = go.Figure(data=[go.Histogram(x=data[:, 0])])
    hist_2 = go.Figure(data=[go.Histogram(x=data[:, 1])])

    # save figures in a dictionary for sending to the dcc.Store
    return {'madurezdigital':madurezdigital,"kpis":kpis,"perfilempresa":perfilempresa,"hist_1": hist_1, "hist_2": hist_2},name,nombre_empresario,fecha_reporte,intro_empresa,


##########################################################################################
## Perfil Empresa
def getKPIPerfilEmpresa(df,name):
    dfEmpresa = df[df['nombreempresa']==name]
    keys = ["AnoIncio","Segmento","ActividadDigital","Tamano","OfertaValor"]
    vals = [" "]*len(keys)
    perfilempresa = dict(zip(keys,vals))
    if len(dfEmpresa)>=1:
        perfilempresa["AnoIncio"] = str(dfEmpresa['creacionempresa'].values.tolist()[0])
        perfilempresa["Segmento"] = dfEmpresa['actividadprincipal'].values.tolist()[0]
        perfilempresa["ActividadDigital"] = dfEmpresa['actividaddigital'].values.tolist()[0]
    return perfilempresa
def processPerfilEmpresa(dataperfilempresa):
    style_table = {'color':'#fff','backgroundColor':'#235795','verticalAlign': 'middle','border': '2px solid #235795','textAlign': 'left'}
    data1 = dataperfilempresa["AnoIncio"]
    data2 = dataperfilempresa["Segmento"]
    data3 = "XXXX" 
    row1 = html.Tr([html.Td("Año de Creación",style=style_table), html.Td(data1)])
    row2 = html.Tr([html.Td("Segmento",style=style_table), html.Td(data2)])
    row3 = html.Tr([html.Td("Oferta de valor",style=style_table), html.Td(data3)])
    table_body1 = [html.Tbody([row1, row2, row3])]
    table1 = dbc.Table(table_body1, borderless=True)

    data1 = "100"
    data2 = dataperfilempresa["ActividadDigital"]
    data3 = "Ecosistema digital"

    row1 = html.Tr([html.Td("Tamaño",style=style_table), html.Td(data1)])
    row2 = html.Tr([html.Td("Actividad Digital de la empresa",style=style_table), html.Td(data2)])
    row3 = html.Tr([html.Td("Enfoque de la oferta de valor",style=style_table), html.Td(data3)])
    table_body2 = [html.Tbody([row1, row2, row3])]
    table2 = dbc.Table(table_body2, borderless=True)

    row = html.Div(
        [
            dbc.Row(dbc.Col(html.P(" "))),
            dbc.Row(dbc.Col(html.H5("Perfil de la empresa",style={'font-weight': 'bold'}))),
            dbc.Row(
                [
                    dbc.Col(table1),
                    dbc.Col(table2),
                ]
            ),
            #dbc.Row(dbc.Col(html.P(" "))),
            #dbc.Row(dbc.Col(html.H5("Cadena de productividad", style={'font-weight': 'bold'}))),
            #dbc.Row(dbc.Col(html.Img(src=app.get_asset_url('cadenaproductividad.png')))),
        ]
    )

    return row
##########################################################################################


##########################################################################################
## Caracterizacion
def getKPIs(df,name):
    dfEmpresa = df[df['nombreempresa']==name]
    KPIs = dict()

    keys = ["Permanentes","Temporales","Independientes"]
    vals = [" "]*len(keys)
    dfEmpresaEmpleados = dfEmpresa[["empleados_numpermanentes","empleados_numtemporales","empleados_numindep"]]
    dfEmpresaEmpleados.fillna(0,inplace=True)
    vals = dfEmpresaEmpleados[["empleados_numpermanentes","empleados_numtemporales","empleados_numindep"]].values.tolist()[0]
    KPIs['Empleados'] = dict(zip(keys,vals))

    keys = ["Tecnicos","Profesionales","Especializacion","Maestría", "Doctorado",'Otra']
    vals = [" "]*len(keys)
    dfEmpresaEmpleados = dfEmpresa[['formacion_tecnicos','formacion_profesionales','formacion_especializados','formacion_maestria','formacion_doctorado','formacion_otros']]
    dfEmpresaEmpleados.fillna(0,inplace=True)
    vals = dfEmpresaEmpleados[['formacion_tecnicos','formacion_profesionales','formacion_especializados','formacion_maestria','formacion_doctorado','formacion_otros']].values.tolist()[0]
    KPIs['Formacion'] = dict(zip(keys,vals))

    return KPIs
def processKPIs(datakpis):

    labels1 = list(datakpis['Empleados'].keys())
    values1 = list(datakpis['Empleados'].values())
    labels2 = list(datakpis['Formacion'].keys())
    values2 = list(datakpis['Formacion'].values())
    labels3 = ['Internet de las cosas','Robótica y automatización','Impresión 3D',
               'Realidad aumentada y virtual','Inteligencia artificial - IA','Big Data y Analítica avanzada',
               'Blockchain','Computación en la nube','Seguridad de la información -…',
               'Gemelos digitales','Comercio Electrónico, Ecommerce','Plataforma de negocio digital',
               'Diseño y animación digital','Georeferenciación','Fintech']
    values3 = [val % 6 for val in range(len(labels3))]
    labels5 = ['Nivel 1. Principios básicos observados y…',
               'Nivel 2. Definición del concepto tecnológico y su…',
               'Nivel 3. Prueba analítica y experimental del…',
               'Nivel 4. Sistema final probado en entornos…',
               'Nivel 5. Sistema real completo y calificado',
               'Nivel 6. Demostración de prototipos del sistema…',
               'Nivel 7. Tecnología demostrada en un ambiente…',
               'Nivel 8. Validación de componentes y/o la…',
               'Nivel 9. Tecnología validada en el laboratorio']
    values5 = [val % 6 for val in range(len(labels5))]

    labels7 = ['Prototipos','Nuevo desarrollo de software','Nuevos productos no patentables','Patentes de invención']
    values7 = [4, 6, 7, 1]

    
    fig1 = go.Figure(data=[go.Pie(labels=labels1, values=values1, hole=.3)])
    fig2 = go.Figure(data=[go.Pie(labels=labels2, values=values2, hole=.3)])
    fig3 = go.Figure(go.Bar(x=values3,y=labels3,orientation='h'))
    fig5 = go.Figure(go.Bar(x=values5,y=labels5,orientation='h'))
    fig7 = go.Figure(data=[go.Pie(labels=labels7, values=values7, hole=.3)])
    fig1.update_layout(title='Tipos de Empleados')
    fig2.update_layout(title='Formación')
    fig3.update_layout(title='Competencias Digitales')
    fig5.update_layout(title='Número de proyectos por nivel')
    fig7.update_layout(title='Total Procesos: '+str(sum(values7)))

    style_table = {'backgroundColor':'#c5d9f1','verticalAlign': 'middle','border': '2px solid #c5d9f1','textAlign': 'center'}
    row1 = html.Tr([html.Td("Número de Clientes de la empresa 2020"), html.Td("15",style=style_table)])
    row2 = html.Tr([html.Td("Sectores a los que vende"), html.Td("Servicios profesionales Finanzas y seguros, Actividad inmobiliaria, Logística, Educación, Gobierno, Salud, Hostelería y turismo",style=style_table)])
    row3 = html.Tr([html.Td("Desarrollo de productos exclusivos para clientes ("+chr(37)+')'), html.Td("70 "+chr(37),style=style_table)])
    row4 = html.Tr([html.Td("Desarrollo de productos digitales propios y los ofrezco en el mercado ("+chr(37)+')'), html.Td("30 "+chr(37),style=style_table)])
    row5 = html.Tr([html.Td("Porcentaje de ventas aplicada a capacitación y desarrollo"), html.Td("10 "+chr(37),style=style_table)])
    table_body = [html.Tbody([row1, row2, row3, row4, row5])]
    fig4 = dbc.Table(table_body,borderless=True)
    fig6 = dbc.Table(table_body,borderless=True)
    

    row = html.Div(
        [
            dbc.Row(dbc.Col(html.P(" "))),
            dbc.Row(dbc.Col(html.H5("Talento Humano",style={'font-weight': 'bold'}))),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=fig1)),
                    dbc.Col(dcc.Graph(figure=fig2)),
                    dbc.Col(dcc.Graph(figure=fig3)),
                ]
            ),
            dbc.Row(dbc.Col(html.P(" "))),
            dbc.Row(
                [
                    dbc.Col(html.H5("Demanda",style={'font-weight': 'bold'})),
                    dbc.Col(html.H5("Portafolio de iniciativas o ideas y proyectos digitales",style={'font-weight': 'bold'})),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(fig4),
                    dbc.Col(dcc.Graph(figure=fig5)),
                ]
            ),
            dbc.Row(dbc.Col(html.P(" "))),
            dbc.Row(
                [
                    dbc.Col(html.H5("Innovación",style={'font-weight': 'bold'})),
                    dbc.Col(html.H5("Propiedad Intelectual",style={'font-weight': 'bold'})),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(fig6),
                    dbc.Col(dcc.Graph(figure=fig7)),
                ]
            ),
        ]
    )
    return row
##########################################################################################

##########################################################################################
## Madurez Digital
def getKPIMadurezDigital(df,name):
    dfEmpresa = df[df['nombreempresa']==name]
    keys = ["AnoIncio","Segmento","ActividadDigital","Tamano","OfertaValor"]
    vals = [" "]*len(keys)
    madurezdigital = dict(zip(keys,vals))
    if len(dfEmpresa)>=1:
        madurezdigital["AnoIncio"] = str(dfEmpresa['creacionempresa'].values.tolist()[0])
        madurezdigital["Segmento"] = dfEmpresa['actividadprincipal'].values.tolist()[0]
        madurezdigital["ActividadDigital"] = dfEmpresa['actividaddigital'].values.tolist()[0]
    madurezdigital['name']=name
    return madurezdigital    
def processMadurezDigital(datamadurezdigital):
    title = 'Nivel de Madurez del Ecosistema de Innovación Digital'
    labels = ['Clientes','Colaboración interna','Estrategia','Operaciones','Colaboración externa','Innovación Digital','Tecnología', 'Talento Humano']
    values = [4,2,5,1,4,2,4,5]
    meanval = sum(values)/len(values)
    figBar = go.Figure()

    figBar.add_trace(go.Bar(x=values,y=labels, text=values, textposition='auto',orientation='h'))
    figBar.add_trace(go.Scatter(
        x=[meanval],
        y=[-1],
        text=[" "],
        mode="text",
    ))
    figBar.add_trace(go.Scatter(
        x=[meanval],
        y=[-2],
        text=["Promedio: "+str(meanval)[:3]],
        mode="text",
    ))
    figBar.add_trace(go.Scatter(
        x=[0.5, 1.5, 2.5, 3.5, 4.5],
        y=[-3,-3,-3,-3,-3],
        text=[" ",
              " ",
              " ",
              " ",
              " "],
        mode="text",
    ))
    figBar.add_trace(go.Scatter(
        x=[0.5, 1.5, 2.5, 3.5, 4.5],
        y=[-4,-4,-4,-4,-4],
        text=["Principiante",
              "Experimentador",
              "Conservador",
              "Prometedor",
              "Líder de Ecos. Digital"],
        mode="text",
    ))
    figBar.add_trace(go.Scatter(
        x=[0.5, 1.5, 2.5, 3.5, 4.5],
        y=[-5,-5,-5,-5,-5],
        text=["Nivel 1",
              "Nivel 2",
              "Nivel 3",
              "Nivel 4",
              "Nivel 5"],
        mode="text",
    )) 
    

    if meanval > 0.5 and meanval < 4.5:
        figBar.update_xaxes(range=[0, 5])
    if meanval <= 0.5:
        figBar.update_xaxes(range=[-0.5, 5])
    if meanval >= 4.5:
        figBar.update_xaxes(range=[0, 5.5])
    
    # Add shapes
    p1 = str(meanval) +' '+ str(len(values)+0.25) 
    p2 = str(meanval+0.25) +' '+ str(len(values)-0.25)
    p3 = str(meanval) +' '+ str(len(values)-0.75) 
    p4 = str(meanval-0.25) +' '+ str(len(values)-0.25)
    po = str(meanval) +' '+ str(len(values)-0.75) 
    pf = str(meanval) +' -1' 
    figBar.update_layout(
        yaxis = dict(
            tickmode = 'array',
            tickvals = list(range(1+len(labels))),
            ticktext = labels+[' ']
        ),
        title=title,
        title_x=0.5,
        showlegend=False,
        shapes=[
            # filled Triangle
            dict(
                type="path",
                path=" M "+p1+" L "+p2+" L "+p3+" L "+p4+" Z",
                fillcolor="LightPink",
                line_color="Crimson",
                opacity=0.8
            ),
            # filled Line
            dict(
                type="path",
                path=" M "+po+" L "+pf+" Z",
                fillcolor="LightPink",
                line_color="Crimson",
            )
        ]
    )



    figCuadrante = go.Figure()

    centerx = 4
    centery = 2
    textEstrategia = '('+str(centerx)[:3]+', '+str(centery)[:3]+')'

    # Create scatter trace of text labels
    figCuadrante.add_trace(go.Scatter(
        x=[0.4, 2.9, 0.5, 2.9, 0.25,  4.7, centerx],
        y=[2,  2,  4.5,  4.5,  0.2,  4.5, centery-0.3],
        text=["PRINCIPIANTE", "CONSERVADOR", "EXPERIMENTADOR","PROMETEDOR","NOVATO","LIDER", textEstrategia],
        mode="text",
        textfont=dict(
            color="black",
            size=18,
            family="Arail",
        )
    ))

    # Update axes properties
    figCuadrante.update_xaxes(
        title_text='Estrategia Digital',
        showticklabels=False,
        showgrid=False,
        zeroline=False,
    )

    figCuadrante.update_yaxes(
        title_text='Capacidad Tecnológica',
        showticklabels=False,
        showgrid=False,
        zeroline=False,
    )

    # Add rects
    # Add a shape whose x and y coordinates refer to the domains of the x and y axes
    figCuadrante.add_shape(type="rect",
        xref="x", yref="y",
        x0=0.0, x1=5, y0=0, y1=5,
    )
    figCuadrante.add_shape(type="rect",
        xref="x", yref="y",
        x0=0.0, x1=2.5, y0=0, y1=2.5,
        line=dict(
            color="Red",
            width=3,
        ),
        fillcolor="Red"
    )
    figCuadrante.add_shape(type="rect",
        xref="x", yref="y",
        x0=2.5, x1=5, y0=0, y1=2.5,
        line=dict(
            color="Yellow",
            width=3,
        ),
        fillcolor="Yellow"
    )
    figCuadrante.add_shape(type="rect",
        xref="x", yref="y",
        x0=0.0, x1=2.5, y0=2.5, y1=5,
        line=dict(
            color="Green",
            width=3,
        ),
        fillcolor="Green"
    )
    figCuadrante.add_shape(type="rect",
        xref="x", yref="y",
        x0=2.5, x1=5, y0=2.5, y1=5,
        line=dict(
            color="LightSeaGreen",
            width=3,
        ),
        fillcolor="PaleTurquoise"
    )

    figCuadrante.add_shape(type="rect",
        xref="x", yref="y",
        x0=0, x1=1, y0=0, y1=1,
        line=dict(
            color="Red",
            width=3,
        ),
        fillcolor="Red"
    )
    figCuadrante.add_shape(type="rect",
        xref="x", yref="y",
        x0=4, x1=5, y0=4, y1=5,
        line=dict(
            color="Blue",
            width=3,
        ),
        fillcolor="Blue"
    )
    

    figCuadrante.add_shape(type="circle",
        xref="x", yref="y",
        fillcolor="Black",
        x0=centerx-0.03, y0=centery-0.1, x1=centerx+0.03, y1=centery+0.1,
        line_color="Black",
    )

    figCuadrante.update_shapes(opacity=0.4, xref="x", yref="y")

    figCuadrante.update_layout(
        title=title,
        title_x=0.5,
        #margin=dict(l=20, r=20, b=100),
        #height=600, width=800,
        plot_bgcolor="white"
    )

    row = html.Div(
        [
            dbc.Row(dbc.Col(dcc.Graph(figure=figBar))),
            dbc.Row(dbc.Col(dcc.Graph(figure=figCuadrante))),
            dbc.Row(
                [
                    dbc.Col(html.Div(" ")),
                    dbc.Col(html.Div(" ")),
                    dbc.Col(html.Div(" ")),
                ]
            ),
        ]
    )
    return row

if __name__ == '__main__':
    app.server.run(host='0.0.0.0', port=8000, debug=True, threaded=True)



