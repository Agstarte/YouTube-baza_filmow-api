import datetime

separator = (40*'~').join(['\n']*2)


class Channel(object):
    def __init__(self, check_date=None, channel_name=None, channel_url=None, subscribers_amount=None,
                 last_week_views=None, last_month_views=None):
        if check_date is None:
            self.check_date = datetime.datetime.now().date()
        else:
            self.check_date = check_date
        self.channel_name = channel_name
        self.channel_url = channel_url
        self.subscribers_amount = subscribers_amount
        self.last_week_views = last_week_views
        self.last_month_views = last_month_views

    def get_dict(self):
        return {
            'data_sprawdzenia': self.check_date,
            'nazwa kanalu': self.channel_name,
            'url kanalu': self.channel_url,
            'liczba subskrybentow': self.subscribers_amount,
            'suma wyswietlen filmow, które ukazaly się na kanale w osatnim tygodniu': self.last_week_views,
            'suma wyswietlen filmow, które ukazaly się na kanale w osatnim miesiacu': self.last_month_views,
        }

    def __str__(self):
        values = self.get_dict()

        return '\n'.join([f'{value}: {values[value]}' for value in values if values[value] is not None])\
                   .join([separator]*2)


class Video(object):
    def __init__(self, check_date: datetime.datetime.date = None, title=None, channel_name=None, channel_url=None,
                 video_length=None, url=None, views=None, pub_date: datetime.datetime = None,
                 days_between_check_and_pub=None):

        if check_date is None:
            self.check_date = datetime.datetime.now().date()
        else:
            self.check_date = check_date
        self.title = title
        self.channel_name = channel_name
        self.channel_url = channel_url
        self.video_length = video_length
        self.url = url
        self.views = views
        self.pub_date = pub_date
        if days_between_check_and_pub is None:
            self.days_between_check_and_pub = (pub_date - check_date).days
        else:
            self.days_between_check_and_pub = days_between_check_and_pub

    def get_dict(self):
        return {
            'check_date': self.check_date,
            'title': self.title,
            'channel_name': self.channel_name,
            'channel_url': self.channel_url,
            'video_length': self.video_length,
            'url': self.url,
            'views': self.views,
            'pub_date': self.pub_date,
            'days_between_check_and_pub': self.days_between_check_and_pub,
        }

    def __str__(self):
        values = self.get_dict()

        return '\n'.join([f'{value}: {values[value]}' for value in values if values[value] is not None]) \
            .join([separator] * 2)
