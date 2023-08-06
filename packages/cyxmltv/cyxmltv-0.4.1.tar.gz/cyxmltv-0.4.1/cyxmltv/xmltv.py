import logging
from typing import List

import pytz
from lxml import etree
from lxml.etree import Element

from .common import Channel
from datetime import datetime

ET = pytz.timezone('Europe/Athens')


def to_programme_date(program_time: datetime) -> str:
    return ET.localize(program_time).strftime('%Y%m%d%H%M%S %z')


def create_programme_tags(channel: Channel, tv: Element):

    for show in channel.shows:
        pr_tag = etree.SubElement(tv, 'programme')
        pr_tag.attrib['start'] = to_programme_date(show.start_time)
        pr_tag.attrib['stop'] = to_programme_date(show.end_time)
        pr_tag.attrib['channel'] = channel.id
        title = etree.SubElement(pr_tag, 'title')
        title.attrib['lang'] = "el"
        title.text = show.name

        desc = etree.SubElement(pr_tag, 'desc')
        desc.attrib['lang'] = 'el'
        desc.text = show.description.replace('\n', '').replace('\t', '')


def create_channel_tags(channel: Channel, tv: Element):
    ch_tag = etree.SubElement(tv, "channel")
    ch_tag.attrib['id'] = channel.id
    name_tag = etree.SubElement(ch_tag, 'display-name')
    name_tag.text = channel.name
    icon_tag = etree.SubElement(ch_tag, 'icon')
    icon_tag.attrib['src'] = channel.icon


def to_xml(channels: List[Channel], tgt_file:str) -> Element:
    tv = etree.Element('tv')
    tv.attrib['source-info-url'] = 'https://www.github.com/hpapaxen/cyxmltv'
    tv.attrib['source-info-name'] = 'Cyprus XMLTV'

    logging.info('Creating xml tags for channels')

    for channel in channels:
        create_channel_tags(channel, tv)

    logging.info('Creating xml tags for shows')

    for channel in channels:
        create_programme_tags(channel, tv)

    tree = etree.ElementTree(tv)

    logging.info("Writing result to %s", tgt_file)
    tree.write(tgt_file,
               pretty_print=True,
               xml_declaration=True,
               encoding='UTF-8',
               doctype='<!DOCTYPE tv SYSTEM "https://raw.githubusercontent.com/XMLTV/xmltv/master/xmltv.dtd">')
