import typing
from typing import Sequence, Mapping

from openfeature.evaluation_context import EvaluationContext
from openfeature.flag_evaluation import FlagValueType, FlagResolutionDetails
from openfeature.provider import AbstractProvider, Metadata


class StatsigProvider(AbstractProvider):
    def get_metadata(self) -> Metadata:
        return Metadata(name="StatsigProvider")

    def resolve_boolean_details(
        self, flag_key: str,
        default_value: bool,
        evaluation_context: typing.Optional[EvaluationContext] = None
    ) -> FlagResolutionDetails[bool]:
        raise NotImplementedError

    def resolve_string_details(
        self,
        flag_key: str,
        default_value: str,
        evaluation_context: typing.Optional[EvaluationContext] = None
    ) -> FlagResolutionDetails[str]:
        raise NotImplementedError

    def resolve_integer_details(
        self,
        flag_key: str,
        default_value: int,
        evaluation_context: typing.Optional[EvaluationContext] = None
    ) -> FlagResolutionDetails[int]:
        raise NotImplementedError

    def resolve_float_details(
        self,
        flag_key: str,
        default_value: float,
        evaluation_context: typing.Optional[EvaluationContext] = None
    ) -> FlagResolutionDetails[float]:
        raise NotImplementedError

    def resolve_object_details(
        self,
        flag_key: str,
        default_value: typing.Union[Sequence[FlagValueType], Mapping[str, FlagValueType]],
        evaluation_context: typing.Optional[EvaluationContext] = None
    ) -> FlagResolutionDetails[typing.Union[Sequence[FlagValueType], Mapping[str, FlagValueType]]]:
        raise NotImplementedError
