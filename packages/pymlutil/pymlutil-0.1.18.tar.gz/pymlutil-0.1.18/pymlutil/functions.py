import torch
import math
import numpy as np

def GaussianBasis(x, zero=0.0, sigma=0.33):
    return torch.exp(-1*torch.square((x-zero)/(2*sigma*sigma))) # torch.square not supported by torch.onnx

def NormGausBasis(len, i, zero, sigma=1.0):
        den = 0.0
        num = 0.0
        for j in range(len):
            bias = GaussianBasis(j,zero,sigma)
            if j==i:
                num=bias
            den = den + bias
        return num/den


# Exponential function from vertex and point
class Exponential():
    def __init__(self,vx=0.0, vy=0.0, px=1.0, py=1.0, power=2.0):
        self.vx = vx
        self.vy = vy
        self.px = px
        self.py = py
        if power < 0:
            raise ValueError('Exponential error power {} must be >= 0'.format(power))
        self.power = power
        if px <= vx:
            raise ValueError('Exponential error px={} must be > vx'.format(px, vx))
        else:
            self.a = (py-vy)/np.power(px-vx,self.power)
    def f(self, x):

        y = np.piecewise(x, 
            [x < self.vx, x > self.px], 
            [self.vy, self.py, lambda x : self.a*pow(x-self.vx,self.power) + self.vy]) 

        return y

def Sigmoid(x, scale = 1.0, offset=0.0, k_exp = 1.0):
    sigmoid = scale/(1.0+np.exp(-1*k_exp*(x-offset)))
    return sigmoid