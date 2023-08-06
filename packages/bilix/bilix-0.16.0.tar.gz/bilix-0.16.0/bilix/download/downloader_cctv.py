import asyncio
from typing import Union
import httpx

import bilix.api.cctv as api
from bilix.handle import Handler
from bilix.download.base_downloader_m3u8 import BaseDownloaderM3u8
from bilix.exception import HandleMethodError


class DownloaderCctv(BaseDownloaderM3u8):
    def __init__(self, videos_dir='videos', video_concurrency=3, part_concurrency=10, stream_retry=5,
                 speed_limit: Union[float, int] = None, progress=None, browser: str = None):
        client = httpx.AsyncClient(**api.dft_client_settings)
        super(DownloaderCctv, self).__init__(client, videos_dir, video_concurrency, part_concurrency, browser=browser,
                                             stream_retry=stream_retry, speed_limit=speed_limit, progress=progress)

    async def get_series(self, url: str, quality=0, hierarchy=True):
        pid, vide, vida = await api.get_id(self.client, url)
        if vida is None:  # 单个视频
            await self.get_video(pid, quality=quality)
        else:  # 剧集
            title, pids = await api.get_series_info(self.client, vide, vida)
            if hierarchy:
                hierarchy = self._make_hierarchy_dir(hierarchy, title)
            await asyncio.gather(*[self.get_video(pid, quality, hierarchy if hierarchy else '') for pid in pids])

    async def get_video(self, url_or_pid: str, quality=0, hierarchy: str = ''):
        if url_or_pid.startswith('http'):
            pid, _, _ = await api.get_id(self.client, url_or_pid)
        else:
            pid = url_or_pid
        title, m3u8_urls = await api.get_media_info(self.client, pid)
        m3u8_url = m3u8_urls[min(quality, len(m3u8_urls) - 1)]
        file_path = await self.get_m3u8_video(m3u8_url, title + ".ts", hierarchy)
        return file_path


@Handler.register(name='CCTV')
def handle(kwargs):
    keys = kwargs['keys']
    method = kwargs['method']
    if 'cctv' in keys[0]:
        d = DownloaderCctv
        if method == 's' or method == 'get_series':
            m = d.get_series
        elif method == 'v' or method == 'get_video':
            m = d.get_video
        else:
            raise HandleMethodError(d, method)
        return d, m
