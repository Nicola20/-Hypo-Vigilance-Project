#!/usr/bin/env/python3

"""
------------------------------------------------------------------------------------------------
 @authors       Nicola Lea Libera (117073), Laura Simon (116992), Chiranjeevi Janjanam()
------------------------------------------------------------------------------------------------
 Description: This script simply prints out a random permutation to decide in which order
              the levels of the space game are going to be played.
------------------------------------------------------------------------------------------------
"""

from numpy import random
import numpy as np


def main():

    arr = np.array([1, 2, 3, 4, 5])
    print(random.permutation(arr))


if __name__ == '__main__':
    main()
