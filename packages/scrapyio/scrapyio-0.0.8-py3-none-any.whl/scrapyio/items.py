import asyncio
import json
import typing
from abc import ABC
from abc import abstractmethod
from asyncio import Task
from functools import partial
from warnings import warn

from pydantic import BaseModel

from scrapyio.item_loaders import ProxyLoader

from .exceptions import IgnoreItemError
from .item_loaders import BaseLoader
from .item_loaders import LoaderState
from .settings import CONFIGS
from .types import ITEM_ADDED_CALLBACK_TYPE
from .types import ITEM_IGNORING_CALLBACK_TYPE
from .utils import load_module

if typing.TYPE_CHECKING:
    from .item_middlewares import BaseItemMiddleWare


def build_items_middlewares_chain() -> typing.Sequence["BaseItemMiddleWare"]:
    return [
        typing.cast("BaseItemMiddleWare", load_module(middleware)())
        for middleware in CONFIGS.ITEM_MIDDLEWARES
    ]


def orjson_dumps_wrapper(*args, **kwargs) -> str:
    import orjson

    if "option" in kwargs:
        kwargs["option"] |= orjson.OPT_INDENT_2  # pragma: no cover
    else:
        kwargs["option"] = orjson.OPT_INDENT_2

    return orjson.dumps(*args, **kwargs).decode(encoding="utf-8")


class BaseItem(BaseModel):
    tablename: typing.ClassVar[typing.Optional[str]] = None

    class Config:
        try:
            import orjson

            json_dumps = orjson_dumps_wrapper
            json_loads = orjson.loads
        except ImportError:
            json_dumps = partial(json.dumps, indent=2)
            json_loads = json.loads


class Item(BaseItem):
    ...


class BaseItemsManager(ABC):
    def __init__(
        self,
        ignoring_callback: typing.Optional[ITEM_IGNORING_CALLBACK_TYPE] = None,
        success_callback: typing.Optional[ITEM_ADDED_CALLBACK_TYPE] = None,
        loaders: typing.Optional[typing.List[BaseLoader]] = None,
    ):
        self.middlewares = build_items_middlewares_chain()
        self.ignoring_callback = ignoring_callback
        self.success_callback = success_callback

        if loaders:
            self.loaders = [ProxyLoader(loader=loader) for loader in loaders]
        else:
            self.loaders = []
        if not loaders:
            warn(
                "Nothing will be saved because no "
                "loaders were specified for the item manager."
            )

    async def tear_down_loaders(self) -> None:
        for loader in self.loaders:
            await loader.close()

    async def _send_single_item_via_middlewares(
        self, item: Item
    ) -> typing.Optional[Item]:
        for middleware in self.middlewares:
            try:
                await middleware.process_item(item=item)
            except IgnoreItemError:
                if self.ignoring_callback:
                    await self.ignoring_callback(item, middleware)
                return None
        if self.success_callback:
            await self.success_callback(item)

        return item

    async def _send_items_via_middlewares(
        self, items: typing.Sequence[Item]
    ) -> typing.Sequence[Item]:
        tasks = [
            asyncio.create_task(self._send_single_item_via_middlewares(item))
            for item in items
        ]

        filtered_items = [
            added_item for added_item in await asyncio.gather(*tasks) if added_item
        ]
        loading_tasks: typing.List[Task] = []
        if self.loaders:
            await asyncio.gather(
                *(
                    loader.open()
                    for loader in self.loaders
                    if loader.state == LoaderState.CREATED
                ),
                return_exceptions=True,
            )
            for loader in self.loaders:
                for item_to_load in filtered_items:
                    loading_tasks.append(asyncio.create_task(loader.dump(item_to_load)))
        await asyncio.gather(*loading_tasks, return_exceptions=True)
        # To ensure that all dumping tasks are closed when
        # the `_tear_down` method is called, the gather method
        # should be called with return_exception=False.

        # If return_exception is set to True, after a single
        # dumping task exception, `_tear_down` will be called,
        # which will close the loader and release the
        # resources, preventing dumping tasks from being processed.

        # TODO: implement dump_exception_callback
        return typing.cast(typing.List[Item], filtered_items)

    @abstractmethod
    async def process_items(self, items: typing.Sequence[Item]) -> None:
        ...


class ItemManager(BaseItemsManager):
    async def process_items(self, items: typing.Sequence[Item]) -> None:
        await self._send_items_via_middlewares(items=items)
        return None
