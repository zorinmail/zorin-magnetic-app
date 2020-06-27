from datetime import datetime as dt
from datetime import timezone
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
import plotly.express as px
import model
# import temp_with_postgre
import openpyxl


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://codepen.io/chriddyp/pen/brPBPO.css', dbc.themes.BOOTSTRAP]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
external_stylesheets=['https://codepen.io/chriddyp/pen/brPBPO.css', dbc.themes.BOOTSTRAP]

server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=external_stylesheets)

# app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})

app.title = ('Indices')




controls = dbc.Card(
    [
        html.Div([
            html.H4('Параметры времени', style={'text-align': 'center'}),
        ]),

        html.Div([
            html.H5('Даты', style={'text-align': 'center'}),
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=dt(2015, 1, 1),
                max_date_allowed=dt(2016, 1, 1),
                initial_visible_month=dt(2015, 2, 10),
                start_date_placeholder_text="Start Period",
                end_date_placeholder_text="End Period",
            ),
        ], style={'text-align': 'center'}),

        html.H5('Время', style={'text-align': 'center'}),

        html.Div([
            html.Div([
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
            html.H4('Индексы', style={'text-align': 'center', 'margin-bottom': '6px', 'margin-top': '6px'}),
            dbc.Button("выбрать всё", color="light", size="sm", id='choose_all'),
        ], style={'text-align': 'center'}),

        html.Div([
            html.Div([
                dbc.FormGroup(
                    [
                        dbc.Label("AE, AU, AL, AO"),
                        dbc.Checklist(
                            options=[
                                {'label': 'AE', 'value': 'ae'},
                                {'label': 'AU', 'value': 'au'},
                                {'label': 'AL', 'value': 'al'},
                                {'label': 'AO', 'value': 'ao'},
                            ],
                            value=[],
                            id="checkbox_1",
                            inputClassName='checkbox_1',
                            switch=True,
                        ),
                    ]
                ),
            ], style={'padding': '0 15px'}),

            html.Div([
                dbc.FormGroup(
                    [
                        dbc.Label("PCN, PCS"),
                        dbc.Checklist(
                            options=[
                                {'label': 'PCN', 'value': 'pcn'},
                                {'label': 'PCS', 'value': 'pcs'},
                            ],
                            value=[],
                            id="checkbox_2",
                            inputClassName='checkbox_2',
                            switch=True,
                        ),
                    ]
                ),
            ], style={'padding': '0 15px'}),

            html.Div([
                dbc.FormGroup(
                    [
                        dbc.Label("SME"),
                        dbc.Checklist(
                            options=[
                                {'label': 'SME', 'value': 'sme'},
                            ],
                            value=[],
                            id="checkbox_3",
                            inputClassName='checkbox_3',
                            switch=True,
                        ),
                    ]
                ),
            ], style={'padding': '0 15px'}),

            html.Div([
                dbc.FormGroup(
                    [
                        dbc.Label("ASY, SYM"),
                        dbc.Checklist(
                            options=[
                                {'label': 'ASY-D', 'value': 'asy_d'},
                                {'label': 'ASY-H', 'value': 'asy_h'},
                                {'label': 'SYM-D', 'value': 'sym_d'},
                                {'label': 'SYM-H', 'value': 'sym_h'},
                            ],
                            value=[],
                            id="checkbox_4",
                            inputClassName='checkbox_4',
                            switch=True,
                        ),
                    ]
                ),
            ], style={'padding': '0 15px'}),

            html.Div([
                dbc.FormGroup(
                    [
                        dbc.Label("AL, AU, AE"),
                        dbc.Checklist(
                            options=[
                                {'label': 'AL (ie)', 'value': 'al_ie'},
                                {'label': 'AU (ie)', 'value': 'au_ie'},
                                {'label': 'AE (ie)', 'value': 'ae_ie'},
                            ],
                            value=[],
                            id="checkbox_5",
                            inputClassName='checkbox_5',
                            switch=True,
                        ),
                    ]
                ),
            ], style={'padding': '0 15px'}),

            html.Div([
                dbc.FormGroup(
                    [
                        dbc.Label("A, K-indices"),
                        dbc.Checklist(
                            options=[
                                {'label': 'Middle Latitude A', 'value': 'middle_latitude_a'},
                                {'label': 'Middle Latitude K-indices', 'value': 'middle_latitude_k_indices'},
                                {'label': 'High Latitude A', 'value': 'high_latitude_a'},
                                {'label': 'High Latitude K-indices', 'value': 'high_latitude_k_indices'},
                                {'label': 'Estimated A', 'value': 'estimated_a'},
                                {'label': 'Estimated K-indices', 'value': 'estimated_k_indices'},
                            ],
                            value=[],
                            id="checkbox_6",
                            inputClassName='checkbox_6',
                            switch=True,
                        ),
                    ]
                ),
            ], style={'padding': '0 15px'}),
        ], style={'padding': '15px 0 0 30px', 'overflow': 'auto', 'justify-content': 'center', 'height': '30vh'}),


        html.Div([
            dbc.Button("Скачать данные", color="success", className="mr-1", id='main_button'),
        ], style={'text-align': 'center', 'margin-top': '15px'}),

        html.Div(id='output_div', style={'text-align': 'center', 'margin-top': '5px'}),

        dbc.Modal(
            [
                dbc.ModalHeader("Вы можете скачать данные по ссылке"),
                dbc.ModalBody(html.Div(id='output_div2', style={'text-align': 'center', 'margin-top': '10px'},
                         children=[html.A(
                             'download',
                             id='download-link',
                             href="#",
                             target="_blank"
                         )]
                    ),),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_modal", className="ml-auto")
                ),
            ],
            id="download_modal",
            centered=True,
        ),


    ],
    body=True,
    style={'overflow': 'auto', 'height': '100%'},
)


# sought_info_px = ['ae','au','al','ao',
#                'middle_latitude_a', 'middle_latitude_k_indices', 'high_latitude_a', 'high_latitude_k_indices', 'estimated_a', 'estimated_k_indices',
#                'pcn','pcs',
#                'sme',
#                'asy_d', 'asy_h', 'sym_d', 'sym_h']
#
# df_express = model.mainFunction('2015-01-01',
#                        '00:00:00',
#                        '2015-01-31',
#                        '23:59:00',
#                        '1D',
#                        sought_info_px)
# df_melt = df_express.melt(id_vars='datetime', value_vars=sought_info_px)
# fig = px.line(df_melt, x="datetime", y='value', color='variable')
dfpx = px.data.iris() # iris is a pandas DataFrame
fig = px.scatter(dfpx, x="sepal_width", y="sepal_length")


app.layout = html.Div(
    [
        html.Div([
            html.H1(children = 'Индексы геомагнитной активности', style = {'margin-bottom': '10px'}),
        ], style = {'text-align': 'center', 'min-height': '10%'}),

        html.Div([
            dbc.Row(
                [
                    dbc.Col(controls, md=3),
                    # dbc.Col(html.Div([
                    #     dbc.Button("Скачать данные", color="success", className="mr-1",),
                    # ], style={'text-align': 'center', 'margin-top': '15px'}),md=9),

                    dbc.Col(dcc.Graph(figure=fig, style={'height': '100%'}, id="index_graph"), md=9),
                ],
                align="center",
            ),
        ], style={'min-height': '90%'}),


    ],
    style={
        'padding': '10px 0 0 0',
        'height': '100%',
        'width': '95%',
        'margin': 'auto'
    }
)






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




# функция для построения графика
@app.callback(
    Output("index_graph", "figure"),
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

    if date_begin is not None and date_end is not None and time_step is not None and len(sought_info) > 0:
        df = model.mainFunction(str(date_begin), str(time_begin)+':00', str(date_end), str(time_end)+':00', str(time_step), sought_info)
        df_melt = df.melt(id_vars='datetime', value_vars=sought_info)
        fig = px.line(df_melt, x="datetime", y='value', color='variable')
        return fig



# функция для передачи параметров запроса в model
@app.callback(
    [Output("output_div", "children"),
     Output("download-link", "href"),
     Output("download-link", "children"),
     Output("download_modal", "is_open")],
    [Input(component_id='main_button', component_property='n_clicks'),
     Input("close_modal", "n_clicks")],
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
     State('checkbox_6', 'value'),
     State("download_modal", "is_open")]
)
def update_output(n_clicks, n_clicks2, date_begin, date_end, time_begin, time_end, time_step,
                  sought_info_1, sought_info_2, sought_info_3, sought_info_4, sought_info_5, sought_info_6,
                  is_open):
    sought_info = sought_info_1 + sought_info_2 + sought_info_3 + sought_info_4 + sought_info_5 + sought_info_6

    if n_clicks is None:
        raise PreventUpdate
    else:
        if date_begin is None or date_end is None:
            return 'Не введены даты!', '#', '', is_open
        elif time_begin is None or time_end is None:
            return 'Не введены диапазоны времени!', '#', '', is_open
        elif time_step is None:
            return 'Не введен шаг времени!', '#', '', is_open
        elif len(sought_info) == 0:
            return 'Не выбраны параметры поля!', '#', '', is_open
        else:
            try:
                b = model.mainFunction(str(date_begin), str(time_begin)+':00', str(date_end), str(time_end)+':00', str(time_step), sought_info)

                now=dt.now(timezone.utc)
                now_str = now.strftime("%d_%m_%Y_%H_%M_%S")
                relative_filename = os.path.join(
                    'created_csv',
                    'file_' + now_str + '.xlsx'
                )
                absolute_filename = os.path.join(os.getcwd(), relative_filename)
                writer = pd.ExcelWriter(absolute_filename)
                b.to_excel(writer, 'Sheet1')
                writer.save()
                if n_clicks or n_clicks2:
                    return '', '/{}'.format(relative_filename), 'Download', not is_open
                return '', '/{}'.format(relative_filename), 'Download', is_open
            except MemoryError:
                return 'Недостаточно памяти. Попробуйте выбрать меньший диапазон времени', '#', ''



@app.server.route('/created_csv/<path:path>')
def my_serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(
        os.path.join(root_dir, 'created_csv'), path
    )


if __name__ == '__main__':
    app.run_server(debug=True)





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