import re
import types
import typing
import asyncio
from multidict import CIMultiDict
from asyncio import AbstractEventLoop

from yarl import URL
from lxml import etree
from aiohttp import (
    ClientTimeout,
    TCPConnector,
    ClientSession as Session
)
import rich.live as rich_live
import rich.progress as rich_progress
from aiohttp.client_reqrep import ClientResponse as Response

from pyxk.utils import get_user_agent
from pyxk.lazy_loader import LazyLoader

rich_box = LazyLoader("rich_box", globals(), "rich.box")
rich_panel = LazyLoader("rich_panel", globals(), "rich.panel")
rich_table = LazyLoader("rich_table", globals(), "rich.table")
rich_console = LazyLoader("rich_console", globals(), "rich.console")



class ClientSession:

    limit: int = 16
    timeout: typing.Union[int, float, dict] = {
        "total": 8,
        "connect": None,
        "sock_read": None,
        "sock_connect": None
    }
    headers: typing.Union[dict, CIMultiDict] = {}
    start_urls: list = []
    user_agent: str = get_user_agent("android")
    aiohttp_kwargs: dict = {}

    def __init__(
        self,
        *,
        loop: AbstractEventLoop=None,
        session: Session=None
    ):
        self._loop: AbstractEventLoop = loop
        self._session: Session = session

    async def start(self):
        """运行开始之前调用"""

    async def stop(self):
        """运行完成之后调用"""

    @classmethod
    def run(cls) -> tuple:
        """类方法: 协程入口 run, 应该从这里开始

        Return: ClientSession, [..., ...]
        返回值: 当前类的实例化, 协程运行结果列表
        """
        # Event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # Instance
        self: ClientSession = cls(loop=loop)
        result: list = self._loop.run_until_complete(self.async_start())
        return self, result

    async def async_start(self):
        try:
            # Event loop
            if not isinstance(self._loop, asyncio.AbstractEventLoop):
                self._loop = asyncio.get_event_loop()

            # Create aiohttp.ClientSession
            if not isinstance(self._session, Session):
                self._session = Session(
                    loop=self._loop,
                    headers=self.merge_headers(),
                    **self.merge_aiohttp_kwargs()
                )
            # run - self.open
            await self.start()
            result: list = await self.start_request()
        finally:
            await self.async_close()
        return result

    async def async_close(self):
        await self.stop()
        # Close aiohttp.ClientSession
        if isinstance(self._session, Session):
            await self._session.close()

    def merge_headers(self) -> CIMultiDict:
        """aiohttp.ClientSession Headers"""
        user_agent = self.user_agent if isinstance(self.user_agent, str) else get_user_agent("android")
        headers = CIMultiDict(self.headers or {})
        headers.setdefault("User-Agent", user_agent)
        return headers

    def merge_aiohttp_kwargs(self) -> dict:
        """aiohttp.ClientSession aiohttp_kwargs"""
        aiohttp_kwargs = self.aiohttp_kwargs.copy()
        timeout_kwargs = dict(
            total=100,
            connect=None,
            sock_read=None,
            sock_connect=None
        )
        if isinstance(self.timeout, (int, float)):
            timeout_kwargs["total"] = self.timeout
        elif isinstance(self.timeout, dict):
            timeout_kwargs.update(self.timeout)

        timeout = ClientTimeout(**timeout_kwargs)
        connector = TCPConnector(limit=self.limit)
        aiohttp_kwargs.setdefault("timeout", timeout)
        aiohttp_kwargs.setdefault("connector", connector)
        return aiohttp_kwargs

    async def request(
        self,
        url: str,
        callback: callable=None,
        method: str="GET",
        cb_kwargs: dict=None,
        **kwargs
    ):
        """异步Request方法

        :params: url
        :params: callback: 回调函数
        :params: method: 请求方法
        :params: cb_kwargs: 回调函数关键词参数
        :params: **kwargs: 异步请求参数
        """
        async with self._session.request(method=method, url=url, **kwargs) as response:
            response = add_response_method(response)
            if callable(callback):
                result = await callback(response=response, **cb_kwargs or {})
                return result
            return

    async def gather_urls(
        self,
        *urls,
        callback: callable=None,
        method: str="GET",
        cb_kwargs: dict=None,
        return_exceptions: bool=False,
        **kwargs
    ):
        """异步Request gather方法 异步发送大量url

        :params: urls: url列表
        :params: callback: 回调函数
        :params: method: 请求方法
        :params: cb_kwargs: 回调函数关键词参数
        :params: return_exceptions: 异常传递 若为真,异常将不抛出 传递值返回结果中
        :params: **kwargs: 异步请求参数
        """
        tasks = [
            self.request(
                url=url,
                callback=callback,
                method=method,
                cb_kwargs=cb_kwargs,
                **kwargs
            )
            for url in urls
        ]
        return await asyncio.gather(*tasks, return_exceptions=return_exceptions)

    async def start_request(self):
        """异步请求入口方法"""
        if not self.start_urls:
            raise NotImplementedError(f"{self.__class__.__name__}.start_urls is empty")
        tasks = [
            self.request(url, callback=self.parse)
            for url in self.start_urls
        ]
        result = await asyncio.gather(*tasks)
        return result

    async def parse(self, response: Response):
        """默认解析方法

        :params: response: 异步请求响应
        :参数传递可以使用 cb_kwargs
        """
        raise NotImplementedError(f"'{self.__class__.__name__}.parse' not implemented")


def add_response_method(response: Response) -> Response:
    # 为 Response 添加 xpath解析方法
    async def _xpath(self, _xpath, **kwargs):
        _htmlparse = etree.HTML(await self.text())
        class XpathList(list):
            def get(self, default=None):
                if not self:
                    return default
                return self[0]
        return XpathList(_htmlparse.xpath(_xpath, **kwargs))

    # 为 Response 添加 regular 方法
    async def _regular(self, pattern, flags=0):
        string = await self.text()
        return re.search(pattern, string, flags)

    # 为 Response 添加 urljoin 方法
    def _urljoin(self, _url: typing.Union[str, URL], /) -> str:
        if isinstance(_url, str):
            _url = URL(_url)
        elif not isinstance(_url, URL):
            return _url

        if _url.is_absolute():
            return _url.human_repr()
        return self.url.join(_url)

    response.xpath = types.MethodType(_xpath, response)
    response.re = types.MethodType(_regular, response)
    response.urljoin = types.MethodType(_urljoin, response)
    return response


default_progress_columns = (
    rich_progress.SpinnerColumn("line"),
    rich_progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
    rich_progress.BarColumn(),
    rich_progress.TextColumn("[progress.description]{task.completed}/{task.total}"),
    # rich_progress.DownloadColumn(),
    # rich_progress.TransferSpeedColumn(),
    rich_progress.TimeElapsedColumn()
)


default_download_progress_columns = (
    rich_progress.SpinnerColumn("line"),
    rich_progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
    rich_progress.BarColumn(),
    #rich_progress.TextColumn("[progress.description]{task.completed}/{task.total}"),
    rich_progress.DownloadColumn(),
    # rich_progress.TransferSpeedColumn(),
    rich_progress.TimeElapsedColumn()
)


def default_live(
    *,
    total: int=None,
    renderable: list=None,
    progress_column: typing.Union[list, tuple]=None,
    transient: bool=False,
    console: rich_console.Console=None,
    refresh_per_second: int=4,
    title: str=None,
    title_align: str=None,
) -> typing.Tuple[rich_live.Live, rich_progress.Progress, rich_progress.Task]:
    # total
    if not isinstance(total, int) or total <= 0:
        total = None
    # progress column
    progress_column = progress_column or default_progress_columns
    progress = rich_progress.Progress(*progress_column)
    progress_task = progress.add_task(description="", total=total)
    # console
    console = console or rich_console.Console()
    # transient
    transient = bool(transient)
    # renderable
    if not renderable:
        live = progress
    else:
        # 创建表单
        live = rich_table.Table(
            box=rich_box.SIMPLE_HEAD, expand=True, show_header=False
        )
        live.add_column(no_wrap=False, justify="center")
        for item in renderable:
            live.add_row(f"{item}")
        live.add_section()
        live.add_row(progress)

        # 将表单装入板块(panel)中
        live = rich_panel.Panel(
            live,
            border_style="bright_blue",
            subtitle=f"[dim]Total: {total or 0}[/]",
            subtitle_align="right",
            title=title,
            title_align=title_align,
        )

    # 装入 live 中进行实时更新
    live = rich_live.Live(
        live,
        transient=transient,
        console=console,
        refresh_per_second=refresh_per_second
    )
    return live, progress, progress_task
