import requests
import pytz
from datetime import time, datetime

PATH = 'http://devman.org/api/challenges/solution_attempts/'


def load_attempts():
    pages = requests.get(PATH).json()['number_of_pages']
    users_data = []
    for page in range(1, pages + 1):
        payload = {'page': page}
        load_data = requests.get(PATH, params=payload).json()
        users_data.extend(load_data['records'])
    return users_data


def get_midnighters(users):
    midnight = time(hour=0, minute=0, microsecond=0)
    morning = time(hour=6, minute=0, microsecond=0)
    users_midnighters = []
    for user in users:
        user_time_zone = pytz.timezone(user['timezone'])
        local_dt = user_time_zone.localize(
            datetime.fromtimestamp(user['timestamp']))

        if midnight < local_dt.time() < morning:
            users_midnighters.append(user['username'])
    return set(users_midnighters)


if __name__ == '__main__':
    print(get_midnighters(load_attempts()))
