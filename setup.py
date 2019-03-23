# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['profanity_filter']

package_data = \
{'': ['*'],
 'profanity_filter': ['data/en_profane_words.txt',
                      'data/en_profane_words.txt',
                      'data/ru_profane_words.txt',
                      'data/ru_profane_words.txt']}

install_requires = \
['cached-property>=1.5,<2.0',
 'ordered-set-stubs>=0.1.3,<0.2.0',
 'ordered-set>=3.0,<4.0',
 'poetry-version>=0.1.3,<0.2.0',
 'spacy>=2.0,<3.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.6.0,<0.7.0']}

setup_kwargs = {
    'name': 'profanity-filter',
    'version': '1.0.11',
    'description': 'A Python library for detecting and filtering profanity',
    'long_description': '# profanity-filter: A Python library for detecting and filtering profanity\n[![Build Status](https://travis-ci.org/rominf/profanity-filter.svg?branch=master)](https://travis-ci.org/rominf/profanity-filter)\n\n<b>PyPI:</b> https://pypi.python.org/pypi/profanity-filter<br>\n\n## Installation\n`profanity-filter` library is universal, it can detect and filter profanity in any language.\nTo accomplish this task it needs profane word dictionaries and language tools with models installed.\n`profanity-filter` is already packaged with English and Russian profane word dictionaries.\n\nFor minimal setup for English you need to install `profanity-filter` with is bundled with `spacy` and download `spacy`\nmodel for tokenization and lemmatization:\n```\n$ pip install profanity-filter\n$ python -m spacy download en\n```\n\nFor more info about `spacy` models read: https://spacy.io/usage/models/.\n\n## Usage\n\n```python\nfrom profanity_filter import ProfanityFilter\n\npf = ProfanityFilter()\n\npf.censor("That\'s bullshit!")\n# "That\'s ********!"\n\npf.censor_char = \'@\'\npf.censor("That\'s bullshit!")\n# "That\'s @@@@@@@@!"\n\npf.censor_char = \'*\'\npf.custom_profane_word_dictionaries = {\'en\': {\'love\', \'dog\'}}\npf.censor("I love dogs and penguins!")\n# "I **** **** and penguins"\n\npf.restore_profane_word_dictionaries()\npf.is_clean("That\'s awesome!")\n# True\n\npf.is_clean("That\'s bullshit!")\n# False\n\npf.is_profane("That\'s bullshit!")\n# True\n\npf.extra_profane_word_dictionaries = {\'en\': {\'chocolate\', \'orange\'}}\npf.censor("Fuck orange chocolates")\n# "**** ****** **********"\n```\n\n## Deep analysis\nDeep analysis detects profane words that are inflected from profane words in profane word dictionary.\n\nTo get deep analysis functionality install additional libraries and dictionary for your language.\n\nFirstly, install `hunspell` and `hunspell-devel` packages with your system package manager.\n\nFor Amazon Linux AMI run:\n```shell\n$ yum install hunspell\n```\n\nThen run (for English):\n```shell\n$ pip install -U -r https://raw.githubusercontent.com/rominf/profanity-filter/master/requirements-deep-analysis.txt\n$ cd profanity_filter/data\n$ wget https://cgit.freedesktop.org/libreoffice/dictionaries/plain/en/en_US.aff\n$ wget https://cgit.freedesktop.org/libreoffice/dictionaries/plain/en/en_US.dic\n$ mv en_US.aff en.aff\n$ mv en_US.dic en.dic\n```\n\nThen use profanity filter as usual:\n```python\nfrom profanity_filter import ProfanityFilter\n\npf = ProfanityFilter()\n\npf.censor("fuckfuck")\n# "********"\n\npf.censor_whole_words = False\npf.censor("oofucksoo")\n# "oo*****oo"\n```\n\n## Multilingual support\nThis library comes with multilingual support, which is enabled automatically after installing `polyglot` package and \nit\'s requirements for language detection. See https://polyglot.readthedocs.io/en/latest/Installation.html for \ninstructions.\n\nFor Amazon Linux AMI run:\n```shell\n$ yum install libicu-devel\n```\n\nThen run:\n```shell\n$ pip install -U -r https://raw.githubusercontent.com/rominf/profanity-filter/master/requirements-multilingual.txt\n```\n\n### Add language\nLet\'s take Russian language for example, to show how to add language support.\n\n#### Russian language support\nFirstly, we need to provide file `profanityfilter/data/ru_badwords.txt` which contains newline separated list of profane\nwords. For Russian language it\'s already present, so we skip file generation.\n\nNext, we need to download appropriate Spacy model. Unfortunately, Spacy model for Russian is not yet ready, \nso we will use English model for tokenization and `hunspell` and `pymorphy2` for lemmatization.\n\nNext, we download dictionaries for deep analysis:\n```shell\n> cd profanity_filter/data\n> wget https://cgit.freedesktop.org/libreoffice/dictionaries/plain/ru_RU/ru_RU.aff\n> wget https://cgit.freedesktop.org/libreoffice/dictionaries/plain/ru_RU/ru_RU.dic\n> mv ru_RU.aff ru.aff\n> mv ru_RU.dic ru.dic\n```\n\n##### Pymorphy2\nFor Russian and Ukrainian languages to achieve better results we suggest you to install `pymorphy2`.\nTo install `pymorphy2` with Russian dictionary run:\n```shell\n$ pip install -U -r https://raw.githubusercontent.com/rominf/profanity-filter/master/requirements-pymorphy2-ru.txt\n```\n\n### Usage\nLet\'s create `ProfanityFilter` to filter Russian and English profanity. \n```python\nfrom profanity_filter import ProfanityFilter\n\npf = ProfanityFilter(languages=[\'ru\', \'en\'])\n\npf.censor("Да бля, это просто shit какой-то!")\n# "Да ***, это просто **** какой-то!"\n```\n\nNote, that order of languages in `languages` argument does matter. If a language tool (profane words list, Spacy model, \nHunSpell dictionary or pymorphy2 dictionary) is not found for a language that was detected for part of text, \n`profanityfilter` library automatically fallbacks to the first suitable language in `languages`.\n\nAs a consequence, if you want to filter just Russian profanity, you still need to specify some other language in \n`languages` argument to fallback on for loading Spacy model to perform tokenization, because, as noted before, there is \nno Spacy model for Russian.\n\n# Console Executable\n\n```bash\n$ profanity_filter -h\nusage: profanity_filter [-h] [-t TEXT | -f PATH] [-l LANGUAGES] [-o OUTPUT_FILE] [--show]\n\nProfanity filter console utility\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -t TEXT, --text TEXT  Test the given text for profanity\n  -f PATH, --file PATH  Test the given file for profanity\n  -l LANGUAGES, --languages LANGUAGES\n                        Test for profanity using specified languages (comma\n                        separated)\n  -o OUTPUT_FILE, --output OUTPUT_FILE\n                        Write the censored output to a file\n  --show                Print the censored text\n```\n\n# Credits\nEnglish profane word dictionary: https://github.com/areebbeigh/profanityfilter/ (author Areeb Beigh).\n\nRussian profane word dictionary: https://github.com/PixxxeL/djantimat (author Ivan Sergeev).\n',
    'author': 'Roman Inflianskas',
    'author_email': 'infroma@gmail.com',
    'url': 'https://github.com/rominf/profanity-filter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
