import numpy as np
from numpy.random import randint, choice
import pandas as pd
import string
import datetime
import linecache
import PySimpleGUI as sg


def ip_is_correct(ip) -> bool:
    first, second, third, fourth = ip[0], ip[1], ip[2], ip[3]
    return not (first == 10 and (0 <= second <= 255 or 0 <= third <= 255 or 0 <= fourth <= 255) or
        first == 172 and (16 <= second <= 31 or 0 <= third <= 255 or 0 <= fourth <= 255) or
        first == 192 and second == 168 and (0 <= third <= 255 or 0 <= fourth <= 255) or
        first == 100 and (64 <= second <= 127 or 0 <= third <= 255 or 0 <= fourth <= 255))


def generate_ip() -> string:
    ip = (randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255))
    while (not ip_is_correct(ip)):
        ip = (randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255))
    return f'{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}'


def generate_email() -> string:
    EMAILS = (
        'gmail.com',
        'mail.ru',
        'outlook.com',
        'yahoo.com',
        'student.spbu.ru',
        'yandex.ru'
    )
    ALPHABET = list(string.ascii_letters + string.digits)
    return f"{''.join(choice(ALPHABET, size=randint(2, 10)))}@{choice(EMAILS, size=1)[0]}"


def generate_date(YEAR, chosen_season) -> string:
    MONTH_RANGE = {
        'autumn': (9, 92),
        'winter': (11, 90),
        'spring': (3, 91),
        'summer': (6, 91)
    }
    delta = datetime.timedelta(
        days=randint(MONTH_RANGE[chosen_season][1] - 1),
        hours=randint(24),
        minutes=randint(60),
    )
    date = datetime.datetime(
        year=YEAR,
        month=MONTH_RANGE[chosen_season][0],
        day=1,
        hour=0,
        minute=0
    )
    return (date + delta).isoformat()


def generate_platform() -> string:
    return linecache.getline('data/websites.txt', randint(1, 51)).rstrip()


def generate_ad(chosen_season) -> string:
    CATEGORIES = (
        'apparel',
        'home-and-garden',
        'jewelery'
    )
    CATEGORIES_LENGTH = {
        'apparel': 20,
        'home-and-garden': 20,
        'jewelery': 20
    }
    AD_PROB = {
        'autumn': (0.7, 0.2, 0.1),
        'winter': (0.4, 0.1, 0.5),
        'spring': (0.6, 0.3, 0.1),
        'summer': (0.5, 0.4, 0.1),
    }
    category = choice(CATEGORIES, size=1, p=AD_PROB[chosen_season])[0]
    return linecache.getline(f'data/{category}.txt', randint(1, CATEGORIES_LENGTH[category] + 1)).rstrip()


def generate_row(YEAR, AD_DUR_COEFF, chosen_season) -> dict:
    ad_num = randint(1, 101)
    ad_time = ad_num * AD_DUR_COEFF
    row = {
        'email': generate_email(),
        'ip': generate_ip(),
        'platform': generate_platform(),
        'date': generate_date(YEAR, chosen_season),
        'ad_num': ad_num,
        'ad_time': ad_time,
        'ad_type': generate_ad(chosen_season),
    }
    assert len(row['ad_type']) != 0, 'BLYA OPyat oshibka'

    return row


def generate_file(SIZE, YEAR, AD_DUR_COEFF, chosen_season) -> list:
    return [generate_row(YEAR, AD_DUR_COEFF, chosen_season) for i in range(int(SIZE))]


# def generate_excel() -> None:
#     df = pd.DataFrame.from_records(generate_file(), columns=[
#         'email',
#         'ip',
#         'platform',
#         'date',
#         'ad_num',
#         'ad_time',s
#         'ad_type'
#     ])
#     df.to_excel('output.xlsx', index=False)


def submit_is_correct(size, year, season, coeff, radio1):
    if size == '' or size is None or year == '' or year is None or season == '' or season is None:
        return False
    return (
        1 <= int(size) <= 50000
        and 2000 <= int(year) <= 2023
        and season in ['autumn', 'winter', 'spring', 'summer']
        and (((coeff == '' or coeff is None) and radio1) or ((coeff != '' and coeff is not None) and not radio1))
    )


def draw():
    sg.theme('DarkPurple1')

    def new_window(window, coeff=False):
        if window is not None:
            window.close()
        layout = [
            [sg.Push(), sg.Text('SPECIFY YOUR DATA', font=('Courier New', 16)), sg.Push()],
            [sg.Push(), sg.Text('num of rows:', font=('Courier New', 16)), sg.Input(size=(10, 10), font=('Courier New', 16), key='-size-'), sg.Push()],
            [sg.Push(), sg.Radio('random ad duration', "RAD1", default=(not coeff), font=('Courier New', 16), enable_events=True, key='-radio1-'),
            sg.Radio('specify ad duration', "RAD1", default=coeff, font=('Courier New', 16), key='-radio2-', enable_events=True), sg.Push()],
            [sg.Push(), sg.Text('ad duration:', visible=coeff, font=('Courier New', 16)),
            sg.Input(size=(6, 1), visible=coeff, key='-coeff-', font=('Courier New', 16)), sg.Push()],
            [sg.Push(), sg.Text('year:', font=('Courier New', 16)), sg.Slider(range=(2000, 2023), default_value=2000, orientation='horizontal', key='-year-'), sg.Push()],
            [sg.Push(), sg.Text('season:', font=('Courier New', 16)), sg.Combo(values=['autumn', 'winter', 'spring', 'summer'], default_value='autumn', font=('Courier New', 16), key='-season-'), sg.Push()],
            [sg.Push(), sg.Submit(key='btnSubmit', font=('Courier New', 16)), sg.Push()],
        ]

        return sg.Window('Specifying data', layout, size=(700,400), element_padding=15)

    window = new_window(None)

    while True:
        event, values = window.read()
        print(values)
        if event == "-radio1-":
            window = new_window(window, coeff=False)
        elif event == '-radio2-':
            window = new_window(window, coeff=True)
        elif event == 'btnSubmit':
            if submit_is_correct(values['-size-'], values['-year-'], values['-season-'], values['-coeff-'], bool(values['-radio1-'])):
                SIZE = int(values['-size-'])
                YEAR = int(values['-year-'])
                if values['-radio2-'] and values['-coeff-'] != '':
                    AD_DUR_COEFF = values['-coeff-']
                else:
                    AD_DUR_COEFF = randint(20, 361)
                chosen_season = values['-season-']
                df = pd.DataFrame.from_records(generate_file(SIZE, YEAR, AD_DUR_COEFF, chosen_season), columns=[
                    'email',
                    'ip',
                    'platform',
                    'date',
                    'ad_num',
                    'ad_time',
                    'ad_type'
                ])
                print('GENERATING!')
                df.to_excel('output.xlsx', index=False)
                break
        elif event == sg.WIN_CLOSED: 
            break

    window.close()


draw()