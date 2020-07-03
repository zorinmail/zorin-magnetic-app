import re
import csv
import os
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Float

import connect_to_db


# для измерения времени выполнения кода
start_time = datetime.now()


# класс со всякой исходной информацией
class Initial_info:
    def __init__(self):
        """Constructor"""
        self._headers_for_csv = {'DGD': ['Y','Mon','D',
                                         'ml_a','ml_k_0','ml_k_3','ml_k_6','ml_k_9','ml_k_12','ml_k_15','ml_k_18','ml_k_21',
                                         'hl_a','hl_k_0','hl_k_3','hl_k_6','hl_k_9','hl_k_12','hl_k_15','hl_k_18','hl_k_21',
                                         'e_a','e_k_0','e_k_3','e_k_6','e_k_9','e_k_12','e_k_15','e_k_18','e_k_21'],
                                'AUALAOAE': ['DATE','TIME','DOY','ae','au','al','ao'],
                                'pcnpcs': ['DATE','TIME','pcn','pcs'],
                                'SME': ['DATETIME','sme'],
                                'SYM_H': ['DATE','TIME','DOY','asy_d','asy_h','sym_d','sym_h'],
                                'IE': ['Y','Mon','D','H','Min','S','al_ie','au_ie','ae_ie']}

        self._contained_info = {'DGD': ['Middle Latitude A','Middle Latitude K-indices',
                                        'High Latitude A','High Latitude K-indices',
                                        'Estimated A','Estimated K-indices'],
                               'AUALAOAE': ['DOY','AE','AU','AL','AO'],
                               'pcnpcs': ['PCN','PCS'],
                               'SME': ['SME'],
                               'SYM_H': ['DOY','ASY-D','ASY-H','SYM-D','SYM-H'],
                               'IE': ['AL-ie','AU-ie','AE-ie']}
        # имена файлов, а после выполнения __set_path - пути
        self._file_names = {'DGD': '2015_DGD.txt',
                           'AUALAOAE': 'AUALAOAE_2015.txt',
                           'pcnpcs': 'pcnpcs.txt',
                           'SME': 'SME_2015.csv',
                           'SYM_H': 'SYM-H.txt',
                           'IE': []}

        self._time_steps_sec = {'DGD': 86400,
                               'AUALAOAE': 60,
                               'pcnpcs': 60,
                               'SME': 60,
                               'SYM_H': 60,
                               'IE': 10}
        self._datetime_formats = {'DGD': {'date': '%Y %m %d', 'time': ''},
                                  'AUALAOAE': {'date': '%Y-%m-%d', 'time': '%H:%M:%S.%f'},
                                  'pcnpcs': {'date': '%Y-%m-%d', 'time': '%H:%M'},
                                  'SME': {'date': '%Y-%m-%d', 'time': '%H:%M:%S'},
                                  'SYM_H': {'date': '%Y-%m-%d', 'time': '%H:%M:%S.%f'},
                                  'IE': {'date': '%Y %m %d', 'time': '%H %M %S'}}
        self.data_dir = "initial"
        self.dir_to_save_csvs = "created_csv"
        self.__set_path()
        self.__set_path_IE()

    # формирование пути к файлам
    def __set_path(self):
        for key in self._file_names:
            if key != 'IE':
                # self._file_names[key] = os.path.join(script_dir, data_dir, self._file_names[key])
                self._file_names[key] = os.path.join(self.data_dir, self._file_names[key])

    # формирование пути к файлам в папке IE
    def __set_path_IE(self):
        IE_dir = "IE_2015"
        IE = []
        tree = os.walk('initial\IE_2015')
        for i in tree:
            IE.append(i)
        for address, dirs, files in IE:
            for file in files:
                # path = os.path.join(script_dir, data_dir, IE_dir, file)
                path = os.path.join(self.data_dir, IE_dir, file)
                self._file_names['IE'].append(path)


initial_info = Initial_info()

# усреднение по времени
def time_selection(df, timestep):
    rule = timestep
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d' + ' ' + '%H:%M:%S')
    dff = df.resample(rule, on='datetime').mean()
    dfff = dff.round(2)
    dfff['datetime'] = dff.index
    return dfff


# преобразование файлов в единообразные dataframe
def change_txts_to_df(path_to_initial, file_type):
    if file_type == 'pcnpcs':
        # out_path = os.path.join('initial', 'pcnpcs_output.txt')
        # with open(path_to_initial, 'r') as in_file:
        #     in_file = ''.join([i for i in in_file]) \
        #         .replace('\U00002013', '-')
        #     with open(out_path, 'w') as out_file:
        #         out_file.writelines(in_file)
        data = pd.read_csv(path_to_initial,
                           skiprows=(0,),
                           delim_whitespace=True,
                           names = initial_info._headers_for_csv[file_type],
                           decimal = '.',
                           converters={'DATE': str,
                                       'TIME': str,
                                       # 'pcn': float,
                                       # 'pcs': float
                                       }
                           )
        data['datetime'] = data['DATE'] + ' ' + data['TIME']
        str_to_date = (initial_info._datetime_formats[file_type]['date'] +
                       ' ' +
                       initial_info._datetime_formats[file_type]['time'])
        data['datetime'] = pd.to_datetime(data['datetime'], format=str_to_date)
        data = data[['datetime', 'pcn', 'pcs']]
        return data
    elif file_type == 'SME':
        data = pd.read_csv(path_to_initial,
                           skiprows=(0,),
                           delimiter=',',
                           names = initial_info._headers_for_csv[file_type],
                           converters={'DATETIME': str,
                                       # 'sme': float
                                       })
        str_to_date = (initial_info._datetime_formats[file_type]['date'] +
                       ' ' +
                       initial_info._datetime_formats[file_type]['time'])
        data['datetime'] = pd.to_datetime(data['DATETIME'], format=str_to_date)
        data = data[['datetime', 'sme']]
        return data
    elif file_type == 'SYM_H':
        data = pd.read_csv(path_to_initial,
                           skiprows=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14),
                           delim_whitespace=True,
                           names = initial_info._headers_for_csv[file_type],
                           converters={'DATE': str,
                                       'TIME': str,
                                       # 'asy_d': float,
                                       # 'asy_h': float,
                                       # 'sym_d': float,
                                       # 'sym_h': float
                                       })
        data['datetime'] = data['DATE'] + ' ' + data['TIME']
        str_to_date = (initial_info._datetime_formats[file_type]['date'] +
                       ' ' +
                       initial_info._datetime_formats[file_type]['time'])
        data['datetime'] = pd.to_datetime(data['datetime'], format=str_to_date)
        data = data[['datetime', 'asy_d','asy_h','sym_d','sym_h']]
        return data
    elif file_type == 'AUALAOAE':
        data = pd.read_csv(path_to_initial,
                           skiprows=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14),
                           delim_whitespace=True,
                           names = initial_info._headers_for_csv[file_type],
                           converters={'DATE': str,
                                       'TIME': str,
                                       # 'ae': float,
                                       # 'au': float,
                                       # 'al': float,
                                       # 'ao': float
                                       })
        data['datetime'] = data['DATE'] + ' ' + data['TIME']
        str_to_date = (initial_info._datetime_formats[file_type]['date'] +
                       ' ' +
                       initial_info._datetime_formats[file_type]['time'])
        data['datetime'] = pd.to_datetime(data['datetime'], format=str_to_date)
        data = data[['datetime', 'ae','au','al','ao']]
        return data
    elif file_type == 'IE':
        i = 0
        data = pd.DataFrame()
        for path in path_to_initial:
            if i == 0:
                data = pd.read_csv(path,
                                   skiprows=(0,1,2,3,4,5,6,7,8,9,10,11),
                                   delim_whitespace=True,
                                   names = initial_info._headers_for_csv[file_type],
                                   converters = {'Y':str,
                                                 'Mon':str,
                                                 'D':str,
                                                 'H':str,
                                                 'Min':str,
                                                 'S':str,
                                                 # 'al_ie': float,
                                                 # 'au_ie': float,
                                                 # 'ae_ie': float
                                                 })
            else:
                data_temp = pd.read_csv(path,
                                        skiprows=(0,1,2,3,4,5,6,7,8,9,10,11),
                                        delim_whitespace=True,
                                        names = initial_info._headers_for_csv[file_type],
                                        converters={'Y': str,
                                                    'Mon': str,
                                                    'D': str,
                                                    'H': str,
                                                    'Min': str,
                                                    'S': str,
                                                    # 'al_ie': float,
                                                    # 'au_ie': float,
                                                    # 'ae_ie': float
                                                    })
                data = data.append(data_temp)
            i = i + 1
        data['datetime'] = data['Y'] + ' ' + data['Mon'] + ' ' + data['D'] + ' ' + data['H'] + ' ' + data['Min'] + ' ' + data['S']
        str_to_date = (initial_info._datetime_formats[file_type]['date'] +
                       ' ' +
                       initial_info._datetime_formats[file_type]['time'])
        data['datetime'] = pd.to_datetime(data['datetime'], format=str_to_date)
        data = data[['datetime', 'al_ie','au_ie','ae_ie']]
        return data
    elif file_type == 'DGD':
        out_path = os.path.join('initial', 'DGD_output.txt')
        with open(path_to_initial, 'r') as in_file:
            in_file = ''.join([i for i in in_file]) \
                .replace("-", " -")
            with open(out_path, 'w') as out_file:
                out_file.writelines(in_file)
        data_temp = pd.read_csv(out_path,
                           skiprows=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
                           delim_whitespace=True,
                           names = initial_info._headers_for_csv[file_type],
                           converters={'Y': str,
                                       'Mon': str,
                                       'D': str})
        # data.columns = initial_info._headers_for_csv[file_type]
        data_temp['datetime'] = data_temp['Y'] + ' ' + data_temp['Mon'] + ' ' + data_temp['D']
        str_to_date = (initial_info._datetime_formats[file_type]['date'])
        data_temp['datetime'] = pd.to_datetime(data_temp['datetime'], format = str_to_date)

        data = pd.DataFrame(columns=['datetime',
                                     'middle_latitude_a', 'middle_latitude_k_indices',
                                     'high_latitude_a', 'high_latitude_k_indices',
                                     'estimated_a', 'estimated_k_indices'])
        i=0
        for index, row in data_temp.iterrows():
            for hour in [0,3,6,9,12,15,18,21]:
                new_datetime = row['datetime'] + timedelta(hours=hour)
                data.loc[i, 'datetime'] = new_datetime
                data.loc[i, 'middle_latitude_a'] = row['ml_a']
                data.loc[i, 'high_latitude_a'] = row['hl_a']
                data.loc[i, 'estimated_a'] = row['e_a']
                data.loc[i, 'middle_latitude_k_indices'] =  row[('ml_k' + '_' + str(hour))]
                data.loc[i, 'high_latitude_k_indices'] =  row[('hl_k' + '_' + str(hour))]
                data.loc[i, 'estimated_k_indices'] =  row[('e_k' + '_' + str(hour))]
                i=i+1
        return data
    return 0



def fill_db_from_files(time_step):
    engine = connect_to_db.create_engine('local')

    if not engine.dialect.has_table(engine, 'indices_local'):  # If table don't exist, Create.
        metadata = MetaData(engine)
        # Create a table with the appropriate Columns
        Table('indices_local', metadata,
              Column('datetime', DateTime(timezone=False), primary_key=True, nullable=False),
              Column('al_ie', Float),
              Column('au_ie', Float),
              Column('ae_ie', Float),
              Column('ae', Float),
              Column('au', Float),
              Column('al', Float),
              Column('ao', Float),
              Column('pcn', Float),
              Column('pcs', Float),
              Column('sme', Float),
              Column('asy_d', Float),
              Column('asy_h', Float),
              Column('sym_d', Float),
              Column('sym_h', Float),
              Column('middle_latitude_a', Float),
              Column('middle_latitude_k_indices', Integer),
              Column('high_latitude_a', Float),
              Column('high_latitude_k_indices', Integer),
              Column('estimated_a', Float),
              Column('estimated_k_indices', Integer),
              )
        # Implement the creation
        metadata.create_all()

    for i in range(1,12):

        df_pcnpcs = change_txts_to_df(initial_info._file_names['pcnpcs'], 'pcnpcs')
        df_pcnpcs = df_pcnpcs[df_pcnpcs['datetime'].dt.month == i]
        df_pcnpcs = time_selection(df_pcnpcs, time_step)
        df_pcnpcs = df_pcnpcs.ffill()
        df_pcnpcs.index.name = None
        df_sym_h = change_txts_to_df(initial_info._file_names['SYM_H'], 'SYM_H')
        df_sym_h = df_sym_h[df_sym_h['datetime'].dt.month == i]
        df_sym_h = time_selection(df_sym_h, time_step)
        df_sym_h = df_sym_h.ffill()
        df_sym_h.index.name = None
        df = pd.merge(df_pcnpcs, df_sym_h, on='datetime')
        del df_pcnpcs
        del df_sym_h

        df_sme = change_txts_to_df(initial_info._file_names['SME'], 'SME')
        df_sme = df_sme[df_sme['datetime'].dt.month == i]
        df_sme = time_selection(df_sme, time_step)
        df_sme = df_sme.ffill()
        df_sme.index.name = None
        df = pd.merge(df, df_sme, on='datetime')
        del df_sme


        df_aualaoae = change_txts_to_df(initial_info._file_names['AUALAOAE'], 'AUALAOAE')
        df_aualaoae = df_aualaoae[df_aualaoae['datetime'].dt.month == i]
        df_aualaoae = time_selection(df_aualaoae, time_step)
        df_aualaoae = df_aualaoae.ffill()
        df_aualaoae.index.name = None
        df = pd.merge(df, df_aualaoae, on='datetime')
        del df_aualaoae


        df_alauae_ie = change_txts_to_df(initial_info._file_names['IE'], 'IE')
        df_alauae_ie = df_alauae_ie[df_alauae_ie['datetime'].dt.month == i]
        df_alauae_ie = time_selection(df_alauae_ie, time_step)
        df_alauae_ie = df_alauae_ie.ffill()
        df_alauae_ie.index.name = None
        df = pd.merge(df, df_alauae_ie, on='datetime')
        del df_alauae_ie


        df_dgd = change_txts_to_df(initial_info._file_names['DGD'], 'DGD')
        df_dgd['middle_latitude_a'] = df_dgd['middle_latitude_a'].astype(int)
        df_dgd['middle_latitude_k_indices'] = df_dgd['middle_latitude_k_indices'].astype(int)
        df_dgd['high_latitude_a'] = df_dgd['high_latitude_a'].astype(int)
        df_dgd['high_latitude_k_indices'] = df_dgd['high_latitude_k_indices'].astype(int)
        df_dgd['estimated_a'] = df_dgd['estimated_a'].astype(int)
        df_dgd['estimated_k_indices'] = df_dgd['estimated_k_indices'].astype(int)
        df_dgd = df_dgd[df_dgd['datetime'].dt.month == i]
        df_dgd.loc[df_dgd['middle_latitude_k_indices'] > 9 or df_dgd['middle_latitude_k_indices'] < (-1), 'middle_latitude_k_indices'] = (-1)
        df_dgd.loc[df_dgd['high_latitude_k_indices'] > 9 or df_dgd['high_latitude_k_indices'] < (-1), 'high_latitude_k_indices'] = (-1)
        df_dgd.loc[df_dgd['estimated_k_indices'] > 9 or df_dgd['estimated_k_indices'] < (-1), 'estimated_k_indices'] = (-1)
        df_dgd = time_selection(df_dgd, time_step)
        df_dgd = df_dgd.ffill()
        df_dgd.index.name = None
        df = pd.merge(df, df_dgd, on='datetime')
        del df_dgd

        df.to_sql('indices_local', engine, if_exists='append', index=False)
        del df

        print(i)



fill_db_from_files('10S')
