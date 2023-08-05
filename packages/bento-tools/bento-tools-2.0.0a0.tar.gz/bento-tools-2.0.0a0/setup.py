# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bento',
 'bento.datasets',
 'bento.geometry',
 'bento.io',
 'bento.plotting',
 'bento.tools',
 'bento.tools.gene_sets']

package_data = \
{'': ['*'], 'bento': ['models/*']}

install_requires = \
['MiniSom>=2.3.0,<3.0.0',
 'Shapely>=1.8.2,<2.0.0',
 'UpSetPlot>=0.6.1,<0.7.0',
 'adjustText>=0.7.3,<0.8.0',
 'anndata>=0.7.6,<0.8.0',
 'astropy>=5.0,<6.0',
 'decoupler>=1.2.0,<2.0.0',
 'emoji>=1.7.0,<2.0.0',
 'geopandas>=0.10.0,<0.11.0',
 'ipywidgets>=8.0,<9.0',
 'kneed>=0.8.1,<0.9.0',
 'matplotlib-scalebar>=0.8.1,<0.9.0',
 'matplotlib>=3.2,<4.0',
 'pandas>=1.5.3,<2.0.0',
 'pygeos>=0.12.0,<0.13.0',
 'rasterio>=1.3.0,<2.0.0',
 'scanpy>=1.9.1,<2.0.0',
 'scipy>=1.7.0,<2.0.0',
 'seaborn>=0.12.1,<0.13.0',
 'sparse>=0.13.0,<0.14.0',
 'statsmodels>=0.13.2,<0.14.0',
 'tensorly>=0.7.0,<0.8.0',
 'tqdm>=4.64.0,<5.0.0',
 'xgboost==1.4.0']

extras_require = \
{':extra == "docs"': ['Sphinx[docs]>=4.1.2,<5.0.0',
                      'sphinx-autobuild[docs]>=2021.3.14,<2022.0.0',
                      'sphinx-book-theme[docs]>=1.0.0,<2.0.0',
                      'sphinx-gallery[docs]>=0.10.1,<0.11.0',
                      'myst-nb[docs]>=0.17.1,<0.18.0',
                      'sphinx_design[docs]>=0.3.0,<0.4.0']}

setup_kwargs = {
    'name': 'bento-tools',
    'version': '2.0.0a0',
    'description': 'A toolkit for subcellular analysis of spatial transcriptomics data',
    'long_description': '\n[![PyPI version](https://badge.fury.io/py/bento-tools.svg)](https://badge.fury.io/py/bento-tools)\n[![codecov](https://codecov.io/gh/ckmah/bento-tools/branch/master/graph/badge.svg?token=XVHDKNDCDT)](https://codecov.io/gh/ckmah/bento-tools)\n[![Documentation Status](https://readthedocs.org/projects/bento-tools/badge/?version=latest)](https://bento-tools.readthedocs.io/en/latest/?badge=latest)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/bento-tools)\n[![GitHub stars](https://badgen.net/github/stars/ckmah/bento-tools)](https://GitHub.com/Naereen/ckmah/bento-tools) \n\n# Bento\n\nBento is a Python toolkit for performing subcellular analysis of spatial transcriptomics data. The package is part of the [Scverse ecosystem](https://scverse.org/packages/#ecosystem). Check out the [documentation](https://bento-tools.readthedocs.io/en/latest/) for installation instructions, tutorials, and API. Cite [our preprint](https://doi.org/10.1101/2022.06.10.495510) if you use Bento in your work. Thanks!\n\n<img src="docs/source/_static/tutorial_img/bento_tools.png" alt="Bento Workflow" width="800">\n\n---\n[![GitHub license](https://img.shields.io/github/license/ckmah/bento-tools.svg)](https://github.com/ckmah/bento-tools/blob/master/LICENSE)\n',
    'author': 'Clarence Mah',
    'author_email': 'ckmah@ucsd.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
