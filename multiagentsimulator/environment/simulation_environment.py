from typing import List, Optional, Dict, Tuple, Mapping, Type, Sequence

import gym

from .finish import DoneFunction
from .interfaces import LocationID, PandemicObservation, NonEssentialBusinessLocationState, ChosenRegulation, \
    InfectionSummary
from .simulator import Simulator
from .reward import RewardFunction, SumReward, RewardFunctionFactory, RewardFunctionType
from .simulator_config import SimulationConfigs
from .simulator_settings import SimulationSettings


class GymEnvironment(gym.Env):
    _pandemic_sim: Simulator
    _stage_to_regulation: Mapping[int, ChosenRegulation]
    _obs_history_size: int
    _sim_steps_per_regulation: int
    _non_essential_business_loc_ids: Optional[List[LocationID]]
    _reward_fn: Optional[RewardFunction]
    _done_fn: Optional[DoneFunction]

    _last_observation: PandemicObservation
    _last_reward: float

    def __init__(self,
                 pandemic_sim: Simulator,
                 pandemic_regulations: Sequence[ChosenRegulation],
                 reward_fn: Optional[RewardFunction] = None,
                 done_fn: Optional[DoneFunction] = None,
                 obs_history_size: int = 1,
                 sim_steps_per_regulation: int = 24,
                 non_essential_business_location_ids: Optional[List[LocationID]] = None,
                 ):
        self._pandemic_sim = pandemic_sim
        self._stage_to_regulation = {reg.stage: reg for reg in pandemic_regulations}
        self._obs_history_size = obs_history_size
        self._sim_steps_per_regulation = sim_steps_per_regulation

        if non_essential_business_location_ids is not None:
            for loc_id in non_essential_business_location_ids:
                assert isinstance(self._pandemic_sim.state.id_to_location_state[loc_id],
                                  NonEssentialBusinessLocationState)
        self._non_essential_business_loc_ids = non_essential_business_location_ids

        self._reward_fn = reward_fn
        self._done_fn = done_fn

        self.action_space = gym.spaces.Discrete(len(self._stage_to_regulation))

    @classmethod
    def from_config(cls: Type['GymEnvironment'],
                    sim_config: SimulationConfigs,
                    pandemic_regulations: Sequence[ChosenRegulation],
                    sim_opts: SimulationSettings = SimulationSettings(),
                    reward_fn: Optional[RewardFunction] = None,
                    done_fn: Optional[DoneFunction] = None,
                    obs_history_size: int = 1,
                    non_essential_business_location_ids: Optional[List[LocationID]] = None,
                    ) -> 'GymEnvironment':
        sim = Simulator.from_config(sim_config, sim_opts)

        if sim_config.max_hospital_capacity == -1:
            raise Exception("Nothing much to optimise if max hospital capacity is -1.")

        reward_fn = reward_fn or SumReward(
            reward_fns=[
                RewardFunctionFactory.default(RewardFunctionType.INFECTION_SUMMARY_ABOVE_THRESHOLD,
                                              summary_type=InfectionSummary.CRITICAL,
                                              threshold=sim_config.max_hospital_capacity),
                RewardFunctionFactory.default(RewardFunctionType.INFECTION_SUMMARY_ABOVE_THRESHOLD,
                                              summary_type=InfectionSummary.CRITICAL,
                                              threshold=3 * sim_config.max_hospital_capacity),
                RewardFunctionFactory.default(RewardFunctionType.LOWER_STAGE,
                                              num_stages=len(pandemic_regulations)),
                RewardFunctionFactory.default(RewardFunctionType.SMOOTH_STAGE_CHANGES,
                                              num_stages=len(pandemic_regulations))
            ],
            weights=[.4, 1, .1, 0.02]
        )

        return GymEnvironment(pandemic_sim=sim,
                              pandemic_regulations=pandemic_regulations,
                              sim_steps_per_regulation=sim_opts.sim_steps_per_regulation,
                              reward_fn=reward_fn,
                              done_fn=done_fn,
                              obs_history_size=obs_history_size,
                              non_essential_business_location_ids=non_essential_business_location_ids)

    @property
    def pandemic_sim(self) -> Simulator:
        return self._pandemic_sim

    @property
    def observation(self) -> PandemicObservation:
        return self._last_observation

    @property
    def last_reward(self) -> float:
        return self._last_reward

    def step(self, action: int) -> Tuple[PandemicObservation, float, bool, Dict]:
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))

        # execute the action if different from the current stage
        if action != self._last_observation.stage[-1, 0, 0]:  # stage has a TNC layout
            regulation = self._stage_to_regulation[action]
            self._pandemic_sim.impose_regulation(regulation=regulation)

        # update the sim until next regulation interval trigger and construct obs from state hist
        obs = PandemicObservation.create_empty(
            history_size=self._obs_history_size,
            num_non_essential_business=len(self._non_essential_business_loc_ids)
            if self._non_essential_business_loc_ids is not None else None)

        hist_index = 0
        for i in range(self._sim_steps_per_regulation):
            # step sim
            self._pandemic_sim.step()

            # store only the last self._history_size state values
            if i >= (self._sim_steps_per_regulation - self._obs_history_size):
                obs.update_obs_with_sim_state(self._pandemic_sim.state, hist_index,
                                              self._non_essential_business_loc_ids)
                hist_index += 1

        prev_obs = self._last_observation
        self._last_reward = self._reward_fn.calculate_reward(prev_obs, action, obs) if self._reward_fn else 0.
        done = self._done_fn.calculate_done(obs, action) if self._done_fn else False
        self._last_observation = obs

        return self._last_observation, self._last_reward, done, {}

    def reset(self) -> PandemicObservation:
        self._pandemic_sim.reset()
        self._last_observation = PandemicObservation.create_empty(
            history_size=self._obs_history_size,
            num_non_essential_business=len(self._non_essential_business_loc_ids)
            if self._non_essential_business_loc_ids is not None else None)
        self._last_reward = 0.0
        if self._done_fn is not None:
            self._done_fn.reset()
        return self._last_observation

    def render(self, mode: str = 'human') -> bool:
        pass
