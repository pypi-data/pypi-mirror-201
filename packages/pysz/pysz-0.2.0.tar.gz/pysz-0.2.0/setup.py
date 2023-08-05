# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pysz']

package_data = \
{'': ['*'], 'pysz': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['numpy>=1.24.2,<2.0.0', 'pandas>=2.0.0,<3.0.0', 'zstandard>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'pysz',
    'version': '0.2.0',
    'description': 'Package for reading and writing svb-zstd compressed data',
    'long_description': '# pysz\nPython interface for writing and reading svb-zstd compressed data\n\n## Installation\n\n```bash\n# First, install a customized version of pystreamvbyte\npip install git+https://github.com/kevinzjy/pystreamvbyte.git\n\n# Install pysz now\npip install pysz\n```\n\n## Usage\n\nExamples for creating new SZ file and saving some data\n\n```python\nimport numpy as np\nfrom pysz.api import CompressedFile\n\nheader = [(\'version\',  \'0.0.1\'), (\'date\', \'2023-04-03\')]\nattr = [(\'ID\', str), (\'Offset\', np.int32), (\'Raw_unit\', np.float32)]\ndatasets = [(\'Raw\', np.uint32), (\'Fastq\', str), (\'Move\', np.uint16), (\'Norm\', np.uint32)]\n\n# Create new SZ file\nsz = CompressedFile(\n    "/tmp/test_sz", mode="w",\n    header=header, attributes=attr, datasets=datasets,\n    overwrite=True, n_threads=8\n)\n\n# Save some reads\nfor i in range(100):\n    sz.put(\n        f"read_{i}", #ID\n        0, #Offset\n        np.random.rand(), #Raw_unit\n        np.random.randint(70, 150, 4000), #Raw\n        \'\'.join(np.random.choice([\'A\', \'T\', \'C\', \'G\'], 450)), #Fastq\n        np.random.randint(0, 1, 4000), #Move\n    )\n\n# Remember to call it to ensure everything finished successfully\nsz.close()\n```\n\nExamples for reading SZ file\n\n```python\nimport numpy as np\nfrom pysz.api import CompressedFile\nsz = CompressedFile(\n        "/tmp/test_sz", mode="r", allow_multiprocessing=True,\n)\n\n# Get the first read\nread = sz.get(0)\nprint(read.ID, read.Offset, read.Raw_unit, read.Raw, read.Fastq, read.Move)\n\n# Get first 10 reads\nreads = sz.get(np.arange(10))\n\n# Filter some reads\nidx = sz.idx.index[sz.idx[\'ID\'].isin([\'read_0\', \'read_1\'])]\nreads = sz.get(idx)\n```',
    'author': 'Jinyang Zhang',
    'author_email': 'zhangjinyang@biols.ac.cn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
