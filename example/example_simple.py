# -*- coding:utf-8 -*-
# Copyright (C) 2011 Renato de Pontes Pereira, renato.ppontes at gmail dot com
#
# This module is part of robotsoccer-python and is released under 
# the MIT  License: http://www.opensource.org/licenses/mit-license.php

"""
A small example of robotsoccer-python usage.

To run this module type in terminal::

   python example_simple.py host port

If host or port is omitted 'localhost' and 1024 are assumed as default
"""
import os
import sys
import math

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from robotsoccer import SoccerClient

if __name__ == '__main__': 
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'    
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1024
    
    sc = SoccerClient()
    sc.connect(host, port)

    # Action loop
    while True:
        # Gets the angle between robot and ball
        ball_angle = sc.get_ball_angle()

        # Gets the angle between goal and robot
        target_angle = sc.get_target_angle()

        # Defines an action based on ball_angle and target_angle, resulting in
        # a value of force for left and right robot's motors
        angle = ball_angle - target_angle
        if angle < -math.pi:
            angle += 2*math.pi
        elif angle > math.pi:
            angle -= 2*math.pi
        elif angle < -math.pi/2:
            angle =  -math.pi/2
        elif angle > math.pi/2:
            angle = math.pi/2
        
        force_left = math.cos(angle) - math.sin(angle)
        force_right = math.cos(angle) + math.sin(angle)

        # Sends the action of robot to simulator
        sc.act(force_left, force_right)

    # Disconnects from match simulator (actually this line is never called)
    sc.disconnect()
