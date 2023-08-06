# Project CyXmlTv

This project is for generating an [xmltv](http://wiki.xmltv.org) compatible
electronic programming guide for cypriot channels. It's primarily used for
operating the Plex DVR.

## How to install

* Option 1: Install through pip with `pip install cyxmltv`
* Option 2: Download the source code and create a distribution via 
`python setup.py sdist`. Then install via 
`pip install dist/cyxmltv-<version>.tar.gz`.

## How to run

Simply run `cyxmltv <filename>`, where `<filename>` is the target file name 
you want to use. Then, you can use the aforementioned file in Plex's
[DVR setup](https://support.plex.tv/articles/225877347-live-tv-dvr/)
