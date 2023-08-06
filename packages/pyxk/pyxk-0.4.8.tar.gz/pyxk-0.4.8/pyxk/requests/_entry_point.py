import click
from pyxk import requests
from pyxk.lazy_loader import LazyLoader

_json = LazyLoader("_json", globals(), "json")
rich_panel = LazyLoader("rich_panel", globals(), "rich.panel")
rich_console = LazyLoader("rich_console", globals(), "rich.console")
rich_columns = LazyLoader("rich_columns", globals(), "rich.columns")



def validate_json(ctx, param, value):
    if value is None:
        return None
    try:
        return _json.loads(value)
    except _json.JSONDecodeError:  # pragma: no cover
        raise click.BadParameter("Not valid JSON")

def validate_auth(ctx, param, value):
    if value == (None, None):
        return None
    username, password = value
    if password == "-":  # pragma: no cover
        password = click.prompt("Password", hide_input=True)
    return (username, password)

@click.command()
@click.argument("url", type=str)
@click.option(
    "--method",
    "-m",
    "method",
    type=str,
    help=(
        "Request method, "
        "suah as GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD."
    )
)
@click.option(
    "--params",
    "-p",
    "params",
    type=(str, str),
    multiple=True,
    help="Request parameters.",
)
@click.option(
    "--data",
    "-d",
    "data",
    type=(str, str),
    multiple=True,
    help="Form data.",
)
@click.option(
    "--files",
    "-f",
    "files",
    type=(str, click.File(mode="rb")),
    multiple=True,
    help="Form files.",
)
@click.option(
    "--json",
    "-j",
    "json",
    type=str,
    callback=validate_json,
    help="Json data.",
)
@click.option(
    "--headers",
    "-h",
    "headers",
    type=(str, str),
    multiple=True,
    help="Http headers.",
)
@click.option(
    "--cookies",
    "cookies",
    type=(str, str),
    multiple=True,
    help="Request cookies.",
)
@click.option(
    "--auth",
    "auth",
    type=(str, str),
    default=(None, None),
    callback=validate_auth,
    help="Username and password"
)
@click.option(
    "--proxies",
    "proxies",
    type=str,
    default=None,
    help="Http or https proxies.",
)
@click.option(
    "--timeout",
    "-t",
    "timeout",
    type=float,
    default=5.0,
    help="Http connection timeout(default: 5.0)"
)
@click.option(
    "--no-allow-redirects",
    "allow_redirects",
    is_flag=True,
    default=True,
    help="Disable automatically follow redirects.",
)
@click.option(
    "--no-verify",
    "verify",
    is_flag=True,
    default=True,
    help="Disable SSL verification.",
)
@click.option(
    "--show-request",
    "show_request",
    is_flag=True,
    default=False,
    help="Show request header"
)
@click.option(
    "--show-response",
    "show_response",
    is_flag=True,
    default=False,
    help="Show response header"
)
@click.option(
    "--no-show-content",
    "no_show_content",
    is_flag=True,
    default=False,
    help="Show request content"
)
@click.option(
    "--output",
    "-o",
    "output",
    type=str,
    default=None,
    help="Save to file"
)
@click.option(
    "--resume",
    "-r",
    "resume",
    is_flag=True,
    default=False,
    help="Restore connection"
)
@click.option(
    "--threads",
    "threads",
    type=int,
    default=1,
    help="Multithreaded download"
)
def main(
    method,
    url,
    params,
    headers,
    data,
    json,
    files,
    cookies,
    auth,
    proxies,
    timeout,
    allow_redirects,
    verify,
    no_show_content,
    show_response,
    show_request,
    output,
    resume,
    threads
):
    if not method:
        method = "POST" if data or files or json else "GET"

    response = requests.wget(
        method=method,
        url=url,
        params=dict(params) or None,
        headers=dict(headers) or None,
        json=json or None,
        files=dict(files) or None,
        cookies=dict(cookies) or None,
        proxies=proxies,
        timeout=timeout,
        allow_redirects=allow_redirects,
        verify=verify,
        auth=auth,
        output=output,
        resume=resume,
        transient=False,
        threads=threads,
    )
    console = None
    if isinstance(response, list):
        response = response[0]

    if show_request:
        if not console:
            console = rich_console.Console()
        renders = [
            f"{i} [magenta]{item[0]}[/]: {item[1]}"
            for i, item in enumerate(response.request.headers.items())
        ]
        renders = rich_columns.Columns(renders, expand=True)
        renders = rich_panel.Panel(
            renders,
            title="[red]request headers[/]",
            title_align="left",
            padding=1,
            border_style="bright_blue"
        )
        console.print(renders)

    if show_response:
        if not console:
            console = rich_console.Console()
        renders = [
            f"{i} [magenta]{item[0]}[/]: {item[1]}"
            for i, item in enumerate(response.headers.items())
        ]
        renders = rich_columns.Columns(renders, expand=True)
        renders = rich_panel.Panel(
            renders,
            title="[red]response headers[red]",
            title_align="left",
            padding=1,
            border_style="bright_blue"
        )
        console.print(renders)

    if not no_show_content and not output and threads==1:
        response.encoding = response.apparent_encoding
        for chunk in response.iter_lines():
            try:
                chunk = chunk.decode(response.encoding)
            except (
                UnicodeDecodeError,
                AttributeError
            ):
                pass
            print(chunk, end="")
