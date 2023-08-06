# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytika']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'typing-extensions>=4.5.0,<5.0.0']

setup_kwargs = {
    'name': 'pytika',
    'version': '0.2.0',
    'description': 'Apache Tika Server python client',
    'long_description': '# PyTika\n\n![Workflow status](https://github.com/agriplace/pytika/actions/workflows/main.yml/badge.svg)\n![PyPi wheel](https://img.shields.io/pypi/wheel/pytika)\n\nAn Apache Tika Server python client.\n\n## Installation\n\nYou can install the package simply from pypi:\n```pip install pytika```\n\n\n## Usage\nThis package is a python client for Apache Tika Server, so you\'ll need to have Tika Server running locally somehow.\nI would recommend using the docker image as that\'s the simplest.\n```docker run --name tika-server -it -d -p 9998:9998 apache/tika:2.7.0-full```\n\nAfter you have that running, you can use PyTika to interface with it.\n\n### Metadata queries\n```python\nfrom pytika.api import TikaApi\n\ntika = TikaApi()\nmetadata = api.get_meta(file)\n\n"""\n>>> metadata\n{\n    \'Content-Type\': \'application/pdf\',\n    ...\n}\n"""\n```\n\n### Text detection queries\n\nFor text detection, Tika Server usually decides on the response type (typically xml/html is the default).\nTo force it to return plain text (Accept: text/plain header) you can set the following configuration:\n\n```python\nfrom pytika.api import TikaApi\nfrom pytika.config import GetTextOptionsBuilder as opt\n\ntika = TikaApi()\n\nwith open("yourfile.whatever", "rb") as file:\n    text = api.get_text(file, opt.AsPlainText()).decode()\n\n```\n\nNotice the awkward configuration - passing a function call as an option - this is coming from a nice Golang standard that makes calling complex APIs a little friendlier. Since we have a lot of options, instead of having each be an argument, we can define an "option class" with chainable functions. This allows the API to validate each separately, avoid having a massive list of arguments for get_text, as well as tidy up the API code. (For more info: [Uptrace](https://uptrace.dev/blog/golang-functional-options.html), [Dave Cheney\'s post](https://dave.cheney.net/2014/10/17/functional-options-for-friendly-apis))\n\n\nFor detection in HOCR format with bounding boxes:\n\n```python\nfrom pytika.api import TikaApi\nfrom pytika.config import GetTextOptionsBuilder as opt\n\ntika = TikaApi()\n\nwith open("yourfile.whatever", "rb") as file:\n    text = api.get_text(file, opt.WithBoundingBoxes()).decode()\n\n```\n\n\nThere are many more configuration options that you can look into in the GetTextOptionsBuilder class, and more to come in the future.\n\n\n\n## Contribution Guide\n\nIf you\'d like to add some missing features that you can find in TikaServer or Tika, then you can contribute to this repo yourself!\n\n1- Clone the repository\n```\ngit clone "url from repo, either ssh or https"\n```\n\n2- Create a branch\n```\ncd pytika\ngit switch -c your-new-branch-name\n```\n\n3- Make necessary changes and commit, and push to Github\n```\ngit add README.md\ngit commit -m "Updated README.md with new API changes"\ngit push -u origin your-new-branch-name\n```\n\n4- Go to your repository and you\'ll see a `Compare and pull request` button, click on that.\n\n5- Wait for us to review your PR, likely leave comments, and hopefully merge it in!\n\n',
    'author': 'RamiAwar',
    'author_email': 'rami.awar.ra@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
