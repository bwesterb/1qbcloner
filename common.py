import math
import cmath
import random

import numpy as np
import scipy.linalg as la

def random_qbit_params():
    return (random.random() * 2 * math.pi,
            random.random() * 2 * math.pi,
            random.random() * 2 * math.pi,
            random.random())

def qbit(phi, chi, psi, l):
    U = unitary(phi, chi, psi)
    rho = U * np.diag([l, 1-l]) * U.H
    rho = (rho + rho.H) * 0.5
    return rho

def unitary(phi, chi, psi):
    return np.matrix([[cmath.exp(1j*psi) * math.cos(phi),
                       cmath.exp(1j*chi) * math.sin(phi)],
                      [-cmath.exp(-1j*chi) * math.sin(phi),
                       cmath.exp(-1j*psi) * math.cos(phi)]])

def dt(r, s):
    return tracenorm(r-s).real

def absm(m):
    return la.sqrtm(m.H * m)
def mysqrtm(m):
    m = 0.5 * (m.H + m)
    ls, vs = la.eigh(m)
    vs = np.matrix(vs)
    try:
        ls = [math.sqrt(max(l.real, 0)) for l in ls]
    except ValueError:
        print m.H - m
        print la.eig(m)
        raise ValueError
    return vs * np.diag(ls) * vs.H

def compare(r, s):
    print 'comparing:'
    print r
    print s
    print 'trace distance', dt(r, s)
    print 'fidelity', fidelity(r, s)

def tracenorm(m):
    return sum([abs(l) for l in la.eigvalsh(.5*(m.H + m))])

def fidelity(r, s):
    root_r = mysqrtm(r)
    root_s = mysqrtm(s)
    ret = tracenorm(root_r * root_s)
    if ret > 1:
        print 'R =',
        octave_print(r)
        print 'S =',
        octave_print(s)
        print ret
        raise ValueError("Fidelity >1")
    return ret

def octave_print(m):
    rows, columns = m.shape
    ret = '['
    firstrow = True
    for r in xrange(rows):
        if firstrow:
            firstrow = False
        else:
            ret += ';\n'
        first = True
        for c in xrange(columns):
            if first:
                first = False
            else:
                ret += ','
            ret += repr(m[r, c])
    print ret+']'

def list_of_reals_to_complex(xs):
    zs = []
    for i in xrange(0, len(xs), 2):
        zs.append(xs[i] + xs[i+1]*1j)
    return zs

def xs_to_Es(xs, N):
    Es = []
    zs = list_of_reals_to_complex(xs)
    for i in xrange(N):
        E = np.matrix(zs[8*i:8*(i+1)]).reshape(2,4)
        Es.append(E)
    the_sum = sum([E * E.H for E in Es])
    the_sum = .5 * (the_sum + the_sum.H)
    supnorm = max([l.real for l in la.eigvalsh(the_sum)])
    Es = [E / math.sqrt(supnorm) * 0.999999999999999 for E in Es]
    return Es

def xs_to_imgs(xs, N, r, s):
    Es = xs_to_Es(xs, N)
    #Es = [E / math.sqrt(norm / 2.0)  for E in Es]
    img_r = sum([E.H * r * E for E in Es])
    img_s = sum([E.H * s * E for E in Es])
    return img_r, img_s

def what_rastegin(xs, r, s, N, rr, ss):
    img_r, img_s = xs_to_imgs(xs, N, r, s)
    if img_r is None or img_s is None:
        return 1001
    return 2 - fidelity(img_r, rr)**2 - fidelity(img_s, ss)**2
def what_df(xs, r, s, N, rr, ss):
    img_r, img_s = xs_to_imgs(xs, N, r, s)
    if img_r is None or img_s is None:
        return 1001
    return math.acos(fidelity(img_r, rr)) + math.acos(fidelity(img_s, ss))
def what_dt(xs, r, s, N, rr, ss):
    img_r, img_s = xs_to_imgs(xs, N, r, s)
    if img_r is None or img_s is None:
        return 1001
    return dt(img_r, rr) + dt(img_s, ss)

WHAT_MAP = {
        'rastegin': what_rastegin,
        'dt': what_dt,
        'df': what_df}


def less_than_the_idenity_constraint(xs, N):
    Es = xs_to_Es(xs, N)
    the_sum = sum([E * E.H for E in Es])
    return min([l.real for l in la.eigvalsh(np.diag([1,1]) - the_sum)])

# vim: sw=4 ts=4 sts=4
