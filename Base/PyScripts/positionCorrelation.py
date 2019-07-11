from py_scripts.utils import *
import numpy as np



def distance(x,y):
    S = (np.abs(x - y)**2).sum()
    return np.sqrt(S)

def pos_cor(config,L,max_dist = 10.0):
    """
    this function takes in the positions of a configuration
    and the boundary dimensions and outputs a probability 
    distrobution for the position corrolation from 0 to 
    max_dist.
    """
    dist = []
    for i in range(len(config["x"])):
        a = np.array([config["x"][i],config["y"][i],config["z"][i]])
        for j in range(len(config["x"])):
            b = np.array([config["x"][j],config["y"][j],config["z"][j]]) 
            d = distance(x,y)
            
