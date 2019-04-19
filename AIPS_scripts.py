#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
────────────────────────────────────────────────────────────────────────────────
Author:            Krešimir Tisanić
Email:             kresimir.tisanic@gmail.com
Project:           SFG SED
Institution:       Department of Physics,
                   Faculty of Science,
                   University of Zagreb,
                   Bijenička cesta 32,
                   10000  Zagreb,
                   Croatia
Created on:        Fri May 26 2017 
Description:       AIPS scripts  
Requirements:      AIPS
────────────────────────────────────────────────────────────────────────────────
"""
def RMSD(basename, imsize, xinc, yinc=None, getn=1):
    '''
    Description:
    ------------
    Function that creates AIPS script for RMSD.
    
    Parameters:
    -----------
    basename: str
              input filename without .fits
    imsize:   int
              circle radius
    xinc:     int
              x increment
    yinc:     int
              y increment
    getn:     int
              image number
    '''
    if yinc is None:
        yinc = xinc
    if not isinstance(imsize, tuple):
        imsize = (imsize, -1)
    print( imsize, xinc, yinc)
    toRMS = [# Basic introductory text to write
             "TASK 'IMLOD'",
             "DEFAULT",
             "DATAIN='"+basename+".fits",
             "GO; WAIT",
             # Noise map generation
             "TASK 'RMSD'",
             "DEFAULT",
             "GETN %d"%getn,
             "IMSIZE=%d, %d"%imsize,
             "XINC=%d"%xinc,
             "YINC=%d"%yinc,
             "GO; WAIT",
             # Exporting noise map,
             "TASK 'FITTP'",
             "DEFAULT",
             "GETN %d"%(getn+1),
             "DATAOUT='"+basename+".rmsd.fits",
             "GO; WAIT",
             # Cleanup
             "FOR i=%d TO %d; GETN i; ZAP; END;"%(getn, getn+1),
             "CLRMSG",
             "CLRTEMP"
            ]
    print( toRMS)
    return toRMS