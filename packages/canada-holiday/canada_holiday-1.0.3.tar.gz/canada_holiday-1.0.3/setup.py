# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['canada_holiday', 'canada_holiday.holiday_info']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'canada-holiday',
    'version': '1.0.3',
    'description': 'Python package for Canadian holidays',
    'long_description': '# canada-holiday\n\n![example workflow](https://github.com/kmsunmin/canada-holiday/actions/workflows/run-tests.yml/badge.svg)\n\na Python package for retrieving Canadian holidays information for all provinces for any given year.\n\n## Installation\n\n### With pip:\n```bash\npip install canada-holiday\n```\n\n### With poetry:\n```bash\npoetry add canada-holiday\n```\n\n## Usage\n\n```python\nimport datetime\nimport canada_holiday\n\non_holidays_2023 = canada_holiday.get_holidays("Ontario", 2023)\n# prints "Getting holiday information of Ontario province..."\nprint(on_holidays_2023)\n# [CanadaHoliday(New Year\'s Day, 2023-01-01, Sunday, all), CanadaHoliday(Family Day, 2023-02-20, Monday, Ontario), ...]\n\nmanitoba_holidays_2023_june = canada_holiday.get_holidays("MB", 2023, 2)\n# prints "Getting holiday information of Manitoba province..."\nprint(manitoba_holidays_2023_june)\n# [CanadaHoliday(Louis Riel Day, 2023-02-20, Monday, Manitoba)]\nlouis_riel_day = manitoba_holidays_2023_june[0]\nprint(louis_riel_day.name)\n# Louis Riel Day\nprint(louis_riel_day.month)\n# 2\nprint(louis_riel_day.day)\n# 20\nprint(louis_riel_day.date)\n# 2023-02-20\nprint(louis_riel_day.province)\n# Manitoba\nprint(louis_riel_day.day_of_the_week)\n# Monday\n\ndate = datetime.date(2023, 8, 7)\nresult = canada_holiday.is_holiday(date, "British Columbia")\n# prints "2023-08-07 is a holiday, B.C. Day in British Columbia province(s) in Canada"\nprint(result)\n# True\ndate = datetime.date(2023, 4, 5)\nresult = canada_holiday.is_holiday(date, "Nova Scotia")\n# prints "2023-04-05 is not a holiday in Nova Scotia province."\nprint(result)\n# False\n```\n',
    'author': 'Sunmin Kim',
    'author_email': 'kmsunmin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kmsunmin/canada-holiday',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
