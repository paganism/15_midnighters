import requests
import pytz
from datetime import datetime


def load_attempts():
    URL = 'http://devman.org/api/challenges/solution_attempts/'
    page = 1
    payload = {'page': page}

    while True:
        try:
            response = requests.get(URL, params=payload).json()
            payload = {'page': page}
            page += 1
            users_attempts = response['records']
            for attempt in users_attempts:
                yield attempt
        except ValueError:
            break


def get_midnighters(users):
    midnight = 0
    morning = 6
    midnighters = []
    for user in users:
        user_time_zone = pytz.timezone(user['timezone'])
        local_dt = user_time_zone.localize(
            datetime.fromtimestamp(user['timestamp']))
        if midnight < local_dt.hour < morning:
            midnighters.append(user['username'])
    return set(midnighters)


def print_midnighters(midnighters):
    print('Совы на Девмане:')
    for midnighter in midnighters:
        print(midnighter)


if __name__ == '__main__':
    midnighters = get_midnighters(load_attempts())
    print_midnighters(midnighters)
