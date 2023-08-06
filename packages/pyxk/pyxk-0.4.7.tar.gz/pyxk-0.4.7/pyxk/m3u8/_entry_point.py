import re, copy
import rich, click
from pyxk import requests

from pyxk.m3u8._m3u8 import load_url, load_content



@click.group(
    invoke_without_command=False,
    chain=True
)
@click.pass_context
@click.option(
    "-o",
    "--output",
    "output",
    type=str,
    default=None,
    help="m3u8 视频保存路径"
)
@click.option(
    "--rerequest",
    is_flag=True,
    default=False,
    help="重新请求 m3u8 网络资源"
)
@click.option(
    "--no-delete",
    "delete",
    is_flag=True,
    default=True,
    help="删除本地 m3u8 文件"
)
@click.option(
    "--reserve",
    "reserve",
    is_flag=True,
    default=False,
    help="保留 segments"
)
@click.option(
    "-h",
    "--headers",
    "headers",
    type=(str, str),
    multiple=True,
    help="Request 请求头"
)
@click.option(
    "--no-verify",
    "verify",
    is_flag=True,
    default=True,
    help="Request SSL验证"
)
@click.option(
    "-l",
    "--limit",
    "limit",
    type=int,
    default=8,
    help="异步下载 Limit"
)
def main(
    ctx, output, rerequest, delete, reserve, headers, verify, limit
):
    """M3U8 下载, 合并管理器(ffmpeg)"""
    ctx.obj = ctx.params


@main.command()
@click.pass_obj
@click.argument(
    "content",
    type=click.Path(exists=True),
    metavar="path <m3u8 文件路径>"
)
@click.option(
    "-u",
    "--url",
    "url",
    type=str,
    default=None,
    help="m3u8 链接地址"
)
@click.option(
    "-o",
    "--output",
    "output",
    type=str,
    default=None,
    help="m3u8 视频保存路径"
)
def file(obj, content, url, output):
    """使用 m3u8文件 下载"""

    kwargs = copy.deepcopy(obj)
    if output is not None:
        kwargs["output"] = output
    load_content(content=content, url=url, **kwargs)


@main.command()
@click.pass_obj
@click.argument(
    "url",
    type=str,
    metavar="url <m3u8 链接地址>"
)
@click.option(
    "-o",
    "--output",
    "output",
    type=str,
    default=None,
    help="m3u8 视频保存路径"
)
def url(obj, url, output):
    """使用 m3u8链接 下载"""

    kwargs = copy.deepcopy(obj)
    if output is not None:
        kwargs["output"] = output
    load_url(url=url, **kwargs)


@main.command()
@click.pass_obj
@click.argument(
    "designation",
    type=str,
    metavar="designation <Jable 番号>"
)
@click.option(
    "-o",
    "--output",
    "output",
    type=str,
    default=None,
    help="m3u8 视频保存路径"
)
def jable(obj, designation, output):
    """Jable.tv 视频下载"""

    kwargs = copy.deepcopy(obj)
    if output is not None:
        kwargs["output"] = output
    jable_video_url = f"https://jable.tv/videos/{designation}/"

    response = requests.get(jable_video_url)
    if response.status_code != 200:
        rich.print(
            f"[bold]Jable[/]: [yellow]{jable_video_url!r}[/] [red]{response.status_code!r}[/]")
        return

    m3u8url = re.search(
        pattern=r"var hlsUrl\s*?=\s*?'(?P<m3u8>.*?)'",
        string=response.text,
        flags=re.M
    )

    if not m3u8url:
        rich.print("[red]没有匹配的M3U8 URL[/]")
        return

    m3u8url = m3u8url.group("m3u8")
    load_url(url=m3u8url, **kwargs)
