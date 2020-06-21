from datetime import datetime as dt
import os
import flask
from flask import Flask, send_from_directory
import xlsxwriter
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import io
import pandas as pd
import model
import openpyxl


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://codepen.io/chriddyp/pen/brPBPO.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


sizes = {
    'container-div': '800px',
}


server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=external_stylesheets)


app.layout = html.Div(
    [
        html.Div([
            dcc.Dropdown(
                id='month_id',
                options=[
                    {'label': '1', 'value': 1},
                    {'label': '2', 'value': 2},
                    {'label': '3', 'value': 3},
                    {'label': '4', 'value': 4},
                    {'label': '5', 'value': 5},
                    {'label': '6', 'value': 6},
                    {'label': '7', 'value': 7},
                    {'label': '8', 'value': 8},
                    {'label': '9', 'value': 9},
                    {'label': '10', 'value': 10},
                    {'label': '11', 'value': 11},
                    {'label': '12', 'value': 12},
                ],
                value=1
            ),
        ], style = {'margin': '0 10px 0 10px', 'width': '100px'}),
        html.Div([
            html.Button('Fill month to DB', id='button_fill_month_to_db',
                        style={'font-weight': '700', 'font-size': '10px'}),
        ], style={'text-align': 'center', 'margin-top': '5px'}),
        html.Div([
            html.H5(id = 'state_filling_db', children = '0', style={'text-align': 'center'}),
        ]),


        html.Div([
            html.H1(children = 'Параметры магнитного поля Земли', style = {'margin-bottom': '10px'}),
        ], style = {'text-align': 'center'}),

        html.Div([
            html.H3('Выберите параметры времени', style = {'text-align': 'center'}),
        ]),

        html.Div([
            html.H5('Даты', style = {'text-align': 'center'}),
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
        ], style = {'text-align': 'center'}),

        html.H5('Время', style = {'text-align': 'center'}),

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
            ], style = {'margin': '0 10px 0 10px', 'width': '100px'}),

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
            ], style = {'margin': '0 10px 0 10px', 'width': '100px'}),
        ],
        style = {
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'center',
        }),


        html.Div([
            html.H5('Шаг', style = {'text-align': 'center'}),
            dcc.Dropdown(
                id='time_step',
                options=[
                    {'label': '10 sec', 'value': '10S'},
                    {'label': '1 min', 'value': '60S'},
                    {'label': '5 min', 'value': '300S'},
                    {'label': '10 min', 'value': '600S'},
                    {'label': '15 min', 'value': '900S'},
                    {'label': '30 min', 'value': '1800S'},
                    {'label': '1 h', 'value': '1H'},
                    {'label': '2 h', 'value': '2H'},
                    {'label': '6 h', 'value': '6H'},
                    {'label': '12 h', 'value': '12H'},
                    {'label': '1 day', 'value': '1D'},
                ],
                value='900S'
            ),
            ], style = {'margin': 'auto', 'width': '100px'}
        ),

        html.Div([
            html.H3('Выберите параметры поля', style = {'text-align': 'center', 'margin-bottom': '6px'}),
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
                    inputClassName ='checkbox_1',
                    options=[
                        {'label': 'AE', 'value': 'AE'},
                        {'label': 'AU', 'value': 'AU'},
                        {'label': 'AL', 'value': 'AL'},
                        {'label': 'AO', 'value': 'AO'},
                    ],
                    value=[]
                ),
            ], style = {'padding': '0 15px'}),
            html.Div([
                dcc.Checklist(
                    # name='checkbox_1',
                    id='checkbox_2',
                    inputClassName='checkbox_2',
                    options=[
                        {'label': 'PCN', 'value': 'PCN'},
                        {'label': 'PCS', 'value': 'PCS'},
                    ],
                    value=[]
                ),
            ], style = {'padding': '0 15px'}),
            html.Div([
                dcc.Checklist(
                    # name='checkbox_1',
                    id='checkbox_3',
                    inputClassName='checkbox_3',
                    options=[
                        {'label': 'SME', 'value': 'SME'},
                    ],
                    value=[]
                ),
            ], style = {'padding': '0 15px'}),
            html.Div([
                dcc.Checklist(
                    # name='checkbox_1',
                    id='checkbox_4',
                    inputClassName='checkbox_4',
                    options=[
                        {'label': 'ASY-D', 'value': 'ASY-D'},
                        {'label': 'ASY-H', 'value': 'ASY-H'},
                        {'label': 'SYM-D', 'value': 'SYM-D'},
                        {'label': 'SYM-H', 'value': 'SYM-H'},
                    ],
                    value=[]
                ),
            ], style = {'padding': '0 15px'}),
            html.Div([
                dcc.Checklist(
                    # name='checkbox_1',
                    id='checkbox_5',
                    inputClassName='checkbox_5',
                    options=[
                        {'label': 'AL-ie', 'value': 'AL-ie'},
                        {'label': 'AU-ie', 'value': 'AU-ie'},
                        {'label': 'AE-ie', 'value': 'AE-ie'},
                    ],
                    value=[]
                ),
            ], style = {'padding': '0 15px'}),
            html.Div([
                dcc.Checklist(
                    # name='checkbox_1',
                    id='checkbox_6',
                    inputClassName='checkbox_6',
                    options=[
                        {'label': 'Middle Latitude A', 'value': 'Middle Latitude A'},
                        {'label': 'Middle Latitude K-indices', 'value': 'Middle Latitude K-indices'},
                        {'label': 'High Latitude A', 'value': 'High Latitude A'},
                        {'label': 'High Latitude K-indices', 'value': 'High Latitude K-indices'},
                        {'label': 'Estimated A', 'value': 'Estimated A'},
                        {'label': 'Estimated K-indices', 'value': 'Estimated K-indices'},
                    ],
                    value=[]
                ),
            ], style = {'padding': '0 15px'}),
        ], style = {'padding': '15px 0 0 30px','display':'flex', 'justify-content': 'center'}),

        html.Div([
            html.Button('OK', id='main_button',
                        style={'margin': 'auto',
                               'display': 'inline-block',
                               'background-color': 'green',
                               'color': 'white',
                               'font-weight':'700',
                               'font-size': '20px'}),
        ], style={'text-align':'center', 'margin-top': '15px'}),

        html.Div(id='output_div', style={'text-align':'center', 'margin-top': '5px'}),
        html.Div(id='output_div2', style={'text-align':'center', 'margin-top': '10px'},
                 children=[html.A(
                    'Download Data',
                    id='download-link',
                    download="data.xlsx",
                    href="#",
                    target="_blank"
                 )]
        ),

    ],
    style={
        'padding': '20px 0 0 0',
        'width': sizes['container-div'],
        'margin': 'auto'
    }
)







@app.callback(
    [Output("state_filling_db", "children")],
    [Input(component_id='button_fill_month_to_db', component_property='n_clicks')],
    [State('month_id', 'value')]
)
def choose_all(n_clicks, month):
    if n_clicks is not None:
        text = str(month) + ' месяц заполнен'
    else:
        text='0'
    return text




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
        cb1_val = ['AE','AU','AL','AO']
        cb2_val = ['PCN', 'PCS']
        cb3_val = ['SME']
        cb4_val = ['ASY-D', 'ASY-H', 'SYM-D', 'SYM-H']
        cb5_val = ['AL-ie', 'AU-ie', 'AE-ie']
        cb6_val = ['Middle Latitude A', 'Middle Latitude K-indices', 'High Latitude A', 'High Latitude K-indices', 'Estimated A', 'Estimated K-indices']
        return cb1_val, cb2_val, cb3_val, cb4_val, cb5_val, cb6_val




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

    # rqst.clear()
    # rqst.update({'date_begin': str(date_begin)})
    # rqst.update({'time_begin': str(time_begin)+':00'})
    # rqst.update({'date_end': str(date_end)})
    # rqst.update({'time_end': str(time_end)+':00'})
    # rqst.update({'time_step': str(time_step)})
    # rqst.update({'sought_info': sought_info})

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
                b = model.main_function(str(date_begin), str(time_begin)+':00', str(date_end), str(time_end)+':00', str(time_step), sought_info)

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