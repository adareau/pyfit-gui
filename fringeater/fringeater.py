# -*- coding: utf-8 -*-
#-------------------------------------#
# fringeater module
# author      : A. Dareau
# created     : 01/2015
# description : implements a fringe suppression algorithm for image processing
#               in order to be integrated to our pyfit gui
# reference   : PRA 82 061606
#-------------------------------------##

import os

import numpy as np
import pylab as pl

from scipy.linalg import inv



def LoadRefImages(file_list,background,min_intensity):   
    """

    loads images, extracts background area and builds the B matrix
    
    
    Parameters
    -------
    file_list : array_like
        list of picture pairs (path to pictures)
        (see ``Example`` section)
        
        
    background : logical array
        logic array (same size as pictures) with ones on the
        background area (used to compute best ref image) and zeroes
        otherwise
               
    min_intensity (opt) : int
        minimum mean intensity on the no_atom picture to consider the shot 
        valid (if mean(no_atoms[background])<min_intensity, we consider it was a bad shot with
        no light)
     
    Returns
    -------
    
    data : array_like
        data = [atoms,no_atoms]
        where (no_)atoms = list of pictures with(out) atoms
        
    
    Example
    -------
    How to format the ``file_list`` argument ::
    
        $ file_list = [(pic1_atoms,pic1_noatoms),
        $               (pic2_atoms,pic2_noatoms) ... etc]
    
    with ::
    
        $ pic1_atoms = "path/to/picture1_atoms.jpg" # path to picture1 (with atoms)
    
    Notes
    ------
    
    See reference PRA 82 061606
    """
    # 0 - declare lists
    
    atom_list = []
    noatom_list = []
    R=[]
    count = 1
    N = len(file_list)
    
    #1 - load images :
    
    for pic_pair in file_list:
        
        p_atoms = pic_pair[0]
        p_noatoms = pic_pair[1]
        
        if not (os.path.isfile(p_atoms) and os.path.isfile(p_noatoms)): continue
            
        print 'load image '+str(count)+' out of '+str(N)+'... ',
        
        data_atoms = pl.imread(p_atoms)
        if len(data_atoms.shape)>2: data_atoms = data_atoms[:,:,0]# some pictures are saved in RGB, then we only take one layer
        
        data_noatoms = pl.imread(p_noatoms)
        if len(data_noatoms.shape)>2: data_noatoms = data_noatoms[:,:,0]# some pictures are saved in RGB, then we only take one layer
        
        # Check whether the shot is valid
        if np.mean(data_noatoms[background])<min_intensity:
            print '[BAD SHOT => NOT USED]'
            continue
            
        atom_list.append(data_atoms)
        noatom_list.append(data_noatoms)
        
        R.append(data_noatoms[background])
        
        print '[DONE]'
        
        count+=1
        
    # Compute B matrix
    print 'compute B'
    
    R = np.array(R)
    B = R.dot(R.T)
    
    # invert B
    
    Binv = inv(B)
    
    
    # RETURN
    data_list = [atom_list,noatom_list]
    REF = {'B':B,
           'Binv':Binv,
           'R':R,
           'background':background}  
           
    return data_list,REF
        
    
def ComputeBestRef(pic,REF):
    """

    computes the cn coefficients for generating best reference picture 
    for the atom picture
    
    
    Parameters
    -------
    pic : array
        picture (with atoms)
        
        
    REF : dict
        dictionnary with reference picture set data
        (returned by LoadRefImages)
     
    Returns
    -------
    
    
    Notes
    ------
    
    See reference PRA 82 061606
    """
    
    A = pic[REF['background']]
    v = REF['R'].dot(A)
    Bi = REF['Binv']
    
    c = Bi.dot(v)
    
    return c
        
        
def GenRefPic(c,ref_pics):
    """

    generate the reference picture from all reference pics with cN coefficients
    
    
    Parameters
    -------
    c : array (size N)
        coefficient list for reference picture
        
        
    ref_pics : array (size NxHxL)
        list of reference pictures
     
    Returns
    -------
    
    ref : array (HxL)
        reference picture
    
    
    Notes
    ------
    
    See reference PRA 82 061606
    """    
    
    ref = np.zeros(ref_pics[0].shape)
    for pi,ci in zip(ref_pics,c):
        ref+=ci*pi

    
    return ref       
    
    