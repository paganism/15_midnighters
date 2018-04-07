import requests
import pytz
from datetime import datetime


def load_attempts():
    url = 'http://devman.org/api/challenges/solution_attempts/'
    page = 1
    payload = {'page': page}

    while True:
        response = requests.get(URL, params=payload).json()
        number_of_pages = response['number_of_pages']
        payload = {'page': page}
        page += 1
        users_attempts = response['records']
        for attempt in users_attempts:
            yield attempt
        if page > number_of_pages:
            break


def get_midnighters(attempts):
    midnight = 0
    morning = 6
    midnighters = []
    for attempt in attempts:
        user_time_zone = attempt['timezone']
        user_time = datetime.fromtimestamp(attempt['timestamp'])
        local_dt = pytz.timezone(user_time_zone).fromutc(user_time)
        if midnight < local_dt.hour < morning:
            midnighters.append(attempt['username'])
    return set(midnighters)


def print_midnighters(midnighters):
    print('Совы на Девмане:')
    for midnighter in midnighters:
        print(midnighter)


if __name__ == '__main__':
    midnighters = get_midnighters(load_attempts())
    print_midnighters(midnighters)
