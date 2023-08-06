from pyxk.m3u8._parser import M3U8Parse
from pyxk.m3u8._download import SegmentsDownload
from pyxk.lazy_loader import LazyLoader

os = LazyLoader("os", globals())
utils = LazyLoader("utils", globals(), "pyxk.utils")
requests = LazyLoader("requests", globals(), "pyxk.requests")



class BaseM3U8:
    """Base M3U8"""

    default_limit = 8

    def __init__(self):
        # m3u8 视频路径
        self._output   = None
        # 下载完成, 删除 m3u8 文件
        self._delete   = False
        # 下载完成, 保留 segments 文件
        self._reserve  = False
        # request.Session()
        self._session  = requests.Session()
        # headers
        self._headers = None
        # verify
        self._verify  = True
        # 不使用本地 m3u8 文件, 重新请求
        self._rerequest = False
        # 异步请求 limit
        self._limit = self.default_limit
        # 所有保存文件的路径
        self.result = []

    @property
    def output(self):
        """m3u8视频文件路径, output=None不下载"""
        return self._output

    @output.setter
    def output(self, path):
        if not path or not isinstance(path, str):
            self._output = None
        else:
            # 去除 output 中间的空白字符
            path = "-".join(path.split())
            # 得到绝对路径
            path = os.path.normpath(os.path.abspath(path))
            # 文件路径去重
            path = utils.rename_file(path, suffix="mp4")[0]
            self._output = path

    @property
    def m3u8temp(self):
        """m3u8文本文件 保存路径(文件夹)"""
        if not self.output:
            return None
        dirname, basename = os.path.split(self.output)
        basename = "." + basename.removesuffix(".mp4") + ".temp"
        return os.path.join(dirname, basename)

    @property
    def limit(self):
        """异步请求 limit"""
        return self._limit

    @limit.setter
    def limit(self, limit):
        if not isinstance(limit, int) or limit <= 0:
            limit = self.default_limit
        self._limit = limit


    def get_m3u8_content(
        self, url: str, *, is_m3u8key: bool=False
    ):
        """获取 m3u8 文件内容

        :params: url: m3u8 链接
        :params: is_m3u8key: 链接是否是 m3u8密钥 链接

        从 url 链接 或者 本地文件获取m3u8文本内容
        若 rerequests=True or self.m3u8temp为假, 则始终从 url 获取内容
        """
        mode, suffix, encoding, attri = "r", ".m3u8", "utf-8", "text"
        if is_m3u8key:
            mode, suffix, encoding, attri = "rb", ".key", None, "content"

        # 文件完整路径
        file = os.path.join(self.m3u8temp, utils.hash256(url)+suffix) if self.m3u8temp else None
        # 从 url 获取 m3u8 内容
        if (
            self._rerequest
            or not file
            or not os.path.isfile(file)
        ):
            response = self._session.get(url=url, headers=self._headers, verify=self._verify)
            content  = getattr(response, attri)
        # 从本地获取 m3u8 内容
        else:
            with open(file=file, mode=mode, encoding=encoding) as fileobj:
                content = fileobj.read()
        return content


    def sava_m3u8_content(
        self, url: str, content: str, *, is_m3u8key: bool=False
    ):
        """保存 m3u8 内容

        :params: url: m3u8 链接
        :params: content: 保存内容
        :params: is_m3u8key: 链接是否是 m3u8密钥 链接

        保存 content 至本地文件
        filepath = self.m3u8temp, filename = hash256(url)
        若 url or self.m3u8temp 为假, 则不保存
        """
        # 若 url or self.m3u8temp 为假, 则不保存
        if (
            not url
            or not self.m3u8temp
            or not isinstance(url, str)
        ):
            return

        mode, suffix, encoding = "w", ".m3u8", "utf-8"
        if is_m3u8key:
            mode, suffix, encoding = "wb", ".key", None

        file = os.path.join(self.m3u8temp, utils.hash256(url)+suffix)
        self.result.append(file)
        # self._rerequests = True or 本地文件不存在 才保存
        if self._rerequest or not os.path.isfile(file):
            with utils.open(file=file, mode=mode, encoding=encoding) as fileobj:
                fileobj.write(content)


class M3U8(BaseM3U8):
    """ Load M3U8 """

    def load_url(self, url: str, *, output: str=None, **kwargs):
        """负载 m3u8 链接

        :params: url: m3u8 链接
        :params: output: 视频输出
        """
        self._initialization_attri(output=output, **kwargs)
        content = self.get_m3u8_content(url=url)
        self._call(content=content, url=url)


    def load_content(self, content: str, url: str=None, *, output: str=None, **kwargs):
        """负载 m3u8 内容 或 文件路径

        :params: content: m3u8文本内容 或者 m3u8本地文件路径
        :params: url: m3u8 链接
        :params: output: 视频输出
        """
        self._initialization_attri(output=output, **kwargs)
        # m3u8文件规定必需以 '#EXTM3U' 开头
        if not content.startswith("#EXTM3U"):
            _m3u8file = os.path.normpath(os.path.abspath(content))
            if os.path.isfile(_m3u8file):
                with open(_m3u8file, "r", encoding="utf-8") as fileobj:
                    content = fileobj.read()
        self._call(content=content, url=url)


    def _call(self, *, content, url=None):
        """调用 M3U8Parse 进行解析"""

        m3u8parse = M3U8Parse.start_parsing_from_content(
            content=content, url=url, m3u8_instance=self
        )
        # 判断 output是否存在
        output_exists = lambda: os.path.isfile(self.output) if self.output else False
        # 开启 异步下载
        if self.output and m3u8parse.segments:
            download = SegmentsDownload.start_download_from_segments(m3u8parse=m3u8parse)
            # 删除 segments
            if not self._reserve and output_exists():
                self._remove(download.result, download.store)
        # 删除 m3u8 文件
        if self._delete and self.m3u8temp:
            self._remove(files=self.result, folder=self.m3u8temp)


    @staticmethod
    def _remove(files: list, folder: str):
        """删除文件和文件夹"""

        for file in files:
            os.remove(file)
        if not isinstance(folder, str):
            return
        if os.path.isdir(folder) and not os.listdir(folder):
            os.rmdir(folder)


    def _initialization_attri(
        self, output=None, rerequest=False, delete=False, reserve=False, headers=None, verify=True, limit=None
    ):
        # output
        self.output = output
        # rerequest
        self._rerequest = bool(rerequest)
        # delete
        self._delete = bool(delete)
        # reserve
        self._reserve = bool(reserve)
        # headers
        self._headers = dict(headers or {})
        # verify
        self._verify = bool(verify)
        # limit
        if limit is not None:
            self.limit = limit
        self.result = []


def load_url(url, *, output=None, rerequest=False, delete=False, reserve=False, headers=None, verify=True, limit=None):
    m3u8_obj = M3U8()
    return m3u8_obj.load_url(url=url, output=output, rerequest=rerequest, delete=delete, reserve=reserve, headers=headers, verify=verify, limit=limit)


def load_content(content, url=None, *, output=None, rerequest=False, delete=False, reserve=False, headers=None, verify=True, limit=None):
    m3u8_obj = M3U8()
    return m3u8_obj.load_content(content=content, url=url, output=output, rerequest=rerequest, delete=delete, reserve=reserve, headers=headers, verify=verify, limit=limit)
