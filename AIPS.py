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
Created on:        Thu May 25 2017
Description:       Simple AIPS wrapper. 
                   -------------------------------------------------------------
                   Example:
                   -------------------------------------------------------------
                   from AIPS import aips
                   a = aips()
                   a.write(["TASK 'IMLOD'",
                            "DEFAULT",
                            "DATAIN='k:GMRT610/test.mosaic.1.fits",
                            "GO; WAIT"])
                   a.run()
                   print(a.output)
                   
Requirements:      AIPS
────────────────────────────────────────────────────────────────────────────────
"""
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Packages
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import subprocess as sp


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class aips:
    '''
        Creates AIPS object instance.

        Description
        -----------
        Initializes AIPS using a user ID and aips location. Writes a log to
        aips_log.
        
        Parameters
        -----------
        user_ID:  int
                  AIPS user ID.
        aips_log: string
                  name of the log file.
        aips_loc: string
                  Bash command to run aips from this location. 
                  Change this if you're not running this on Mephisto.
        end:      string or list
                  commands to execute at the end of file. 
                  Defaults to "CLRMSG", "KLEENEX", and "EOF".
    '''
    def __init__(self,
                 user_ID  = 1120,
                 aips_log = "aips.log",
                 aips_loc = "source /home/vernesa/software/aips/LOGIN.SH",
                 end      = ["CLRMSG", "KLEENEX", "EOF"]):
        '''
        Creates AIPS object instance.

        Description
        -----------
        Initializes AIPS using a user ID and aips location. Writes a log to
        aips_log.
        
        Parameters
        -----------
        user_ID:  int
                  AIPS user ID.
        aips_log: string
                  name of the log file.
        aips_loc: string
                  Bash command to run aips from this location. 
                  Change this if you're not running this on Mephisto.
        end:      string or list
                  commands to execute at the end of file. 
                  Defaults to "CLRMSG", "KLEENEX", and "EOF".
        '''
        self.user_ID   = user_ID
        self.aips_log  = aips_log
        self.aips_loc  = aips_loc
        self.base      = "aips notv << EOF | tee %s;\n\n%d"%(
                          self.aips_log, self.user_ID)
        self.invoked   = []
        self.end       = end
        
    
    def write(self, x):
        '''
        Creates AIPS script
        Description
        -----------
        Write a program as a list of commands (or a command) and put it in x.

        Parameters
        -----------
        x: string or list
           commands to execute
        '''
        if isinstance( x, str):
            x = [x]
        if len(self.invoked) == 0:
            self.invoked.extend([self.aips_loc, self.base])
        self.invoked.extend(x)

    def run(self):
        '''
        Runs your script.

        Description
        -----------
        Writes your script to bash and saves output to .comms and .output 
        class instance attributes. 

        Output
        -----------
        comms:  list
                full communicate output message (unformatted)
        output: list
                formatted output as writte in the terminal
            
        '''
        self._finish()
        out         = str.encode("\n".join(self.invoked))
        S           = sp.Popen(['/bin/bash'],
                               stdin  = sp.PIPE,
                               stdout = sp.PIPE)
        self.comms  = S.communicate(out)
        self.output = self.comms[0].decode('UTF-8')

        
    def _finish(self):
        '''
        Writes finishing lines. 
        '''
        if isinstance(self.end, str):
            self.end = [self.end]
        self.invoked.extend(self.end)

    def clear(self, n):
        """
        clears busy status of a file
        
        Parameters
        ----------
        n:    int
              file index
        """
        A  = aips()
        A.write(['GETN %d'%n, 'CLRSTAT', 'ZAP'])
        A.run()
        print(A.output)
        
    def pca(self):
        """
        Lists open files
        """
        A  = aips()
        A.write('pca')
        A.run()
        print(A.output)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# End
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
