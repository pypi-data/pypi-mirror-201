# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newsdash']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0', 'loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'newsdash',
    'version': '0.1.0',
    'description': 'NewsDash is a fast and reliable Python wrapper for the News API that simplifies accessing the latest news articles from around the world.',
    'long_description': '![NewsDash](./readme-assets/poster.jpg)\n# NewsDash\n**note**:This is a WIP library, please report bugs if you find one\n[![Python 3.9-3.11](https://img.shields.io/badge/Python-3.9--3.11-blue.svg)]()\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![GitHub stars](https://img.shields.io/github/stars/NaviTheCoderboi/NewsDash.svg)](https://github.com/NaviTheCoderboi/NewsDash)\n![GitHub last commit](https://img.shields.io/github/last-commit/NaviTheCoderboi/NewsDash.svg)\n\n***\nNewsDash is a fast and reliable Python wrapper for the News API that simplifies accessing the latest news articles from around the world. 📰\n***\nMade by: NaviTheCoderboi\n***\n# Features\n\n- **Fast performance:** This API wrapper is designed to be fast and efficient, allowing users to retrieve news articles quickly and easily.\n- **Reliable functionality:** The wrapper uses best practices to ensure reliable functionality and accuracy in retrieving news articles from the API.\n- **Easy-to-use interface:** The API wrapper has an intuitive interface that makes it easy for developers to interact with the API and retrieve news articles without having to worry about the details of the underlying protocol.\n- **Built with aiohttp:** The wrapper is built using the popular aiohttp library, which provides high-performance asynchronous HTTP client/server for asyncio and Python. This means the wrapper takes advantage of the latest and greatest in async programming techniques to provide fast and efficient performance.\n- **Customizable functionality:** The wrapper has a range of customization options, allowing developers to tailor their use of the API to their specific needs.\n- **Flexible data handling:** The wrapper is designed to handle a wide variety of data formats, allowing developers to work with the data in the way that best suits their needs.\n- **Well-documented:** The wrapper has clear and comprehensive documentation, making it easy for developers to get up and running quickly and troubleshoot any issues that may arise.\n# Installation\n```bash\npython -m pip install newsdash\n```\n# Examples\n- with client\n```python\nfrom newsdash import NewsDash\nimport asyncio\n\ncl = NewsDash("your_api_key")\nasync def get_news():\n  print(await cl.get_everything(query="tech",pageSize=5))\n  print(await cl.get_top_headlines(query="Microsoft"))\n  print(await cl.get_sources(country="in",language="en"))\n\nasyncio.run(get_news())\n```\n- with async context manager\n```python\nfrom newsdash import NewsDash\nimport asyncio\n\nasync def main():\n  async with NewsDash("api_key") as nd:\n    print(await nd.get_everything(query="apple"))\n\nasyncio.run(main())\n```\n# Important urls\n- [NewsApi](https://newsapi.org)\n- [NewsDash repository](https://github.com/NaviTheCoderboi/NewsDash)\n- [NewsDash pypi](https://pypi.org/project/NewsDash)',
    'author': 'NaviTheCoderboi',
    'author_email': 'navindersingh568@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NaviTheCoderboi/NewsDash',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
