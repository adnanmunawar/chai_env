#!/usr/bin/env python
from tf import transformations
from geometry_msgs.msg import Pose
from chai_msgs.msg import ObjectCmd
from wd import WatchDog
import rospy


class Object(WatchDog):
    def __init__(self, a_name):
        super(Object, self).__init__()
        self.time_stamp = []
        self.sim_step_cur = 0
        self.sim_step_pre_update = 0
        self.name = a_name
        self.pose = Pose()
        self.cmd = ObjectCmd()
        self.pub = None
        self.sub = None
        self.pub_flag = True
        self._active = False

    def set_active(self):
        self._active = True

    def is_active(self):
        return self._active

    def ros_cb(self, data):
        self.name = data.name.data
        self.pose = data.pose
        self.time_stamp = data.header.stamp
        self.sim_step_cur = data.sim_step

    def command(self, double fx, double fy, double fz, double nx, double ny, double nz, *jnt_cmds):
        self.cmd.wrench.force.x = fx
        self.cmd.wrench.force.y = fy
        self.cmd.wrench.force.z = fz
        self.cmd.wrench.torque.x = nx
        self.cmd.wrench.torque.y = ny
        self.cmd.wrench.torque.z = nz
        for jcmd in jnt_cmds:
            self.cmd.joint_cmds.append(jcmd)
        self.cmd.header.stamp = rospy.Time.now()

        self.sim_step_pre_update = self.sim_step_cur
        self.acknowledge_wd()

    def get_cur_sim_step(self):
        return self.sim_step_cur

    def get_pre_update_sim_step(self):
        return self.sim_step_pre_update

    def clear_cmd(self):
        self.cmd.wrench.force.x = 0
        self.cmd.wrench.force.y = 0
        self.cmd.wrench.force.z = 0
        self.cmd.wrench.torque.x = 0
        self.cmd.wrench.torque.y = 0
        self.cmd.wrench.torque.z = 0

    def get_pose(self):
        quat = self.pose.orientation
        explicit_quat = [quat.x, quat.y, quat.z, quat.w]
        rpy = transformations.euler_from_quaternion(explicit_quat, 'szyx')
        pose = [self.pose.position.x,
                self.pose.position.y,
                self.pose.position.z,
                rpy[0],
                rpy[1],
                rpy[2]]
        return pose

    def run_publisher(self):
        if self.pub_flag:
            if self.is_wd_expired():
                self.console_print(self.name)
                self.clear_cmd()
            self.pub.publish(self.cmd)

