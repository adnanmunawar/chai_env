#include "chai_env/Object.h"
namespace chai_env{
Object::Object(std::string a_name): ObjectRosCom(a_name){

}

void Object::cur_position(double px, double py, double pz){
    m_trans.setOrigin(tf::Vector3(px, py, pz));
    m_State.pose.position.x = px;
    m_State.pose.position.y = py;
    m_State.pose.position.z = pz;
}

void Object::cur_orientation(double roll, double pitch, double yaw){
    tf::Quaternion rot_quat;
    rot_quat.setRPY(roll, pitch, yaw);
    m_trans.setRotation(rot_quat);
    tf::quaternionTFToMsg(rot_quat, m_State.pose.orientation);
}

void Object::cur_orientation(double qx, double qy, double qz, double qw){
    tf::Quaternion rot_quat(qx, qy, qz, qw);
    m_trans.setRotation(rot_quat);
    tf::quaternionTFToMsg(rot_quat, m_State.pose.orientation);
}

void Object::cur_force(double fx, double fy, double fz){
    tf::Vector3 f(fx, fy, fz);
    tf::vector3TFToMsg(f, m_State.wrench.force);
}

void Object::cur_torque(double nx, double ny, double nz){
    tf::Vector3 n(nx, ny, nz);
    tf::vector3TFToMsg(n, m_State.wrench.torque);
}

void Object::update_cmd_from_ros(){
    m_cmd.update(&m_Cmd);
}

void Object::set_chai_wall_time(double a_sec){
    m_State.chai_wall_time = a_sec;
    increment_sim_step();
    m_State.header.stamp = ros::Time::now();
}

extern "C"{

Object* create_object(std::string name){
    return new Object(name);
}

void destroy_object(Object* obj){
    delete obj;
}

}
}
