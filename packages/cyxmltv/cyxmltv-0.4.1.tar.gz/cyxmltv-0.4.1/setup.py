from pathlib import Path

from setuptools import setup

from cyxmltv import version


setup(name='cyxmltv',
      version=version.VERSION,
      entry_points={
          'console_scripts': ['cyxmltv=cyxmltv.__main__:run']
      },
      description='Command line utility to create an XmlTv formatted EPG for '
                  'cypriot channels',
      long_description=Path('README.md').read_text(encoding='utf-8'),
      long_description_content_type='text/markdown',
      author='Harry Papaxenopoulos',
      author_email='hpapaxen@gmail.com',
      packages=['cyxmltv'],
      keywords='cyprus xmltv plex cypriot epg rik1 rik',
      license='MIT',
      install_requires=[
          'lxml',
          'requests',
          'beautifulsoup4',
          'pytz'
      ],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      )
