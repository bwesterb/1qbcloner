import random
import time
import json
import math
import sys

import zmq
import numpy as np
import scipy.optimize
import scipy.linalg as la

from common import *

def main():
    zmqc = zmq.Context()
    zmqs = zmqc.socket(zmq.PUSH)
    zmqs.connect('tcp://sw.w-nz.com:4324')
    while True:
        print 'Preparing'
        r_params = random_qbit_params()
        s_params = random_qbit_params()
        r = qbit(*r_params)
        s = qbit(*s_params)
        N = random.randint(1,8)
        n = N * 8 * 2
        initial = [random.random() for x in range(n)]
        print '  minimizing'
        xs, duration = minimize(r, s, N, initial)
        res = {'N': N,
               'r': r_params,
               's': s_params,
               'duration': duration,
               'initial': initial,
               'xs': tuple(xs)}
        print '  sending'
        zmqs.send_json(res)

def minimize(r, s, N, initial):
    rr = np.kron(r, r)
    ss = np.kron(s, s)
    n = N * 8 * 2
    start = time.time()
    res = scipy.optimize.minimize(cloningfidelity, 
                    initial,
                    [r, s, N, rr, ss],
                    method='SLSQP',
                    bounds=[(-1,1)]*n,
                    options={'maxiter': 1000})
    duration = start - time.time()
    return res.x, duration


if __name__ == '__main__':
    main()

# vim: sw=4 ts=4 sts=4
