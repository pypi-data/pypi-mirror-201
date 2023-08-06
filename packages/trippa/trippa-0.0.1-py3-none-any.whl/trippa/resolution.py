from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, ClassVar, Mapping, Sequence, Type

from typing_extensions import Self

from trippa.dependencies import find_deps
from trippa.tasks import EntityTasks
from trippa.utils.asyncio import maybe_await
from trippa.utils.types import T

from .base import AnyFeature, BaseFeature, Info
from .results import FeatureResult, ResultFailure, ResultSuccess


@dataclass
class Resolution:
    """
    This is the hearth of `trippa`.

    The Resolution (aka resolution context) keeps track of all the computed features
    and determines how to resolve them.

    Spawn a new Resolution any time you want to calculate stuff
    on a new entity/row or just reset the calculations
    """

    features: Mapping[str, AnyFeature]
    """Features definitions available."""
    ctx: Any
    """Context passed to the resolvers."""

    _inputs: dict[str, FeatureResult[Any]] = field(default_factory=dict)
    _tasks: EntityTasks = field(default_factory=EntityTasks)

    def input(self, inputs: Mapping[AnyFeature, Any] | Mapping[str, Any]) -> Self:
        """Sets a mapping of feature values that will be used in other resolutions."""
        # Set results from inputs
        parsed_input: dict[str, FeatureResult[Any]] = {
            f.name if isinstance(f, BaseFeature) else f: ResultSuccess(v)
            for f, v in inputs.items()
        }
        self._inputs = self._inputs | parsed_input
        return self

    async def resolve_many(
        self, features: Sequence[AnyFeature]
    ) -> dict[AnyFeature, Any]:
        """Resolve many features at once."""
        results = await asyncio.gather(*[self.resolve(f) for f in features])
        return {f: results[i] for i, f in enumerate(features)}

    async def safe_resolve_many(
        self, features: Sequence[AnyFeature]
    ) -> dict[AnyFeature, FeatureResult[Any]]:
        """Same as resolve many but using `safe_resolve`."""
        results: Sequence[FeatureResult] = await asyncio.gather(
            *[self.safe_resolve(f) for f in features]
        )
        return {f: results[i] for i, f in enumerate(features)}

    async def resolve(
        self,
        feature: BaseFeature[T],
    ) -> T:
        """Resolves a feature, returning it's value. Throws on Exception"""
        result = await self.safe_resolve(feature)
        if isinstance(result, ResultFailure):
            raise result.error
        return result.value

    async def safe_resolve(self, feature: BaseFeature[T]) -> FeatureResult[T]:
        """
        Resolves a feature, returning a FeatureResult.

        Does not throw on exception, instead returns a ResultFailure wrapping it
        """
        if result := self._inputs.get(feature.name):
            return result

        if not self._tasks.get(feature):
            self._tasks[feature] = asyncio.create_task(self._safe_resolve(feature))

        return await self._tasks[feature]

    async def _safe_resolve(
        self,
        feature: BaseFeature[T],
    ) -> FeatureResult[T]:
        try:
            return ResultSuccess(await self._instance_resolver(feature))
        except Exception as err:
            return ResultFailure(err)

    async def _instance_resolver(self, feature: BaseFeature[T]) -> T:
        return await maybe_await(feature.resolver(self._info()))

    def _info(self) -> Info[Any]:
        return Info(self.ctx, self.resolve)


class Trippa:
    """Application entrypoint, used to generated resolution contexts'"""

    resolution_class: ClassVar[Type[Resolution]] = Resolution

    features: Mapping[str, AnyFeature]

    def __init__(self, features: Sequence[AnyFeature]) -> None:
        self.features = {f.name: f for f in features}

    def find_deps(self, feature: AnyFeature) -> set[AnyFeature]:
        return find_deps(feature, self.features)

    @classmethod
    def from_modules(cls, modules: list[Any]) -> Self:
        return cls(cls._get_features_from_modules(modules))

    @staticmethod
    def _get_features_from_modules(modules: list[Any]) -> list[AnyFeature]:
        return [
            feature
            for module in modules
            for feature in module.__dict__.values()
            if isinstance(feature, BaseFeature)
        ]

    def start(self, ctx: Any = None) -> Resolution:
        """Starts a new resolution context."""
        return Resolution(self.features, ctx)
