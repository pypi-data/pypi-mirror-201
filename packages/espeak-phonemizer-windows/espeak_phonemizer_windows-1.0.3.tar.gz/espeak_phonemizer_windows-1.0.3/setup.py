# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['espeak_phonemizer']

package_data = \
{'': ['*'],
 'espeak_phonemizer': ['espeak-ng/*',
                       'espeak-ng/espeak-ng-data/*',
                       'espeak-ng/espeak-ng-data/lang/*',
                       'espeak-ng/espeak-ng-data/lang/aav/*',
                       'espeak-ng/espeak-ng-data/lang/art/*',
                       'espeak-ng/espeak-ng-data/lang/azc/*',
                       'espeak-ng/espeak-ng-data/lang/bat/*',
                       'espeak-ng/espeak-ng-data/lang/bnt/*',
                       'espeak-ng/espeak-ng-data/lang/ccs/*',
                       'espeak-ng/espeak-ng-data/lang/cel/*',
                       'espeak-ng/espeak-ng-data/lang/cus/*',
                       'espeak-ng/espeak-ng-data/lang/dra/*',
                       'espeak-ng/espeak-ng-data/lang/esx/*',
                       'espeak-ng/espeak-ng-data/lang/gmq/*',
                       'espeak-ng/espeak-ng-data/lang/gmw/*',
                       'espeak-ng/espeak-ng-data/lang/grk/*',
                       'espeak-ng/espeak-ng-data/lang/inc/*',
                       'espeak-ng/espeak-ng-data/lang/ine/*',
                       'espeak-ng/espeak-ng-data/lang/ira/*',
                       'espeak-ng/espeak-ng-data/lang/iro/*',
                       'espeak-ng/espeak-ng-data/lang/itc/*',
                       'espeak-ng/espeak-ng-data/lang/jpx/*',
                       'espeak-ng/espeak-ng-data/lang/map/*',
                       'espeak-ng/espeak-ng-data/lang/miz/*',
                       'espeak-ng/espeak-ng-data/lang/myn/*',
                       'espeak-ng/espeak-ng-data/lang/poz/*',
                       'espeak-ng/espeak-ng-data/lang/roa/*',
                       'espeak-ng/espeak-ng-data/lang/sai/*',
                       'espeak-ng/espeak-ng-data/lang/sem/*',
                       'espeak-ng/espeak-ng-data/lang/sit/*',
                       'espeak-ng/espeak-ng-data/lang/tai/*',
                       'espeak-ng/espeak-ng-data/lang/trk/*',
                       'espeak-ng/espeak-ng-data/lang/urj/*',
                       'espeak-ng/espeak-ng-data/lang/zle/*',
                       'espeak-ng/espeak-ng-data/lang/zls/*',
                       'espeak-ng/espeak-ng-data/lang/zlw/*',
                       'espeak-ng/espeak-ng-data/voices/!v/*']}

setup_kwargs = {
    'name': 'espeak-phonemizer-windows',
    'version': '1.0.3',
    'description': 'Uses espeak-ng to transform text into IPA phonemes.',
    'long_description': "# eSpeak Phonemizer Windows\n\n\nUses [espeak-ng](https://github.com/espeak-ng/espeak-ng) to transform text into [IPA](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet) phonemes.\n\nThis is a fork of [espeak-phonemizer](https://github.com/rhasspy/espeak-phonemizer) that adds support for Windows.\n\n## Installation\n\n```sh\npip install espeak_phonemizer_windows\n```\n\nIf installation was successful, you should be able to run:\n\n```sh\nespeak-phonemizer --version\n```\n\n## Basic Phonemization\n\nSimply pass your text into the standard input of `espeak-phonemizer`:\n\n```sh\necho 'This is a test.' | espeak-phonemizer -v en-us\nðɪs ɪz ɐ tˈɛst\n```\n\n### Separators\n\nPhoneme and word separators can be changed:\n\n```sh\necho 'This is a test.' | espeak-phonemizer -v en-us -p '_' -w '#'\nð_ɪ_s#ɪ_z#ɐ#t_ˈɛ_s_t\n```\n\n### Punctuation and Stress\n\nSome punctuation can be kept (.,;:!?) in the output:\n\n```sh\necho 'This: is, a, test.' | espeak-phonemizer -v en-us --keep-punctuation\nðˈɪs: ˈɪz, ˈeɪ, tˈɛst.\n```\n\nStress markers can also be dropped:\n\n```sh\necho 'This is a test.' | espeak-phonemizer -v en-us --no-stress\nðɪs ɪz ɐ tɛst\n```\n\n### Delimited Input\n\nThe `--csv` flag enables delimited input with fields separated by a '|' (change with `--csv-delimiter`):\n\n```sh\necho 's1|This is a test.' | espeak-phonemizer -v en-us --csv\ns1|This is a test.|ðɪs ɪz ɐ tˈɛst\n```\n\nPhonemes are added as a final column, allowing you to pass arbitrary metadata through to the output.\n\n",
    'author': 'mush42',
    'author_email': 'ibnomer2011@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mush42/espeak-phonemizer-windows',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
