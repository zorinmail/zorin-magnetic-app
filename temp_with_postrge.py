import csv
import os
import pandas as pd
from datetime import datetime
import sys
import datetime
import psycopg2

from psycopg2 import sql
from psycopg2.extensions import AsIs
import sqlalchemy



pg_user = 'axtwbbjtiajlqn'
pg_pass = 'b08a23d4e8da8bb01e89b5c02e29fa7b959a3a91be994ac1e7ec0c20fb322615'
pg_host = 'ec2-34-230-231-71.compute-1.amazonaws.com'
pg_port = '5432'
pg_dbname = 'de51bdao4jre75'

connection_string = 'postgresql+psycopg2://' + pg_user + ':' + pg_pass + '@' + pg_host + ':' + pg_port + '/' + pg_dbname


engine = sqlalchemy.create_engine(connection_string)
# engine_two = sqlalchemy.create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/gindices")

# PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

# папка с данными по месяцам
# initial_dirname = os.path.join(PROJECT_PATH, 'initial')

# усреднение по времени
def time_selection(df, timestep):
    rule = timestep
    #df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d' + ' ' + '%H:%M:%S')
    dff = df.resample(rule, on='datetime').mean()
    dfff = dff.round(1)
    # dfff['DATETIME'] = dff.index
    return dfff

def mainFunction(month):
    filename = str(month) + '.csv'
    PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
    initial_dirname = os.path.join(PROJECT_PATH, 'initial')
    _path = os.path.join(initial_dirname, filename)
    d = pd.read_csv(_path, ';')  # csv в dataframe
    d['datetime'] = pd.to_datetime(d['datetime'], format='%Y-%m-%d' + ' ' + '%H:%M:%S')
    d = time_selection(d, '1H')
    d.to_sql('indices', engine, if_exists='append')  # dataframe в postgre



# # создание sql-запроса
# def create_sql_query(date_begin, time_begin, date_end, time_end, sought_info: list):
#     datetime_begin = date_begin + ' ' + time_begin
#     datetime_end = date_end + ' ' + time_end
#     cols = (', '.join(sought_info)).lower()
#     sqlquery = "select datetime, " + cols + " from tabs where datetime between " + "'" + datetime_begin + "'" + " and " + "'" +  datetime_end + "'" + " order by datetime"
#     return sqlquery
#
#
#
#
# # запрос-заплатка
# sought_info = ['ae','au','al','ao',
#                'middle_latitude_a', 'middle_latitude_k_indices', 'high_latitude_a', 'high_latitude_k_indices', 'estimated_a', 'estimated_k_indices',
#                'pcn','pcs',
#                'sme',
#                'asy_d', 'asy_h', 'sym_d', 'sym_h']
# # sought_info = ['AE_ie', 'SYM-D']
# date_begin = '2015-01-01'
# time_begin = '00:00:00'
# date_end = '2015-01-02'
# time_end = '23:59:00'
# time_step = '10S'
#
#
# start_time = datetime.datetime.now()
# sqlquery= create_sql_query(date_begin, time_begin, date_end, time_end, sought_info)
# df = pd.read_sql_query(sqlquery, con=engine)
# str_time = str(datetime.datetime.now() - start_time)
# print('1: ' + str_time)
# df = time_selection(df, time_step)
# str_time = str(datetime.datetime.now() - start_time)
# print('2: ' + str_time)
# relative_filename = os.path.join(
#     'files',
#     'file1' + '.xlsx'
# )
# absolute_filename = os.path.join(os.getcwd(), relative_filename)
# writer = pd.ExcelWriter(absolute_filename)
# str_time = str(datetime.datetime.now() - start_time)
# print('3: ' + str_time)
# df.to_excel(writer, 'Sheet1')
# str_time = str(datetime.datetime.now() - start_time)
# print('4: ' + str_time)
# writer.save()
# str_time = str(datetime.datetime.now() - start_time)
# print('5: ' + str_time)



# оценка сложности (по времени выполнения)


# date_end = '2015-07-01'
# dctnry = {'names': ['rule', 'time', 'df_size_rows', 'df_size_bytes']}
#
#
# list_of_rules = ['10S','60S','300S','600S','900S','1800S','1H','2H','6H','12H','1D']
#
# for rule in list_of_rules:
#     list_of_times_one = []
#     list_of_times_one.append(rule)
#     sqlquery = create_sql_query(date_begin, time_begin, date_end, time_end, sought_info)
#     df = pd.read_sql_query(sqlquery, con=engine)
#     start_time = datetime.datetime.now()
#     df = time_selection(df, rule)
#     str_time = str(datetime.datetime.now() - start_time)
#     list_of_times_one.append(str_time)
#     df_size_rows = str(df.size)
#     df_size_bytes = str(sys.getsizeof(df))
#     list_of_times_one.append(df_size_rows)
#     list_of_times_one.append(df_size_bytes)
#     dctnry[rule] = list_of_times_one
#     df = pd.DataFrame(columns=df.columns)
#
# dff = pd.DataFrame(data=dctnry)
# dff.to_excel("output.xlsx")
#
# a=0


# dictionary = {'names': ['date_end','sqlquery','read_sql_query','time_selection','size_of_df','excel']}
# date_end = datetime.datetime(2015,1,1)
# i=0
#
# while date_end <= datetime.datetime(2015,9,15):
#
#     list_of_times = []
#
#     date_end_text = datetime.datetime.strftime(date_end, '%Y-%m-%d')
#
#     list_of_times.append(date_end_text)
#
#     print(date_end_text)
#
#     start_time = datetime.datetime.now()
#     sqlquery = create_sql_query(date_begin, time_begin, date_end_text, time_end, sought_info)
#     str_time = str(datetime.datetime.now() - start_time)
#     print('sqlquery: ' + str_time)
#     list_of_times.append(str_time)
#
#     start_time = datetime.datetime.now()
#     df = pd.read_sql_query(sqlquery, con=engine)
#     str_time = str(datetime.datetime.now() - start_time)
#     df_size = str(df.size)
#     df_size_bytes = str(sys.getsizeof(df))
#     print('read_sql_query: время: ' + str_time + '; размер df: ' + df_size)
#     print('размер dataframe байт: ' + df_size_bytes)
#     list_of_times.append(str_time)
#
#
#
#     start_time = datetime.datetime.now()
#     df = time_selection(df, time_step)
#     str_time = str(datetime.datetime.now() - start_time)
#     print('time_selection: ' + str_time + '; размер df после: ' + str(df.size))
#     list_of_times.append(str_time)
#     list_of_times.append(df_size_bytes)
#     dictionary[df_size] = list_of_times
#
#
#     relative_filename = os.path.join(
#         'files',
#         'file' + str(i) + '.xlsx'
#     )
#     absolute_filename = os.path.join(os.getcwd(), relative_filename)
#     start_time = datetime.datetime.now()
#     writer = pd.ExcelWriter(absolute_filename)
#     df.to_excel(writer, 'Sheet1')
#     writer.save()
#     str_time = str(datetime.datetime.now() - start_time)
#     print('запись в эксель: время: ' + str_time)
#     list_of_times.append(str_time)
#
#
#     print(' ')
#     df = pd.DataFrame(columns=df.columns)
#     date_end += datetime.timedelta(days=3)
#
#     i=i+1
#
# dff = pd.DataFrame(data=dictionary)
# dff.to_excel("output.xlsx")




a=0
# with psycopg2.connect(dbname='indices', user='postgres', password='admin', host='localhost') as conn:
#     with conn.cursor() as cursor:
#
#         conn.autocommit = True
#
#         values = [
#             (4, a, 200.1, 300.2),
#             (5, b, 201.1, 301.2),
#             (6, c, 202.1, 302.2),
#         ]
#
#         insert = sql.SQL('INSERT INTO main_table (id, datetime, au, ae) VALUES {}').format(
#             sql.SQL(',').join(map(sql.Literal, values))
#         )
#         cursor.execute(insert)
#         #cursor.execute('CREATE TABLE tab()')





