import re
import asyncio
from multidict import CIMultiDict

import yarl
import aiohttp
from lxml import etree

from pyxk.utils import get_user_agent
from pyxk.lazy_loader import LazyLoader

rich_box = LazyLoader("rich_box", globals(), "rich.box")
rich_live = LazyLoader("rich_live", globals(), "rich.live")
rich_panel = LazyLoader("rich_panel", globals(), "rich.panel")
rich_table = LazyLoader("rich_table", globals(), "rich.table")
rich_console = LazyLoader("rich_console", globals(), "rich.console")
rich_progress = LazyLoader("rich_progress", globals(), "rich.progress")



default_progress_columns = (
    rich_progress.SpinnerColumn("line"),
    rich_progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
    rich_progress.BarColumn(),
    rich_progress.TextColumn("[progress.description]{task.completed}/{task.total}"),
    # rich_progress.DownloadColumn(),
    # rich_progress.TransferSpeedColumn(),
    rich_progress.TimeElapsedColumn()
)

def default_live(total=None, progress_columns=None, renderable=None):
    """基于 rich模块 实时进度显示"""
    console = rich_console.Console()
    progress_columns = progress_columns or default_progress_columns
    progress = rich_progress.Progress(*progress_columns)
    task = progress.add_task(description="", total=total)

    if renderable:
        live_render = rich_table.Table(
            box=rich_box.SIMPLE_HEAD,
            expand=True,
            show_header=False
        )
        live_render.add_column(no_wrap=False, justify="center")
        for item in renderable:
            live_render.add_row(f"{item}")
        live_render.add_section()
        live_render.add_row(progress)

        live_render = rich_panel.Panel(
            live_render,
            border_style="bright_blue",
            title="[red]downloading[/]",
            title_align="center",
        )
    else:
        live_render = progress
    live = rich_live.Live(live_render, console=console)
    return live, progress, task


class AsyncSession:

    start_urls = []
    headers = {}
    aiohttp_kwargs = {}
    timeout = 5
    limit = 100

    def __init__(self, loop=None):
        self.loop = loop
        self.session = None
        # start_urls
        if not self.__class__.start_urls:
            raise NotImplementedError(f"{self.__class__.__name__}.start_urls is empty")

    async def start_request(self):
        return await self.gather_urls(
            *self.start_urls,
            callback=self.parse
        )

    async def parse(self, response, *args, **kwargs):
        raise NotImplementedError(f"{self.__class__.__name__}.parse not implement")

    async def request(self, url, method="GET", callback=None, cb_kwargs=None, **kwargs):
        while True:
            try:
                async with self.session.request(method=method, url=url, **kwargs) as response:
                    setattr(response, "xpath", self._add_response_attr_xpath)
                    setattr(response, "re", self._add_response_attr_regular)
                    setattr(response, "urljoin", self._add_response_attr_urljoin)

                    if callable(callback):
                        if not isinstance(cb_kwargs, dict):
                            cb_kwargs = {}
                        return await callback(response=response, **cb_kwargs)
            # 请求超时 重试
            except asyncio.exceptions.TimeoutError:
                await asyncio.sleep(1)
            # 连接错误 重试
            except (
                aiohttp.client_exceptions.ClientOSError,
                aiohttp.client_exceptions.ClientPayloadError,
                aiohttp.client_exceptions.ClientConnectorError,
            ):
                await asyncio.sleep(2)
            # 服务器拒绝连接
            except aiohttp.client_exceptions.ServerDisconnectedError:
                await asyncio.sleep(2)

    async def open_spider(self):
        """开启下载之前调用"""

    async def close_spider(self):
        """下载完成之后调用"""

    @staticmethod
    async def _add_response_attr_xpath(response, xpath, **kwargs):
        htmlparse = etree.HTML(await response.text(), **kwargs)
        return htmlparse.xpath(xpath)

    @staticmethod
    def _add_response_attr_regular(pattern, flags=0):
        pattern = re.compile(pattern=pattern, flags=flags)
        return pattern

    @staticmethod
    def _add_response_attr_urljoin(response, url):
        url = yarl.URL(url)
        if url.is_absolute():
            return url
        return response.url.join(url)

    async def gather_urls(self, *urls, method="GET", callback=None, cb_kwargs=None, return_exceptions=False, **kwargs):
        """收集urls 并发发送"""
        tasks = [
            self.request(
                url=url,
                method=method,
                callback=callback,
                cb_kwargs=cb_kwargs,
                **kwargs
            )
            for url in urls
        ]
        return await asyncio.gather(
            *tasks,
            return_exceptions=return_exceptions
        )

    def merge_headers(self, headers, /):
        """合并UserAgent"""
        default_headers = CIMultiDict(self.headers or {})
        default_headers.update(headers or {})
        if not default_headers.__contains__("User-Agent"):
            default_headers["User-Agent"] = get_user_agent("android")
        return default_headers

    @classmethod
    def start(cls, loop=None, headers=None, limit=None):
        # event loop
        loop = loop or asyncio.new_event_loop()
        asyncio.set_event_loop(loop=loop)

        # 实例化
        self = cls(loop=loop)
        return self.loop.run_until_complete(
            self.async_start(loop=loop, self=self, headers=headers, limit=limit)
        )

    @classmethod
    async def async_start(cls, loop=None, self=None, headers=None, limit=None):
        try:
            self = self or cls()
            if not isinstance(self.loop, asyncio.AbstractEventLoop):
                self.loop = loop or asyncio.get_event_loop()

            headers = self.merge_headers(headers)
            # aiohttp.TCPConnector -> limit
            self.aiohttp_kwargs.setdefault("connector", aiohttp.TCPConnector(limit=limit or self.limit))
            self.aiohttp_kwargs.setdefault(
                "timeout", aiohttp.ClientTimeout(total=self.timeout)
            )
            # 创建 aiohttp.ClientSession
            self.session = aiohttp.ClientSession(
                loop=self.loop, headers=headers, **self.aiohttp_kwargs
            )
            # 运行异步请求
            await self.open_spider()
            result = await self.start_request()
        finally:
            await self.async_close()
        return result

    async def async_close(self):
        await self.close_spider()
        # 关闭 aiohttp.ClientSession
        if self.session:
            await self.session.close()
