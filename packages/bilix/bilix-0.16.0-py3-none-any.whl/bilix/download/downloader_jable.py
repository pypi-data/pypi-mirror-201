import asyncio
import re
from typing import Union
import httpx
import bilix.api.jable as api
from bilix.handle import Handler
from bilix.download.base_downloader_m3u8 import BaseDownloaderM3u8
from bilix.exception import HandleMethodError


class DownloaderJable(BaseDownloaderM3u8):
    def __init__(self, videos_dir: str = "videos", video_concurrency: int = 3, part_concurrency: int = 10,
                 stream_retry=5, speed_limit: Union[float, int] = None, progress=None, browser: str = None):
        client = httpx.AsyncClient(**api.dft_client_settings)
        super(DownloaderJable, self).__init__(client, videos_dir, video_concurrency, part_concurrency, browser=browser,
                                              stream_retry=stream_retry, speed_limit=speed_limit, progress=progress)

    async def get_model(self, url: str, image=True, hierarchy=True):
        data = await api.get_model_info(self.client, url)
        if hierarchy:
            hierarchy = self._make_hierarchy_dir(hierarchy, data['model_name'])
        await asyncio.gather(*[self.get_video(url, image, hierarchy) for url in data['urls']])

    async def get_video(self, url: str, image=True, hierarchy=True):
        video_info = await api.get_video_info(self.client, url)
        if hierarchy:
            hierarchy = self._make_hierarchy_dir(hierarchy, f"{video_info.avid} {video_info.model_name}")
        cors = [self.get_m3u8_video(m3u8_url=video_info.m3u8_url, file_name=video_info.title + '.ts',
                                    hierarchy=hierarchy if hierarchy else '')]
        if image:
            cors.append(self._get_static(video_info.img_url, name=video_info.title,
                                         hierarchy=hierarchy if hierarchy else ''))
        await asyncio.gather(*cors)


@Handler.register('jable')
def handle(kwargs):
    keys = kwargs['keys']
    method = kwargs['method']
    if 'jable' in keys[0] or re.match(r"[A-Za-z]+-\d+", keys[0]):
        d = DownloaderJable
        if method == 'get_video' or method == 'v':
            m = d.get_video
        elif method == 'get_model' or method == 'm':
            m = d.get_model
        else:
            raise HandleMethodError(DownloaderJable, method)
        return d, m
