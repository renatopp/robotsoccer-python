# -*- coding:utf-8 -*-
# Copyright (C) 2011 Renato de Pontes Pereira, renato.ppontes at gmail dot com
#
# This module is part of robotsoccer-python and is released under 
# the MIT  License: http://www.opensource.org/licenses/mit-license.php

import math
from robotsoccer import Socket
from robotsoccer import C

CMD_GET_WORLD = 0
CMD_ACT = 4
CMD_GET_MATCH_STATUS = 6

class Robot(object):
    """
    Robot description.
    """
    def __init__(self):
        self.force = [0, 0]
        self.pos = C()
        self.old_pos = C()
        self.angle = 0
        self.old_angle = 0
        self.obstacle = C()

    def __str__(self):
        return '<Robot %s>'%str(self.pos)

    def __repr__(self):
        return str(self)


class SoccerClient(object):
    """
    Client interface for a robot soccer match simulator.

    All methods of this class are relative to own robot, i.e, the ``robot_id`` 
    robot.

    Notice that ``world_height``, ``world_width``, ``goal_length`` actually are 
    the half of real size. This values come directly from robot soccer match.
    """
    def __init__(self):
        self.scores = [0, 0]
        
        self.world_height = 0
        self.world_width = 0
        
        self.goals = [C(), C()]
        self.goal_deep = 0
        self.goal_length = 0
        
        self.robot_id = 0
        self.robot_radius = 0
        self.robot_count = 0
        
        self.ball = C()
        self.robots = None
        self.socket = None

    def connect(self, host='localhost', port=1024):
        """
        Connects to robot soccer match simulator.
        """
        self.socket = Socket()
        self.socket.connect((host, port))

        self.robot_id = self.socket.recv_int()
        self.socket.send_int(CMD_GET_WORLD)
        self.robot_count = self.socket.recv_int()
        self.robot_radius = self.socket.recv_float()
        self.world_width = self.socket.recv_float()
        self.world_height = self.socket.recv_float()
        self.goal_length = self.socket.recv_float()
        self.goal_deep = self.socket.recv_float()

        self.goals[0].x = -self.world_width
        self.goals[1].x = self.world_width

        self.robots = [Robot() for i in xrange(self.robot_count)]
        
        self.socket.send_int(CMD_GET_MATCH_STATUS)
        self.__update_match()
    
    def disconnect(self):
        """
        Disconnects from robot soccer match simulator.
        """
        self.socket.close()

    def act(self, force_left, force_right):
        """
        Does action for the robot. Receives the forces of left and right motor.
        """
        self.socket.send_int(CMD_ACT)
        self.socket.send_int(self.robot_id)
        self.socket.send_float(force_left)
        self.socket.send_float(force_right)
        self.__update_match()
    
    def __update_match(self):
        """
        Gets match status.
        """
        self.ball.x = self.socket.recv_float()
        self.ball.y = self.socket.recv_float()
        self.socket.recv_int()

        for robot in self.robots:
            robot.pos.x = self.socket.recv_float()
            robot.pos.y = self.socket.recv_float()
            robot.angle = self.socket.recv_float()
            robot.old_pos.x = self.socket.recv_float()
            robot.old_pos.y = self.socket.recv_float()
            robot.old_angle = self.socket.recv_float()
            robot.obstacle.x = self.socket.recv_float()
            robot.obstacle.y = self.socket.recv_float()
            robot.force[0] = self.socket.recv_float()
            robot.force[1] = self.socket.recv_float()
            self.socket.recv_int()

        self.scores[0] = self.socket.recv_int()
        self.scores[1] = self.socket.recv_int()

    def get_ball_angle(self):
        """
        Calculates angle difference between robot and ball, in radians.
        """
        robot = self.get_own_robot()
        alpha = (self.ball-robot.pos).angle() - robot.angle
        return self.__adjust_angle(alpha)

    def get_target_angle(self):
        """
        Calculates angle difference in radians between robot and correspondent
        goal.
        """
        robot = self.get_own_robot()
        goal = self.get_own_goal()
        alpha = (goal-self.ball).angle() - (self.ball-robot.pos).angle()
        return self.__adjust_angle(alpha)

    def get_obstacle_angle(self):
        """
        Calculates angle difference in radians between robot and the nearest 
        obstacle.
        """
        robot = self.get_own_robot()
        alpha = (robot.obstacle-robot.pos).angle() - robot.angle
        return self.__adjust_angle(alpha)

    def get_spin(self):
        """
        Calculates the angle momentum in radians.
        """
        robot = self.get_own_robot()
        alpha = robot.angle-robot.old_angle
        return self.__adjust_angle(alpha)

    def get_ball_distance(self):
        """
        Calculates distance in milimeters between robot and ball.
        """
        robot = self.get_own_robot()
        return (self.ball-robot.pos).size() - self.robot_radius

    def get_target_distance(self):
        """
        Calculates distance in milimeters between robot and goal.
        """
        robot = self.get_own_robot()
        goal = self.get_own_goal()
        return (goal-robot.pos).size() - self.robot_radius

    def get_obstacle_distance(self):
        """
        Calculates distance in milimeters between robot and the nearest 
        obstacle.
        """
        robot = self.get_own_robot()
        return (robot.obstacle-robot.pos).size() - self.robot_radius

    def get_own_robot(self):
        """
        Gets the own robot description
        """
        return self.robots[self.robot_id]

    def get_own_goal(self):
        """
        Gets own attacking goal's center.  Notice the goal of robots[1] (right) 
        is goal[0] (left) and vice versa.
        """
        return self.goals[1-self.robot_id]
    
    def get_own_score(self):
        """
        Gets scores of the own robot.
        """
        return self.scores[self.robot_id]
    
    def get_rival_robot(self):
        """
        Gets the rival robot description.
        """
        if self.robot_count == 2:
            return self.robots[1-self.robot_id]
    
    def get_rival_goal(self):
        """
        Gets attacking goal's center of the rival. Notice the goal of robots[1] 
        (right) is goal[0] (left) and vice versa.
        """
        return self.goals[self.robot_id]
    
    def get_rival_score(self):
        """
        Gets scores of the rival's robot.
        """
        return self.scores[1-self.robot_id]
    
    def __adjust_angle(self, angle):
        if angle > math.pi:
            angle -= 2*math.pi
        elif angle < -math.pi:
            angle += 2*math.pi
        
        return angle