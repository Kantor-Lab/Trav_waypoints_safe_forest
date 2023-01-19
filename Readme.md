## Repo for reading the traversability map and waypoints - Safe Forest
This repo contains the data generated from the traversability evaluation and the waypoints generation.

This is a catkin package that only requires scipy as external python dependency. 
```
pip install scipy
```
or
```
conda install scipy
```

If worried about mixing dependencies in the system, I suggest using a virtual environment. However the ROS dependencies need to be installed in the new virtual env. For that, **activate** your virtual environment and run:
```
pip install -U rosinstall msgpack empy defusedxml netifaces
```

An additional package that needs to be installed is the [ROS navigation stack](https://github.com/ros-planning/navigation). This package is used to read the traversability image and publish it into a occupancy grid. 

The configs folder contains the yaml that configurates the package in terms of resolution, world origin and image to be read.

The data folder contains the results of *offline* processing the traversability. The repo for that will be released soon. For now, we have tiffs for georeferenced traversability and fuel maps, the traversability png image and the file containng the waypoints. The current waypoint file is *.mat*, but will be changed to numpy *.npy* soon.

The published topics are */map* as a 2D occupancy grid, and */scout_fuel_waypoints* as a pose array msg. To run everything source the catkin_ws and run:
```
roslaunch scout_waypoint_trav map_trav_pub.launch
```

If having problems running the node to generate the waypoints, try changing the permissions of the python file.