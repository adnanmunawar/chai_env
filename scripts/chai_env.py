#!/usr/bin/env python
from chai_client import ChaiClient
from gym import spaces
import numpy as np
import math
import time
from chai_world import World
from chai_object import Object
from numpy import linalg as LA


class Observation:
    def __init__(self):
        self.state = [0]*13
        self.dist = 0
        self.reward = 0.0
        self.prev_reward = 0.0
        self.cur_reward = 0.0
        self.is_done = False
        self.info = {}
        self.sim_step_no = 0

    def cur_observation(self):
        return np.array(self.state), self.reward, self.is_done, self.info


class ChaiEnv:
    def __init__(self):
        self.obj_handle = Object
        self.world_handle = World

        self.chai_client = ChaiClient()
        self.chai_client.create_objs_from_rostopics()
        self.n_skip_steps = 5
        self.enable_step_throttling = True
        self.action = []
        self.obs = Observation()
        self.action_lims_low = np.array([-30, -30, -30, -2, -2, -2, 0])
        self.action_lims_high = np.array([30, 30, 30, 2, 2, 2, 1])
        self.action_space = spaces.Box(self.action_lims_low, self.action_lims_high)
        self.observation_space = spaces.Box(-np.inf, np.inf, shape=(13,))

        self.base_handle = self.chai_client.get_obj_handle('Base')
        self.prev_sim_step = 0

        pass

    def skip_sim_steps(self, num):
        self.n_skip_steps = num
        self.world_handle.set_num_step_skips(num)

    def set_throttling_enable(self, check):
        self.enable_step_throttling = check
        self.world_handle.enable_throttling(check)

    def make(self, a_name):
        self.obj_handle = self.chai_client.get_obj_handle(a_name)
        self.world_handle = self.chai_client.get_obj_handle('World')
        self.world_handle.enable_throttling(self.enable_step_throttling)
        self.world_handle.set_num_step_skips(self.n_skip_steps)
        if self.obj_handle is None or self.world_handle is None:
            raise Exception

    def reset(self):
        action = [0.0,
                  0.0,
                  0.0,
                  0.0,
                  0.0,
                  0.0,
                  0.0]
        return self.step(action)[0]

    def step(self, action):
        assert len(action) == 7
        action = np.clip(action, self.action_lims_low, self.action_lims_high)
        self.action = action

        self.obj_handle.pose_command(action[0],
                                     action[1],
                                     action[2],
                                     action[3],
                                     action[4],
                                     action[5],
                                     action[6])
        self.world_handle.update()
        self._update_observation(action)
        return self.obs.cur_observation()

    def render(self, mode):
        print ' I am a {} POTATO'.format(mode)

    def _update_observation(self, action):
        if self.enable_step_throttling:
            step_jump = 0
            while step_jump < self.n_skip_steps:
                step_jump = self.obj_handle.get_sim_step() - self.prev_sim_step
                time.sleep(0.00001)
            self.prev_sim_step = self.obj_handle.get_sim_step()
            if step_jump > self.n_skip_steps:
                print 'WARN: Jumped {} steps, Default skip limit {} Steps'.format(step_jump, self.n_skip_steps)
        else:
            cur_sim_step = self.obj_handle.get_sim_step()
            step_jump = cur_sim_step - self.prev_sim_step
            self.prev_sim_step = cur_sim_step

        state = self.obj_handle.get_pose() + self.base_handle.get_pose() + [step_jump]
        self.obs.state = state
        self.obs.reward = self._calculate_reward(state, action)
        self.obs.is_done = self._check_if_done()
        self.obs.info = self._update_info()

    def _calculate_reward(self, state, action):
        prev_dist = self.obs.dist
        cur_dist = LA.norm(np.subtract(state[6:9], state[0:3]))
        action_penalty = np.sum(np.square(action))

        reward = (prev_dist - cur_dist) - 4 * action_penalty
        self.obs.dist = cur_dist
        return reward

    def _check_if_done(self):
        return False

    def _update_info(self):
        return {}
