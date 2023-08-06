# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['atflagger']
install_requires = \
['astropy>=5,<6',
 'bokeh',
 'dask>=2022,<2023',
 'distributed>=2022,<2023',
 'h5py',
 'matplotlib',
 'numpy',
 'tqdm',
 'xarray']

entry_points = \
{'console_scripts': ['atflagger = atflagger:cli']}

setup_kwargs = {
    'name': 'atflagger',
    'version': '0.4.6',
    'description': 'Simple method for flagging UWL data.',
    'long_description': "# atflagger\n\nA simple flagger for continuum UWL data. Flag persistent RFI first, then run this auto-flagger.\n\n## Installation\n\nInstalling requires `pip` and `python3` (3.8 and up).\n\nStable version:\n```\npip install atflagger\n```\n\nLatest version:\n```\npip install git+https://github.com/AlecThomson/atflagger\n```\n\n## Usage\n```\n❯ atflagger -h\nusage: atflagger [-h] [-i] [-b BEAM] [-s SIGMA] [-n N_WINDOWS] [-w] [-r REPORT] [-c CORES] [-t THREADS_PER_WORKER] filenames [filenames ...]\n\natflagger - Automatic flagging of UWL data. This flagger divides each subband into a number of windows, and then uses sigma clipping to remove outliers. The number of windows is set by the 'n-windows' argument, and the number of sigma is set by the 'sigma' argument. Parallelism is handled by dask.distributed. The 'cores' argument sets the number of\nDask workers, and 'threads-per-worker' sets the number of threads. See https://docs.dask.org/en/stable/deploying-python.html#reference for more information.\n\npositional arguments:\n  filenames             Input SDHDF file(s)\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -i, --inplace         Update flags in-place (default: create new file)\n  -b BEAM, --beam BEAM  Beam label\n  -s SIGMA, --sigma SIGMA\n                        Sigma clipping threshold\n  -n N_WINDOWS, --n-windows N_WINDOWS\n                        Number of windows to use in box filter\n  -w, --use-weights     Use weights table instead of flag table\n  -r REPORT, --report REPORT\n                        Optionally save the Dask (html) report to a file\n  -c CORES, --cores CORES\n                        Number of workers to use (default: Dask automatic configuration)\n  -t THREADS_PER_WORKER, --threads-per-worker THREADS_PER_WORKER\n                        Number of threads per worker (default: Dask automatic configuration)\n```\n",
    'author': 'Alec Thomson',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
