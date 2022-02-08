from youtube_api.data_structure import Playlist, Video
from datetime import datetime
from youtube_api import duration_parser


def convert_playlist(playlist_json):
    next_page_token, publish_date, video_owner_channel_title = (None, )*3

    try:
        playlist_id = playlist_json['items'][0]['snippet']['playlistId']
        if 'nextPageToken' in playlist_json.keys():
            next_page_token = playlist_json['nextPageToken']
        videos = []
        for item in playlist_json['items']:
            # publish_date = datetime.fromisoformat(item['contentDetails']['videoPublishedAt'])
            if 'videoPublishedAt' in item['contentDetails'].keys():
                publish_date = datetime.strptime(item['contentDetails']['videoPublishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            title = item['snippet']['title']
            description = item['snippet']['description']
            video_id = item['contentDetails']['videoId']
            if 'videoOwnerChannelTitle' in item['snippet'].keys():
                video_owner_channel_title = item['snippet']['videoOwnerChannelTitle']
            video_owner_channel_id = item['snippet']['videoOwnerChannelId']
            videos.append(Video(published_at=publish_date, title=title, channel_id=video_owner_channel_id,
                                description=description, video_id=video_id, channel_title=video_owner_channel_title))
    except KeyError:
        return None
    return Playlist(playlist_id=playlist_id, videos_list=videos, next_page_token=next_page_token)


def convert_video(video_json: dict):
    channel_title, tags, category_id, default_language, default_audio_language, \
    licensed_content, view_count, like_count, comment_count, thumbnails = (None,) * 10

    video_id = video_json['id']
    publish_date = datetime.strptime(video_json['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
    channel_id = video_json['snippet']['channelId']
    title = video_json['snippet']['title']
    if 'channelTitle' in video_json['snippet'].keys():
        channel_title = video_json['snippet']['channelTitle']
    if 'tags' in video_json['snippet'].keys():
        tags = video_json['snippet']['tags']
    if 'categoryId' in video_json['snippet'].keys():
        category_id = video_json['snippet']['categoryId']
    if 'defaultLanguage' in video_json['snippet'].keys():
        default_language = video_json['snippet']['defaultLanguage']
    if 'defaultAudioLanguage' in video_json['snippet'].keys():
        default_audio_language = video_json['snippet']['defaultAudioLanguage']
    duration = str(duration_parser.parse_isoduration(video_json['contentDetails']['duration'])) + 's'
    if 'licensedContent' in video_json['contentDetails'].keys():
        licensed_content = video_json['contentDetails']['licensedContent']
    projection = video_json['contentDetails']['projection']
    if 'viewCount' in video_json['statistics'].keys():
        view_count = video_json['statistics']['viewCount']
    if 'likeCount' in video_json['statistics'].keys():
        like_count = video_json['statistics']['likeCount']
    if 'commentCount' in video_json['statistics'].keys():
        comment_count = video_json['statistics']['commentCount']
    kind = video_json['kind']
    if 'thumbnails' in video_json['snippet'].keys():
        thumbnails = video_json['snippet']['thumbnails']

    return Video(video_id=video_id, published_at=publish_date, channel_id=channel_id, title=title, kind=kind,
                 channel_title=channel_title, tags=tags, category_id=category_id, default_language=default_language,
                 default_audio_language=default_audio_language, duration=duration, licensed_content=licensed_content,
                 projection=projection, view_count=view_count, like_count=like_count, comment_count=comment_count,
                 thumbnails=thumbnails)


def convert_video_list(video_list_json):
    videos = []
    for item in video_list_json['items']:
        videos.append(convert_video(item))

    return videos
