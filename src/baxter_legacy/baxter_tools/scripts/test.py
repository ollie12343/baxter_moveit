#!/usr/bin/env python3

import threading
import rospy
import time
import os
from sensor_msgs.msg import JointState
from baxter_core_msgs.msg import JointCommand, DigitalIOState


save = [{}, {}]


def subscriber():
	rospy.Subscriber('/robot/digital_io/right_button_back/state', DigitalIOState, callback, queue_size=10)
	rospy.spin()
		
def callback(msg):
	if msg.state == 1:
		raise KeyboardInterrupt


def saver():
		rospy.Subscriber('/robot/joint_states',JointState, save_callback, queue_size=10)
		rospy.spin()


def save_callback(msg):
	pos = list(msg.position)
	if len(pos) < 3:
		return
	for i, p in enumerate(pos):
		pos[i] = round(p, 3)

	r = {'right_s0':0, 'right_s1':0, 'right_e0':0, 'right_e1':0,'right_w0':0,  'right_w1':0, 'right_w2':0}
	l = {'left_s0':0,'left_s1':0,'left_e0':0, 'left_e1':0, 'left_w0':0, 'left_w1':0, 'left_w2':0}
	l['left_e0'] = pos[2]
	l['left_e1'] = pos[3]
	l['left_s0'] = pos[4]
	l['left_s1'] = pos[5]
	l['left_w0'] = pos[6]
	l['left_w1'] = pos[7]
	l['left_w2'] = pos[8]
	r['right_e0'] = pos[9]
	r['right_e1'] = pos[10]
	r['right_s0'] = pos[11]
	r['right_s1'] = pos[12]
	r['right_w0'] = pos[13]
	r['right_w1'] = pos[14]
	r['right_w2'] = pos[15]
	save.clear()
	save.append(r)
	save.append(l)
	raise KeyboardInterrupt

def publisher(save):
	rospy.publisher('/robot/limb/right/joint_command',JointCommand, queue_size=10)

	rate = rospy.Rate(500)
	while not rospy.ris_shutdown():
		publisher.publish(cmd)
		rate.sleep()


def main():

	try:
		rospy.init_node('subscriber')
		subscriber()
	except KeyboardInterrupt:
		os.system("rosnode kill subscriber")

	try:
		rospy.init_node('saver')
		saver()
	except KeyboardInterrupt:
		os.system("rosnode kill SAVER")
		print(save[0].values())
		time.sleep(5)
	
	try:
		cmd = JointCommand()
		cmd.names = save[0].keys()
		cmd.mode = JointCommand.POSITION_MODE
		cmd.command = set(save[0].values())
		rospy.init_node('publisher')
		publisher()
	except KeyboardInterrupt:
		os.system("rosnode kill publisher")
	
	try:
		rospy.init_node('saver')
		saver()
	except KeyboardInterrupt:
		os.system("rosnode kill saver")
		print(save[0].vaues())
		time.sleep(5)
		
	
	rclpy.shutdown()
	
if __name__ == '__main__':
	main()
