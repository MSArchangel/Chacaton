import datetime
import pprint

import requests

dict_names = {1: 'Выкладка фишек', 2: 'Сортировка', 3: 'Маркировка', 4: 'Выкладка оснований',
              5: 'Раскладка', 6: 'Упаковка'}
dict_of_status = {0: 'Выключена', 1: 'Работает', 2: 'Ожидание', 3: 'Ошибка'}

dict_wait = {0: 'Нет ожидания', 1: 'Ожидание заготовок на входе',
             2: 'Линия переполнена или ожидание готовности следующей ячейки'}


def info_yach(cell_num: int):
    data = requests.get('http://roboprom.kvantorium33.ru/api/current').json()['data']
    pprint.pprint(data)
    kol_vo_chasov = int(str(datetime.datetime.now()).split()[1].split(':')[0])
    name = dict_names[cell_num]
    avg_load_per_hour = round(
        (data[cell_num - 1]['load_h'][1] + data[cell_num - 1]['load_h'][2]) * 100,
        2)
    avg_load_per_day = round(
        (data[cell_num - 1]['load_d'][1] + data[cell_num - 1]['load_d'][2]) * 100,
        2)
    int_per_day = data[cell_num - 1]['count_d']
    int_per_hour = data[cell_num - 1]['count_h']
    # status_chart_data = [x_values=[i for i in range(kol_vo_chasov)], y_values=[0, 1, 3, 4, 2, 0, 3]],
    cell_status_pie = [(data[cell_num - 1]['status_d'][1]) / 60,
                       (data[cell_num - 1]['status_d'][0]) / 60,
                       (data[cell_num - 1]['status_d'][2]) / 60,
                       (data[cell_num - 1]['status_d'][3]) / 60]

    cell_status_table = data[cell_num - 1]['status']
    status_time_day = round(data[cell_num - 1]['status_d'][data[cell_num - 1]['status']] / 60, 2)
    status_percentage_day = round(
        (data[cell_num - 1]['status_d'][data[cell_num - 1]['status']] / sum(
            data[cell_num - 1][
                'status_d'])) * 100, 2)

    status_time_hour = round(data[cell_num - 1]['status_h'][data[cell_num - 1]['status']] / 60)
    status_percentage_hour = round((data[cell_num - 1]['status_h'][data[cell_num - 1]['status']] /
                                    sum(data[cell_num - 1][
                                            'status_h'])) * 100, 2)

    cell_wait_status_table = [
        data[cell_num - 1]['wait'],
        data[cell_num - 1]['wait_d'][
            data[cell_num - 1]['wait']],
        round((data[cell_num - 1][
                   'wait_d'][
                   data[
                       cell_num - 1][
                       'wait']] /
               sum(data[
                       cell_num - 1][
                       'wait_d']) * 100), 2),
        data[cell_num - 1]['wait_h'][
            data[cell_num - 1]['wait']],
        round((data[
                   cell_num - 1][
                   'wait_h'][
                   data[
                       cell_num - 1][
                       'wait']] /
               sum(data[
                       cell_num - 1][
                       'wait_h'])) * 100, 2)]
    return [cell_num, name, avg_load_per_day, avg_load_per_hour, int_per_day, int_per_hour,
            cell_status_pie, dict_of_status[cell_status_table],
            status_time_day, status_percentage_day, status_time_hour, status_percentage_hour,
            dict_wait[cell_wait_status_table[0]],
            cell_wait_status_table[1:]]
    # cell_chill_pie = CellChillPie(no_reason=1, broken=0, maintenance=0, fixing=0)
    # cell_chill_table=list[CellChillTableRow]
