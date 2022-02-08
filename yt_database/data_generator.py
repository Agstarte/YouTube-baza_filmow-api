import datetime

import pandas as pd
import numpy as np
import os

from yt_database import data_structure

import youtube_api.data_structure as api_structure

from utils.utils import generate_channel_url, generate_video_url, append_row_to_csv, get_datetime


def make_directory(path):
    dir_name = os.path.dirname(path)
    if dir_name and not os.path.isdir(dir_name):
        os.makedirs(dir_name)


class CsvGenerator(object):
    def __init__(self):
        self.data_dict = dict()

    def append_row(self, row: dict):
        for key in row.keys():
            if key in self.data_dict.keys():
                self.data_dict[key].append(row[key])
            else:
                # if self.data_dict.keys():
                #     self.data_dict[key] = [None, ] * (len(list(self.data_dict.keys())[0]) - 1) + [row[key]]
                # else:
                #     self.data_dict[key] = [row[key]]
                self.data_dict[key] = [row[key]]

    def save_csv(self, path):
        make_directory(path)
        dataframe = pd.DataFrame.from_dict(self.data_dict)
        dataframe.to_csv(path, quoting=1, index=False, sep=',', encoding='utf-8', mode='a')


class Generator(object):
    def __init__(self, playlist_csv, videos_csv, channels_csv, out_videos_csv=None, out_channels_csv=None):
        self.playlist_file = pd.read_csv(playlist_csv)
        self.videos_file = pd.read_csv(videos_csv)
        self.out_videos_csv = out_videos_csv
        self.out_channels_csv = out_channels_csv

        if type(channels_csv) in [list, set, tuple]:
            self.channels_file = pd.concat([pd.read_csv(f) for f in channels_csv]).drop_duplicates(
                subset=pd.read_csv(channels_csv[0]).keys()[1:])
        else:
            self.channels_file = pd.read_csv(channels_csv)

    def generate_videos_csv(self, min_time=120, ignore_shorts=True, max_days=31, ignore_vertical=True,
                            accepted_languages: list = None, out_videos_csv=None):
        if self.out_videos_csv is None and out_videos_csv is None:
            raise ValueError('Out videos file not passed')
        elif out_videos_csv is None:
            out_videos_csv = self.out_videos_csv

        csv_generator = CsvGenerator()

        for video in self.get_videos(min_time, ignore_shorts, max_days, ignore_vertical, accepted_languages):
            # append_row_to_csv(out_videos_csv, out_video.get_dict())
            csv_generator.append_row(video.get_dict())
        csv_generator.save_csv(out_videos_csv)

    def get_videos(self, min_time=120, ignore_shorts=True, max_days=31, ignore_vertical=True,
                   accepted_languages: list = None):
        check_date = datetime.datetime.now().date()

        for row in self.videos_file.values:
            video = api_structure.Video(*row)

            if int(video.duration.replace('s', '')) > min_time and \
                    (not ignore_shorts or ('#short' not in str(video.tags) and '#short' not in video.title)) and \
                    (not ignore_vertical or 'vertical' not in video.projection):

                if accepted_languages and video.default_language not in accepted_languages + [np.nan] \
                        and video.default_audio_language not in accepted_languages + [np.nan]:
                    continue

                days = (check_date - get_datetime(video.published_at).date()).days

                if days > max_days:
                    continue

                out_video = data_structure.Video(check_date=check_date, title=video.title,
                                                 channel_name=video.channel_title,
                                                 channel_url=generate_channel_url(video.channel_id),
                                                 video_length=video.duration, url=generate_video_url(video.id),
                                                 views=video.view_count, pub_date=video.published_at,
                                                 days_between_check_and_pub=days)

                yield out_video

    def generate_channels_csv(self, accepted_languages: list = None, out_channels_csv=None):
        if self.out_channels_csv is None and out_channels_csv is None:
            raise ValueError('Out channels file not passed')
        elif out_channels_csv is None:
            out_channels_csv = self.out_channels_csv

        csv_generator = CsvGenerator()

        for channel in self.get_channels(accepted_languages):
            # append_row_to_csv(out_channels_csv, channel.get_dict())
            csv_generator.append_row(channel.get_dict())

        csv_generator.save_csv(out_channels_csv)

    def get_channels(self, accepted_languages: list = None):
        check_date = datetime.datetime.now().date()

        values = {value: index for index, value in enumerate(self.channels_file)}

        for row in self.channels_file.values:
            channel = data_structure.Channel(check_date=check_date,
                                             subscribers_amount=row[values['subscribers_count']],
                                             channel_name=row[values['nazwa kanalu']],
                                             channel_url=generate_channel_url(row[values['social_id']]))
            videos = []
            for vid in self.videos_file.values:
                video = api_structure.Video(*vid)
                if video.channel_id in channel.channel_url:
                    videos.append(video)

            channel.last_month_views, channel.last_week_views = 0, 0
            for video in videos:
                if accepted_languages and video.default_language not in accepted_languages + [np.nan] \
                        and video.default_audio_language not in accepted_languages + [np.nan]:
                    continue
                days = (check_date - get_datetime(video.published_at).date()).days
                if days <= 7:
                    channel.last_week_views += video.view_count
                    channel.last_month_views += video.view_count
                elif days <= 31:
                    channel.last_month_views += video.view_count

            yield channel
