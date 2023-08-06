import dataclasses
from dataclasses import dataclass
from typing import Any, Awaitable, cast

from trippa.base import AnyFeature, BaseFeature
from trippa.results import FeatureResult
from trippa.utils.types import T


@dataclass
class EntityTasks:
    _tasks: dict[AnyFeature, Any] = dataclasses.field(default_factory=dict)

    def __getitem__(self, __key: BaseFeature[T]) -> Awaitable[FeatureResult[T]]:
        return cast(
            Awaitable[FeatureResult[T]],
            self._tasks[__key],
        )

    def get(self, __key: BaseFeature[T]) -> Awaitable[FeatureResult[T]] | None:
        return self._tasks.get(__key)

    def __setitem__(
        self,
        __key: BaseFeature[T],
        item: Awaitable[FeatureResult[T]],
    ) -> None:
        self._tasks[__key] = item
