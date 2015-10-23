# -*- coding: utf-8 -*-
'''----------------------------------------------------------
  file        : lattice_depth.py
  author      : A.  Dareau
  created     : 2015-23-10
  modified    : ...
  description : functions to compute lattice depth from Kapitza-Dirac/Raman-Nath 
                diffration experiment
                (recycled from "Watch'n'MOT" MATLAB version)
----------------------------------------------------------'''

from __future__ import division
import numpy as np
import scipy.constants as c
import matplotlib.pyplot as plt

from functools import partial
from scipy.optimize import minimize

#--- Fit function

def get_lattice_depth(Nat,T,n=15,Npoints=1e3,guess=1,n_cut=None,lbda=760e-9,m=174*1.66e-27,plot=True):
    """
    Description : Gets lattice depth from diffraction pattern, using
                  Hamiltonian diagonalization (restricted to n diffraction orders).

    Inputs : Nat = matrix with atom number in different orders 
                    ( size(Nat) = n_orders x n_times)
             T = matrix with pulse length (in units of hbar/Er)
             n = number of orders to consider (for simulation)
             Npoints = number of points to plot
             guess = lattice depth guess for the fit
             n_cut = specify the number of orders to fit/plot
             lbda = lattice wavelength in m (opt, only for fitting)
             plot = if True, we display fit result
             
    Outputs : alpha = U0/Er (Er : recoil energy, U0 : lattice depth)
              
    """
    
    # 1 - Constants and input parsing   
    
    hbar = c.hbar
    k = 2*np.pi/lbda
    Er = hbar**2*k**2/2/m
    
    n_orders = len(Nat)
    
    if n_cut is None:
        n_cut = n_orders
    else:
        if n_cut > n_orders: n_cut=n_orders
        if n_cut == 0: n_cut = n_orders
    
    if n_orders>n:n = n_orders+5
    
    # 2 - Normalize atom number
    
    Nat_tot = np.zeros(np.shape(Nat[0]))
    for N in Nat:
        Nat_tot += np.array(N)
    
    Nat_norm = [np.array(N)/Nat_tot for N in Nat]
    
    # 3 - Fit
    alpha = guess
    err_fun = partial(error_for_fit,Nat=Nat_norm,T=T,n=n)
    res  = minimize(err_fun, guess)
    alpha = res.x[0]
    
    # 4 - Plot
    
    Psi, Nfit, T_fit = lattice_pulse_1D(alpha,n,T.max(),Npoints=500,lbda=lbda,m=m,plot=False)
    
    if plot:
        plt.figure()
        for N in Nfit:
            plt.plot(T_fit*hbar/Er*1e6, N,'--k')
            
            
        for N in Nat_norm:
            plt.plot(T*hbar/Er*1e6, N, marker='o', linestyle='')
        
        plt.show()
    
    
    return alpha, Nat_norm, Nfit, T_fit

#--- Side functions

def gen_lattice_hamiltonian(Er,alpha,n):
    """
    generates the Hamiltonian for a 1D pulsed lattice, restricted to
    the 2phk diffractions order (p between -n and n).
    
    Parameters
    -------
    Er : double
        recoil energy
        
    alpha : double
        U0/Er (Er : recoil energy, U0 : lattice depth)
        
    n : int
        number of orders to consider
   
    Returns
    -------
    H : array (n times n)
        hamiltonian (in units of J)

    """
    
    # super and sub diagonal
    sd = np.zeros(2*n)+alpha/4.0
    
    # diagonal
    d = 4*np.arange(-n,n+1)**2.0
    
    # combine
    H = np.diag(d,0)+np.diag(sd,-1)+np.diag(sd,+1)
    H *= Er
    
    return H

def evolution_operator(H,norm=True):
    """
    Gives the evolution operator from an Hamiltonian.
    
    Parameters
    -------
    H : array (matrix)
        hamiltonian (in units of J)
        
    norm : bool (opt)
        if True, then we set hbar to 1

   
    Returns
    -------
    U(t) : function (returns array)
        evolution operator
        
    D : array (matrix)
        eigenvalues matrix
        
    Q : array (matrix)
        transfer matrix
    """
    
    ## hbar normalization
    if norm: 
        hbar=1.
    else:
        hbar = c.hbar
        
    ## diagonalize H
    D,Q = np.linalg.eig(H)
    D = np.diag(D)*(1+0j)
    #Q *= (1+0j)
    
    ## define U(t)
    Dt = lambda t: np.diag(np.exp(-1j*np.diag(D)*t/hbar))
    U = lambda t: np.dot(np.dot(Q,Dt(t)),np.transpose(Q))
    
    return U,D,Q

def lattice_pulse_1D(alpha,n,T,Npoints=1e3,lbda=760e-9,m=174*1.66e-27,plot=True):
    """
    Computes system evolution for a diffraction experiment
    (function used for test purposes)
    
    Inputs : alpha = U0/Er (Er : recoil energy, U0 : lattice depth)
             n = number of orders to consider
             T = max pulse lenght (in units of hbar/U0)
             Npoints = number of points to plot
             lambda = lattice wavelength in m (opt)
    
    """  
    
    # 1 - Constants and input parsing   
    
    hbar = c.hbar
    k = 2*np.pi/lbda
    Er = hbar**2*k**2/2/m
    
    # 2 - Hamiltonian and diagonalization
    
    H = gen_lattice_hamiltonian(1,alpha,n) # we define H with Er = 1;
    U,D,Q = evolution_operator(H) # we compute the evolution operator (with hbar = 1);
    
    ''''NB : now time is in unit of hbar/Er '''
    
    # 3 - Evolution
    
    init = np.zeros(2*n+1,complex)
    init[n] = 1+0j # initial state is |0> (center of H)

    time_window = np.linspace(0,T,Npoints)
    Psi = np.zeros((len(time_window),2*n+1),complex)
    it = 0

    for t in time_window:
        psi_t = np.dot(U(t),init)
        Psi[it,:] = psi_t
        it += 1

    
    # 4 - Plot
    Nat = []
    
    t = time_window*hbar/Er
    if plot:
        plt.figure('lattice pulse 1D')
        plt.clf()
    
    # zeroth order
    N = np.abs(Psi[:,n])**2
    Nat.append(np.array(N))
    
    if plot: plt.plot(t*1e6,N)
    for p in range(1,n+1):
        N = np.abs(Psi[:,n+p])**2+np.abs(Psi[:,n-p])**2
        if N.max()>1e-3:
            if plot: plt.plot(t*1e6,N)
            Nat.append(np.array(N))
            
        
    
    return Psi,Nat,time_window
    
## Test

def error_for_fit(alpha,Nat,T,n):
    
    ## Inputs parsing
    n_order = len(Nat)
    
    ## Diago
    H = gen_lattice_hamiltonian(1,alpha,n) # we define H with Er = 1;
    U,D,Q = evolution_operator(H) # we compute the evolution operator (with hbar = 1);
    
    ## Evolution
    init = np.zeros(2*n+1,complex)
    init[n] = 1+0j # initial state is |0> (center of H)

    Psi = np.zeros((len(T),2*n+1),complex)
    it = 0

    for t in T:
        Psi[it,:] = np.dot(U(t),init)
        it += 1

    
    ## Error
    error = 0
    
    # zeroth order
    N = np.abs(Psi[:,n])**2
    error += np.abs(Nat[0]-N)**2
    
    
    # other orders
    for p in range(1,n_order):
        N = np.abs(Psi[:,n+p])**2+np.abs(Psi[:,n-p])**2
        error += np.abs(Nat[p]-N)**2
        
    error = np.sum(error)

    return error
    

'''
alpha = 14
n = 3
T = 10
Npoints = 1e3

m = 174*c.m_p
lbda = 760e-9
hbar = c.hbar
k = 2*np.pi/lbda
Er = hbar**2*k**2/2/m

#H = gen_lattice_hamiltonian(1, alpha, n)
#U,D,Q = evolution_operator(H)
Psi,Nat,T_list = lattice_pulse_1D(alpha,n,T,Npoints)
'''
