# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gatorpy',
 'gatorpy.archives',
 'gatorpy.archives.toolbox-02032023',
 'gatorpy.toolbox']

package_data = \
{'': ['*']}

install_requires = \
['Brotli>=1.0.9,<2.0.0',
 'anndata>=0.8.0,<0.9.0',
 'argparse>=1.4.0,<2.0.0',
 'dask>=2022.8.1,<2023.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.23.2,<2.0.0',
 'opencv-python>=4.6.0.66,<5.0.0.0',
 'pandas>=1.4.4,<2.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scikit-learn>=1.2.1,<2.0.0',
 'tensorflow<2.11',
 'tifffile>=2022.8.12,<2023.0.0',
 'zarr>=2.12.0,<3.0.0']

setup_kwargs = {
    'name': 'gatorpy',
    'version': '0.1.11',
    'description': 'GATOR: A scalable framework for automated processing of highly multiplexed tissue images',
    'long_description': '# gatorpy\n GATOR: A scalable framework for automated processing of highly multiplexed tissue images\n',
    'author': 'Ajit Johnson Nirmal',
    'author_email': 'ajitjohnson.n@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/gatorpy/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
