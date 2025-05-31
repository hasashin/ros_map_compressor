ROS Map compressor
---

ROS module for compressing OccupancyGrid and PointCloud2 data.

## Reason
This module was created to make sending map data easier (or even possible) via wireless network. During engineer's thesis there was VR application created which used map data. 
VR headset was able to communicate via wireless network only, so any help to reduce amount of data sent was needed.

## How it works
Module subscribes to map (`/map`) and pointcloud (provided as argument) topics and publishes `/compressed_map` and `/compressed_pointcloud2` topics with compressed data.
Data is compressed using zlib
