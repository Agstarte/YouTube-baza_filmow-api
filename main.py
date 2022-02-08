import os

from yt_database.database_generator import DatabaseGenerator
import logging

logging.basicConfig(level='DEBUG')
in_csvs = {
    # 'DE': ['channels/germany/2021-12-17/subscribers channels rank.csv',
    #        'channels/germany/2021-12-17/views_avg channels rank.csv'],
    # 'PL': ['channels/poland/2021-12-17/subscribers channels rank.csv',
    #        'channels/poland/2021-12-17/views_avg channels rank.csv'],
    # 'GB': ['channels/united kingdom/2021-12-17/subscribers channels rank.csv',
    #        'channels/united kingdom/2021-12-17/views_avg channels rank.csv'],
    'CH': ['channels/switzerland/2021-12-17/subscribers channels rank.csv',
           'channels/switzerland/2021-12-17/views_avg channels rank.csv'],
}

languages = {
    'DE': ['de'],
    'PL': ['pl'],
    'GB': ['en'],
}

for csv in in_csvs:
    generator = DatabaseGenerator(in_csvs[csv], csv)
    generator.generate_database()
    #
    generator._generate_csvs()

