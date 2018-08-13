//===========================================================================
/*
    Software License Agreement (BSD License)
    Copyright (c) 2017-2018

    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:

    * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
    copyright notice, this list of conditions and the following
    disclaimer in the documentation and/or other materials provided
    with the distribution.

    * Neither the name of CHAI3D nor the names of its contributors may
    be used to endorse or promote products derived from this software
    without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
    ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.

    \author    amunawar@wpi.edu
    \author    Adnan Munawar
    \version   0.1
*/
//===========================================================================

#ifndef CHAI_ENV_H
#define CHAI_ENV_H
#include <ros/ros.h>
#include "chai_env/Object.h"
#include <tf/LinearMath/Transform.h>

struct Observation{
public:
    Observation();

    geometry_msgs::PoseStamped m_nextState;
    double m_reward;
    double m_done;
};

class ChaiEnv{
public:
    ChaiEnv();
    ~ChaiEnv();
    void add_object(std::string name);
    chai_env::Object* get_object_handle(std::string name);
    bool object_cur_position(std::string name, double px, double py, double pz);
    bool object_cur_orientation(std::string name, double roll, double pitch, double yaw);
    bool object_cur_force(std::string name, double fx, double fy, double fz);
    bool object_cur_torque(std::string name, double nx, double ny, double nz);

private:

    bool object_exists(std::string name);
    static const int max_obj_size=10;
    int m_numObjects;
    std::map<std::string, boost::shared_ptr<chai_env::Object> > m_objectMap;
    std::map<std::string, boost::shared_ptr<chai_env::Object> >::iterator m_objectIt;
    boost::shared_ptr<chai_env::Object> m_Objects[max_obj_size];
};


#endif
