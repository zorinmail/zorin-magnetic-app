import re
import csv
import os
import pandas as pd
from datetime import datetime


# для измерения времени выполнения кода
start_time = datetime.now()


# класс со всякой исходной информацией
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


# преобразование файлов в csv
def txt_to_csv(path_to_txt_file, dirname, filename, csv_header, is_it_IL, is_it_DGD):

    path_to_save_CSV = dirname + "\\" + filename
    # os.makedirs(dirname, exist_ok=True)

    tree = os.walk(dirname)
    walked = []
    for i in tree:
        walked.append(i)
    for address, dirs, files in walked:
        if filename not in files:
            if not is_it_IL and not is_it_DGD:
                with open(path_to_txt_file, 'r') as in_file:
                    stripped = [re.sub(" +", " ", line) for line in in_file]
                    stripped = [re.sub("\n", "", line) for line in stripped]
                    stripped = [re.sub(",", " ", line) for line in stripped]
                    # stripped = [line.strip() for line in in_file]
                    # lines = [line.split(" ") for line in stripped if not (line.isspace() or line == ' ') and (line.find('|')<0)]
                    lines = (line.split(" ") for line in stripped
                             if line and line.find('|')<0 and line.find('#')<0 and
                             line.find('%')<0 and re.search('\d+', line) is not None and
                             line.find(':Product:')<0 and line.find(':Issued:')<0)

                    with open(path_to_save_CSV, 'w', newline='') as out_file:
                        writer = csv.writer(out_file)
                        writer.writerow((initial_info._headers_for_csv[csv_header]))
                        # print(lines[0])
                        writer.writerows(lines)
                        # for line in lines:
                        #     if not line.isspace():
                        #         writer.writerow(line)
            elif is_it_IL:
                with open(path_to_save_CSV, 'w', newline='') as out_file:
                    writer = csv.writer(out_file)
                    writer.writerow((initial_info._headers_for_csv[csv_header]))
                    for item in path_to_txt_file:
                        # print(item)
                        with open(item, 'r') as in_file:
                            # r'^(.*?(cat.*?){1})cat', r'\1Bull', s
                            stripped = [re.sub(r'^(.*?(\s.*?){2})\s', r'\1  ', line) for line in in_file]
                            stripped = [re.sub("  +", "  ", line) for line in stripped]
                            stripped = [re.sub("\n", "", line) for line in stripped]
                            lines = (line.split("  ") for line in stripped if line and line.find('%')<0)
                        writer.writerows(lines)
            elif is_it_DGD:
                with open(path_to_txt_file, 'r') as in_file:
                    stripped = [re.sub("  +", "  ", line) for line in in_file]
                    stripped = [re.sub("\n", "", line) for line in stripped]
                    lines = (line.split("  ") for line in stripped
                             if line and line.find('|') < 0 and line.find('#') < 0 and
                             line.find('%') < 0 and re.search('\d+', line) is not None and
                             line.find(':Product:') < 0 and line.find(':Issued:') < 0)

                    with open(path_to_save_CSV, 'w', newline='') as out_file:
                        writer = csv.writer(out_file)
                        writer.writerow((initial_info._headers_for_csv[csv_header]))
                        writer.writerows(lines)
            return 1
        else:
            print("file " + filename + " is already in there")
            return 0


# возвращает список csv, в которых есть запрошенные параметры
def find_info_in_csv(sought_info: list):
    founded_csv = []
    for param in sought_info:
        for key in initial_info._contained_info:
            for i in initial_info._contained_info[key]:
                if i == param:
                    founded_csv.append(key)
            # if param in initial_info._contained_info[key]:
    founded_csv = dict([(item, None) for item in founded_csv]).keys()
    # print(founded_csv)
    return founded_csv


# объединение csv в один
# def merge_csv(path_to_initial, path_to_save_CSV, output_filename):
#     walked = []
#     csv_path = []
#     tree = os.walk(path_to_initial)
#     for i in tree:
#         walked.append(i)
#     for address, dirs, files in walked:
#         for file in files:
#             path = os.path.join(path_to_initial, file)
#             csv_path.append(path)
#     # print(csv_path)
#     a = pd.read_csv(csv_path[0])
#     b = pd.read_csv(csv_path[1])
#     merged = a.merge(b, on='DATE')
#     merged.to_csv("output.csv", index=False)
#     # dict1 = {row[0]: row[1:] for row in r}...dict2 = {row[0]: row[1:] for row in r}
#     combined_csv = pd.concat((pd.read_csv(f) for f in csv_path), sort=True)
#     # print(combined_csv)
#     combined_csv.to_csv("combined_csv.csv", index=False) #, encoding='utf-8-sig'

# объединение csv (пока просто конкатинация)
def concat_csvs(a, b):
    c = pd.concat([a,b], ignore_index=True, sort=False)
    return c


# выборка, соответствующая запросу
def selection(date_begin, date_end, sought_info: list):
    # преобразуем строки в даты
    date_begin = datetime.strptime(date_begin, '%Y-%m-%d').date()
    # time_begin = datetime.strptime(time_begin, '%H:%M:%S.%f').time()
    date_end = datetime.strptime(date_end, '%Y-%m-%d').date()
    # time_end = datetime.strptime(time_end, '%H:%M:%S.%f').time()

    # создание папки для новых csv
    dirname = initial_info.dir_to_save_csvs
    os.makedirs(dirname, exist_ok=True)

    # массив названий, в которых есть запрошенные параметры
    arr = find_info_in_csv(sought_info)

    # преобразуем нужные файлы в csv
    for i in arr:
        path_to_txt_file = initial_info._file_names[i]
        filename = i + '.csv'
        csv_header = i
        if i == "IE":
            is_it_IL = 1
        else:
            is_it_IL = 0
        if i == "DGD":
            is_it_DGD = 1
        else:
            is_it_DGD = 0
        txt_to_csv(path_to_txt_file, dirname, filename, csv_header, is_it_IL, is_it_DGD)

    # создание папок для каждого нового запроса
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
    # чтение csv и удаление лишнего
    to_concat = None
    arr_path = dict([(line, initial_info.dir_to_save_csvs + "\\" + line + ".csv") for line in arr])
    files_count = 0
    for item in arr_path:
        csv_file = arr_path[item]
        #читаем csv в словарь
        a = pd.read_csv(csv_file).to_dict()

        #массив названий, которые нужно удалить (не относящиеся к запросу)
        names_to_delete = []
        for key in a:
            if key not in sought_info and key not in ['DATE', 'TIME']:
                names_to_delete.append(key)
        #удаление столбцов, не относящихся к запросу
        for del_key in names_to_delete:
            del a[del_key]

        # массив для имен файлов
        names_for_files = []
        for key in a:
            if key in sought_info and key not in ['DATE', 'TIME']:
                names_for_files.append(key)
        names_for_files = '_'.join(names_for_files)
        #определение строк, которые нужно оставить
        first_row = 0
        last_row = 0
        for date_key in a['DATE']:
            date_value = a['DATE'][date_key]
            convert_csv_to_datetime = datetime.strptime(date_value, initial_info._datetime_formats[item]['date']).date()
            if convert_csv_to_datetime == date_begin:
                first_row = date_key
                break
        for date_key in reversed(a['DATE']):
            date_value = a['DATE'][date_key]
            convert_csv_to_datetime = datetime.strptime(date_value, initial_info._datetime_formats[item]['date']).date()
            if convert_csv_to_datetime == date_end:
                last_row = date_key
                break

        #удаление строк, не входящих в запрошенный диапазон
        for some in a:
            full_length = len(a[some])
            for row_number in range(0, full_length):
                if row_number in a[some]:
                    if row_number < first_row or row_number > last_row:
                        del a[some][row_number]
        a = pd.DataFrame(a)
        a.to_csv(path_or_buf = initial_info.dir_to_save_csvs + '\\' + str(j) + '\\' + names_for_files + '.csv', index = False)
        if to_concat is None:
            to_concat = a
        else:
            c = concat_csvs(to_concat, a)
            to_concat = c

        files_count += 1

        # объединение файлов с одинаковой длиной. Не доработано
        # tree = os.walk(initial_info.dir_to_save_csvs + '\\' + str(j))
        # walked = []
        # temp = {}
        # for i in tree:
        #     walked.append(i)
        # for address, dirs, files in walked:
        #     for file in files:
        #         d = pd.read_csv(initial_info.dir_to_save_csvs + '\\' + str(j) + '\\' + file).to_dict()
        #         if temp[len(d['DATE'])] is None:
        #             temp[len(d['DATE'])] = [file]
        #         else:
        #             temp[len(d['DATE'])].append(file)
        # m = []
        # r = {}
        # for n in temp:
        #     if len(temp[n]) > 1:
        #         m.append(temp[n])
        # for n in m:
        #     for p in n:
        #         d = pd.read_csv(initial_info.dir_to_save_csvs + '\\' + str(j) + '\\' + p).to_dict()
        #         if r in None:
        #             r = d
        #         else:
        #             for s in d:
        #                 if s not in ['DATE', 'TIME']:
        #                     r[s] = d[s]
        #     r = pd.DataFrame(r)
        #     r.to_csv(path_or_buf=initial_info.dir_to_save_csvs + '\\' + str(j) + '\\' + ''.join(n) + '.csv', index=False)


    # to_concat.to_csv(path_or_buf=initial_info.dir_to_save_csvs + '\\' + str(j) + '\\concated.csv', index=False)



# запрос
sought_info = ['AE', 'AO', 'Middle Latitude K-indices', 'ASY-D', 'High Latitude K-indices', 'PCS', 'SME', 'SYM-D','SYM-H']
selection('2015-02-01', '2015-02-10', sought_info)


print(datetime.now() - start_time)