"""
import pyxk.utils
"""
from pyxk.lazy_loader import LazyLoader

re = LazyLoader("re", globals())
os = LazyLoader("os", globals())
time = LazyLoader("time", globals())
typing = LazyLoader("typing", globals())
base64 = LazyLoader("base64", globals())
hashlib = LazyLoader("hashlib", globals())
difflib = LazyLoader("difflib", globals())
warnings = LazyLoader("warnings", globals())
multidict = LazyLoader("multidict", globals())
functools = LazyLoader("functools", globals())
itertools = LazyLoader("itertools", globals())
collections = LazyLoader("collections", globals())


__all__ = [
    "runtime",
    "async_runtime",
    "open_decorator",
    "is_base64",
    "tobytes_from_base64",
    "get_user_agent",
    "default_headers",
    "md5",
    "rename_file",
    "rename_folder",
    "human_playtime_pr",
    "hash256",
    "transfer_lazyloader",
    "transfer_lazyloader_from_file",
    "units_conversion_from_byte"
]


def runtime(func):
    """计算函数运行时间"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        ret = func(*args, **kwargs)
        end_time   = time.perf_counter()
        try:
            from rich import print
        except ModuleNotFoundError:
            pass
        print(f"{func.__name__!r} runtime:", end_time - start_time)
        return ret
    return wrapper


def async_runtime(func):
    """计算异步函数运行时间"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        ret = await func(*args, **kwargs)
        end_time   = time.perf_counter()
        try:
            from rich import print
        except ModuleNotFoundError:
            pass
        print(f"{func.__name__!r} runtime:", end_time - start_time)
        return ret
    return wrapper


def open_decorator(func):
    """
    内置函数 open 装饰器
    作用: 写或追加模式下 创建不存在的目录
    """
    @functools.wraps(func)
    def wrapper(
        file,
        mode="r",
        buffering=-1,
        encoding=None,
        errors=None,
        newline=None,
        closefd=True,
        opener=None
    ):
        if not isinstance(mode, str):
            raise TypeError(
                f"{func.__name__}() argument 'mode'"
                f"must be str, not {type(mode).__name__!r}"
            )

        # 判断 mode 是否属于 写或追加 模式
        # collections.Counter 统计可迭代对象 每项出现的次
        # itertools.product 求多个可迭代对象的笛卡尔积
        _mode = tuple(
            collections.Counter(i+j)
            for i in ("a", "w")
            for j in ("b", "+", "b+", "")
        )

        # 创建目录
        if collections.Counter(mode) in _mode:
            os.makedirs(os.path.dirname(file), exist_ok=True)
        # 二进制模式下不应该使用 encoding
        if mode.find("b") != -1 and encoding is not None:
            warnings.warn(
                "binary mode doesn't take an encoding argument",
                DeprecationWarning
            )
            encoding = None
        return func(
            file=file,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd,
            opener=opener
        )
    return wrapper

make_open = open = open_decorator(open)


def is_base64(data: typing.Union[str, bytes]) -> bool:
    """判断base64数据类型

    :params: data: 需要检测的数据
    """
    if isinstance(data, bytes):
        # base64 数据类型 正则表达式判断
        B64_RE_PATTERN_B = re.compile(rb"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$")
        return bool(B64_RE_PATTERN_B.match(data))

    if isinstance(data, str):
        # base64 数据类型 正则表达式判断
        B64_RE_PATTERN   = re.compile(r"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$")
        return bool(B64_RE_PATTERN.match(data))
    # str 或 bytes 以外类型返回 False
    return False


def tobytes_from_base64(
    data: typing.Union[str, bytes], encoding="UTF-8"
) -> typing.Tuple[bool, typing.Union[str, bytes]]:
    """base64数据类型 转化为bytes

    :params: data: 需要 base64 解密的数据
    :params: encoding: type(data) is 'str' 通过 encoding 转换为 bytes
    """
    if (
        not isinstance(data, (str, bytes))
        or not is_base64(data)
    ):
        return False, data
    if isinstance(data, str):
        data = data.encode(encoding)
    return True, base64.b64decode(data)


# User-Agnet
UA_ANDROID  = "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36"
UA_WINDOWNS = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
UA_MAC      = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
UA_IPHONE   = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
UA_IPAD     = "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1"
UA_SYMBIAN  = "Mozilla/5.0 (Symbian/3; Series60/5.2 NokiaN8-00/012.002; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/533.4 (KHTML, like Gecko) NokiaBrowser/7.3.0 Mobile Safari/533.4 3gpp-gba"
UA_APAD     = "Mozilla/5.0 (Linux; Android 11; Phh-Treble vanilla Build/RQ3A.211001.001;) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.91 Safari/537.36"
UA_ALL = {
    "android" : UA_ANDROID,
    "windows" : UA_WINDOWNS,
    "mac"     : UA_MAC,
    "iphone"  : UA_IPHONE,
    "ipad"    : UA_IPAD,
    "symbian" : UA_SYMBIAN,
    "apad"    : UA_APAD
}


def get_user_agent(
    user_agent: str, overwrite: bool=False
) -> str:
    """获取 UserAgent

    :params: user_agent: 返回 useragent 模糊查找的结果
    :params: overwrite: 重写 useragent, 若为True, 直接返回useragent
    """
    if not isinstance(user_agent, str):
        raise ValueError(
            f"invalid user_agent: '{user_agent}', "
            f"type: '{type(user_agent).__name__}'")
    # 重写
    if overwrite:
        return user_agent

    user_agent = difflib.get_close_matches(user_agent.lower(), UA_ALL, 1)
    if not user_agent:
        return UA_ANDROID
    return UA_ALL[user_agent[0]]


def default_headers():
    """默认 headers

    headers = {"User-Agent": "..."}
    """
    headers = (("User-Agent", get_user_agent("android")),)
    return multidict.CIMultiDict(headers)


def md5(
    data: typing.Union[str, bytes], encoding: str="UTF-8"
) -> str:
    """ MD5 加密

    :params: data: 需要加密的数据
    :params: encoding: type(data) is 'str' 通过 encoding 转换为 bytes
    """
    if isinstance(data, str):
        data = data.encode(encoding=encoding)

    elif not isinstance(data, bytes):
        raise TypeError(
            "md5 encrypted data must be a 'str' or 'bytes'"
            f", can't be a {type(data).__name__!r}")
    return hashlib.md5(data).hexdigest()


def rename_file(file: str, *, suffix: str=None) -> typing.Tuple[str, str, str]:
    """重命名本地存在的文件
    :params: file: 文件路径
    :params: suffix: 文件后缀名

    return:
    Tuple(rename_file, dirname, basename)
    """
    # 绝对路径
    file = os.path.abspath(file)
    # 后缀名解析
    if not isinstance(suffix, str) or not suffix:
        file_split, suffix = file.rsplit(".", 1), ""
        if len(file_split) == 2 and len(file_split[-1]) < 6:
            suffix = file_split[-1]
    suffix = "." + suffix.strip().removeprefix(".") if suffix.strip() else suffix.strip()
    # 完整文件路径
    if not file.endswith(suffix):
        file += suffix

    if not os.path.isfile(file):
        return file, *os.path.split(file)

    for index in itertools.count(1):
        newfile = file.removesuffix(suffix) + f".{index}" + suffix
        if not os.path.isfile(newfile):
            break
    return newfile, *os.path.split(newfile)


def rename_folder(folder: str) -> typing.Tuple[str, str, str]:
    """重命名本地存在的文件夹
    :params: folder: 文件夹路径

    return:
    Tuple(rename_folder, dirname, basename)
    """
    folder = os.path.abspath(folder)

    if not os.path.isdir(folder):
        return folder, *os.path.split(folder)

    for index in itertools.count(1):
        new_folder = folder + f".{index}"
        if not os.path.isdir(new_folder):
            break
    return new_folder, *os.path.split(new_folder)


def human_playtime_pr(
    playtime: typing.Union[int, float]
) -> str:
    """人类直观时间展示

    :params: playtime: 传入一个时间(秒), 返回人类能理解的时间格式
    """
    if not isinstance(playtime, (int, float)):
        if playtime is None:
            return None
        raise TypeError(
            f"'playtime' must be a 'int' or 'float', got {type(playtime).__name__!r}")

    symbol, playtime = "-" if playtime < 0 else "", round(abs(playtime))
    hour, second = divmod(playtime, 3600)
    minute, second = divmod(second, 60)
    return f"{symbol}{hour}:{minute:0>2}:{second:0>2}"


def hash256(
    data:typing.Union[str, bytes], encoding: str="UTF-8"
) -> str:
    """HASH_256

    :params: data: 需要加密的数据
    :params: encoding: type(data) is 'str' 通过 encoding 转换为 bytes
    """
    if isinstance(data, str):
        data = data.encode(encoding)
    return hashlib.sha256(data).hexdigest()


def transfer_lazyloader(string: str, /) -> str:
    """python模块转换懒加载

    :params: string: python代码
    """
    pattern = re.compile(
        r"^from\s+?(?P<from_name>\S+)\s+?import\s+?(?P<from_import_name>\S+)\s*?(as\s+?(?P<from_import_alias>\S+))?$|^import\s+?(?P<import_name>\S+)(\s+?as\s+(?P<import_alias>\S+?))?\s*?$",
        flags=re.M
    )
    is_replace = False

    def repl_string(match):
        match_dict = match.groupdict()
        nonlocal is_replace
        import_name, alias, is_replace = None, None, True
        result = '{alias} = LazyLoader("{alias}", globals(), "{import_name}")'

        # from导入
        if match_dict["from_name"]:
            import_name = f'{match_dict["from_name"]}.{match_dict["from_import_name"]}'
            alias = match_dict["from_import_name"]
        else:
            import_name = f'{match_dict["import_name"]}'
            alias = match_dict["import_name"]

        # alias
        if match_dict["from_import_alias"]:
            alias = match_dict["from_import_alias"]
        elif match_dict["import_alias"]:
            alias = match_dict["import_alias"]

        return result.format(alias=alias, import_name=import_name)

    # 替换懒加载
    string = pattern.sub(repl=repl_string, string=string)
    if is_replace:
        string = "from pyxk.lazy_loader import LazyLoader\n\n" + string
    return string


def transfer_lazyloader_from_file(
    read_file: str, write_file: str, *, encoding="utf-8"
):
    """python模块转换懒加载 从文件

    :params: read_file: 读取python代码文件
    :params: write_file: 写入转换后的python代码文件
    """
    with open(read_file, "r", encoding=encoding) as fileobj:
        content = fileobj.read()

    with open(write_file, "w", encoding=encoding) as fileobj:
        content = transfer_lazyloader(content)
        fileobj.write(content)

def units_conversion_from_byte(
    target: typing.Union[int, float], /
) -> typing.Tuple[float, str]:
    """字节单位自动换算

    :params: 换算目标(Bytes)
    """
    target, target_units = float(target), "Bytes"
    units_dict = {"Bytes": 1, "KB": 1024, "MB": 1024, "GB": 1024, "TB": 1024, "PB": 1024, "EB": 1024, "ZB": 1024, "YB": 1024, "BB": 1024}
    for units, rate in units_dict.items():
        if target >= rate:
            target, target_units = target/rate, units
            continue
        break
    return round(target, 2), target_units
