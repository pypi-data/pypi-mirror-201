from setuptools import setup

'''
:authors: 1Floppa3
:license: GPL-3.0 license, see LICENSE.md file
:copyright: (c) 2023 1Floppa3
'''

version = '1.2.1'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='VidUniq',
    version=version,
    author='1Floppa3',
    author_email='denis.kochetkov2006@gmail.com',
    description='A simple video uniquelizer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/1floppa3/VidUniqLib',
    download_url='https://github.com/1floppa3/VidUniqLib/archive/main.zip',
    license='GPL-3.0 license',
    packages=['VidUniq'],
    install_requires=['requests', 'moviepy'],
    python_requires='>=3.10',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)