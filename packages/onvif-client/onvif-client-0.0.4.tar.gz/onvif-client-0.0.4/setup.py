# Author: Katsuya Hashimoto <hasimoka@gmail.com>
# Copyright (c) 2023- Katsuya Hashimoto
# License: GNU Lesser General Public License v3 or later (LGPLv3+)

from setuptools import setup, find_packages
import onvif


CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Communications'
]

with open('README.rst', 'r') as fp:
    readme = fp.read()
with open('CONTACT.txt', 'r') as fp:
    contacts = fp.read()
long_description = readme + '\n\n' + contacts

setup(name='onvif-client',
      author='Katsuya Hashimoto',
      maintainer='hasimoka@gmail.com',
      maintainer_email='hasimoka@gmail.com',
      description='onvif-client: WS-Discovery and Simple ONVIF camera client library',
      long_description=long_description,
      url='https://github.com/hasimoka/onvif-client',
      version=onvif.__version__,
      download_url='https://github.com/hasimoka/onvif-client',
      python_requires='>=3.9',
      install_requires=['WSDiscovery', 'onvif2-zeep'],
      packages=find_packages(),
      package_data={'onvif': ['wsdl/*']},
      classifiers=CLASSIFIERS,
      include_package_data=True
)
