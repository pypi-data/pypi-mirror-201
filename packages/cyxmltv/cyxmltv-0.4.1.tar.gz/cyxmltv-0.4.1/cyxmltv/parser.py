from datetime import date, datetime, timedelta
from typing import List

import logging
import requests
from bs4 import BeautifulSoup, Tag

from .common import Channel, TVShow, ChannelMappings


def to_date_time(base_date: date, minutes: str) -> datetime:
    today = datetime.combine(base_date, datetime.min.time())
    return today + timedelta(minutes=int(minutes))


def populate_shows(channel: Channel, tag: Tag, base_date: date):
    for program_tag in tag.find_all('div', attrs={'class': 'program'}):
        title_tag = program_tag.find('span', attrs={'class': 'program_title'})
        if not title_tag:
            continue

        title = title_tag.getText()
        start_time = to_date_time(base_date, program_tag.attrs['data-start'])
        minutes = int(program_tag.attrs['data-dur'])
        end_time = timedelta(minutes=minutes) + start_time
        content = program_tag.find('div', attrs={'class': 'data'}).getText()
        channel.shows.append(TVShow(start_time, end_time, title, content))


def parse_shows(tag: Tag, channels: List[Channel], base_date: date):
    ch_program_tags = tag.find_all('div', attrs={'class': 'epgrow'})

    filtered = [f for f in ch_program_tags if 'fakeepgrow' not in f['class']]

    for i in range(0, len(channels)):
        populate_shows(channels[i], filtered[i], base_date)


def find_channel(channels: List[Channel], ch_id: str):
    return next((c for c in channels if c.id == ch_id), None)


def merge(base_list: List[Channel], new_list: List[Channel]):
    for new_channel in new_list:
        old_channel = find_channel(base_list, new_channel.id)
        if old_channel:
            old_channel.shows.extend(new_channel.shows)
        else:
            base_list.append(new_channel)


def parse_week() -> List[Channel]:

    logging.info('Downloading epg information...')

    channels = []
    for i in range(0, 6):
        merge(channels, parse_tv(i))

    return channels


def parse_tv(day: int) -> List:
    content = download(day)
    soup = BeautifulSoup(content, 'html.parser')

    logging.debug("Parsing channels for day %d", day)

    left_tag = soup.find('div', attrs={'id':'left'})
    channels = parse_channels(left_tag)

    right_tag = soup.find('div', attrs={'id': 'right'})
    base_date = date.today() + timedelta(days=day)

    logging.debug("Parsing shows for day %d", day)
    parse_shows(right_tag, channels, base_date)

    return channels


def parse_channels(tag: Tag) -> List[Channel]:

    channels = []

    ch_tags = tag.find_all('a', attrs={'class': 'channel_link'})
    for ch_tag in ch_tags:
        ch_id = ch_tag.attrs['data-reveal-id']
        img = ch_tag.find('div', attrs={'class': 'channel'}).attrs['style']
        img = img.replace('background-image: url(', '')
        img = img.replace(');', '')
        img = img.replace('\'', '')

        name = ChannelMappings.get(ch_id)

        channels.append(Channel(name, ch_id, img, []))

    return channels


def download(day: int) -> str:

    logging.debug("Downloading schedule for day %d", day)

    base_url = "https://data.cytavision.com.cy/epg/index.php"
    url = "{}?site=cyprus&category=1&lang=en&day={}".format(base_url, day)
    r = requests.get(url, verify=False)
    r.encoding = 'UTF8'

    return r.text
