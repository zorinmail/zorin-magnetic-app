import os
import pandas as pd
import psycopg2
import sqlalchemy

import connect_to_db
engine = connect_to_db.create_engine('server')

# pg_user = 'axtwbbjtiajlqn'
# pg_pass = 'b08a23d4e8da8bb01e89b5c02e29fa7b959a3a91be994ac1e7ec0c20fb322615'
# pg_host = 'ec2-34-230-231-71.compute-1.amazonaws.com'
# pg_port = '5432'
# pg_dbname = 'de51bdao4jre75'
# connection_string = 'postgresql+psycopg2://' + pg_user + ':' + pg_pass + '@' + pg_host + ':' + pg_port + '/' + pg_dbname
#
# engine = sqlalchemy.create_engine(connection_string)

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
