import datetime
import os

import pandas as pd


def append_row_to_csv(file: str, row: dict) -> None:
    if os.path.dirname(file) is not None:
        if not os.path.isdir(os.path.dirname(file)) and os.path.dirname(file) != '':
            os.makedirs(os.path.dirname(file))

    out = pd.DataFrame([[value for value in row.values()]], columns=[key for key in row.keys()])
    if os.path.exists(file):
        out.to_csv(file, mode='a', header=False, quoting=1, index=False, encoding='UTF-8')
    else:
        out.to_csv(file, mode='w', header=True, quoting=1, index=False, encoding='UTF-8')


def generate_video_url(video_id) -> str:
    return 'https://www.youtube.com/channel/%s' % video_id


def generate_channel_url(channel_id) -> str:
    return 'https://www.youtube.com/channel/%s' % channel_id


def generate_playlist_url(playlist_id) -> str:
    return 'https://www.youtube.com/playlist?list=%s' % playlist_id


def get_datetime(date_str) -> datetime.datetime:
    if type(date_str) == datetime.datetime:
        return date_str

    if len(date_str) > 11:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    else:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d')
