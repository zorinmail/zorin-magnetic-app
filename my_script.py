import csv
import os
import pandas as pd
from datetime import datetime


# для измерения времени выполнения кода
# start_time = datetime.now()


# класс со всякой исходной информацией. Много чего здесь не используется.
class Initial_info:
    def __init__(self):
        """Constructor"""
        self._headers_for_csv = {'DGD': ['DATE',
                                         'Middle Latitude A','Middle Latitude K-indices',
                                         'High Latitude A','High Latitude K-indices',
                                         'Estimated A','Estimated K-indices'],
                                'AUALAOAE': ['DATE','TIME','DOY','AE','AU','AL','AO'],
                                'pcnpcs': ['DATE','TIME','PCN','PCS'],
                                'SME': ['DATE','TIME','SME'],
                                'SYM_H': ['DATE','TIME','DOY','ASY-D','ASY-H','SYM-D','SYM-H'],
                                'IE': ['DATE','TIME','AL_ie','AU_ie','AE_ie']}

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
        self.data_dir = "data"
        self.initial_dir = "initial"
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
        tree = os.walk('data\IE_2015')
        for i in tree:
            IE.append(i)
        for address, dirs, files in IE:
            for file in files:
                # path = os.path.join(script_dir, data_dir, IE_dir, file)
                path = os.path.join(self.data_dir, IE_dir, file)
                self._file_names['IE'].append(path)


initial_info = Initial_info()


# напечатать csv в консоль
def printCSV(pathToFile, rowsNumber=0):
    with open(pathToFile) as f:
        reader = csv.reader(f)
        i = 0
        if rowsNumber == 0:  # печатать полностью весь csv
            for row in reader:
                print(row)
        else:  # печатать первые rowsNumber строк
            for row in reader:
                if i < rowsNumber:
                    print(row)
                    i += 1
                else:
                    break


# определение принадлежности даты к кварталу
def quarter(asked_datetime):
    # asked_datetime = datetime.strptime(asked_datetime, '%Y-%m-%d' + ' ' + '%H:%M:%S')
    jan = {'begin': datetime.strptime('2015-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
           'end': datetime.strptime('2015-01-31 23:59:50', '%Y-%m-%d %H:%M:%S')}
    feb = {'begin': datetime.strptime('2015-02-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
           'end': datetime.strptime('2015-02-28 23:59:50', '%Y-%m-%d %H:%M:%S')}
    mar = {'begin': datetime.strptime('2015-03-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
           'end': datetime.strptime('2015-03-31 23:59:50', '%Y-%m-%d %H:%M:%S')}
    apr = {'begin': datetime.strptime('2015-04-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
           'end': datetime.strptime('2015-04-30 23:59:50', '%Y-%m-%d %H:%M:%S')}
    may = {'begin': datetime.strptime('2015-05-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
           'end': datetime.strptime('2015-05-31 23:59:50', '%Y-%m-%d %H:%M:%S')}
    jun = {'begin': datetime.strptime('2015-06-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
           'end': datetime.strptime('2015-06-30 23:59:50', '%Y-%m-%d %H:%M:%S')}
    jul = {'begin': datetime.strptime('2015-07-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
           'end': datetime.strptime('2015-07-31 23:59:50', '%Y-%m-%d %H:%M:%S')}
    aug = {'begin': datetime.strptime('2015-08-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
           'end': datetime.strptime('2015-08-31 23:59:50', '%Y-%m-%d %H:%M:%S')}
    sep = {'begin': datetime.strptime('2015-09-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
           'end': datetime.strptime('2015-09-30 23:59:50', '%Y-%m-%d %H:%M:%S')}
    oct = {'begin': datetime.strptime('2015-10-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
           'end': datetime.strptime('2015-10-31 23:59:50', '%Y-%m-%d %H:%M:%S')}
    nov = {'begin': datetime.strptime('2015-11-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
           'end': datetime.strptime('2015-11-30 23:59:50', '%Y-%m-%d %H:%M:%S')}
    dec = {'begin': datetime.strptime('2015-12-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
           'end': datetime.strptime('2015-12-31 23:59:50', '%Y-%m-%d %H:%M:%S')}

    if asked_datetime >= jan['begin'] and asked_datetime <= jan['end']:
        return '1'
    elif asked_datetime > jan['end'] and asked_datetime <= feb['end']:
        return '2'
    elif asked_datetime > feb['end'] and asked_datetime <= mar['end']:
        return '3'
    elif asked_datetime > mar['end'] and asked_datetime <= apr['end']:
        return '4'
    elif asked_datetime > apr['end'] and asked_datetime <= may['end']:
        return '5'
    elif asked_datetime > may['end'] and asked_datetime <= jun['end']:
        return '6'
    elif asked_datetime > jun['end'] and asked_datetime <= jul['end']:
        return '7'
    elif asked_datetime > jul['end'] and asked_datetime <= aug['end']:
        return '8'
    elif asked_datetime > aug['end'] and asked_datetime <= sep['end']:
        return '9'
    elif asked_datetime > sep['end'] and asked_datetime <= oct['end']:
        return '10'
    elif asked_datetime > oct['end'] and asked_datetime <= nov['end']:
        return '11'
    elif asked_datetime > nov['end'] and asked_datetime <= dec['end']:
        return '12'
    else:
        return 'asked datetime do not belongs to 2015 year'


# определение месяцев, входящих в диапазон дат
def find_quarters(datetime_begin, datetime_end):

    if datetime_begin > datetime_end:
        return 'окончание не может быть раньше начала'
    csvs = []
    begin_quarter = int(quarter(datetime_begin))
    end_quarter = int(quarter(datetime_end))
    if begin_quarter == end_quarter:
        csvs.append(begin_quarter)
        return csvs
    for i in range(begin_quarter, end_quarter+1):
        csvs.append(str(i))
    return csvs


#создание новых папок (0, 1, 2, 3 ...)
def create_new_folder(dirname):
    tree = os.walk(dirname)
    walked = []
    j = 0
    for i in tree:
        walked.append(i)
    for address, dirs, files in walked:
        if len(dirs) == 0:
            os.makedirs(dirname + '\\' + str(j), exist_ok=True)
        else:
            for dir in dirs:
                if int(dir) > j:
                    j = int(dir)
            os.makedirs(dirname + '\\' + str(j), exist_ok=True)
            j += 1
    return j



# усреднение по времени
def time_selection(df, timestep):
    rule = timestep
    df['DATETIME'] = pd.to_datetime(df['DATETIME'], format='%Y-%m-%d' + ' ' + '%H:%M:%S')
    dff = df.resample(rule, on='DATETIME').mean()
    dfff = dff.round(1)
    # dfff['DATETIME'] = dff.index
    return dfff


# вход - запрос и пути к файлам, выход - dataframe, соответствующий запросу
def selection(quarters_path, sought_info, datetime_begin, datetime_end, time_step):
    if len(quarters_path) == 1:
        csv_file = quarters_path[0]
        # читаем csv в словарь
        a = pd.read_csv(csv_file, ';').to_dict()
        # массив названий, которые нужно удалить (не относящиеся к запросу)
        names_to_delete = []
        for key in a:
            if key not in sought_info and key not in ['DATE', 'TIME', 'DATETIME']:
                names_to_delete.append(key)
        # удаление столбцов, не относящихся к запросу
        for del_key in names_to_delete:
            del a[del_key]
        # определение строк, которые нужно оставить
        first_row = 0
        last_row = 0
        for date_key in a['DATETIME']:
            date_value = a['DATETIME'][date_key]
            convert_csv_to_datetime = datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S')
            if convert_csv_to_datetime == datetime_begin:
                first_row = date_key
                break
        for date_key in a['DATETIME']:
            date_value = a['DATETIME'][date_key]
            convert_csv_to_datetime = datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S')
            if convert_csv_to_datetime == datetime_end:
                last_row = date_key
                break
        # удаление строк, не входящих в запрошенный диапазон
        for some in a:
            full_length = len(a[some])
            for row_number in range(0, full_length):
                if row_number in a[some]:
                    if row_number < first_row or row_number > last_row:
                        del a[some][row_number]
        a = pd.DataFrame(a)
        a = time_selection(a, time_step)
        return a
    elif len(quarters_path) > 1:
        count = 0
        df = pd.DataFrame({'A' : []})
        for item in quarters_path:
            csv_file = item
            #читаем csv в словарь
            a = pd.read_csv(csv_file, ';').to_dict()
            # массив названий, которые нужно удалить (не относящиеся к запросу)
            names_to_delete = []
            for key in a:
                if key not in sought_info and key not in ['DATE', 'TIME', 'DATETIME']:
                    names_to_delete.append(key)
            # удаление столбцов, не относящихся к запросу
            for del_key in names_to_delete:
                del a[del_key]
            # удаление строк
            if count == 0: #если это первый просмотренный квартал, то сравнивать дату окончания не надо
                first_row = 0
                for date_key in a['DATETIME']:
                    date_value = a['DATETIME'][date_key]
                    convert_csv_to_datetime = datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S')
                    if convert_csv_to_datetime == datetime_begin:
                        first_row = date_key
                        break
                # удаление строк, не входящих в запрошенный диапазон
                for some in a:
                    full_length = len(a[some])
                    for row_number in range(0, full_length):
                        if row_number in a[some]:
                            if row_number < first_row:
                                del a[some][row_number]
                a = pd.DataFrame(a)
                a = time_selection(a, time_step)
                if df.empty:
                    df = a
                else:
                    df = pd.concat([df, a])
            elif count == len(quarters_path)-1: #если это последний просмотренный квартал, то сравнивать дату начала не надо
                last_row = 0
                for date_key in a['DATETIME']:
                    date_value = a['DATETIME'][date_key]
                    convert_csv_to_datetime = datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S')
                    if convert_csv_to_datetime == datetime_end:
                        last_row = date_key
                        break
                # удаление строк, не входящих в запрошенный диапазон
                for some in a:
                    full_length = len(a[some])
                    for row_number in range(0, full_length):
                        if row_number in a[some]:
                            if row_number > last_row:
                                del a[some][row_number]
                a = pd.DataFrame(a)
                a = time_selection(a, time_step)
                if df.empty:
                    df = a
                else:
                    df = pd.concat([df, a])
            else:
                a = pd.DataFrame(a)
                a = time_selection(a, time_step)
                if df.empty:
                    df = a
                else:
                    df = pd.concat([df, a])
            count += 1
        return df

UPLOAD_DIRECTORY = "/created_csv"




# обработка запроса
def main_function(date_begin, time_begin, date_end, time_end, time_step, sought_info: list):
    # преобразуем строки в даты
    datetime_begin = datetime.strptime(date_begin + ' ' + time_begin, '%Y-%m-%d' + ' ' + '%H:%M:%S')
    datetime_end = datetime.strptime(date_end + ' ' + time_end, '%Y-%m-%d' + ' ' + '%H:%M:%S')

    PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

    # папка с данными по кварталам
    initial_dirname = os.path.join(PROJECT_PATH, initial_info.initial_dir)

    # создание папки для новых csv created_csv
    created_csv = os.path.join(PROJECT_PATH, initial_info.dir_to_save_csvs)
    # path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'TestDir')

    dir=[]
    tree = os.walk(created_csv)
    for i in tree:
        dir.append(i)
    for address, dirs, files in dir:
        if len(files) > 0:
            for file in files:
                os.remove(os.path.join(created_csv, file))

    quarters = find_quarters(datetime_begin, datetime_end)
    quarters_path = [os.path.join(initial_dirname, str(line) + '.csv') for line in quarters]

    # выборка. Возвращается dataframe, соответствующий диапазону дат и параметрам поля
    a = selection(quarters_path, sought_info, datetime_begin, datetime_end, time_step)
    return a




# # запрос
# sought_info = ['AE', 'AO', 'Middle Latitude K-indices', 'ASY-D', 'High Latitude K-indices', 'PCS', 'SME', 'SYM-D','SYM-H', 'AE_ie']
# # sought_info = ['AE_ie', 'SYM-D']
# date_begin = '2015-01-01'
# time_begin = '10:00:10'
# date_end = '2015-10-10'
# time_end = '23:59:00'
# time_step = '1D'
#
#
# main_function(date_begin, time_begin, date_end, time_end, time_step, sought_info)
# print(datetime.now() - start_time)