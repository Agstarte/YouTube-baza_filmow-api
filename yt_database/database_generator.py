import datetime
import pickle

import pandas as pd
import os
from utils import utils
from utils.utils import get_datetime

from youtube_api import api_connector, api_data_converter
from yt_database.data_generator import Generator


class DatabaseGenerator(object):

    def __init__(self, in_csv_files, working_directory, languages: list = None, days=31):
        self.in_csv_files = in_csv_files
        self.working_directory = working_directory
        self.cur_date = datetime.datetime.now().date()

        self.languages = languages
        self.days = days

        self.check_date = datetime.datetime.now().date()

        self._save_path = os.path.join('save', str(self.cur_date))
        self._load_save()

    def generate_database(self):
        if type(self.in_csv_files) in [list, set, tuple]:
            combined_csv = pd.concat([pd.read_csv(f) for f in self.in_csv_files]).drop_duplicates(
                subset=pd.read_csv(self.in_csv_files[0]).keys()[1:])
        else:
            combined_csv = pd.read_csv(self.in_csv_files)

        for channel_id in combined_csv['social_id']:
            playlist_id = 'UU' + channel_id[2:]
            if playlist_id not in self._save:
                self._analyse_playlist(playlist_id)
                self._save.append(playlist_id)
                self._save_save()

        self._generate_csvs()

    def _analyse_playlist(self, playlist_id, page_token=None):
        con = api_connector.Connector()

        playlist_info = con.get_playlist_info(playlist_id=playlist_id, pageToken=page_token)
        if playlist_info is None:
            return
        playlist = api_data_converter.convert_playlist(playlist_info)
        if not playlist:
            return
        utils.append_row_to_csv(os.path.join(self.working_directory, str(self.cur_date), 'playlists.csv'),
                                playlist.get_dict())

        videos = [video.id for video in playlist.videos_list]

        videos_data = con.get_videos_info(videos)
        videos = api_data_converter.convert_video_list(videos_data)
        for video in videos:
            if video:
                utils.append_row_to_csv(os.path.join(self.working_directory, str(self.cur_date), 'videos.csv'),
                                        video.get_dict())

        if self.days >= (self.check_date - get_datetime(videos[0].published_at).date()).days \
                and playlist.next_page_token:
            self._analyse_playlist(playlist_id, page_token=playlist.next_page_token)

    def _generate_csvs(self):
        generator = Generator(os.path.join(self.working_directory, str(self.cur_date), 'playlists.csv'),
                              os.path.join(self.working_directory, str(self.cur_date), 'videos.csv'),
                              self.in_csv_files,
                              out_channels_csv=os.path.join(self.working_directory, str(self.cur_date) + 'out',
                                                            'channels.csv'),
                              out_videos_csv=os.path.join(self.working_directory, str(self.cur_date) + 'out',
                                                          'videos.csv'))

        generator.generate_channels_csv(accepted_languages=self.languages)
        generator.generate_videos_csv(accepted_languages=self.languages)

    def _load_save(self):
        self._save = list()

        if os.path.isfile(self._save_path):
            self._save = pickle.load(open(self._save_path, 'rb'))

    def _save_save(self):
        pickle.dump(self._save, open(self._save_path, 'wb'), protocol=4)
