# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dateparse']

package_data = \
{'': ['*']}

install_requires = \
['datetime>=4.9,<5.0']

setup_kwargs = {
    'name': 'dateparse',
    'version': '1.3.0',
    'description': 'A pure Python library for parsing natural language time expressions, with minimal dependencies',
    'long_description': 'Dateparse\n===========\n\nA python library for parsing natural language time descriptions. \n\nInstallation\n-------------\nDateparse is on PyPi; install with Pip: :code:`$ pip install dateparse`\n\nUsage\n------ \n>>> import dateparse\n>>> from datetime import date\n\n>>> # The main use case is extracting a single date from a string\n>>> dateparse.basic_parse(date.today(), "a week from friday")\nDateResult(date=datetime.date(2023, 2, 10), start=0, end=15, content=\'a week from fri\')\n\n>>> # by default the first (leftmost) encountered date is returned\n>>> dateparse.basic_parse(date.today(), "a week from thursday and a week from friday")\nDateResult(date=datetime.date(2023, 2, 9), start=0, end=15, content=\'a week from thu\') \n\n>>> # the from_right option changes this\n>>> dateparse.get_first(date.today(), "a week from thursday and a week from friday")\nDateResult(date=datetime.date(2023, 2, 10), start=0, end=15, content=\'a week from fri\')\n\n>>> # default behavior for all parse functions is to get the next future date matching the expression\n>>> # relative to the given base date\n>>> # this can be changed with the allow_past option\n>>> dateparse.basic_parse(date(1970, 9, 8), "january 1", allow_past=True)\nDateResult(date=datetime.date(1970, 1, 1), start=0, end=9, content=\' january 1\')\n\n>>> # parse_all gets all expressions in a list\n>>> dateparse.parse_all(date.today(), "a week from thursday and four days before march 11")\n[DateResult(date=datetime.date(2023, 2, 9), start=0, end=15, content=\'a week from thu\'), DateResult(date=datetime.date(2023, 3, 7), start=24, end=50, content=\'four days before march 11\')]\n\n>>> # the default return type for dates is a DateResult, a simple named tuple containing the date\'s info\n>>> # For convenience, there are also functions to just get the date\n>>> dateparse.basic_date_parse(date.today(), "february 9")\ndatetime.date(2023, 2, 9)\n\n>>> # parse_all_dates works in the same way\n>>> # a DateParser object holds a specified baseline date \n>>> # by default, assumes the baseline date is date.today()\n>>> parser = dateparse.DateParser() \n\n>>> # parses dates with a reference point of january 17, 2021 \n>>> parser_january = dateparse.DateParser(base_date = date(2021, 17, 1)) \n\n>>> # DateParser also supports named days by default\n>>> parser.get_first("four days after halloween 2024")\nDateResult(date=datetime.date(2024, 11, 4), start=0, end=31, content=\'four days after october 31 2024\')\n\n>>> # You can also define your own custom named days as a string dictionary and pass it into the parser\n>>> my_dates = {\'my birthday\' : \'june 11\'}\n>>> my_parser = dateparse.DateParser(named_days = my_dates)\n>>> my_parser.get_first("a month before my birthday")\nDateResult(date=datetime.date(2023, 5, 14), start=0, end=22, content=\'a month before june 11\')\n\n>>> # DateParser.get_first and DateParser.get_last are convenience wrappers around basic_parse\n>>> # to get the first or last expression, with the base date defined at initialization\n>>> my_parser.get_first("a week from thurs and two months after friday")\nDateResult(date=datetime.date(2023, 2, 9), start=0, end=15, content=\'a week from thu\')\n>>> my_parser.get_last("a week from thurs and two months after friday")\nDateResult(date=datetime.date(2023, 4, 3), start=21, end=42, content=\'two months after fri\')\n\n>>> # DateParser.get_all and DateParser.get_all_dates wrap parse_all and parse_all_dates\n>>> my_parser.get_all("a week from thurs and two months after friday")\n[DateResult(date=datetime.date(2023, 2, 9), start=0, end=15, content=\'a week from thu\'), DateResult(date=datetime.date(2023, 4, 3), start=21, end=42, content=\'two months after fri\')]\n>>> my_parser.get_all_dates("a week from thurs and two months after friday")\n[datetime.date(2023, 2, 9), datetime.date(2023, 4, 3)]\n\n\nOther Info\n----------\n**This project is under active development.** The core API is unlikely to change much at this point, but the under-the-hood details are still very much in flux. \n\nDateparse requires Python 3.10 or higher, thanks the author\'s neurotic devotion to type annotations. \n',
    'author': 'keagud',
    'author_email': 'keagud@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
