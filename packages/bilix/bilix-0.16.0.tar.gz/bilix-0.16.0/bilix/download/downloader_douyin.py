import asyncio
from typing import Union

import httpx

import bilix.api.douyin as api
from bilix.handle import Handler
from bilix.download.base_downloader_part import BaseDownloaderPart
from bilix.utils import legal_title
from bilix.exception import HandleMethodError


class DownloaderDouyin(BaseDownloaderPart):
    def __init__(self, videos_dir='videos', part_concurrency=10, stream_retry=5,
                 speed_limit: Union[float, int] = None, progress=None, browser: str = None):
        client = httpx.AsyncClient(**api.dft_client_settings)
        super(DownloaderDouyin, self).__init__(client, videos_dir, part_concurrency, stream_retry=stream_retry,
                                               speed_limit=speed_limit, progress=progress, browser=browser)

    async def get_video(self, url: str, image=False):
        video_info = await api.get_video_info(self.client, url)
        title = legal_title(video_info.author_name, video_info.title)
        cors = [self.get_file(video_info.nwm_urls, file_name=title + ".mp4")]
        if image:
            cors.append(self._get_static(video_info.cover, title))
        await asyncio.gather(*cors)


@Handler.register(name='抖音')
def handle(kwargs):
    keys = kwargs['keys']
    if 'douyin' in keys[0]:
        method = kwargs['method']
        d = DownloaderDouyin
        if method == 'v' or method == 'get_video':
            m = d.get_video
        else:
            raise HandleMethodError(d, method)
        return d, m
