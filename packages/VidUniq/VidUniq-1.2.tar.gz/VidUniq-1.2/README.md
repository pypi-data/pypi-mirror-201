# VidUniqLib

![Language](https://img.shields.io/badge/Language-Python3.10-yellow.svg?style=flat)
![License](https://img.shields.io/pypi/l/VidUniqLib?color=blueviolet)

_**PyPi**_ Video Uniquelizer Library
###### The purpose of the library is to slightly modify the video so that it cannot be matched with the original video

## Installation
Install the current version with [PyPI](https://pypi.org/project/VidUniqLib/):
```bash
pip install VidUniq
```
Or from GitHub:
```bash
pip install https://github.com/1floppa3/VidUniqLib/archive/main.zip
```

## Usage
You can generate a token for clubhouse by going to the account section and generating a new token
```python
from VidUniqLib import VideoUniquelizer

url: str = 'https://some_invalid_site.site/api.php?wtf=invalid.mp4' #  Could be list
path_list: list[str] = [ #  Could bee 'str' or 'pathlib.Path'
    'some_invalid_folder_IdnaP19f/',
    'some_invalid_file_dmAgo30z.mp4'
]

uniq = VideoUniquelizer(path=path_list, url=url)
uniq.uniquelize('uniquelized/')
```

## Example
You can find an example of usage here: [VidUniq](https://github.com/1floppa3/VidUniq)