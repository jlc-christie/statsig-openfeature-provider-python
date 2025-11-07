from typing import Any, Mapping, Optional, Sequence, Union

from openfeature.evaluation_context import EvaluationContext
from openfeature.exception import ProviderFatalError
from openfeature.flag_evaluation import FlagResolutionDetails, FlagValueType, Reason
from openfeature.provider import AbstractProvider, Metadata
from statsig_python_core import Statsig, StatsigOptions, StatsigUser

DEFAULT_TARGETING_KEY = "anonymous-user"


class StatsigProvider(AbstractProvider):
    def __init__(
        self,
        sdk_key: Optional[str] = None,
        client_options: Optional[StatsigOptions] = None,
        client: Optional[Statsig] = None,
        default_targeting_key: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            sdk_key: SDK key to pass to Statsig client when initializing, cannot be passed if providing a client
            client_options: options to pass to the Statsig client when initializing, cannot be passed if providing a
                client
            client: an initialized Statsig client, if provided then client_options and sdk_key cannot be provided
            default_targeting_key: the targeting key to use for the StatsigUser used to evaluate the flag when the
                evaluation context doesn't provide one
        Returns:
            None
        """
        super().__init__(*args, **kwargs)
        if client and sdk_key:
            raise ProviderFatalError("either pass in an initialized Statsig client or an API key but not both")
        elif client and client_options:
            raise ProviderFatalError("passing in client_options has no effect if using a pre-initialized client")

        if client:
            self._client = client
        elif sdk_key:
            statsig = Statsig(sdk_key=sdk_key, options=client_options)
            statsig.initialize().wait()
            self._client = statsig
        else:
            raise ProviderFatalError("either an SDK key or an initialized client is needed to initialize the provider")

        self._default_targeting_key = default_targeting_key if default_targeting_key else DEFAULT_TARGETING_KEY

    def _get_statsig_user(self, evaluation_context: Optional[EvaluationContext] = None) -> StatsigUser:
        custom = dict(evaluation_context.attributes) if evaluation_context and evaluation_context.attributes else {}

        # TODO(jlc-christie): handle incompatible types between openfeature evaluation context properties and statsig
        #   user custom properties, e.g. datetime, Mapping, etc.
        if evaluation_context and evaluation_context.targeting_key:
            user = StatsigUser(evaluation_context.targeting_key, custom=custom)  # type:ignore[arg-type]
        else:
            user = StatsigUser(self._default_targeting_key, custom=custom)  # type:ignore[arg-type]

        return user

    def get_metadata(self) -> Metadata:
        return Metadata(name="StatsigProvider")

    def resolve_boolean_details(
        self,
        flag_key: str,
        default_value: bool,
        evaluation_context: Optional[EvaluationContext] = None,
    ) -> FlagResolutionDetails[bool]:
        user = self._get_statsig_user(evaluation_context)
        resp = self._client.get_feature_gate(user, flag_key)
        reason = Reason.TARGETING_MATCH if resp.rule_id else Reason.DEFAULT

        return FlagResolutionDetails(
            value=resp.value,
            error_code=None,
            error_message=None,
            reason=reason,
            variant=None,
            flag_metadata={},
        )

    def resolve_string_details(
        self,
        flag_key: str,
        default_value: str,
        evaluation_context: Optional[EvaluationContext] = None,
    ) -> FlagResolutionDetails[str]:
        raise NotImplementedError

    def resolve_integer_details(
        self,
        flag_key: str,
        default_value: int,
        evaluation_context: Optional[EvaluationContext] = None,
    ) -> FlagResolutionDetails[int]:
        raise NotImplementedError

    def resolve_float_details(
        self,
        flag_key: str,
        default_value: float,
        evaluation_context: Optional[EvaluationContext] = None,
    ) -> FlagResolutionDetails[float]:
        raise NotImplementedError

    def resolve_object_details(
        self,
        flag_key: str,
        default_value: Union[Sequence[FlagValueType], Mapping[str, FlagValueType]],
        evaluation_context: Optional[EvaluationContext] = None,
    ) -> FlagResolutionDetails[Union[Sequence[FlagValueType], Mapping[str, FlagValueType]]]:
        raise NotImplementedError
