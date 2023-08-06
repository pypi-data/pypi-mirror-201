from pyxk.lazy_loader import LazyLoader

os = LazyLoader("os", globals())
m3u8 = LazyLoader("m3u8", globals())
rich = LazyLoader("rich", globals())
columns = LazyLoader("columns", globals(), "rich.columns")
panel = LazyLoader("panel", globals(), "rich.panel")

utils = LazyLoader("utils", globals(), "pyxk.utils")



class M3U8Parse:
    """M3U8 解析类"""

    def __init__(
        self, *, content: str, url: str, m3u8_instance: object
    ):
        self.obj = m3u8.loads(content=content, uri=url)
        self.m3u = m3u8_instance
        self.url = url
        self.keys = None
        self.segments = None
        self.maximum  = None
        self.duration = None


    @classmethod
    def start_parsing_from_content(
        cls, *, content: str, url: str, m3u8_instance: object
    ):
        """类方法 解析 m3u8"""
        self = cls(content=content, url=url, m3u8_instance=m3u8_instance)
        self.start_parsing()
        return self


    def start_parsing(self):
        """解析 m3u8 入口"""

        self.parsing_playlists()
        self.parsing_keys()
        self.parsing_segments()
        self.print_parsing_result()


    def parsing_playlists(self):
        """解析 m3u8 playlists"""

        if not self.obj.is_variant:
            return

        # 排序 playlists, 获取最大带宽 m3u8 链接
        def _sorted(playlist):
            playlist.uri = playlist.absolute_uri
            return playlist.stream_info.bandwidth
        playlists = sorted(self.obj.playlists, key=_sorted)

        # 保存 m3u8 文件
        self.m3u.sava_m3u8_content(url=self.url, content=self.obj.dumps())

        # 加载 playlist 数据
        self.url = variant_url = playlists[-1].uri
        variant_content = self.m3u.get_m3u8_content(url=variant_url)
        self.obj = m3u8.loads(content=variant_content, uri=variant_url)


    def parsing_keys(self):
        """解析 m3u8 keys"""

        m3u8_keys = {}
        for key in self.obj.keys:
            if not key:
                continue
            url = key.uri = key.absolute_uri
            secret = self.m3u.get_m3u8_content(url=url, is_m3u8key=True)
            m3u8_keys[url] = {
                "key": secret,
                "iv": key.iv.removeprefix("0x")[:16] if key.iv else secret[:16]
            }
            # 保存密钥
            self.m3u.sava_m3u8_content(url=url, content=secret, is_m3u8key=True)
        self.keys = m3u8_keys


    def parsing_segments(self):
        """解析 m3u8 segments"""

        segments_dict, duration = {}, 0
        for index, segment in enumerate(self.obj.segments):
            url = segment.uri = segment.absolute_uri
            key, duration = None, segment.duration + duration

            # segment 加密 - 解析
            if segment.key and self.keys:
                if segment.key.uri in self.keys:
                    key = segment.key.uri
            segments_dict[index] = {"url": url, "key": key}

        # 保存 m3u8 文件
        if self.obj.is_endlist:
            self.m3u.sava_m3u8_content(url=self.url, content=self.obj.dumps())

        self.segments = segments_dict
        self.duration = duration
        self.maximum  = len(segments_dict)


    def print_parsing_result(self):
        """打印 m3u8 解析结果"""

        filepath, filename = os.path.split(self.m3u.output) if self.m3u.output else (None, None)
        m3u8_url = panel.Panel(
            columns.Columns([self.url if self.url else "None"], expand=True, align="center")
        )

        information = [
            f"Limit: {self.m3u.limit}",
            f"Maximum: {self.maximum}",
            f"PlayTime: {utils.human_playtime_pr(self.duration)}",
            f"Encryption: {bool(self.keys)}",
            f"FileName: {filename}",
            f"FilePath: {filepath}",
            "Result: [yellow]==>[/] " \
            + ("[green b]Parsing success ![/]" \
            if self.obj.is_endlist \
            else "[red b]Parsing failure ![/]")
        ]

        information = [f"{i+1} {x}" for i, x in enumerate(information)]
        information.insert(0, m3u8_url)
        information = panel.Panel(
            columns.Columns(information, expand=True),
            border_style="yellow"
        )

        rich.print(information)


    def close(self):
        """关闭"""
        self.obj = None
        self.m3u = None
        self.url = None
        self.keys = None
        self.segments = None
        self.maximum  = None
        self.duration = None
