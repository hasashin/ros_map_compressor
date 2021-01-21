#!/usr/bin/env python
import rospy
from nav_msgs.msg import OccupancyGrid
from map_compressor.msg import CompressedMap
import zlib
import base64
import time

current_map = OccupancyGrid()
compressed_map = CompressedMap()

def map_callback(the_map):
    global current_map 
    global compressed_map
    current_map = the_map
    rospy.loginfo('Starting compression')
    compressed_map = CompressedMap()
    compressed_map.header = the_map.header
    compressed_map.info = the_map.info
    new_data = []
    for i in the_map.data:
        new_data.append(i+127)
    compressed_data = zlib.compress(str(bytearray(new_data)))
    compressed_map.data = base64.b64encode(compressed_data)


sub = rospy.Subscriber('/map', OccupancyGrid, callback=map_callback)
pub = rospy.Publisher('/compressed_map', CompressedMap, queue_size=2)
rospy.init_node('map_compressor')
rate = rospy.Rate(1)

rospy.loginfo("Map Compressor started")

while not rospy.is_shutdown():
    pub.publish(compressed_map)
    rate.sleep()

rospy.loginfo("Map Compressor is stopping")