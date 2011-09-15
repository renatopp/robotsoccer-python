# -*- coding:utf-8 -*-
# Copyright (C) 2011 Renato de Pontes Pereira, renato.ppontes at gmail dot com
#
# This module is part of robotsoccer-python and is released under 
# the MIT  License: http://www.opensource.org/licenses/mit-license.php

import math
import socket
from struct import pack, unpack

class Socket(socket.socket):
    """
    Socket interface with specific methods for commmunication with robot soccer
    match simulator.
    """
    def __init__(self):
        super(Socket, self).__init__(type=socket.SOCK_STREAM)

    def send_float(self, n):
        """
        Receive a string or a number and send via socket in specific float byte
        format
        """
        super(Socket, self).send(pack('f', float(n)))

    def send_int(self, n):
        """
        Receive a string or a number and send via socket in specific int byte
        format
        """
        super(Socket, self).send(pack('i', int(n)))

    def recv_int(self):
        """
        Receive a string in integer byte format and returns an integer
        """
        return unpack('i', self.recv(4))[0]
    
    def recv_float(self):
        """
        Receive a string in float byte format and returns a float
        """
        return unpack('f', self.recv(4))[0]


class Coord(object):
    """
    Represents a point in 2D cartesian system
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return 'C('+str(self.x)+', '+str(self.y)+')'

    def __repr__(self):
        return str(self)

    def __sub__(self, o):
        return C(self.x-o.x, self.y-o.y)
    
    def __add__(self, o):
        return C(self.x+o.x, self.y+o.y)

    def angle(self):
        if self.x == 0 and self.y == 0:
            return 0
        
        return math.atan2(self.y, self.x)

    def size(self):
        return math.sqrt(self.x**2 + self.y**2)

C = Coord
