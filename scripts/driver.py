#!/usr/bin/env python3
import rospy
from ping1d.msg import PingRange
from brping import Ping1D


def publish_sonar_data():
    # Specification of the sonar sensor is available here:
    # https://www.bluerobotics.com/store/sensors-sonars-cameras/sonar/ping-sonar-r2-rp/
    rospy.init_node("ping1d_driver")

    usb_port = rospy.get_param('~usb_port', '/dev/ttyUSB0')
    frequency = rospy.get_param('~frequency', 10)
    frame = rospy.get_param('~frame', "ping1d_link")
    fov = rospy.get_param('~fov', 0.523)
    min_range = rospy.get_param("~min_range", 0.5)
    max_range = rospy.get_param("~max_range", 50.0)

    sonar_driver = Ping1D()
    sonar_driver.connect_serial(device_name=usb_port)
    if sonar_driver.initialize() is False:
        print("Fail to initialize Ping!")
        exit(1)

    rospy.loginfo("connecting to Ping1D Sonar at {}".format(usb_port))
    pub_sonar = rospy.Publisher("/ping1d/range", PingRange, queue_size=1)
    range_msg = PingRange()
    range_msg.header.frame_id = frame
    range_msg.radiation_type = 1
    range_msg.field_of_view = fov
    range_msg.min_range = min_range
    range_msg.max_range = max_range
    rate = rospy.Rate(frequency)

    while not rospy.is_shutdown():
        data = sonar_driver.get_distance_simple()
        confidence = data["confidence"]
        range_msg.confidence = confidence
        range_msg.range = data["distance"] / 1000.0
        range_msg.header.stamp = rospy.Time.now()
        pub_sonar.publish(range_msg)
        # rospy.loginfo(
        #     f"Distance: {range_msg.range: .4f}\tConfidence: {confidence: .0f}")
        rate.sleep()


if __name__ == "__main__":
    try:
        publish_sonar_data()
    except rospy.ROSInterruptException:
        pass
