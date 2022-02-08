separator = (40*'~').join(['\n']*2)


class Playlist(object):
    def __init__(self, playlist_id=None, next_page_token=None, videos_list=None):
        if videos_list is None:
            videos_list = []
        self.playlist_id = playlist_id
        self.next_page_token = next_page_token
        self.videos_list = videos_list

    def get_dict(self):
        return {
            'playlist_id': self.playlist_id,
            'next_page_token': self.next_page_token,
            'videos_ids': [video.id for video in self.videos_list]
        }

    def __str__(self):
        values = self.get_dict()

        return '\n'.join([f'{value}: {values[value]}' for value in values if values[value] is not None])\
                   .join([separator]*2)


class Video(object):
    def __init__(self, video_id=None, kind=None, published_at=None, channel_id=None, channel_title=None, title=None,
                 description=None, tags=None, category_id=None, default_language=None, default_audio_language=None,
                 duration=None, licensed_content=None, projection=None, view_count=None, like_count=None,
                 comment_count=None, thumbnails=None):

        self.id = video_id
        self.kind = kind
        self.published_at = published_at
        self.channel_id = channel_id
        self.channel_title = channel_title
        self.title = title
        self.description = description
        self.tags = tags
        self.category_id = category_id
        self.default_language = default_language
        self.default_audio_language = default_audio_language
        self.duration = duration
        self.licensed_content = licensed_content
        self.projection = projection
        self.view_count = view_count
        self.like_count = like_count
        self.comment_count = comment_count
        self.thumbnails = thumbnails

    def get_dict(self):
        return {
            'video_id': self.id,
            'kind': self.kind,
            'published_at': self.published_at,
            'channel_id': self.channel_id,
            'channel_tittle': self.channel_title,
            'title': self.title,
            'description': self.description,
            'tags': self.tags,
            'category_id': self.category_id,
            'default_language': self.default_language,
            'default_audio_language': self.default_audio_language,
            'duration': self.duration,
            'licensed_content': self.licensed_content,
            'projection': self.projection,
            'view_count': self.view_count,
            'like_count': self.like_count,
            'comment_count': self.comment_count,
            'thumbnails': self.thumbnails,
        }

    def __str__(self):
        values = self.get_dict()

        return '\n'.join([f'{value}: {values[value]}' for value in values if values[value] is not None]) \
            .join([separator] * 2)


class Category(object):

    def __init__(self, cat_id, cat_title):
        self.cat_id = cat_id
        self.cat_title = cat_title

    def get_dict(self):
        return {
            'cat_id': self.cat_id,
            'cat_title': self.cat_title,
        }

    def __str__(self):
        values = self.get_dict()

        return '\n'.join([f'{value}: {values[value]}' for value in values if values[value] is not None]) \
            .join([separator] * 2)


class Channel(object):
    def __init__(self, channel_id, channel_title, country, channel_description,
                 view_count, subscriber_count, video_count):
        self.channel_id = channel_id
        self.channel_title = channel_title
        self.country = country
        self.channel_description = channel_description
        self.view_count = view_count
        self.subscriber_count = subscriber_count
        self.video_count = video_count

    def get_dict(self):
        return {
            'channel_id': self.channel_id,
            'channel_title': self.channel_title,
            'country': self.country,
            'channel_description': self.channel_description,
            'view_count': self.view_count,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
        }

    def __str__(self):
        values = self.get_dict()

        return '\n'.join([f'{value}: {values[value]}' for value in values if values[value] is not None]) \
            .join([separator] * 2)

