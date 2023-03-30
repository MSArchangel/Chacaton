import requests
import pprint
import datetime




def sr_zn_oborud():
    arr = []
    api_status_count = f'http://roboprom.kvantorium33.ru/api/current'
    data = requests.get(api_status_count).json()
    for elem in data['data']:
        arr.append(elem['load_h'][1] * 100)
    return round(sum(arr) / 6)


def for_graph():
    from_hours, an_hours_ago = datetime.datetime.now(), datetime.datetime.now() - datetime.timedelta(
        hours=1)
    arr = []
    x = str(datetime.datetime.now()).split()[1].split(':')[0]
    for i in range(1, int(x) + 1):
        api_status_count = f'http://roboprom.kvantorium33.ru/api/history?cell=6&param=count&from={int(datetime.datetime.timestamp(an_hours_ago))}&to={int(datetime.datetime.timestamp(from_hours))}'
        data = requests.get(api_status_count).json()
        from_hours = an_hours_ago
        an_hours_ago = from_hours - datetime.timedelta(hours=1)

        if len(data['data']) > 0:
            arr.append(data['data'][-1]['value'])
        else:
            arr.append(0)
    return arr[::-1]

