from datetime import datetime as dt
import os
import flask
from flask import Flask, send_from_directory
import xlsxwriter
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import io
import pandas as pd
import plotly.graph_objs as go
import model
# import temp_with_postgre
import openpyxl


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://codepen.io/chriddyp/pen/brPBPO.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
external_stylesheets=[dbc.themes.BOOTSTRAP]

sizes = {
    'container-div': '800px',
}


server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=external_stylesheets)



app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})

app.title = ('Indices')



controls = dbc.Card(
    [
        html.Div([
            html.H3('Выберите параметры времени', style={'text-align': 'center'}),
        ]),

        html.Div([
            html.H5('Даты', style={'text-align': 'center'}),
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=dt(2015, 1, 1),
                max_date_allowed=dt(2016, 1, 1),
                initial_visible_month=dt(2015, 2, 10),
                # end_date=dt(2015, 3, 17),
                # start_date=dt(2015, 2, 1),
                start_date_placeholder_text="Start Period",
                end_date_placeholder_text="End Period",
            ),
        ], style={'text-align': 'center'}),

        html.H5('Время', style={'text-align': 'center'}),

        html.Div([
            html.Div([
                # html.Label('начальное время', style = {'text-align': 'center'}),
                dcc.Dropdown(
                    id='start_time',
                    options=[
                        {'label': '00:00', 'value': '00:00'},
                        {'label': '01:00', 'value': '01:00'},
                        {'label': '02:00', 'value': '02:00'},
                        {'label': '03:00', 'value': '03:00'},
                        {'label': '04:00', 'value': '04:00'},
                        {'label': '05:00', 'value': '05:00'},
                        {'label': '06:00', 'value': '06:00'},
                        {'label': '07:00', 'value': '07:00'},
                        {'label': '08:00', 'value': '08:00'},
                        {'label': '09:00', 'value': '09:00'},
                        {'label': '10:00', 'value': '10:00'},
                        {'label': '11:00', 'value': '11:00'},
                        {'label': '12:00', 'value': '12:00'},
                        {'label': '13:00', 'value': '13:00'},
                        {'label': '14:00', 'value': '14:00'},
                        {'label': '15:00', 'value': '15:00'},
                        {'label': '16:00', 'value': '16:00'},
                        {'label': '17:00', 'value': '17:00'},
                        {'label': '18:00', 'value': '18:00'},
                        {'label': '19:00', 'value': '19:00'},
                        {'label': '20:00', 'value': '20:00'},
                        {'label': '21:00', 'value': '21:00'},
                        {'label': '22:00', 'value': '22:00'},
                        {'label': '23:00', 'value': '23:00'},
                    ],
                    value='00:00'
                ),
            ], style={'margin': '0 10px 0 10px', 'width': '100px'}),

            html.Div([
                # html.Label('конечное время', style = {'text-align': 'center'}),
                dcc.Dropdown(
                    id='end_time',
                    options=[
                        {'label': '00:00', 'value': '00:00'},
                        {'label': '01:00', 'value': '01:00'},
                        {'label': '02:00', 'value': '02:00'},
                        {'label': '03:00', 'value': '03:00'},
                        {'label': '04:00', 'value': '04:00'},
                        {'label': '05:00', 'value': '05:00'},
                        {'label': '06:00', 'value': '06:00'},
                        {'label': '07:00', 'value': '07:00'},
                        {'label': '08:00', 'value': '08:00'},
                        {'label': '09:00', 'value': '09:00'},
                        {'label': '10:00', 'value': '10:00'},
                        {'label': '11:00', 'value': '11:00'},
                        {'label': '12:00', 'value': '12:00'},
                        {'label': '13:00', 'value': '13:00'},
                        {'label': '14:00', 'value': '14:00'},
                        {'label': '15:00', 'value': '15:00'},
                        {'label': '16:00', 'value': '16:00'},
                        {'label': '17:00', 'value': '17:00'},
                        {'label': '18:00', 'value': '18:00'},
                        {'label': '19:00', 'value': '19:00'},
                        {'label': '20:00', 'value': '20:00'},
                        {'label': '21:00', 'value': '21:00'},
                        {'label': '22:00', 'value': '22:00'},
                        {'label': '23:00', 'value': '23:00'},
                    ],
                    value='00:00'
                ),
            ], style={'margin': '0 10px 0 10px', 'width': '100px'}),
        ],
            style={
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center',
            }),

        html.Div([
            html.H5('Шаг', style={'text-align': 'center'}),
            dcc.Dropdown(
                id='time_step',
                options=[
                    {'label': '10 sec', 'value': '10S', 'disabled': True},
                    {'label': '1 min', 'value': '60S', 'disabled': True},
                    {'label': '5 min', 'value': '300S', 'disabled': True},
                    {'label': '10 min', 'value': '600S', 'disabled': True},
                    {'label': '15 min', 'value': '900S', 'disabled': True},
                    {'label': '30 min', 'value': '1800S', 'disabled': True},
                    {'label': '1 h', 'value': '1H'},
                    {'label': '2 h', 'value': '2H'},
                    {'label': '6 h', 'value': '6H'},
                    {'label': '12 h', 'value': '12H'},
                    {'label': '1 day', 'value': '1D'},
                ],
                value='1H'
            ),
        ], style={'margin': 'auto', 'width': '100px'}
        ),

        html.Div([
            html.H3('Выберите параметры поля', style={'text-align': 'center', 'margin-bottom': '6px'}),
            html.Button('выбрать всё', id='choose_all',
                        style={'display': 'inline-block',
                               'background-color': 'white',
                               'color': 'gray',
                               'font-weight': '500',
                               'font-size': '10px',
                               'padding': '0 2px'}),
        ], style={'text-align': 'center'}),

        html.Div([
            html.Div([
                dcc.Checklist(
                    # name ='checkbox_1',
                    id='checkbox_1',
                    inputClassName='checkbox_1',
                    options=[
                        {'label': 'AE', 'value': 'ae'},
                        {'label': 'AU', 'value': 'au'},
                        {'label': 'AL', 'value': 'al'},
                        {'label': 'AO', 'value': 'ao'},
                    ],
                    value=[]
                ),
            ], style={'padding': '0 15px'}),
            html.Div([
                dcc.Checklist(
                    # name='checkbox_1',
                    id='checkbox_2',
                    inputClassName='checkbox_2',
                    options=[
                        {'label': 'PCN', 'value': 'pcn'},
                        {'label': 'PCS', 'value': 'pcs'},
                    ],
                    value=[]
                ),
            ], style={'padding': '0 15px'}),
            html.Div([
                dcc.Checklist(
                    # name='checkbox_1',
                    id='checkbox_3',
                    inputClassName='checkbox_3',
                    options=[
                        {'label': 'SME', 'value': 'sme'},
                    ],
                    value=[]
                ),
            ], style={'padding': '0 15px'}),
            html.Div([
                dcc.Checklist(
                    # name='checkbox_1',
                    id='checkbox_4',
                    inputClassName='checkbox_4',
                    options=[
                        {'label': 'ASY-D', 'value': 'asy_d'},
                        {'label': 'ASY-H', 'value': 'asy_h'},
                        {'label': 'SYM-D', 'value': 'sym_d'},
                        {'label': 'SYM-H', 'value': 'sym_h'},
                    ],
                    value=[]
                ),
            ], style={'padding': '0 15px'}),
            html.Div([
                dcc.Checklist(
                    # name='checkbox_1',
                    id='checkbox_5',
                    inputClassName='checkbox_5',
                    options=[
                        {'label': 'AL (ie)', 'value': 'al_ie'},
                        {'label': 'AU (ie)', 'value': 'au_ie'},
                        {'label': 'AE (ie)', 'value': 'ae_ie'},
                    ],
                    value=[]
                ),
            ], style={'padding': '0 15px'}),
            html.Div([
                dcc.Checklist(
                    # name='checkbox_1',
                    id='checkbox_6',
                    inputClassName='checkbox_6',
                    options=[
                        {'label': 'Middle Latitude A', 'value': 'middle_latitude_a'},
                        {'label': 'Middle Latitude K-indices', 'value': 'middle_latitude_k_indices'},
                        {'label': 'High Latitude A', 'value': 'high_latitude_a'},
                        {'label': 'High Latitude K-indices', 'value': 'high_latitude_k_indices'},
                        {'label': 'Estimated A', 'value': 'estimated_a'},
                        {'label': 'Estimated K-indices', 'value': 'estimated_k_indices'},
                    ],
                    value=[]
                ),
            ], style={'padding': '0 15px'}),
        ], style={'padding': '15px 0 0 30px', 'display': 'flex', 'justify-content': 'center'}),

        html.Div([
            html.Button('OK', id='main_button',
                        style={'margin': 'auto',
                               'display': 'inline-block',
                               'background-color': 'green',
                               'color': 'white',
                               'font-weight': '700',
                               'font-size': '20px'}),
        ], style={'text-align': 'center', 'margin-top': '15px'}),

        html.Div(id='output_div', style={'text-align': 'center', 'margin-top': '5px'}),
        html.Div(id='output_div2', style={'text-align': 'center', 'margin-top': '10px'},
                 children=[html.A(
                     'Download Data',
                     id='download-link',
                     download="data.xlsx",
                     href="#",
                     target="_blank"
                 )]
                 ),
    ],
    body=True,
)



app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(controls, md=6),
                dbc.Col(dcc.Graph(id="cluster-graph"), md=6),
            ],
            align="center",
        ),

        html.Div([
            html.H1(children = 'Индексы геомагнитной активности', style = {'margin-bottom': '10px'}),
        ], style = {'text-align': 'center'}),


    ],
    style={
        'padding': '20px 0 0 0',
        'width': sizes['container-div'],
        'margin': 'auto'
    }
)

# функция для наполнения БД
# @app.callback(
#     [Output('state_filling_db', 'children')],
#     [Input('button_fill_month_to_db', 'n_clicks')],
#     [State('month_id', 'value')]
# )
# def choose_all(n_clicks, month):
#     if n_clicks is None:
#         text = ['0']
#     else:
#         temp_with_postgre.mainFunction(month)
#         text = [str(month) + ' месяц заполнен']
#     return text


# функция для выбора всех индексов
@app.callback(
    [Output("checkbox_1", "value"),
     Output("checkbox_2", "value"),
     Output("checkbox_3", "value"),
     Output("checkbox_4", "value"),
     Output("checkbox_5", "value"),
     Output("checkbox_6", "value"),],
    [Input(component_id='choose_all', component_property='n_clicks')],
)
def choose_all(n_clicks):
    if n_clicks is None or n_clicks%2 == 0:
        cb1_val = []
        cb2_val = []
        cb3_val = []
        cb4_val = []
        cb5_val = []
        cb6_val = []
        return cb1_val, cb2_val, cb3_val, cb4_val, cb5_val, cb6_val
    else:
        cb1_val = ['ae','au','al','ao']
        cb2_val = ['pcn', 'pcs']
        cb3_val = ['sme']
        cb4_val = ['asy_d', 'asy_h', 'sym_d', 'sym_h']
        cb5_val = ['al_ie', 'au_ie', 'ae_ie']
        cb6_val = ['middle_latitude_a', 'middle_latitude_k_indices', 'high_latitude_a', 'high_latitude_k_indices', 'estimated_a', 'estimated_k_indices']
        return cb1_val, cb2_val, cb3_val, cb4_val, cb5_val, cb6_val









# функция для графика
@app.callback(
    [Output("cluster-graph", "figure")],
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('start_time', 'value'),
     Input('end_time', 'value'),
     Input('time_step', 'value'),
     Input('checkbox_1', 'value'),
     Input('checkbox_2', 'value'),
     Input('checkbox_3', 'value'),
     Input('checkbox_4', 'value'),
     Input('checkbox_5', 'value'),
     Input('checkbox_6', 'value')
     ],
)
def update_output(date_begin, date_end, time_begin, time_end, time_step,
                  sought_info_1, sought_info_2, sought_info_3, sought_info_4, sought_info_5, sought_info_6):
    sought_info = sought_info_1 + sought_info_2 + sought_info_3 + sought_info_4 + sought_info_5 + sought_info_6

    if date_begin is not None or date_end is not None:
        if time_step is not None:
            if len(sought_info) > 0:
                try:
                    df = model.mainFunction(str(date_begin), str(time_begin)+':00', str(date_end), str(time_end)+':00', str(time_step), sought_info)

                    data = []
                    for i in sought_info:
                        trace = go.Scatter(x=df.datetime.tolist(),
                                           y=df.i.tolist(),
                                           name=i)
                        data.append(trace)

                    # data = [
                    #     {
                    #         "x": df.index,
                    #         "y": df["ae"],
                    #         "name": "ae",
                    #         "type": "line",
                    #         "marker": {"color": "#00ff00"},
                    #     },
                    #     {
                    #         "x": df.index,
                    #         "y": df["au"],
                    #         "name": "au",
                    #         "type": "line",
                    #         "marker": {"color": "#ff0000"},
                    #     },
                    # ]
                    layout = go.Layout(xaxis={'title': 'Time'},
                                       yaxis={'title': 'Produced Units'},
                                       margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                                       hovermode='closest')

                    # layout = {"xaxis": {"title": 'time'}, "yaxis": {"title": 'y'}}
                    return go.Figure(data=data, layout=layout)
                except MemoryError:
                    return 0







# функция для передачи параметров запроса в model
@app.callback(
    [Output("output_div", "children"),
     Output("download-link", "href"),],
    [Input(component_id='main_button', component_property='n_clicks')],
    [State('my-date-picker-range', 'start_date'),
     State('my-date-picker-range', 'end_date'),
     State('start_time', 'value'),
     State('end_time', 'value'),
     State('time_step', 'value'),
     State('checkbox_1', 'value'),
     State('checkbox_2', 'value'),
     State('checkbox_3', 'value'),
     State('checkbox_4', 'value'),
     State('checkbox_5', 'value'),
     State('checkbox_6', 'value')]
)
def update_output(n_clicks, date_begin, date_end, time_begin, time_end, time_step,
                  sought_info_1, sought_info_2, sought_info_3, sought_info_4, sought_info_5, sought_info_6):
    sought_info = sought_info_1 + sought_info_2 + sought_info_3 + sought_info_4 + sought_info_5 + sought_info_6

    if n_clicks is None:
        raise PreventUpdate
    else:
        if date_begin is None or date_end is None:
            return 'Не введены даты!', '#'
        elif time_begin is None or time_end is None:
            return 'Не введены диапазоны времени!', '#'
        elif time_step is None:
            return 'Не введен шаг времени!', '#'
        elif len(sought_info) == 0:
            return 'Не выбраны параметры поля!', '#'
        else:
            try:
                b = model.mainFunction(str(date_begin), str(time_begin)+':00', str(date_end), str(time_end)+':00', str(time_step), sought_info)

                relative_filename = os.path.join(
                    'created_csv',
                    'file.xlsx'
                )
                absolute_filename = os.path.join(os.getcwd(), relative_filename)
                writer = pd.ExcelWriter(absolute_filename)
                b.to_excel(writer, 'Sheet1')
                writer.save()

                return '', '/{}'.format(relative_filename)
            except MemoryError:
                return 'Недостаточно памяти. Попробуйте выбрать меньший диапазон времени', '#'



@app.server.route('/created_csv/<path:path>')
def my_serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(
        os.path.join(root_dir, 'created_csv'), path
    )


if __name__ == '__main__':
    app.run_server(debug=True)