# -*- coding:utf-8 -*-

import math
from robotsoccer.client import SoccerClient

class TLFNClient(SoccerClient):
    '''
    Robot SoccerClient using TLFN network.
    '''
    def __init__(self, weight_file=None):
        super(TLFNClient, self).__init__()

        self.weight_file = weight_file
        self.layer_h = []
        self.layer_o = []
        self.outputs = [0, 0]

        if self.weight_file:
            self.load_weights(weight_file)

    def load_weights(self, weight_file):
        '''
        Load a weight file.

        File format::

            <size of input layer> <size of hidden layer> <size of output layer>
            <ball dist> <ball ang> <target ang> <obst dist> <obst ang> <spin> <last leftmotor> <last rightmotor> <actual leftmotor> <actual rightmotor>
            ... next train set ...
        '''

        wf = open(weight_file)
        self.n_inputs, \
        self.n_hiddens, \
        self.n_outputs = [int(i) for i in wf.readline().strip().split()]

        self.layer_h = []
        self.layer_o = []
        for i in xrange(self.n_hiddens):
            n = []
            line = wf.readline().strip()
            for j, v in enumerate(line.split()):
                n.append(float(v))
            self.layer_h.append(n)

        for i in xrange(self.n_outputs):
            n = []
            line = wf.readline().strip()
            for j, v in enumerate(line.split()):
                n.append(float(v))
            self.layer_o.append(n)
            
        self.outputs = [0, 0]

    def run(self):
        '''
        Run the TLFN client.
        '''
        while True:
            self.step()
            

    def step(self):
        '''
        Calculate the next motor forces and apply the ``act``
        '''
        inputs = [
            self.get_ball_distance(),
            self.get_ball_angle(),
            self.get_target_angle(),
            self.get_obstacle_distance(),
            self.get_obstacle_angle(),
            self.get_spin(),
            self.outputs[0],
            self.outputs[1],
            1
        ]

        i_ = []
        for i in xrange(self.n_hiddens):
            temp = 0
            for j, k in zip(inputs, self.layer_h[i]):
                temp += j*k
            
            i_.append(math.tanh(temp))
        i_.append(1)

        self.outputs = []
        for i in xrange(self.n_outputs):
            temp = 0
            for j, k in zip(i_, self.layer_o[i]):
                temp += j*k
            
            self.outputs.append(temp)
        
        self.act(self.outputs[0], self.outputs[1])
        
        return self.outputs