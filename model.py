import pandas as pd
import psycopg2
# import sqlalchemy

import connect_to_db
engine = connect_to_db.create_engine()

# pg_user = 'axtwbbjtiajlqn'
# pg_pass = 'b08a23d4e8da8bb01e89b5c02e29fa7b959a3a91be994ac1e7ec0c20fb322615'
# pg_host = 'ec2-34-230-231-71.compute-1.amazonaws.com'
# pg_port = '5432'
# pg_dbname = 'de51bdao4jre75'
#
# connection_string = 'postgresql+psycopg2://' + pg_user + ':' + pg_pass + '@' + pg_host + ':' + pg_port + '/' + pg_dbname
#
# engine = sqlalchemy.create_engine(connection_string)



# усреднение по времени
def time_selection(df, timestep):
    rule = timestep
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d' + ' ' + '%H:%M:%S')
    dff = df.resample(rule, on='datetime').mean()
    dfff = dff.round(1)
    # dfff['datetime'] = dff.index
    return dfff


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

# создание sql-запроса
def create_sql_query(date_begin, time_begin, date_end, time_end, sought_info: list):
    datetime_begin = date_begin + ' ' + time_begin
    datetime_end = date_end + ' ' + time_end
    cols = (', '.join(sought_info)).lower()
    sqlquery = "select datetime, " + cols + " from indices where datetime between " + "'" + datetime_begin + "'" + " and " + "'" +  datetime_end + "'" + " order by datetime"
    return sqlquery


def mainFunction(date_begin, time_begin, date_end, time_end, time_step, sought_info: list):
    sqlquery= create_sql_query(date_begin, time_begin, date_end, time_end, sought_info)
    df = pd.read_sql_query(sqlquery, con=engine)
    df = time_selection(df, time_step)
    return df
