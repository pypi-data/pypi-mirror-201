from pyxk.lazy_loader import LazyLoader

os = LazyLoader("os", globals())
time = LazyLoader("time", globals())
shlex = LazyLoader("shlex", globals())
typing = LazyLoader("typing", globals())
warnings = LazyLoader("warnings", globals())
asyncio = LazyLoader("asyncio", globals())
threading = LazyLoader("threading", globals())
subprocess = LazyLoader("subprocess", globals())

aiohttp = LazyLoader("aiohttp", globals())
aiofiles = LazyLoader("aiofiles", globals())
progress = LazyLoader("progress", globals(), "rich.progress")

aes = LazyLoader("aes", globals(), "pyxk.aes")
utils = LazyLoader("utils", globals(), "pyxk.utils")



class SegmentsDownload:
    """Segments 异步下载"""

    def __init__(
        self, *, m3u8parse: typing.Union["M3U8Parse"]
    ):
        # m3u8 解析类
        self.m3u8parse = m3u8parse
        # m3u8 keys -> cipher
        self.cipher = {
            index: aes.Cryptor(**cipher)
            for index, cipher in m3u8parse.keys.items()
        } or None
        # segments 下载保存目录
        self.store = os.path.join(m3u8parse.m3u.m3u8temp, "segments")
        # limit
        self.limit = m3u8parse.m3u.limit
        # 异步请求默认超时时间
        self.default_timeout = 2 * 60
        # rich 进度条
        self.progress = None
        self.progress_task = None
        # 下载完成后全部文件路径
        self.result = []


    def close(self):
        """关闭"""
        self.m3u8parse.close()
        self.cipher = None
        self.progress = None
        self.progress_task = None


    def start_download(self):
        """异步下载 入口"""

        # 创建文件夹
        os.makedirs(self.store, exist_ok=True)
        # 开启下载 进度条
        with progress.Progress(
            *(
                progress.SpinnerColumn("line"),
                #progress.TextColumn("[progress.description]{task.description}"),
                progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
                progress.BarColumn(finished_style="green"),
                progress.TextColumn("[progress.description]{task.completed}/{task.total}"),
                progress.TimeElapsedColumn(),
                # progress.TransferSpeedColumn(),
            ),
        ) as self.progress:
            self.progress_task = self.progress.add_task(
                description=None,
                total=self.m3u8parse.maximum
            )
            result = asyncio.run(self.gather_request())
        self.result = result
        self.merge_segments()


    async def gather_request(self):
        """异步下载管理器 收集所有异步任务"""

        headers   = utils.default_headers()
        timeout   = aiohttp.ClientTimeout(total=self.default_timeout)
        connector = aiohttp.TCPConnector(limit=self.limit)

        async with aiohttp.ClientSession(
            timeout=timeout, headers=headers, connector=connector
        ) as session:

            tasks = [
                self.request(session=session, file=file, **segment)
                for file, segment in self.m3u8parse.segments.items()
            ]
            result = await asyncio.gather(*tasks)
        return result


    async def request(self, session, url, file, key=None):
        """下载 解密 保存 segment"""

        file = os.path.join(self.store, f"{file}.ts")

        # 本地存在 ts 文件不下载
        if (
            not os.path.isfile(file)
            or not os.path.getsize(file)
        ):
            # 下载 ts 文件
            content = await self.send_request(session=session, url=url)
            # AES 解密
            if key and self.cipher:
                content = self.cipher[key].decrypt(content)
            # 保存 ts 文件
            async with aiofiles.open(file, "wb") as fileobj:
                await fileobj.write(content)
        # 更新进度条
        self.progress.update(self.progress_task, advance=1)
        return file


    @staticmethod
    async def send_request(session, url):
        """请求 segment"""
        while True:
            try:
                async with session.get(url=url) as response:
                    # 异常状态码捕获
                    if 403 <= response.status <= 410:
                        raise aiohttp.InvalidURL(
                            f"invalid url:{str(response.url)!r}, status_code: {response.status!r}"
                        )
                    # 重试部分请求
                    if response.status != 200:
                        await asyncio.sleep(1)
                        continue

                    content = await response.content.read()
                    return content
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


    @classmethod
    def start_download_from_segments(
        cls, *, m3u8parse: typing.Union["M3U8Parse"]
    ):
        """类方法 下载segments"""
        self = cls(m3u8parse=m3u8parse)
        try:
            self.start_download()
        finally:
            self.close()
        return self


    def merge_segments(self):
        """合并 segments 文件"""

        # 创建 filelist 文件
        filelist, filesize = os.path.join(self.store, "filelist.txt"), 0
        with utils.open(filelist, "w", encoding="utf-8") as fileobj:
            for file in self.result:
                fileobj.write(f"file '{file}'\n")
                filesize += (os.path.getsize(file) - 16400)
        self.result.append(filelist)

        # ffmpeg 视频合并代码, 监测合并完成状态
        output = self.m3u8parse.m3u.output
        args   = shlex.split(
            f"ffmpeg -loglevel quiet -f concat -safe 0 -i {filelist} -c copy {output} -y"
        )
        merge_completed = False

        # ffmpeg 合并函数
        def merge():
            try:
                subprocess.run(args=args, check=True)
            except FileNotFoundError as error:
                reason = getattr(error, "filename", None)
                if reason != "ffmpeg":
                    raise
                warnings.warn("ffmpeg没在找到, 调用失败", stacklevel=1)
                self.m3u8parse.m3u._reserve = True
            finally:
                nonlocal merge_completed
                merge_completed = True

        # 进度条显
        def show_progress():
            completed_filezise = lambda: os.path.getsize(output) if os.path.isfile(output) else 0
            with progress.Progress(
                *(
                    progress.SpinnerColumn("line"),
                    progress.TextColumn("[progress.description]{task.description}"),
                    progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
                    progress.BarColumn(finished_style="green"),
                    # progress.TextColumn("[progress.description]{task.completed}/{task.total}"),
                    progress.DownloadColumn(),
                    # progress.TransferSpeedColumn(),
                    # progress.TimeElapsedColumn()
                ),
                transient=True
            ) as show_progress:
                progress_task = show_progress.add_task(
                    description=os.path.basename(output),
                    total=filesize
                )
                while True:
                    show_progress.update(progress_task, completed=completed_filezise())
                    if merge_completed:
                        show_progress.update(progress_task, completed=filesize)
                        break
                    time.sleep(0.1)

        task1 = threading.Thread(target=merge)
        task2 = threading.Thread(target=show_progress)
        task1.start()
        task2.start()
        task1.join()
        task2.join()
