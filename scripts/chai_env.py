#!/usr/bin/env python
from chai_client import ChaiClient, Object
from gym import spaces
import numpy as np
import time
import math


class Observation:
    def __init__(self):
        self.state = []
        self.reward = 0.0
        self.is_done = False
        self.info = {}
        self.m_sim_step_no = 0

    def cur_observation(self):
        return np.array(self.state), self.reward, self.is_done, self.info


class ChaiEnv():
    def __init__(self):
        self.m_obj_handle = []

        self.m_chai_client = ChaiClient()
        self.m_chai_client.create_objs_from_rostopics()
        # self.m_chai_client.print_summary()
        self.m_chai_client.start()

        self.m_obs = Observation()
        self.action_lims = np.array([30, 30, 30, 2, 2, 2])
        self.action_space = spaces.Box(-self.action_lims, self.action_lims)
        self.observation_space = spaces.Box(-np.inf, np.inf, shape=(6,))

        self.m_Base = self.m_chai_client.get_obj_handle('Base')

        pass

    def make(self, a_name):
        self.m_obj_handle = self.m_chai_client.get_obj_handle(a_name)
        self.m_chai_client.enable_throttling(True)
        if self.m_obj_handle is None:
            raise Exception

    def reset(self):
        action = [0.0,
                  0.0,
                  0.0,
                  0.0,
                  0.0,
                  0.0]
        return self.step(action)[0]

    def step(self, action):
        action[0:3] = np.clip(action[0:3], -self.action_lims[0:3], self.action_lims[0:3])
        action[3:6] = np.clip(action[3:6], -self.action_lims[3:6], self.action_lims[3:6])
        assert len(action) == 6
        self.m_obj_handle.command(action[0],
                                  action[1],
                                  action[2],
                                  action[3],
                                  action[4],
                                  action[5])
        time.sleep(0.005)
        self.update_observation()
        return self.m_obs.cur_observation()

    def render(self, mode):
        print ' I am a {} POTATO'.format(mode)

    def update_observation(self):
        state = 0
        while state == 0:
            state = self.m_obj_handle.get_pose()

        self.m_obs.state = state
        self.m_obs.reward = self.calculate_reward(state)
        self.m_obs.is_done = self.check_if_done()
        self.m_obs.info = self.update_info()

    def calculate_reward(self, state):
        cur_pose = state
        pos_epsilon = 0.5
        rot_epsilon = 0.1
        reward = 0.0
        if math.fabs(cur_pose[0]) < pos_epsilon and\
            math.fabs(cur_pose[1]) < pos_epsilon and\
            0.926 - math.fabs(cur_pose[2]) < pos_epsilon:
            reward = 100
        if math.fabs(cur_pose[3]) < rot_epsilon and\
            math.fabs(cur_pose[4]) < rot_epsilon and\
            math.fabs(cur_pose[5]) < rot_epsilon:
            reward += 50
        return reward

    def check_if_done(self):
        return False

    def update_info(self):
        return {}
