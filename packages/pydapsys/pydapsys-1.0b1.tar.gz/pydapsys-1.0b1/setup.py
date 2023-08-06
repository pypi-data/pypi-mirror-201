# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydapsys', 'pydapsys.neo_convert', 'pydapsys.toc', 'pydapsys.util']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21,<2.0']

extras_require = \
{'neo': ['neo>=0.11.1,<0.12.0']}

setup_kwargs = {
    'name': 'pydapsys',
    'version': '1.0b1',
    'description': 'Read recordings made with DAPSYS',
    'long_description': '# PyDapsys - Read DAPSYS recordings with Python\n\n[![PyPI](https://img.shields.io/pypi/v/pydapsys?style=for-the-badge)](https://pypi.org/project/pydapsys/)\n\nPyDapsys is a package to read neurography recordings made with [DAPSYS](http://dapsys.net/) (Data Acquisition Processor System). It is based on a reverse-engineered specification of the binary data format used by the latest DAPSYS version.\n\nOptionally, the library provides functionality to store loaded data into [Neo](https://github.com/NeuralEnsemble/python-neo) datastrucutres, from where they can be exported into various other formats.\n\n## Installation\n\nEither download the wheel file for offline installation or use pypi.\n\n### Basic functionalities\n\nWill only offer the data representation of PyDapsys, without ability to convert to Neo. Has only numpy as sole dependency. \n\n`pip install pydapsys`\n\n`pip install {name_of_downloaded_wheel}.whl`\n\n### With Neo converters\n\nInstall base library with additional dependencies required to load data into Neo datastructures. Writing Neo datastructures to some formats may require additional dependencies. Please see the Neo documentation for further information.\n\n`pip install pydapsys[neo]`\n\n`pip install {name_of_downloaded_wheel}.whl[neo]`\n\n## Usage\n\n### Quickstart\n\nA DAPSYS file is made up of two parts: A sequential list of blocks or **pages**, which store either a text with a timestamp or a waveform with associated timestamps, and a table of contents (toc). The toc consists of **folders** and **streams**. Each page has an id unique in the context of the file. Streams in the toc have an array of ids of the pages belonging to the stream. A stream is either a text stream (referring only to text pages) or a data stream (referring only to recording pages).\n\n#### Load a file\nUse `File.from_binary` to read from a BinaryIO object.\n```python\nfrom pydapsys.file import File\nfrom pathlib import Path\nMY_DAPSYS_FILE = Path(".")/"to"/"my"/"dapsys_file.dps"\nwith open(MY_DAPSYS_FILE, \'rb\') as file:\n    file = File.from_binary(file)\n```\nThe `File` object has two fields, the root of the table of contents and a dictionary mapping the page ids to their respective pages.\n##### Inspect file structure\nTo inspect the ToC structure of a loaded file, use the `structure` property of the toc `Root`, preferable together with `pprint`:\n```python\nimport pprint\npprint.PrettyPrinter(indent=4).pprint(file.toc.structure)\n```\nThis will print the structure, names and types of all elements in the table of contents. For Streams, the number of associated pages it also printed after their type.\n#### Access data from a file\nTo access data, use the `File.get_data` method. The method takes a path from the toc structure (WITHOUT THE NAME OF THE ROOT!) and will return all associated pages.\nPlease note, that the path is  case insensitive\n```python\nfrom pydapsys.toc.entry import StreamType\nmy_texts = list(file.get_data("myrecording/my text stream", stype=StreamType.Text))\nmy_waveforms = list(file.get_data("myrecording/somewhere else/ my waveform stream", stype=StreamType.Waveform))\n```\n##### Text pages\n\nA text page consists of three fields:\n\n* `text`: The text stored in the page, string\n\n* `timestamp_a`: The first timestamp of the page, float64 (seconds)\n\n* `timestamp_b`: The second timestamp of the page (float64, seconds), which sometimes is not presented and is thus set to None\n\n##### Waveform pages\n\nWaveform pages consist of three fields:\n\n* `values`: Values of the waveform, float32 (volt)\n\n* `timestamps`: Timestamps corresponding to `values`, float64 (seconds)\n\n* `interval`: Interval between values, float64 (seconds)\n\nIn **continuously sampled waveforms**, only the timestamp of the first value will be present, in addition to the sampling `interval`. The timestamps of the other values can be calculated by this two values.\n\n**Irregularly sampled waveforms** will have one timestamp for each value, but no `interval`.\n\n## Neo converters\n\nThe module `pydapsys.neo_convert` contains classes to convert a Dapsys recording to the Neo format. **IMPORTANT: importing the module without installing neo first will raise an exception**\n\nAs Dapsys files may have different structures, depending on how it was configured and what hardware is used, different converters are required for each file structure.\n\nCurrently there is only one converter available, for recordings made using a NI Pulse stimulator.\n\n### NI Pulse stimulator\n\nConverter class for Dapsys recording created using an NI Pulse stimulator. Puts everything into one neo sequence. \nWaveform pages of the continuous recording are merged if the difference between a pair of consecutive pages is less than a specified threshold (`grouping_tolerance`).\n\n```python\nfrom pydapsys.neo_convert.ni_pulse_stim import NIPulseStimulatorToNeo\n\n# convert a recording to a neo block\nneo_block = NIPulseStimulatorToNeo(file, grouping_tolerance=1e-9).to_neo()\n```\n\n#### Expected file structure\n\n{stim_folder} must be one of "NI Puls Stimulator", "pulse stimulator", "NI Pulse stimulator", but can be changed by adding entries to `NIPulseStimulatorToNeo.stim_foler_names`\n\n* Root\n  \n  * [Text] Comments -> Converted into a single event called "comments"\n  \n  * {stim_folder}\n    \n    * [Text] Pulses -> Converted into one neo event streams, one per unique text\n    \n    * [Waveform] Continuous recording -> Converted into multiple AnalogSignals\n    \n    * Responses\n      \n      * Tracks for All Responses -> Optional. Will silently ignore spike trains if this folder does not exist\n        \n        * ... [Text] tracks... -> Converted into spike trains\n',
    'author': 'Peter Konradi',
    'author_email': 'codingchipmunk@posteo.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Digital-C-Fiber/PyDapsys',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
