#!/usr/bin/env python
import rospy
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import PointCloud2
from map_compressor.msg import CompressedMap, CompressedPointcloud2
import zlib
import base64
import sys

compressed_map = CompressedMap()
compressed_pointcloud = CompressedPointcloud2()

def map_callback(the_map):
    global compressed_map
    compressed_map = CompressedMap()
    compressed_map.header = the_map.header
    compressed_map.info = the_map.info
    rospy.loginfo('Compressing map for {}'.format(the_map.header.frame_id))
    new_data = []
    for i in the_map.data:
        new_data.append(i+127)
    compressed_data = zlib.compress(str(bytearray(new_data)))
    compressed_map.data = base64.b64encode(compressed_data)

def pointcloud_callback(the_pointcloud):
    global compressed_pointcloud
    compressed_pointcloud_temp = CompressedPointcloud2()
    compressed_pointcloud_temp.header = the_pointcloud.header
    compressed_pointcloud_temp.height = the_pointcloud.height
    compressed_pointcloud_temp.width = the_pointcloud.width
    compressed_pointcloud_temp.is_bigendian = the_pointcloud.is_bigendian
    compressed_pointcloud_temp.point_step = the_pointcloud.point_step
    compressed_pointcloud_temp.row_step = the_pointcloud.row_step
    compressed_pointcloud_temp.is_dense - the_pointcloud.is_dense
    rospy.loginfo('Compressing pointcloud for {}'.format(the_pointcloud.header.frame_id))
    #
    #    Screw it, client doesn't need point fields
    #
    # new_fields = []
    # for field in the_pointcloud.fields:
    #     compressed_field = field.name
    #     compressed_field_data  = bytearray()
    #     compressed_field_data.append(field.offset)
    #     compressed_field_data.append(field.datatype)
    #     compressed_field_data.append(field.count)
    #     temp = zlib.compress(str(compressed_field_data))
    #     compressed_field = compressed_field + base64.b64encode(temp)
    #     new_fields.append(compressed_field)
    # compressed_pointcloud_temp.fields = new_fields
    compressed_pointcloud_temp.fields = []
    new_data = []
    for entry in the_pointcloud.data:
        new_data.append(entry)
    compressed_data = zlib.compress(str(bytearray(new_data)))
    compressed_pointcloud_temp.data = base64.b64encode(compressed_data)
    compressed_pointcloud = compressed_pointcloud_temp

poincloud_topic = ''

if len(sys.argv)-1 >= 1:
    poincloud_topic = sys.argv[1]
else:
    print 'You have to provide pointcloud topic'
    exit(-1)

sub_map = rospy.Subscriber('/map', OccupancyGrid, callback=map_callback)
pub_map = rospy.Publisher('/compressed_map', CompressedMap, queue_size=2)
sub_point = rospy.Subscriber(poincloud_topic, PointCloud2, callback=pointcloud_callback)
pub_point = rospy.Publisher('/compressed_pointcloud2', CompressedPointcloud2, queue_size=2)
rospy.init_node('map_compressor')
rate = rospy.Rate(1)

rospy.loginfo("Map Compressor started")

while not rospy.is_shutdown():
    pub_map.publish(compressed_map)
    pub_point.publish(compressed_pointcloud)
    rate.sleep()

rospy.loginfo("Map Compressor is stopping")