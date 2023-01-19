#!/usr/bin/env python
# license removed for brevity
import rospy
import sys
import numpy as np
from std_msgs.msg import String
import os.path
from threading import Timer, Event, Thread

# path_data = '/home/fyandun/Documents/projects/drone_slam/Integration-Pilot-Final/catkin_ws/src/scout_waypoint_trav/data/'

# def find_trav_map():
#     full_path = path_data + 'traversability_maps.npy'
#     if os.path.isfile(full_path):
#         # self.trav_map = np.load(full_path)
#         found_trav_map  = True
#     else:
#         print("Unable to read the traversability map")
#         found_trav_map  = False

class RepeatingTimer(Thread):
    def __init__(self, interval_seconds, callback):
        super().__init__()
        self.stop_event = Event()
        self.interval_seconds = interval_seconds
        self.callback = callback

    def run(self):
        while not self.stop_event.wait(self.interval_seconds):
            self.callback()

    def stop(self):
        self.stop_event.set()

class publish_trav_way():
    def __init__(self):
        self.pub_trav_map = rospy.Publisher('/scout_trav_map', String, queue_size=10)
        self.pub_waypoints = rospy.Publisher('/scout_fuel_waypoints', String, queue_size=10)

        self.path_data = '/home/fyandun/Documents/projects/drone_slam/Integration-Pilot-Final/catkin_ws/src/scout_waypoint_trav/data/'
        
        self.found_waypoints = False
        self.found_trav_map = False

        self.trav_map = "Test"
        self.timer_trav = Timer(30.0, self.find_trav_map)

    def find_trav_map(self):
        full_path = self.path_data + 'traversability_map.npy'
        if os.path.isfile(full_path):
            self.trav_map = 'TEst'#np.load(full_path)
            self.found_trav_map  = True
            return True
        else:
            print("Unable to read the traversability map")
            self.found_trav_map  = False        
            return False

    def find_waypoints(self):
        full_path = self.path_data + 'waypoints.npy'
        if os.path.isfile(full_path):
            self.trav_map = np.load(full_path)
            self.found_waypoints = True
        else:
            print("Unable to read the traversability map")
            self.found_waypoints = False
        
    def publish_trav_map(self):

        if self.found_trav_map:
            # timer.stop()
            self.pub_trav_map.publish(self.trav_map)


def main():
    rospy.init_node('trav_waypoints_pub', anonymous=True)
    rate = rospy.Rate(10)

    publisher = publish_trav_way()

    timer_trav_map = RepeatingTimer(20, publisher.find_trav_map)
    timer_trav_map.start()    
    # timer_trav_map = rospy.Timer(rospy.Duration(5), publisher.find_trav_map)

    while not rospy.is_shutdown():
        publisher.publish_trav_map()
        rate.sleep()
    timer_trav_map.stop()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass