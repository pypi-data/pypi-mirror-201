import argparse

from .parser import parse_week
from .xmltv import to_xml

import logging

description = """
Collect and parse the EPG for cypriot channels to XMLTV. It supports the 
following channels: RIK1, RIK2, ERT World, Omega, Sigma, Extra, Plus, 
CapitalTV, 4E, Vouli, Alpha Cyprus, TV Mall, Action 24 and TNT Cyprus. Please
be diligent and respectful when using this utility, as it pulls its info from
cyta.com.cy. Overloading their servers wouldn't be nice. Refreshes don't happen
more than once a day anyway, so there's no point in running this utility more
than that."""

arg_parser = argparse.ArgumentParser(
    description=description,
    prog='cyxmltv',
    formatter_class=argparse.RawTextHelpFormatter)
arg_parser.add_argument('file', type=str,
                        help='The output file for the XMLTV formatted EPG')


def config_log():
    logging.basicConfig(level=logging.INFO, format='%(message)s')


def run():

    config_log()

    args = arg_parser.parse_args()
    channels = parse_week()
    to_xml(channels, args.file)


if __name__ == '__main__':
    run()
