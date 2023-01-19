#!/usr/bin/env python3
import rospy
import sys
import numpy as np
from std_msgs.msg import String
import os.path
from geometry_msgs.msg import PoseArray, Pose
import scipy.io as sio

class publish_trav_way():
    def __init__(self):
        self.pub_waypoints = rospy.Publisher('/scout_fuel_waypoints', PoseArray, queue_size=10)

        self.path_data = '/home/fyandun/Documents/projects/drone_slam/Integration-Pilot-Final/catkin_ws/src/scout_waypoint_trav/data/'

        self.waypoints = None

    def find_waypoints(self):        
        full_path_numpy = self.path_data + 'waypoints.npy'
        full_path_matlab = self.path_data + 'waypoints_matlab.mat'
        #first check if I have a matlab file #debugging, I should get rid of the matlab stuff soon.. - FY
        if os.path.isfile(full_path_matlab):
            self.waypoints = sio.loadmat(full_path_matlab)['centers']
            self.update_pose_list()
            return True
        else:          
            if os.path.isfile(full_path_numpy):
                self.waypoints = np.load(full_path_numpy)
                self.update_pose_list()
                return True
            else:
                # print("Unable to read the traversability map")
                return False 

    def update_pose_list(self):
        poses = []
        for waypoint in self.waypoints:
            pose = Pose()
            pose.position.x = waypoint[0]
            pose.position.y = waypoint[1]
            pose.position.z = 0. 

            pose.orientation.x = 0.
            pose.orientation.y = 0.
            pose.orientation.z = 0.
            pose.orientation.w = 1.

            poses.append(pose)

        return poses

    def publish_waypoints(self):
        if self.find_waypoints():
            pose_array = PoseArray()
            pose_array.header.frame_id = 'map'
            pose_array.header.stamp = rospy.Time.now()
            pose_list = self.update_pose_list()
            pose_array.poses = pose_list
            self.pub_waypoints.publish(pose_array)        



def main():
    rospy.init_node('trav_waypoints_pub', anonymous=True)
    rate = rospy.Rate(10)

    publisher = publish_trav_way()

    while not rospy.is_shutdown():
        publisher.publish_waypoints()
        rate.sleep()

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass