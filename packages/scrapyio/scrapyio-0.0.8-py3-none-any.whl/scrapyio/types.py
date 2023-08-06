import typing

from httpx._client import Response

if typing.TYPE_CHECKING:
    from scrapyio import Request

    from .item_middlewares import BaseItemMiddleWare
    from .items import Item

RESPONSE_GENERATOR = typing.AsyncGenerator[Response, None]
CLEANUP_WITH_RESPONSE = typing.Tuple[RESPONSE_GENERATOR, Response]

ITEM_IGNORING_CALLBACK_TYPE = typing.Callable[
    ["Item", "BaseItemMiddleWare"], typing.Coroutine[typing.Any, typing.Any, typing.Any]
]

ITEM_ADDED_CALLBACK_TYPE = typing.Callable[
    ["Item"], typing.Coroutine[typing.Any, typing.Any, typing.Any]
]

START_REQUESTS_TYPE = typing.List[typing.Union["Request", str]]

DOWNLOADER_EXCEPTION_CALLBACK = typing.Callable[["Request", BaseException], None]
