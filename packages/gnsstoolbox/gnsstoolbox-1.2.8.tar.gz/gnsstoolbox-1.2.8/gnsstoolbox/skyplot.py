#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (C) 2014-2023, Jacques Beilin <jacques.beilin@gmail.com>

This software is governed by the CeCILL-C license under French law and
abiding by the rules of distribution of free software.  You can  use, 
modify and/ or redistribute the software under the terms of the CeCILL-C
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info". 

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability. 

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or 
data to be ensured and,  more generally, to use and operate it in the 
same conditions as regards security. 

The fact that you are presently reading this means that you have had
knowledge of the CeCILL-C license and that you accept its terms.

"""

import re
import numpy as np
import os
import gpsdatetime as gpst
import gnsstoolbox.rinex_o as rx
import gnsstoolbox.orbits as orb
import gnsstoolbox.gnsstools as tools

class skyplot():
    """ Classe de creation d'un skyplot gnss """
    def __init__(self,rnx, sp3):
        """
        Input 
        rnx : full path to rinex obs file
        sp3 : full path (or list o full paths) to sp3 file(s)
        
        """
        self.rnx = rx.rinex_o(rnx)
        self.sp3 = orb.orbit()
        self.sp3.loadSp3(sp3)
        
        """ default value : Galileo, GPS, Glonass """ 
        self.const = 'GRE'
        
        """ default values for time window : full rinex
        self.start and self.end are gpsdatetime objects """
        self.start = self.rnx.headers[0].epochs[0].tgps
        self.end = self.rnx.headers[-1].epochs[-1].tgps
        
        self.title = self.rnx.headers[0].MARKER_NAME
        
        """ default value for cut-off = 0 [decimal degrees] """
        self.cutoff = 0

        """ gmt settings """        
        self.PointSizeAllMissing = "0.008c"
        self.PointSizeOneMissing = "0.03c"
        self.PointSizeAll = "0.03c"
        self.colorAllMissing = "255/0/0"
        self.ColorOneMissing = "255/120/0"
        self.ColorAll = "0/250/0"
        
        self.gmt_header   = ['PROJ_LENGTH_UNIT cm',
            'PS_CHAR_ENCODING  Standard+',
            'PS_PAGE_ORIENTATION portrait',
            'PS_MEDIA a3',
            'MAP_FRAME_WIDTH 0.2c',
            'MAP_TICK_LENGTH 0.2c',
            'FONT_TITLE 24p,Helvetica,black',
            'FONT_LABEL 18,Helvetica,black',
            'FORMAT_CLOCK_IN hh:mm:ss',
            'FORMAT_DATE_IN yyyy-mm-dd',
            'FORMAT_CLOCK_MAP hh:mm',
            'GMT_LANGUAGE  US',
            'FORMAT_TIME_PRIMARY_MAP  a',
            'FORMAT_TIME_SECONDARY_MAP a',
            'FONT_ANNOT_PRIMARY 16,Helvetica,black',
            'FONT_ANNOT_SECONDARY 16,Helvetica,black',
            'MAP_TITLE_OFFSET 1c',
            'MAP_ANNOT_OFFSET_PRIMARY 0.1c',
            'MAP_ANNOT_OFFSET_SECONDARY 0.1c']
        
        """ default value : Galileo, GPS, Glonass """ 
        self.const = 'GRE'
        
        """ default values for time window : full rinex
        self.start and self.end are gpsdatetime objects """
        try:
            self.start = self.rnx.headers[0].epochs[0].tgps
            self.end = self.rnx.headers[-1].epochs[-1].tgps
        except:
            return
        
        self.title = self.rnx.headers[0].MARKER_NAME
        
        """ default value for cut-off = 0 [decimal degrees] """
        self.cutoff = 0

    def CalcTheoricalPosSat(self):

        try:
            interval = self.rnx.headers[0].INTERVAL
        except:
            return
        if interval < 1:
            interval = 30
        
        d2r = np.pi/180.0
        t0 = self.start
        t1 = self.end
        t1 += 1
        
#        print("\nCalcTheoricalPosSat")
        
        self.LAllMissing = []        
        while t0 < t1:
            
#            print(t0.st_pyephem_epoch())
            
            if re.search('G',self.const):
                for i in range(len(self.sp3.sp3G)):
                    prn = i+1
#                    print("PRN ",'G',prn)
                    try:
                        Xs,Ys,Zs,dte = self.sp3.calcSatCoord('G',prn,t0.mjd,3)  
                        if (Xs**2+Ys**2+Zs**2)**0.5 < 20e6:
                            continue
                        Az,Ele,h = tools.toolAzEleH(self.X0, self.Y0, self.Z0, Xs, Ys, Zs)
                        try:
                            if Ele<self.cutoff*d2r:
                                continue
                        except:
                            continue
                        self.LAllMissing.append("%.2f %.2f %d" % (Az/d2r, Ele/d2r, prn))
                    except:
                        pass
                
            if re.search('R',self.const):
                for i in range(len(self.sp3.sp3R)):
                    prn = i+1
#                    print("PRN ",'R',prn)
                    try:
                        Xs,Ys,Zs,dte = self.sp3.calcSatCoord('R',prn,t0.mjd,3)              
                        if (Xs**2+Ys**2+Zs**2)**0.5 < 20e6:
                            continue
                        Az,Ele,h = tools.toolAzEleH(self.X0, self.Y0, self.Z0, Xs, Ys, Zs)
                        try:
                            if Ele<self.cutoff*d2r:
                                continue
                        except:
                            continue              
                        self.LAllMissing.append("%.2f %.2f %d" % (Az/d2r, Ele/d2r, prn))
                    except:
                        pass
                    
            if re.search('E',self.const):
                for i in range(len(self.sp3.sp3E)):
                    prn = i+1
#                    print("PRN ",'E',prn)
                    try:
                        Xs,Ys,Zs,dte = self.sp3.calcSatCoord('E',prn,t0.mjd,3)   
                        if (Xs**2+Ys**2+Zs**2)**0.5 < 20e6:
                            continue
                        Az,Ele,h = tools.toolAzEleH(self.X0, self.Y0, self.Z0, Xs, Ys, Zs)
                        try:
                            if Ele<self.cutoff*d2r:
                                continue
                        except:
                            continue              
                        self.LAllMissing.append("%.2f %.2f %d" % (Az/d2r, Ele/d2r, prn))
                    except:
                        pass
                    
            t0 += interval
        return 0        
        
        
    def CalcRinexPosSat(self):
        
        self.LAll = []
        self.LOneMissing = []
        d2r = np.pi/180.0
        
#        print("\n\nCalcRinexPosSat")
        
        for H in self.rnx.headers:       
            self.X0 = H.X
            self.Y0 = H.Y
            self.Z0 = H.Z
            
#            print("Approx Coord : ",self.X0,self.Y0,self.Z0)
            for E in H.epochs:
                if E.tgps<self.start:
                    continue
                if E.tgps>self.end:
                    break
                
#                print(E.tgps.st_pyephem_epoch())
                
                for sat in E.satellites:
                    
                    if re.search(sat.const,self.const):
#                        print(sat.const,sat.PRN,E.tgps.mjd)
                        Xs,Ys,Zs,dte = self.sp3.calcSatCoord(sat.const,sat.PRN,E.tgps.mjd,3)
                        if (Xs**2+Ys**2+Zs**2)**0.5 < 20e6:
                            continue
                        sat.Az,sat.Ele,h = tools.toolAzEleH(self.X0, self.Y0, self.Z0, Xs, Ys, Zs)
    
                        try:
                            if sat.Ele<self.cutoff*d2r:
                                continue
                        except:
                            continue
                        
                        s = "%.2f %.2f %d" % (sat.Az/d2r, sat.Ele/d2r, sat.PRN)
                    
                        """ recherche des obs completes/incompletes """
                        if H.typeFreq==1:
                            if ('C1' in sat.obs) and ('L1' in sat.obs):
                                self.LAll.append(s) 
                            else:
                                if (len(sat.obs)>0): 
                                    self.LOneMissing.append(s)
                        else:      
                            if ('C1' in sat.obs) and ('P2' in sat.obs) and ('L1' in sat.obs) and ('L2' in sat.obs):
                                self.LAll.append(s) 
                            else:
                                if (len(sat.obs)>0): 
                                    self.LOneMissing.append(s)                            

    def WriteGmtScript(self,gmtfilebasename=""):
        
        if (gmtfilebasename==""):
            return -1
        
        try:
            title = self.title
        except:
            return

        gm0 = gmtfilebasename+".gm0"
        gm1 = gmtfilebasename+".gm1"
        gm2 = gmtfilebasename+".gm2"
        ps = gmtfilebasename+".ps"
        self.ps = ps
        try:
            with open(gm0,"wt") as F:
                for s in self.LAllMissing:
                    F.write(s+"\n")
        except:
            print ('Unable to create %s' % (gm0))
            
        try:
            with open(gm1,"wt") as F:
                for s in self.LOneMissing:
                    F.write(s+"\n")
        except:
            print ('Unable to create %s' % (gm1))       

        try:
            with open(gm2,"wt") as F:
                for s in self.LAll:
                    F.write(s+"\n")
        except:
            print ('Unable to create %s' % (gm2))
        
        Lcmd = []
        for s in self.gmt_header:
            Lcmd.append('gmt gmtset '+s)     
        
        cmd = 'gmt psxy -R0/360/0/90 -JPa25c/0r -Sc%s -Bg90f30a90:."%s":/f10a30g10 -G%s -W1,%s -K %s > %s' % (self.PointSizeAllMissing,title,self.colorAllMissing,self.colorAllMissing,gm0,ps)
        Lcmd.append(cmd)
        cmd = 'gmt psxy -R -JP -Sc%s -G%s  -W1,%s -O -K %s >> %s' % (self.PointSizeAll,self.ColorAll,self.ColorAll,gm2,ps)
        Lcmd.append(cmd)
        cmd = 'gmt psxy -R -JP -Sc%s -G%s  -W1,%s -O -K %s >> %s' % (self.PointSizeOneMissing,self.ColorOneMissing,self.ColorOneMissing,gm1,ps)
        Lcmd.append(cmd)
        cmd = 'gmt psxy "." -R -JP -Sc0.01c -G255/255/255  -W1,255/255/255 -O >> %s' % (ps)
        Lcmd.append(cmd)
        
        for cmd in Lcmd:
            os.system(cmd)
        
        return 0
        
if __name__ == "__main__":

    tic = gpst.gpsdatetime()
    print("Hello world !")
   
    datadir = '/home/GPSTOOLS/skyplots/'
    Rinexfilename = datadir+'BASS086Y.18o'
    sk = skyplot(Rinexfilename,[datadir+'esa19942.sp3'])
    sk.const='RG'
    sk.cutoff = 3
    sk.CalcRinexPosSat()
    sk.CalcTheoricalPosSat()   
    sk.WriteGmtScript('/home/GPSTOOLS/skyplots/test')
    
    
    toc = gpst.gpsdatetime()
    print ('%.3f sec elapsed ' % (toc-tic))
