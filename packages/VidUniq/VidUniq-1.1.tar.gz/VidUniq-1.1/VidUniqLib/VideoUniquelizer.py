import os
import random
import requests
from http import HTTPStatus
from pathlib import Path

from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx

VideoUniquelizer_Path_Alias = list[Path | str] | Path | str | None
VideoUniquelizer_Url_Alias = list[str] | str | None


class VideoUniquelizer:
    def __init__(self, *, path: VideoUniquelizer_Path_Alias = None, url: VideoUniquelizer_Url_Alias = None):
        self.path_list: list[Path] = []
        self.url_list: list[str] = []

        if path is not None:
            for i in ([path], path)[isinstance(path, list)]:
                if isinstance(i, str):
                    i = Path(i)

                if not i.exists():
                    print(f'[WARNING] Path "{i}" is invalid. (Skip)')
                    continue

                if i.is_file():
                    self.path_list.append(i)
                elif i.is_dir():
                    [self.path_list.append(file) for file in i.iterdir()]

        if url is not None:
            self.url_list = ([url], url)[isinstance(url, list)]

    def uniquelize(self, path: Path | str):
        if isinstance(path, str):
            path = Path(path)

        # Создать папку(и) если её нет
        path.mkdir(parents=True, exist_ok=True)

        # Фильтры ffmpeg -filter_complex
        filter_params = []
        for c in 'rgb':  # red, green, blue
            for r in 's':  # shadows, midtones, highlights
                filter_params.append(f'colorbalance={c}{r}={random.uniform(-0.15, 0.15)}')

        for i, video_path in enumerate(self.path_list):
            clip = VideoFileClip(str(video_path))

            # Уникализация
            clip = self.__uniquelize(clip)

            # Сохраняем видео в папку
            clip.write_videofile(str(path.joinpath(self.__format_video_filename(i))),
                                 ffmpeg_params=['-filter_complex', random.choice(filter_params)])

        for i, url in enumerate(self.url_list):
            if not self.__download_video(i, Path(f'temp_{self.__format_url_filename(i)}.mp4')):
                print(f'[WARNING] URL "{url}" is invalid. (Skip)')
                continue

            clip = VideoFileClip(f'temp_{self.__format_url_filename(i)}.mp4')

            # Уникализация
            clip = self.__uniquelize(clip)

            # Сохраняем видео в папку
            clip.write_videofile(str(path.joinpath(self.__format_url_filename(i))),
                                 ffmpeg_params=['-filter_complex', random.choice(filter_params)])
            del clip
            os.remove(f'temp_{self.__format_url_filename(i)}.mp4')

    def __download_video(self, index: int, path: Path) -> bool:
        response = requests.get(self.url_list[index])
        if response.status_code == HTTPStatus.OK:
            if len(response.content) == 0:
                return False
            with open(path, 'wb') as f:
                f.write(response.content)
            return True
        return False

    @staticmethod
    def __uniquelize(clip: VideoFileClip) -> VideoFileClip:
        # Эффекты video fx
        clip = vfx.fadein(clip, duration=2)  # Эффект появления
        clip = vfx.fadeout(clip, duration=2)  # Эффект затухания
        return clip

    @staticmethod
    def __format_filename(name: str) -> str:
        return name + '_uniq' + '.mp4'

    def __format_video_filename(self, index: int) -> str:
        return self.__format_filename(self.path_list[index].stem)

    def __format_url_filename(self, index: int) -> str:
        deprecated_chars = r'<>:"/\|?*'
        allowed_filename = ''.join(['.' if char in deprecated_chars else char for char in self.url_list[index]])
        return self.__format_filename(allowed_filename)
