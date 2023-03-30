from datetime import datetime

import flask
import pprint
import requests
import time


def func_api():
    arr = []
    dict_for_diagrama = {'Количество включенных ячеек': 0, 'Количество выключенных ячеек': 0,
                         'Количество ожидающих ячеек': 0, 'Количество ячеек с ошибкой': 0}

    dict_of_status = {0: 'выключена', 1: 'работает', 2: 'ожидание', 3: 'ошибка'}

    dict_of_waiting = {0: 'нет ожидания',
                       1: 'ожидание заготовок на входе',
                       2: 'линия переполнена или ожидание готовности следующей ячейки'}

    dict_of_modes = {0: 'ручной или пошаговый режим', 1: 'автоматический режим'}

    api = 'http://roboprom.kvantorium33.ru/api/current'
    response = requests.get(api).json()
    if response['result'] == 'success':
        data = response['data']
        for cells in data:
            spisok = {f"Ячейка №{cells['cell']}": ['0', 'нет информации', 'нет информации',
                                                   'нет информации']}
            for paraming in cells['params']:
                if paraming['param'] == 'status':
                    spisok[f"Ячейка №{cells['cell']}"][2] = f"{dict_of_status[paraming['value']]}"
                    if paraming['value'] == 1:
                        dict_for_diagrama['Количество включенных ячеек'] += 1
                    if paraming['value'] == 0:
                        dict_for_diagrama['Количество выключенных ячеек'] += 1
                    if paraming['value'] == 2:
                        dict_for_diagrama['Количество ожидающих ячеек'] += 1
                    if paraming['value'] == 3:
                        dict_for_diagrama['Количество ячеек с ошибкой'] += 1

                if paraming['param'] == 'wait':
                    spisok[f"Ячейка №{cells['cell']}"][3] = f"{dict_of_waiting[paraming['value']]}"

                if paraming['param'] == 'count':
                    spisok[f"Ячейка №{cells['cell']}"][0] = (f'{paraming["value"]}')

                if paraming['param'] == 'mode':
                    spisok[f"Ячейка №{cells['cell']}"][0] = f'{dict_of_modes[paraming["value"]]}е'
            arr.append(spisok)
        dict_for_diagrama = {'Количество включенных ячеек': 0, 'Количество выключенных ячеек': 0,
                             'Количество ожидающих ячеек': 0, 'Количество ячеек с ошибкой': 0}
        for elem in data:
            if elem['status'] == 0:
                dict_for_diagrama['Количество выключенных ячеек'] += 1
            if elem['status'] == 1:
                dict_for_diagrama['Количество включенных ячеек'] += 1
            if elem['status'] == 2:
                dict_for_diagrama['Количество ожидающих ячеек'] += 1
            if elem['status'] == 3:
                dict_for_diagrama['Количество ячеек с ошибкой'] += 1
        for i in range(len(arr)):
            arr[i][f'Ячейка №{i + 1}'][0] = data[i]['count_d']
            arr[i][f'Ячейка №{i + 1}'][-1] = dict_of_waiting[data[i]['wait']]
            arr[i][f'Ячейка №{i + 1}'][2] = dict_of_status[data[i]['status']]
        return dict_for_diagrama, arr
    else:
        return 'error'

