#ifndef OBJECTROSCOM_H
#define OBJECTROSCOM_H

#include "chai_env/RosComBase.h"
#include <chai_msgs/ObjectState.h>
#include <chai_msgs/ObjectCmd.h>


class ObjectRosCom: public RosComBase<chai_msgs::ObjectState, chai_msgs::ObjectCmd>{
public:
    ObjectRosCom(std::string a_name);
    ObjectRosCom(std::string a_name, int a_freq);
    ~ObjectRosCom();
    virtual void init();
    virtual void run_publishers();


protected:
    virtual void reset_cmd();
    void sub_cb(chai_msgs::ObjectCmdConstPtr msg);
};


#endif
