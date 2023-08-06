# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nkt_basik', 'nkt_basik.dll']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nkt-basik',
    'version': '0.2.0',
    'description': 'Python interface for the NKT Photonics Basik fiber seed laser',
    'long_description': "# NKT-basik\nVersion 0.1\n\nInterface for [NKT Photonics Basik fiber seed laser](https://www.nktphotonics.com/lasers-fibers/product/koheras-basik-low-noise-single-frequency-oem-laser-modules/), only tested with a Y10 model.  \nConsists of a class Basik which has the methods to modify wavelength, frequency, modulation, etc.\n\n## Install\nTo use the package install with `python setup.py install`\n\n## Code Example\n\n```Python\nfrom nkt_basik import Basik\n\ndevice = Basik('COM4', 1)\n\n# get the wavelength in nm \nprint(f'Device wavelength: {device.wavelength} nm')\n\n# get the frequency in GHz\nprint(f'Device frequency: {device.frequency:.4f} GHz')\n\n# get the temperature in C\nprint(f'Device temperature: {device.temperature:.1f} C')\n\n# set the wavelength setpoint in nm\nprint('Setting the wavelength to 1086.77 nm')\ndevice.wavelength = 1086.77\n\n# get the wavelength in nm \nprint(f'Device wavelength: {device.wavelength} nm')\n\n# enable emission\nprint('Enable emission')\ndevice.emission = True\n\n# enable wavelength modulation\ndevice.modulation = True\n\n# get device errors\nprint('Errors:',device.error)\n\n# get device status\nprint('Status:',device.status)\n\n# disable emission\nprint('Disable emission')\ndevice.emission = False\n\n# get device status\nprint('Status:',device.status)\n```\n\n## TODO\n* more testing\n* add tests\n",
    'author': 'ograsdijk',
    'author_email': 'o.grasdijk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ograsdijk/NKT-Basik',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
