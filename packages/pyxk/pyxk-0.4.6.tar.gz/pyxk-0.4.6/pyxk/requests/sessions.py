import requests.exceptions
from requests import Session as _Session
from requests.structures import CaseInsensitiveDict
from pyxk.lazy_loader import LazyLoader

os = LazyLoader("os", globals())
time = LazyLoader("time", globals())
warnings = LazyLoader("warnings", globals())
urllib_parse = LazyLoader("urllib_parse", globals(), "urllib.parse")
concurrent_futures = LazyLoader("concurrent_futures", globals(), "concurrent.futures")

rich_box = LazyLoader("rich_box", globals(), "rich.box")
rich_progress = LazyLoader("rich_progress", globals(), "rich.progress")
rich_live = LazyLoader("rich_live", globals(), "rich.live")
rich_panel = LazyLoader("rich_panel", globals(), "rich.panel")
rich_table = LazyLoader("rich_table", globals(), "rich.table")
rich_console = LazyLoader("rich_console", globals(), "rich.console")
utils = LazyLoader("utils", globals(), "pyxk.utils")


class Session(_Session):

    default_timeout = 5

    def __init__(
        self,
        *,
        base_url: str=None,
        user_agent: str=None,
        transient: bool=False,
    ):
        super().__init__()
        self.headers["User-Agent"] = user_agent or "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36"
        self._base_url = self._set_base_url(base_url)
        self._transient = bool(transient)
        self._console = rich_console.Console()

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, url: str, /):
        self._base_url = self._set_base_url(url)

    def _set_base_url(self, url: str, /):
        if not isinstance(url, str):
            url = ""
        return url if self._is_absolute_url(url) else ""

    @staticmethod
    def _is_absolute_url(url: str, /):
        if not isinstance(url, str):
            return False
        _url = urllib_parse.urlsplit(url)
        return bool(_url.scheme and _url.netloc)

    def build_absolute_url(self, url: str, /):
        """构造绝对url"""
        if self._is_absolute_url(url):
            return url
        if self.base_url:
            return urllib_parse.urljoin(self.base_url, url)
        return url

    def request(
        self,
        method,
        url,
        *,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
        transient=None
    ):
        url = self.build_absolute_url(url)
        request_status, exc_count = None, 10
        transient = self._transient if transient is None else bool(transient)
        if not transient:
            request_status = self._console.status(f"Request <[magenta]{method}[/] [bright_blue u]{url}[/]>", spinner="arc")
            request_status.start()
        try:
            while True:
                try:
                    response = super().request(
                        method=method,
                        url=url,
                        params=params,
                        data=data,
                        headers=headers,
                        cookies=cookies,
                        files=files,
                        auth=auth,
                        timeout=timeout or self.default_timeout,
                        allow_redirects=allow_redirects,
                        proxies=proxies,
                        hooks=hooks,
                        stream=stream,
                        verify=verify,
                        cert=cert,
                        json=json
                    )
                    break

                except requests.exceptions.Timeout:
                    exc_count -= 1
                    if exc_count < 0:
                        raise
                    warnings.warn(f"Timeout: {timeout!r}", stacklevel=4)
                    time.sleep(1)

                except requests.exceptions.ConnectionError as exc:
                    reason = str(exc.args[0])
                    reason_re = ("[Errno 7]", )
                    reason_ok = lambda : True in [item in reason for item in reason_re]
                    if not reason_ok():
                        raise
                    exc_count -= 1
                    if exc_count < 0:
                        raise
                    warnings.warn("Network connection failed", stacklevel=4)
                    time.sleep(1)
        finally:
            if request_status:
                request_status.stop()
        return response

    def get(
        self,
        url,
        *,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
        transient=None
    ):
        return self.request(
            method="GET",
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
            transient=transient
        )

    def post(
        self,
        url,
        *,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
        transient=None
    ):
        return self.request(
            method="POST",
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
            transient=transient
        )

    def head(
        self,
        url,
        *,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=False,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
        transient=None
    ):
        return self.request(
            method="HEAD",
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
            transient=transient
        )

    def put(
        self,
        url,
        *,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
        transient=None
    ):
        return self.request(
            method="PUT",
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
            transient=transient
        )

    def patch(
        self,
        url,
        *,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
        transient=None
    ):
        return self.request(
            method="PATCH",
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
            transient=transient
        )

    def delete(
        self,
        url,
        *,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
        transient=None
    ):
        return self.request(
            method="DELETE",
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
            transient=transient
        )

    def options(
        self,
        url,
        *,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
        transient=None
    ):
        return self.request(
            method="OPTIONS",
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
            transient=transient
        )

    def wget(
        self,
        url,
        method="GET",
        *,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=True,
        verify=None,
        cert=None,
        json=None,
        transient=False,
        output=None,
        resume=False,
        threads=1,
    ):
        """流式响应下载文件(支持多线程下载)

        :params: transient: 下载可视化内容 转瞬即逝(default: False)
        :params: output: 文件保存路径(default: None)
        :params: resume: 文件续传(default: False)
        :params: threads: 多线程下载(default: 1)
        """
        if not isinstance(threads, int) or threads <= 0:
            threads = 1
        transient = self._transient if transient is None else bool(transient)

        # 初始化数据
        output, threads, content_length, output_list = self._init_wget_attr(
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=False,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
            transient=transient,
            output=output,
            resume=resume,
            threads=threads
        )
        # content length换算
        if content_length:
            ret = utils.units_conversion_from_byte(content_length)
            content_length = f"{ret[0]}{ret[1]}"

        if not output:
            transient = True
        # headers更新
        for file in output_list.values():
            headers = CaseInsensitiveDict(headers)
            headers.update(dict(file["headers"]))
            file["headers"] = headers

        # rich live 动态进度条
        download_progress_list, download_task_list = [], []
        for index in range(threads):
            # 开启 rich_progress
            download_progress = rich_progress.Progress(
                *(
                    rich_progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
                    rich_progress.BarColumn(finished_style="green"),
                    rich_progress.DownloadColumn(),
                    rich_progress.TransferSpeedColumn(),
                    rich_progress.TimeElapsedColumn()
                )
            )
            # 创建 rich.progress任务
            download_task = download_progress.add_task(
                description="",
                total=output_list[index].get("total") if output_list else None,
            )
            download_progress_list.append(download_progress)
            download_task_list.append(download_task)

        # 创建 rich.live
        live_render = rich_table.Table(
            box=rich_box.SIMPLE_HEAD,
            expand=True,
            show_header=False
        )
        live_render.add_column(no_wrap=False, justify="center")
        live_render.add_row(f"size: [green]{content_length}[/]")
        live_render.add_row(f"store: [magenta]{output}[/]")
        live_render.add_section()

        for progress in download_progress_list:
            live_render.add_row(progress)

        live_render = rich_panel.Panel(
            live_render,
            subtitle=f"[dim i]threads: {threads}[/]",
            subtitle_align="right",
            border_style="bright_blue",
            title="[red]downloading[/]",
            title_align="center",
        )

        live, threads_pool, threads_return_list = None, None, []
        try:
            # 开启 rich.live 动态刷新
            live = rich_live.Live(live_render, transient=transient, console=self._console)
            if output:
                live.start()

            # 下载函数 self._stream_download 参数
            kwargs = dict(
                params=params,
                data=data,
                cookies=cookies,
                files=files,
                auth=auth,
                timeout=timeout,
                allow_redirects=allow_redirects,
                proxies=proxies,
                hooks=hooks,
                stream=stream,
                verify=verify,
                cert=cert,
                json=json,
                transient=transient,
            )

            # 创建线程池
            threads_pool = concurrent_futures.ThreadPoolExecutor()
            # 提交线程任务
            threads_tasks_list = [
                threads_pool.submit(
                    self._stream_download,
                    method=method,
                    url=url,
                    download_progress=download_progress_list[index],
                    download_task=download_task_list[index],
                    **kwargs,
                    **output_list[index] if output_list else {},
                )
                for index in range(threads)
            ]
            # 收集线程运行结果
            threads_return_list = [future.result() for future in threads_tasks_list]

        # 关闭 rich.live, 等待子线程运行结束
        finally:
            if live:
                live.stop()
            if threads_pool:
                threads_pool.shutdown(wait=True)

        # 合并下载文件
        if output:
            self._moviepy_merge(output, [file["output"] for file in output_list.values()])
        return threads_return_list[0] if threads_return_list and threads == 1 else threads_return_list

    def _stream_download(
        self,
        method,
        url,
        *,
        download_task,
        download_progress,
        total=None,
        output=None,
        completed=0,
        file_mode="wb",
        **kwargs
    ):
        """流式响应 下载(下载单个文件 配合线程池可以多线程下载)"""
        kwargs["transient"] = True
        response = self.request(method, url, **kwargs)
        # 状态码不属于 200-299区间
        if (
            not output
            or not(200 <= response.status_code <= 299)
        ):
            if response.status_code == 416:
                download_progress.update(download_task, completed=total)
            return response

        # 流式响应下载
        with utils.open(output, file_mode) as write_file:
            download_progress.update(download_task, completed=completed)
            for chunk in response.iter_content(chunk_size=1024):
                write_file.write(chunk)
                download_progress.update(download_task, advance=1024)
        return response

    def _init_wget_attr(self, url, output, resume, threads, **kwargs):
        """初始化 wget 数据"""
        kwargs["transient"] = True
        kwargs["allow_redirects"] = True
        response = self.head(url, **kwargs)
        # 获取文件 content_length
        output = self._complete_file_path(response=response, output=output)
        content_length = response.headers.get("Content-Length")
        if not content_length or content_length == "0":
            threads, content_length = 1, 0

        # 多线程片段区间 headers={"Range": "bytes=xxx-xxx"}
        parts_range_list = self._equal_parts(0, int(content_length), threads)
        # 多线程文件名以及部分参数
        output_list = {
            index: {
                "output": output + f"_{threads}_{index}.temp",
                "file_mode": "wb",
                "completed": 0,
                "total": parts_range_list[index][1] - parts_range_list[index][0] + 1 if isinstance(parts_range_list[index][1], int) else None,
                "headers": {"Range": f"bytes={parts_range_list[index][0]}-{parts_range_list[index][1]}"}
            }
            for index in range(threads)
        } if output else {}

        if not resume or not output_list:
            return output, threads, content_length, output_list

        # 单线程配置
        if threads == 1:
            output_list[0]["output"] = output
        # 文件续传
        for index, file in output_list.items():
            if not os.path.isfile(file["output"]):
                continue
            complete = os.path.getsize(file["output"])
            file["completed"] = complete
            file["file_mode"] = "ab"
            file["headers"] = {"Range": f"bytes={parts_range_list[index][0] + complete}-{parts_range_list[index][1]}"}
        return output, threads, content_length if content_length else None, output_list

    @staticmethod
    def _moviepy_merge(output, parts_movies):
        """合并多线程下载的文件"""
        # 判断文件是否存在
        for file in parts_movies:
            if not os.path.isfile(file):
                return
        os.rename(parts_movies.pop(0), output)
        # 创建生成器读取文件
        def read_parts_file(file, chunk_size=1024):
            with open(file, "rb") as read_file:
                while True:
                    chunk = read_file.read(chunk_size)
                    if not chunk:
                        return
                    yield chunk
        # 拼接文件
        with open(output, "ab") as write_file:
            for file in parts_movies:
                for _chunk in read_parts_file(file):
                    write_file.write(_chunk)
                # 合并完成 删除文件
                os.remove(file)

    @staticmethod
    def _equal_parts(start, end, parts_number=1):
        """多线程下载 切割数据区间"""
        if not isinstance(parts_number, int) or parts_number <= 0:
            parts_number = 1

        if not end:
            return [[start, ""]]
        total = end - start
        parts_size = total // parts_number
        if parts_size == 0:
            parts_number = 1

        result, temp = [], start
        for _ in range(parts_number-1):
            parts_start = temp
            parts_end = parts_start + parts_size -1
            temp = parts_end + 1
            result.append([parts_start, parts_end])
        result.append([temp, end])
        return result

    @staticmethod
    def _complete_file_path(response, output):
        """获取文件完整路径"""
        if not output or not isinstance(output, str):
            return None
        output   = os.path.normpath(os.path.abspath(output))
        basename = os.path.basename(output).split(".")
        if (
            len(basename) >= 2
            and len(basename[-1]) >= 1
        ):
            return output

        content_type = response.headers.get("Content-Type")
        if not content_type:
            suffix = ""
        else:
            suffix = content_type.split(";", 1)[0].strip()
            suffix = suffix.rsplit("/", 1)[-1].strip()
            suffix = "." + suffix if suffix else ""
        return output.removesuffix(".") + suffix
