import functools

import googleapiclient.discovery
import os
import pickle
from googleapiclient.errors import HttpError

import logging


def _api_switcher(function):
    @functools.wraps(function)
    def wrapper(self, *args, **kwargs):
        try:
            result = function(self, *args, **kwargs)
        except HttpError as e:
            if e.status_code in [403, 400] and self.developer_key_number < len(self._API_KEYS) - 1:
                self.developer_key_number += 1
                self.youtube = self._setup(self._API_KEYS[self.developer_key_number])
                logging.debug('Changed developer key to: %s. Error code: %s' %
                              (self.developer_key_number, e.status_code))
                return wrapper(self, *args, **kwargs)
            else:
                raise
        else:
            return result

    return wrapper


class Connector(object):
    def __init__(self, developer_key: str = None):
        if developer_key is None:
            import youtube_api.credentials.developer_secret as secret
            self._API_KEYS = secret.API_KEYS

            self.developer_key_number = 0
            developer_key = self._API_KEYS[self.developer_key_number]
        self.youtube = self._setup(developer_key)

    def _setup(self, developer_key):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"
        api_service_name = "youtube"
        api_version = "v3"
        return googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=developer_key)

    @_api_switcher
    def get_playlist_info(self, playlist_id, max_results: int = 100, pageToken=None):
        request = self.youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=max_results,
            pageToken=pageToken,
            playlistId=playlist_id
        )
        try:
            response = request.execute()
        except HttpError as e:
            if 'invalidPart' in str(e):
                print('aaa')
                return None
            else:
                raise

        logging.debug('Got playlist: %s' % playlist_id)

        return response

    @_api_switcher
    def get_videos_info(self, videos_ids):
        start_value = videos_ids

        if type(videos_ids) in [tuple, list]:
            videos_ids = ','.join(videos_ids)

        if not videos_ids.split(',') or [a for a in videos_ids.split(',') if len(a) != 11]:
            raise ValueError(f'{start_value} is not valid')

        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=videos_ids
        )

        try:
            response = request.execute()
        except HttpError as e:
            if 'invalidPart' in str(e):
                ids_list = videos_ids.split(',')

                logging.debug('Error while getting %s videos, trying to get splitted' % len(ids_list))
                logging.debug('Errored with ids: %s' % videos_ids)

                if len(ids_list) > 1:
                    response = self.get_videos_info(videos_ids=ids_list[:int(len(ids_list) / 2)])
                    response2 = self.get_videos_info(videos_ids=ids_list[int(len(ids_list) / 2):])

                    if response is None:
                        response = response2
                    elif response2 is not None:
                        response['items'] += response2['items']
                else:
                    return None
            else:
                raise

        return response

    @_api_switcher
    def get_country_categories(self, region_code):
        request = self.youtube.videoCategories().list(
            part="snippet",
            hl="en",
            regionCode=region_code
        )
        response = request.execute()

        return response

    @_api_switcher
    def get_most_popular_videos(self, region_code=None, video_category_id=None, page_token=None):
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            chart="mostPopular",
            maxResults=400,
            pageToken=page_token,
            regionCode=region_code,
            videoCategoryId=video_category_id
        )
        try:
            response = request.execute()
        except HttpError:
            return None

        if "nextPageToken" in response:
            next_response = self.get_most_popular_videos(region_code, video_category_id, response['nextPageToken'])
            if "items" in next_response:
                response['items'] += next_response['items']

        return response

    @_api_switcher
    def get_channels_info(self, channels_ids):
        start_value = channels_ids

        if type(channels_ids) in [tuple, list, set]:
            channels_ids = ','.join(channels_ids)

        if [a for a in channels_ids.split(',') if len(a) != 24]:
            raise ValueError(f'{start_value} is not valid')

        request = self.youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=channels_ids
        )

        try:
            response = request.execute()
        except HttpError:
            ids_list = channels_ids.split(',')
            response = self.get_channels_info(channels_ids=ids_list[:int(len(ids_list) / 2)])
            response2 = self.get_channels_info(channels_ids=ids_list[int(len(ids_list) / 2):])
            response['items'] += response2['items']

        return response
