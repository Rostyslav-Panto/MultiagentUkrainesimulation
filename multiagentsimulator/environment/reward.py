
import enum
from abc import abstractmethod, ABCMeta
from typing import Any, Dict, List, Optional, Union, Type, Sequence

import numpy as np


from .interfaces import PandemicObservation, InfectionSummary, sorted_infection_summary


class RewardFunction(metaclass=ABCMeta):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def calculate_reward(self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation) -> float:
        pass


class RewardFunctionType(enum.Enum):
    INFECTION_SUMMARY_INCREASE = 'infection_summary_increase'
    INFECTION_SUMMARY_ABOVE_THRESHOLD = 'infection_summary_above_threshold'
    INFECTION_SUMMARY_ABSOLUTE = 'infection_summary_absolute'
    UNLOCKED_BUSINESS_LOCATIONS = 'unlocked_business_locations'
    LOWER_STAGE = 'lower_stage'
    SMOOTH_STAGE_CHANGES = 'smooth_stage_changes'

    @staticmethod
    def values() -> List[str]:
        return [c.value for c in RewardFunctionType.__members__.values()]


_REWARDS_REGISTRY: Dict[RewardFunctionType, Type[RewardFunction]] = {}


def _register_reward(type: RewardFunctionType, reward_fun: Type[RewardFunction]) -> None:
    if type not in _REWARDS_REGISTRY:
        _REWARDS_REGISTRY[type] = reward_fun
        return

    raise RuntimeError(f'Reward type {type} already registered')


class RewardFunctionFactory:
    @staticmethod
    def default(reward_function_type: Union[str, RewardFunctionType], *args: Any, **kwargs: Any) -> RewardFunction:
        rf_type = RewardFunctionType(reward_function_type)

        if rf_type not in _REWARDS_REGISTRY:
            raise ValueError('Unknown reward function type.')

        return _REWARDS_REGISTRY[rf_type](*args, **kwargs)


class SumReward(RewardFunction):

    _reward_fns: List[RewardFunction]
    _weights: np.ndarray

    def __init__(self, reward_fns: List[RewardFunction], weights: Optional[List[float]] = None,
                 *args: Any,
                 **kwargs: Any):

        super().__init__(*args, **kwargs)
        if weights is not None:
            assert len(weights) == len(reward_fns), 'There must be one weight for each reward function.'
        else:
            weights = [1.] * len(reward_fns)
        self._weights = np.asarray(weights)
        self._reward_fns = reward_fns

    def calculate_reward(self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation) -> float:
        rewards = np.array([rf.calculate_reward(prev_obs, action, obs) for rf in self._reward_fns])
        return float(np.sum(rewards * self._weights))


class InfectionSummaryIncreaseReward(RewardFunction):
    _index: int

    def __init__(self, summary_type: InfectionSummary, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        assert summary_type in [InfectionSummary.INFECTED, InfectionSummary.CRITICAL, InfectionSummary.DEAD]
        self._index = sorted_infection_summary.index(summary_type)

    def calculate_reward(self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation) -> float:
        prev_summary = prev_obs.global_infection_summary[..., self._index]
        summary = obs.global_infection_summary[..., self._index]
        if np.any(prev_summary == 0):
            return 0
        return -1 * float(np.clip((summary - prev_summary) / prev_summary, 0, np.inf).mean())


class InfectionSummaryAbsoluteReward(RewardFunction):
    _index: int

    def __init__(self, summary_type: InfectionSummary, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        assert summary_type in [InfectionSummary.INFECTED, InfectionSummary.CRITICAL, InfectionSummary.DEAD]
        self._index = sorted_infection_summary.index(summary_type)

    def calculate_reward(self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation) -> float:
        return float(-1 * np.mean(obs.global_infection_summary[..., self._index]))


class InfectionSummaryAboveThresholdReward(RewardFunction):
    _threshold: float
    _index: int

    def __init__(self, summary_type: InfectionSummary, threshold: float, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._threshold = threshold
        assert summary_type in [InfectionSummary.INFECTED, InfectionSummary.CRITICAL, InfectionSummary.DEAD]
        self._index = sorted_infection_summary.index(summary_type)

    def calculate_reward(self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation) -> float:
        return float(-1 * max(np.mean(obs.global_infection_summary[..., self._index]
                                      - self._threshold) / self._threshold, 0))


class UnlockedBusinessLocationsReward(RewardFunction):
    _obs_indices: Optional[Sequence[int]] = None

    def __init__(self, obs_indices: Optional[Sequence[int]] = None, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._obs_indices = obs_indices

    def calculate_reward(self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation) -> float:
        if obs.unlocked_non_essential_business_locations is None:
            return 0.
        else:
            unlocked_locations = (obs.unlocked_non_essential_business_locations if self._obs_indices is None
                                  else obs.unlocked_non_essential_business_locations[..., self._obs_indices])
            return float(np.mean(unlocked_locations))


class LowerStageReward(RewardFunction):
    _stage_rewards: np.ndarray

    def __init__(self, num_stages: int, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        stage_rewards = np.arange(0, num_stages) ** 1.5
        self._stage_rewards = stage_rewards / np.max(stage_rewards)

    def calculate_reward(self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation) -> float:
        return -float(self._stage_rewards[action])


class SmoothStageChangesReward(RewardFunction):

    def __init__(self, num_stages: int, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    def calculate_reward(self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation) -> float:
        return float(-1 * np.abs(obs.stage - prev_obs.stage).mean())


_register_reward(RewardFunctionType.INFECTION_SUMMARY_INCREASE, InfectionSummaryIncreaseReward)
_register_reward(RewardFunctionType.INFECTION_SUMMARY_ABOVE_THRESHOLD, InfectionSummaryAboveThresholdReward)
_register_reward(RewardFunctionType.INFECTION_SUMMARY_ABSOLUTE, InfectionSummaryAbsoluteReward)
_register_reward(RewardFunctionType.UNLOCKED_BUSINESS_LOCATIONS, UnlockedBusinessLocationsReward)
_register_reward(RewardFunctionType.LOWER_STAGE, LowerStageReward)
_register_reward(RewardFunctionType.SMOOTH_STAGE_CHANGES, SmoothStageChangesReward)
