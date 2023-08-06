# This file implements spiking neural networks as described
# in the work:
#   A. Yanguas-Gil, Coarse scale representation of spiking neural networks:
#   backpropagation through spikes and applications to neuromorphic hardware,
#   International Conference on Neuromorphic Systems (ICONS), 2020

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import math as m

class HardSoft(torch.autograd.Function):

    @staticmethod
    def forward(ctx, input, constant):
        # ctx is a context object that can be used to stash information
        # for backward computation
        ctx.constant = constant
        output = torch.sigmoid(constant*input)
        ctx.save_for_backward(output)
        return H(input)

    @staticmethod
    def backward(ctx, grad_output):
        # We return as many input gradients as there were arguments.
        # Gradients of non-Tensor arguments to forward must be None.
        fakeoutput, = ctx.saved_tensors
        return grad_output * fakeoutput*(1-fakeoutput)*ctx.constant, None

def H(x):
    return 0.5*(torch.sign(x)+1)

hardsoft = HardSoft.apply

class SpikingVextLayer(nn.Module):

    def __init__(self, tau, v0=1, beta=5):
        super(SpikingVextLayer, self).__init__()
        self.a = m.exp(-1./tau)
        self.b = tau*(1 - self.a)
        self.c = tau*(1-self.b)
        self.b = self.b/self.c
        self.v0 = v0
        self.beta = beta

    def forward(self, xi):
        xi=1.1*xi
        v = (1-s) * (self.a * v + self.b*xi) + s * xi
        s = hardsoft(v-self.v0, self.beta)
        return s, v

class SpikingLayer(nn.Module):

    def __init__(self, tau, v0=1, beta=5):
        super(SpikingLayer, self).__init__()
        self.tau = tau
        self.a = m.exp(-1./tau)
        self.b = tau*(1 - self.a)
        self.c = tau*(1-self.b)
        self.v0 = v0
        self.beta = beta

    def reset(self, xi):
        self.v = torch.zeros_like(xi).to(xi.device)
        self.s = torch.zeros_like(xi).to(xi.device)

    def forward(self, xi, init=False):
        if init:
            v = torch.zeros_like(xi).to(xi.device)
            s = torch.zeros_like(xi).to(xi.device)
        else:
            v = self.v
            s = self.s
        self.v = (1-s) * (self.a * v + self.b * xi) + s * self.c * xi
        self.s = hardsoft(self.v-self.v0, self.beta)
        return s


class SpikingDecay(nn.Module):

    def __init__(self, tau, v0=1, beta=5):
        super(SpikingDecay, self).__init__()
        self.tau = tau
        self.a = 1/tau
        self.v0 = v0
        self.beta = beta

    def forward(self, xi, init=False):
        if init:
            v = torch.zeros_like(xi).to(xi.device)
            s = torch.zeros_like(xi).to(xi.device)
        else:
            v = self.v
            s = self.s
        self.v = (1-s) * self.a * v + xi
        self.s = hardsoft(self.v-self.v0, self.beta)
        return s


class SpikingLayer2(nn.Module):

    def __init__(self, tau, v0=1, beta=5):
        super(SpikingLayer2, self).__init__()
        self.tau = tau
        self.a = m.exp(-1./tau)
        self.b = tau*(1 - self.a)
        self.v0 = v0
        self.beta = beta

    def forward(self, xi, s, v):
        v = (1-s) * (self.a * v + self.b * xi)
        s = hardsoft(v-self.v0, self.beta)
        return s, v



class SpikingNet(nn.Module):

    def __init__(self):
        super(SpikingNet, self).__init__()

    def single_pass(self, xi, init):
        pass

    def forward(self, x):
        n_batch, n_steps, Nx, Ny = x.shape
        sp = torch.zeros(n_batch, n_steps, self.Nout).to(x.device)
        for i in range(n_steps):
            init = True if i==0 else False
            xi = x[:,i,:,:].view((n_batch, 1, Nx, Ny))
            sp[:,i,:] = self.single_pass(xi, init)
        return sp

