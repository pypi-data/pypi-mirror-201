# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ausdex']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'cached-property>=1.5.2,<2.0.0',
 'importlib-metadata<4.3',
 'kaleido==0.2.1',
 'modin>=0.18.1,<0.19.0',
 'numpy>=1.22.0,<2.0.0',
 'openpyxl>=3.0.0,<4.0.0',
 'pandas>=1.3.2,<2.0.0',
 'plotly>=5.4.0,<6.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'typer>=0.4.0,<0.5.0',
 'xlrd>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['ausdex = ausdex.main:app']}

setup_kwargs = {
    'name': 'ausdex',
    'version': '1.2.0',
    'description': 'A Python package for adjusting Australian dollars for inflation',
    'long_description': '# ausdex\n\n![pipline](https://github.com/rbturnbull/ausdex/actions/workflows/pipeline.yml/badge.svg)\n[<img src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/rbturnbull/49262550cc8b0fb671d46df58de213d4/raw/coverage-badge.json">](<https://rbturnbull.github.io/ausdex/coverage/>)\n[<img src="https://github.com/rbturnbull/ausdex/actions/workflows/docs.yml/badge.svg">](<https://rbturnbull.github.io/ausdex/>)\n[<img src="https://img.shields.io/badge/code%20style-black-000000.svg">](<https://github.com/psf/black>)\n[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)\n[![status](https://joss.theoj.org/papers/817baa72d2b17b535af8f421a43404b0/status.svg)](https://joss.theoj.org/papers/817baa72d2b17b535af8f421a43404b0)\n\nA Python package for adjusting Australian dollars for inflation.\n\nThe Australian Bureau of Statistics (ABS) publishes the Consumer Price Index (CPI) \nfor Australia and its capital cities which allows for adjustment of the value of Australian dollars for inflation. \n`ausdex` makes these data available with an inflation calculator in a convenient Python package with simple programmatic and command-line interfaces.\n\nABS datasets are generally housed in Microsoft Excel spreadsheets linked from the data catalogue. Working with these spreadsheets directly is cumbersome. The `ausdex` package provides an Application Programming Interface (API) for Australian CPI data that seemlessly interoperates with `NumPy` and `pandas`. It makes working with Australian dollars in Python convenient in a similar manner to the [cpi](https://github.com/palewire/cpi) Python package which adjusts US dollars for inflation.\n\nThe package is documented here: https://rbturnbull.github.io/ausdex\n\n## Installation\n\nYou can install `ausdex` from the Python Package Index (PyPI):\n\n```\npip install ausdex\n```\n\n`ausdex` requires Python 3.8 or higher.\n\nTo install ausdex for development, see the documentation for [contributing](https://rbturnbull.github.io/ausdex/contributing.html).\n\n## Command Line Usage\n\nAdjust single values using the command line interface:\n```\nausdex inflation VALUE ORIGINAL_DATE\n```\nThis adjust the value from the original date to the equivalent for the most recent quarter.\n\nFor example, to adjust $26 from July 21, 1991 to the latest quarter run:\n```\n$ ausdex inflation 26 "July 21 1991" \n$ 52.35\n```\n\nTo choose a different date for evaluation use the `--evaluation-date` option. This adjusts the value to dollars in the quarter corresponding to that date. For example, this command adjusts $26 from July 1991 to dollars in September 1999:\n```\n$ ausdex inflation 26 "July 21 1991"  --evaluation-date "Sep 1999"\n$ 30.27\n```\n\nBy default, `ausdex` uses the CPI for Australia in general but you can calculate the inflation for specific capital cities with the `--location` argument:\n```\n$ ausdex inflation 26 "July 21 1991"  --evaluation-date "Sep 1999" --location sydney\n$ 30.59\n```\n\nLocation options are: \'Australia\', \'Sydney\', \'Melbourne\', \'Brisbane\', \'Adelaide\', \'Perth\', \'Hobart\', \'Darwin\', and \'Canberra\'.\n\n\n## Module Usage\n\n```\n>>> import ausdex\n>>> ausdex.calc_inflation(26, "July 21 1991")\n52.35254237288135\n>>> ausdex.calc_inflation(26, "July 21 1991", evaluation_date="Sep 1999")\n30.27457627118644\n>>> ausdex.calc_inflation(26, "July 21 1991", evaluation_date="Sep 1999", location="sydney")\n30.59083191850594\n```\nThe dates can be as strings or Python datetime objects.\n\nThe values, the dates and the evaluation dates can be vectors by using NumPy arrays or Pandas Series. e.g.\n```\n>>> df = pd.DataFrame(data=[ [26, "July 21 1991"],[25,"Oct 1989"]], columns=["value","date"] )\n>>> df[\'adjusted\'] = ausdex.calc_inflation(df.value, df.date)\n>>> df\n   value          date   adjusted\n0     26  July 21 1991  52.352542\n1     25      Oct 1989  54.797048\n```\n\n## Dataset and Validation\n\nThe Consumer Price Index dataset is taken from the [Australian Bureau of Statistics](https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia). It uses the nation-wide CPI value. The validation examples in the tests are taken from the [Australian Reserve Bank\'s inflation calculator](https://www.rba.gov.au/calculator/). This will automatically update each quarter as the new datasets are released.\n\nThe CPI data goes back to 1948. Using dates before this will result in a NaN.\n\nTo access the raw CPI data as a pandas DataFrame, use this function:\n```\ndf = ausdex.latest_cpi_df()\n```\n\nThe Excel spreadsheet for this is stored in the user\'s cache directory. \nIf you wish to download this Excel file to a specific location, use this function:\n```\nausdex.files.cached_download_cpi(local_path="cpi-data.xlsx")\n```\n\nFor more infomation about the methods to download data from the ABS, see the [API specification](https://rbturnbull.github.io/ausdex/reference.html).\n\n## Contributing\n\nSee the guidelines for contributing and our code of conduct in the [documentation](https://rbturnbull.github.io/ausdex/contributing.html).\n\n## License and Disclaimer\n\n`ausdex` is released under the Apache 2.0 license.\n\nWhile every effort has been made by the authors of this package to ensure that the data and calculations used to produce the results are accurate, as is stated in the license, we accept no liability or responsibility for the accuracy or completeness of the calculations. \nWe recommend that users exercise their own care and judgment with respect to the use of this package.\n \n## Credits\n\n`ausdex` was written by [Dr Robert Turnbull](https://findanexpert.unimelb.edu.au/profile/877006-robert-turnbull) and [Dr Jonathan Garber](https://findanexpert.unimelb.edu.au/profile/787135-jonathan-garber) from the [Melbourne Data Analytics Platform](https://mdap.unimelb.edu.au/).\n\nPlease cite from the article when it is released. Details to come soon.\n\n## Acknowledgements\n\nThis project came about through a research collaboration with [Dr Vidal Paton-Cole](https://findanexpert.unimelb.edu.au/profile/234417-vidal-paton-cole) and [Prof Robert Crawford](https://findanexpert.unimelb.edu.au/profile/174016-robert-crawford). We acknowledge the support of our colleagues at the Melbourne Data Analytics Platform: [Dr Aleksandra Michalewicz](https://findanexpert.unimelb.edu.au/profile/27349-aleks-michalewicz) and [Dr Emily Fitzgerald](https://findanexpert.unimelb.edu.au/profile/196181-emily-fitzgerald).\n',
    'author': 'Robert Turnbull',
    'author_email': 'robert.turnbull@unimelb.edu.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rbturnbull/ausdex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0.0',
}


setup(**setup_kwargs)
