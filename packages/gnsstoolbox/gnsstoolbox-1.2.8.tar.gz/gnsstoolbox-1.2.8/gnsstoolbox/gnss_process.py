# -*- coding: utf-8 -*-
"""
Copyright (C) 2014-2023, Jacques Beilin <jacques.beilin@gmail.com>

This software is a computer program whose purpose is to [describe
functionalities and technical features of your software].

This software is governed by the CeCILL-C license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL-C
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author, the holder of the
economic rights, and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading, using, modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate, and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and, more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL-C license and that you accept its terms.

"""


import re
import math
import numpy as np
import copy

import gpsdatetime as gps
import gnsstoolbox.rinex_o as rx
import gnsstoolbox.orbits as orb
import gnsstoolbox.gnss_const as const
import gnsstoolbox.gnsstools as tool
import gnsstoolbox.gnss_corr as corr

class gnss_process():
    """GNSS proccess class"""


    def __init__(self):

        """Options par defaut"""
        self.process="spp" #"DGNSS","phase"
        self.freq="C1"
        self.cut_off=3*const.d2r
        self.X0 = np.zeros((3,1))
        self.iono = 'none'
        self.nav = 'sp3'
        self.const= 'GRE'
        self.type="o"
        self.constraint=0 # contraintes sur la position, utilisé pour solution DGNSS

        self.nb_sat = 0
        self.nb_GPS = 0
        self.nb_GLO = 0
        self.nb_GAL = 0

        self.nb_GPS_calc = 0
        self.nb_GLO_calc = 0
        self.nb_GAL_calc = 0

    def __str__(self):
        """ overloads print function """

        st =''
        for s in self.__dict__:
            if (not re.search('tgps',s)):
                st += '%-35s : %s\n' % (s, self.__dict__.get(s))
            elif (re.search('tgps',s)):
                st += '%-35s : %s\n' % (s+ ' (gpsdatetime object)', self.__dict__.get(s).st_iso_epoch())
            else:
                st += '%-35s : %s\n' % (s, "")
#        print(st)
        return st

    def spp(self,epoch,nav):
        """Process epoch using spp

        Jacques Beilin - 2017-12-24

        Input :
        - epoch : GNSS epoch  obtained by epoch = myrinex.get_epoch_by_mjd(t.mjd)
        - nav : orbits object loaded with orb.loadSp3() or orb.loadRinexN()
        Output :
        - epoch2 : GNSS epoch including proccessed elements

        """

        self.nb_sat=len(epoch.satellites)

        #print(epoch.satellites[0].__dict__.keys())

        R = np.linalg.norm(self.X0)

        toberemoved = []

        if self.constraint>0:
            self.sta_pos = copy.copy(self.X0)

        for i in range(len(epoch.satellites)):
            S = epoch.satellites[i]

            S.comment = ""

            if (not re.search(S.const,self.const)):
#                print "A virer : ", S.const,S.PRN
                toberemoved.append(i)
                S.comment = "Constellation %s removed by user" % (S.const)
                continue

            if re.search('G',S.const) : self.nb_GPS+=1
            if re.search('R',S.const) : self.nb_GLO+=1
            if re.search('E',S.const) : self.nb_GAL+=1

            if re.search('C1',self.freq):
                S.PR = S.getObs('C1')
            elif re.search('iono_free',self.freq):
                S.PR = const.k_L3 * (const.f1_2 * S.getObs('C1') - const.f2_2 *  S.getObs('P2')) # P3
                
            if math.isnan(S.PR):
                toberemoved.append(i)
                S.comment = "no valid observable"
                continue

            """ Calcul de la date de réception (mjd) """
            S.tr = epoch.tgps.mjd

            """ Calcul de la date d'émission (mjd) """
            S.TravelTime = S.PR / const.c
            S.te = S.tr - S.TravelTime / 86400.0

            """ Calcul de la correction relativiste (s) et derive l'horloge satellite """
            if nav.type == 'nav':
                S.dte = nav.calcDte(S.const,S.PRN,S.tr)
            else:
                delta_t = 1e-3 # écart de temps en +/- pour calculer la dérivée
                (Xs0,Ys0,Zs0,clocks0) = nav.calcSatCoordSp3(S.const, S.PRN, S.te, 9)
                if (Xs0**2 +Ys0**2 +Zs0**2)**0.5 < 1.0:
                    toberemoved.append(i)
                    S.comment="No orbit available"
                    continue
                (Xs1,Ys1,Zs1,clocks1) = nav.calcSatCoordSp3(S.const,S.PRN,S.te - delta_t / 86400.0,9)
                (Xs2,Ys2,Zs2,clocks2) = nav.calcSatCoordSp3(S.const,S.PRN,S.te + delta_t / 86400.0,9)
                VX = (np.array([Xs2-Xs1, Ys2-Ys1, Zs2-Zs1]))/2.0/delta_t
                VX0 = np.array([Xs0,Ys0,Zs0])

                Drelat = -2.0 * np.dot(VX0.T,VX) /const.c/const.c
                S.dte = clocks0 + Drelat

            #  Corrected emission time and corrected PR
            S.te_corr = S.te - S.dte / 86400.0

            S.PR = S.PR + const.c * S.dte

            """
            Computing satellite position
            """
            if nav.type == 'nav':

                if S.const == 'R':
                    ret = nav.calcSatCoordNav(S.const,S.PRN,S.te_corr)
                    S.Xs = ret[0];S.Ys = ret[1];S.Zs = ret[2];clocks = ret[3]

                elif re.search(S.const,'GE'):
                    (S.Xs,S.Ys,S.Zs,clocks) = nav.calcSatCoordNav(S.const,S.PRN,S.te_corr)

            else:
                (S.Xs,S.Ys,S.Zs,clocks) = nav.calcSatCoordSp3(S.const,S.PRN,S.te_corr,9)
               
            if math.isnan(S.Xs):
                toberemoved.append(i)
                S.comment="No valid position"
                continue            

            # Az and Ele computation : for cut_off and tropospheric delay computation
            # Computation if initial coordinates are on the earth
            if (R>const.Rmin and R<const.Rmax): # on earth ?
                [S.Az,S.Ele,h]=tool.toolAzEleH(self.X0[0],self.X0[1],self.X0[2],S.Xs,S.Ys,S.Zs)

                # cut off
                if(S.Ele < self.cut_off):
                    toberemoved.append(i)
                    S.comment="Elevation %.2f deg < %.2f deg" % (S.Ele/const.d2r,self.cut_off/const.d2r)
                    continue

                # tropospheric delay - Saastamoinen model
#                print(const.P,const.T,const.H,h,math.pi/2 - S.Ele)
                S.dtropo = corr.corr_dtropo_saast(const.P,const.T,const.H,h,math.pi/2 - S.Ele)

            else:
                S.Az = 0.0
                S.Ele = 0.0
                S.dtropo = 0.0
                
            S.PR -= S.dtropo

            # Ionospheric correction computation
            if re.search('iono_free',self.freq):
                S.diono = 0 # no additional correction

            elif (re.search('F1',self.freq) or re.search('F2',self.freq)):
                if (self.iono=='klobuchar' and self.nav=='brdc'):
                    S.diono = 0
#                    alpha_ion = NAV_header.GPSA;
#                    beta_ion = NAV_header.GPSB;
#                    S.diono = corr_iono_klobuchar(X0(1),X0(2),X0(3),G{numsat,11}.Xs,G{numsat,11}.Ys,G{numsat,11}.Zs,alpha_ion,beta_ion,G{numsat,11}.te_corr,G{numsat,10},freq);
                else:
                    S.diono = 0

            else:
                S.diono = 0

            S.PR -= S.diono

            if hasattr(S,'dr'):
                if abs(S.dr)<0.0000001:
                    toberemoved.append(i)
                    S.comment="No DGPS correction"
                else:
                    S.PR += S.dr

            # time rotation during wave propagation
            alpha = -2.0 * math.pi * S.PR / 86400.0 / const.c
            [S.Xs,S.Ys,S.Zs] = tool.toolRotZ(S.Xs,S.Ys,S.Zs,alpha)

        epoch.X0 = self.X0

        epoch2 = copy.deepcopy(epoch)

        if len(toberemoved)>0:
            for i in range(len(toberemoved)-1,-1,-1):
                print("Sat %s%02d removed from current process : %s" % (epoch2.satellites[toberemoved[i]].const, epoch2.satellites[toberemoved[i]].PRN,epoch2.satellites[toberemoved[i]].comment))
                del(epoch2.satellites[toberemoved[i]])

        self.nb_GPS=0;self.nb_GLO=0;self.nb_GAL=0
        for i in range(len(epoch2.satellites)):
            if (re.search('G',epoch2.satellites[i].const)):self.nb_GPS+=1
            if (re.search('R',epoch2.satellites[i].const)):self.nb_GLO+=1
            if (re.search('E',epoch2.satellites[i].const)):self.nb_GAL+=1

        self.nb_sat = self.nb_GPS + self.nb_GLO + self.nb_GAL

        print(epoch2.__dict__.keys())
        self.calc_LS_code(epoch2)

        return epoch2


    def calc_LS_code(self,epoch):
        """function [result] = calc_LS_code(epoch)
        Least Square computation for code
        GPS | GLONASS | GALILEO | GPS + GLONASS + GALILEO | GPS + GLONASS | GPS + GALILEO
        Estimation of 1 cdtr per epoch, cGGTO and cGPGL for all data in input -> if one epoch
        Estimation of one pos per epoch or one pos for the whole obs -> if several epochs

        GGTO = GPS to Galileo Time Offset
        GPGL = GPS to GLonass time offset
        P depends on elevation of satellites"""

        nb_GAL_GGTO = 2 # number of min Galileo satellites to compute GGTO
        # -> if less satellites than nb_GAL_GGTO, no Galileo satellites used in computation
        nb_GLO_GPGL = 2 # number of min Glonass satellites to compute GPGL
        # -> if less satellites than nb_GLO_GPGL, no Glonass satellites used in computation

        # No computation if just Gal + Glo
        if (self.nb_GPS == 0 and self.nb_GLO > 0 and self.nb_GAL > 0):
            print('No computation with only GAL and GLO satellites')
            return

        # only one constellation -> no estimation of any time offset
        pos_cGGTO=0
        pos_cGPGL=0
        if (self.nb_GPS == self.nb_sat or self.nb_GLO == self.nb_sat or self.nb_GAL == self.nb_sat):
            estim_GPGL = 0
            estim_GGTO = 0

            # number of satellites to compute a position
            nb_sat_min = 4 # min 4 satellites to compute (position + dtr)

        # several constellations -> time offsets estimation
        else:

            # number of satellites to compute a position
            nb_sat_min = 6 # 3 for position + 1 for dtr + 1 for GGTO + 1 for GPGL = 6

            # cGGTO
            if (self.nb_GAL<nb_GAL_GGTO): # too few Galileo satellites to estimate the offset between gpsdatetime and GalileoTime
                estim_GGTO = 0
                self.nb_GAL = 0
                nb_sat_min = nb_sat_min - 1

                # TODO : suppress Galileo satellites
            else:
                estim_GGTO = 1;
                pos_cGGTO=4

            # cGPGL
            if (self.nb_GLO<nb_GLO_GPGL): # too few Glonass satellites to estimate the offset between gpsdatetime and GlonassTime

                estim_GPGL = 0;
                self.nb_GLO = 0;
                nb_sat_min = nb_sat_min - 1;
                # TODO : suppress GLONASS satellites
            else:
                estim_GPGL = 1;
                if estim_GGTO>0:
                    pos_cGPGL=pos_cGGTO+1
                else :
                    pos_cGPGL=4

        # updating X0 vector

        X0 = epoch.X0
        X0 = 1.0e3 * np.floor(X0/1000) # arrondi au km
        X0 = np.concatenate((X0,np.zeros((1+estim_GGTO+estim_GPGL,1))),axis=0)
        X0 = np.squeeze(X0)
        print("X0 =",X0)

        self.nb_sat = self.nb_GPS + self.nb_GLO + self.nb_GAL

        n = self.nb_sat # equation number
        p = len(X0) # unknown number

        # Sat position extraction (conversion to matrices)
        Xs = np.zeros((n))
        Ys = np.zeros((n))
        Zs = np.zeros((n))
        Dobs = np.zeros((n))
#        print "X0 ",X0
        for i in range(len(epoch.satellites)):
            S = epoch.satellites[i]
#            print( "Sat %2d %s %02d %14.3f %14.3f %14.3f" % (i,S.const,S.PRN,S.Xs, S.Ys, S.Zs))
            Xs[i] = S.Xs    
            Ys[i] = S.Ys
            Zs[i] = S.Zs
            Dobs[i] = S.PR

        # Weight matrix
        sigma = 2.0 # default value 2m

        if self.constraint > 0:
            SigmaB = sigma**2 * np.eye(n+3)
            SigmaB[n,n]=self.constraint**2
            SigmaB[n+1,n+1]=self.constraint**2
            SigmaB[n+2,n+2]=self.constraint**2
        else:
            SigmaB = sigma**2 * np.eye(n)

        R = ((X0[0])**2 + (X0[1])**2 + (X0[2])**2)**0.5
        if (R > const.Rmin and R < const.Rmax): # if X0 on earth, sigma calculated as a function of elevation 
            print("Processing observation sigma from elevation")
            [az,ele,h]=tool.toolAzEleH(X0[0],X0[1],X0[2],Xs,Ys,Zs)
            for i in range(len(epoch.satellites)):
                SigmaB[i,i] *= math.cos(math.pi - ele[i])**2

        if self.nb_GLO > 0:
            print("Glonass sigma = GPS/GAL sigma * sqrt(2)")
        for i in range(len(epoch.satellites)):
            if re.search('R',epoch.satellites[i].const):
                SigmaB[i,i] *= 2.0 # for glonass P = P/2 (we consider Var(glo) = Var(gps) / sqrt(2)

        P = np.linalg.inv(SigmaB)

        # convergence criterium
        n_iter = 0
        sigma02priori = 1E25
        epsilon = 1E-6
        sigma02 = 0.0

        # matrices creation
        D = np.zeros((n))

        if self.constraint>0:
            A = np.zeros((n+3,p))
            B = np.zeros(n+3)
        else:
            A = np.zeros((n,p))
            B = np.zeros(n)

        while (n_iter < 15):
#            print "Iteration ", n_iter
            # Calculated distance
            A.fill(0)
            B.fill(0)

            D = ((X0[0]-Xs)**2 +(X0[1]-Ys)**2 +(X0[2]-Zs)**2)**0.5

            A[0:n,0] = (X0[0] - Xs)/D
            A[0:n,1] = (X0[1] - Ys)/D
            A[0:n,2] = (X0[2] - Zs)/D
            A[0:n,3] = np.ones((n))
            B[0:n] = Dobs - D - X0[3]

            if self.constraint>0:
                A[n,0]=1.0
                A[n+1,1]=1.0
                A[n+2,2]=1.0
                B[n]=self.sta_pos[0]-X0[0]
                B[n+1]=self.sta_pos[1]-X0[1]
                B[n+2]=self.sta_pos[2]-X0[2]

            # cGGTO
            if estim_GGTO==1:
                for i in range(len(epoch.satellites)):
                    if re.search('E',epoch.satellites[i].const):
                        A[i,pos_cGGTO] = 1.0
                        B[i] -= X0[pos_cGGTO]

            # cGPGL
            if estim_GPGL==1:
                for i in range(len(epoch.satellites)):
                    if re.search('R',epoch.satellites[i].const):
                        A[i,pos_cGPGL] = 1.0
                        B[i] -= X0[pos_cGPGL]
                        
#            print(A)
#            print(B)

            # system resolution
            N = np.dot(np.dot(A.T,P),A)
            C = np.dot(np.dot(A.T,P),B)

            dX = np.dot(np.linalg.inv(N),C)

            X0 += dX

            # residual computation
            V = B - np.dot(A,dX)

            if n-p != 0: # cas GAL==4 debug
                sigma02 = np.dot(np.dot(V.T,P),V)/ (n-p)
            else:
                sigma02 = 1000


            # Convergence criteria (sigma0 variation < epsilon)
            n_iter +=1
            if (abs((sigma02-sigma02priori))<epsilon):
                break
            sigma02priori = sigma02;


            epoch.X = X0[0];epoch.Y = X0[1];epoch.Z = X0[2];epoch.cdtr=X0[3]
            if estim_GPGL==1:
                epoch.X = X0[4]

        epoch.V = V

        for i in range(len(epoch.satellites)):
            S = epoch.satellites[i]
            S.V = V[i]
            S.dr = D[i] + epoch.cdtr -S.PR
#            print S.V, S.dr

        epoch.n_iter = n_iter
        print("#iterations : ", n_iter)
        epoch.sigma02=sigma02
        print("sigma02 : %.2f" % (sigma02))

        epoch.X = X0[0];epoch.Y = X0[1];epoch.Z = X0[2];epoch.cdtr = X0[3]
        print( "X=%.3f Y=%.3f Z=%.3f cdtr=%.3f" % (X0[0], X0[1], X0[2],X0[3]))
        if pos_cGGTO>0:
            epoch.cGGTO = X0[pos_cGGTO]
            print( "cGGTO=%.3f" % (X0[pos_cGGTO]))
        if pos_cGPGL>0:
            epoch.cGPGL = X0[pos_cGPGL]
            print( "cGPGL=%.3f" % (X0[pos_cGPGL]))

        epoch.SigmaX =  epoch.sigma02 * np.linalg.inv(N)

    def calc_stat_indic(self,epoch):
        """
        local VCV matrix
     Confidence ellipsoid computation (1-sigma) from Qxx matrix estimated in calc_LS (NOT YET IMPLEMENTED)
     Correlation matrix computation (NOT YET IMPLEMENTED)
     DOP computation
     If several dtr estimated, TDOP correspond to first epoch

     Beilin Jacques - DPTS - 2017-09-21

     Input :
     - Qxx : variance matrix (4*4)
     - X,Y,Z : estimated coordinates

     Output :
     - stat : structure containing statistic indicators :
     		- ell : structure containing error ellipsoid in the local frame
    		 example :
      		 ell =
      		 {
       		  Az1 = 319.00     # Azimuth 1
       		  Ele1 = -80.00    # Elevation 1
    		 err1 = 24.71     % Semi-major axis 1
    		 Az2 = 54.00      % Azimuth 2
    		 Ele2 = -11.00    % Elevation 2
    		 err2 = 2.84      % Semi-major axis 2
    		 Az3 = 357.00     % Azimuth 3
    		 Ele3 = 17.00     % Elevation 3
       		  err3 = 3.35      % Semi-major axis 3
      		 }
     		- Qenu : variance matrix in local frame
     		- Corr_enu : correlation matrix in local frame
     		- GDOP,PDOP,HDOP,VDOP,TDOP

       if X, Y or Z == 0, no calculation and 0 or empty matrix returned
        """
        if not hasattr(epoch, 'SigmaX'):
            print('Please process SigmaX first')
            return

        # geographic coordinates
        [l,p,h] = tool.tool_cartgeo_GRS80(epoch.X,epoch.Y,epoch.Z)

        n=epoch.SigmaX.shape[0]
        # topocentric matrix ECEF
        M = np.eye(n)
        M[0:3,0:3] = np.array([[-np.sin(p)*np.cos(l), -np.sin(p)*np.sin(l), np.cos(p)],[-np.sin(l), np.cos(l),0.0],[np.cos(p)*np.cos(l), np.cos(p)*np.sin(l), np.sin(p)]])

        # variance propagation
        epoch.SigmaENU = np.dot(M, np.dot(epoch.SigmaX, M.T))

        # standard deviation extraction
        sE2 = epoch.SigmaENU[0,0]
        sN2 = epoch.SigmaENU[1,1]
        sU2 = epoch.SigmaENU[2,2]
        st2 = epoch.SigmaX[3,3]

        # DOP
        epoch.GDOP = np.sqrt(sE2+sN2+sU2+st2)
        epoch.PDOP = np.sqrt(sE2+sN2+sU2)
        epoch.HDOP = np.sqrt(sE2+sN2)
        epoch.VDOP = np.sqrt(sU2)
        epoch.TDOP = np.sqrt(st2)

def main():


    myrinex = rx.rinex_o()
    datadir = '../data/2013150/'
    filename = datadir+'mlvl1500.13o'
    ret = myrinex.loadRinexO(filename)


    if ret<0:
        print(ret)
        return


    t=gps.gpsdatetime()
    t.rinex_t('13  5 30  1  0 30.0000000')

    Ep = myrinex.getEpochByMjd(t.mjd)

    #print(Ep.__dict__)

    mysp3 = orb.orbit()

    mysp3.loadSp3([datadir+'igs17424.sp3',datadir+'igl17424.sp3',datadir+'grm17424.sp3'])

    myspp = gnss_process()
    myspp.const='GRE'
    myspp.constraint=0
    myspp.cut_off = 10 * const.d2r
    myspp.X0[0]=myrinex.headers[0].X
    myspp.X0[1]=myrinex.headers[0].Y
    myspp.X0[2]=myrinex.headers[0].Z

    E2 = myspp.spp(Ep,mysp3)
    myspp.calc_stat_indic(E2)

    print("GDOP = ",E2.GDOP)

    [E,N,U]= tool.toolCartLocGRS80(float(myspp.X0[0]),float(myspp.X0[1]),float(myspp.X0[2]),E2.X,E2.Y,E2.Z)
    print("dE = %.2fm dN = %.2fm dU = %.2fm " % (E,N,U))

#
#    try:
#        Answer = 1/0
#        printAnswer
#    except:
#        print 'Program terminated'
#        return
#    print 'You wont see this'
    
def trilatGps(PosSat,Dobs,X0):
    """ Calcul d'une trilatération simple avec un offset
    correspondant à l'erreur d'horloge du récepteur """

    NbSat = PosSat.shape[0]

    """ Extraction des coordonnées des satellites """
    # on reshape systématiquement pour avoir des matrices et non des vecteurs
    Xs = PosSat[:,0].reshape((NbSat,1))
    Ys = PosSat[:,1].reshape((NbSat,1))
    Zs = PosSat[:,2].reshape((NbSat,1))
    Dobs = Dobs.reshape((NbSat,1))
    X0 = X0.reshape((4,1))

    """ Pondération à 2m """
    sigma = 2
    SigmaB = sigma**2 * np.eye(NbSat)
    P = np.linalg.inv(SigmaB)

    Vsigma0 = []
    for NbIter in range(15):

        Dcalc = ((X0[0]-Xs)**2 +(X0[1]-Ys)**2 +(X0[2]-Zs)**2)**0.5
        A0 = (X0[0] - Xs)/Dcalc
        A1 = (X0[1] - Ys)/Dcalc
        A2 = (X0[2] - Zs)/Dcalc
        A3 = np.ones((NbSat,1))
        A = np.hstack((A0,A1,A2,A3))

        B = Dobs - (Dcalc + X0[3])

        N =  A.T @ P @ A
        K =  A.T @ P @ B
        dX = np.linalg.inv(N) @ K

        X0 = X0 + dX

        V = B - A.dot(dX)
        Vsigma0.append(V.T.dot(P.dot(V)) / (NbSat-4))

        sigma0_2 = Vsigma0[-1].squeeze()
        if NbIter>1:
            if abs(Vsigma0[-1]-Vsigma0[-2])<1e-6:
                break

    SigmaX = sigma0_2 * np.linalg.inv(N)
    X = X0[0].squeeze()
    Y = X0[1].squeeze()
    Z = X0[2].squeeze()
    cdtr = X0[3].squeeze()
    return X,Y,Z,cdtr,sigma0_2,V,SigmaX

def trilatGnss(PosSat,Dobs,X0,sat_index):
    """ Calcul d'une trilatération multiconstellation avec un offset
    correspondant à l'erreur d'horloge du récepteur """

    NbSat = PosSat.shape[0]

    """ Extraction des coordonnées des satellites """
    # on reshape systématiquement pour avoir des matrices et non des vecteurs
    Xs = PosSat[:,0].reshape((NbSat,1))
    Ys = PosSat[:,1].reshape((NbSat,1))
    Zs = PosSat[:,2].reshape((NbSat,1))
    Dobs = Dobs.reshape((NbSat,1))
    X0 = X0.reshape((4,1))

    """ Test du nombre de satellites Galileo
    Si moins de 2 satellites Galileo -> suppression des obs Galileo"""

    """ satellites GPS """
    nb_GPS = sum(sat_index==1);

    """ satellites Galileo """
    nb_GAL = sum(sat_index==2);

    """ satellites Glonass """
    nb_GLO = sum(sat_index==3);

    """ nombre total de satellites """
    nb_sat = nb_GPS + nb_GLO + nb_GAL;

    print("GPS : %d\nGLO : %d\nGAL : %d" % (nb_GPS,nb_GLO,nb_GAL))

    if nb_GLO>2:
        X0 = np.concatenate((X0,np.zeros((1,1))),axis=0)
    if nb_GAL>2:
        X0 = np.concatenate((X0,np.zeros((1,1))),axis=0)

    """ Nombres de colonnes de A :
    3 pour les coordonnées + Nbconst colonnes pour stocker des biais d'horloges récepteur"""

    """ Pondération à 2m """
    sigma = 2
    SigmaB = sigma**2 * np.eye(NbSat)
    P = np.linalg.inv(SigmaB)

    Vsigma0 = []
    for NbIter in range(15):

        Dcalc = ((X0[0]-Xs)**2 +(X0[1]-Ys)**2 +(X0[2]-Zs)**2)**0.5
        A0 = (X0[0] - Xs)/Dcalc
        A1 = (X0[1] - Ys)/Dcalc
        A2 = (X0[2] - Zs)/Dcalc

        B = Dobs - (Dcalc + X0[3])
        
        A_GPS=np.zeros((NbSat,1))
        A_GLO=np.zeros((NbSat,1))
        A_GAL=np.zeros((NbSat,1))
        for i in range(NbSat):
            if sat_index[i]==1:
                A_GPS[i]=1
            if sat_index[i]==2:
                A_GPS[i]=1
                A_GLO[i]=1
                try:
                    B[i] -= X0[4]
                except:
                    pass
            if sat_index[i]==3:
                A_GPS[i]=1
                A_GAL[i]=1
                try:
                    B[i] -= X0[5]
                except:
                    pass

        A = np.concatenate((A0,A1,A2,A_GPS),axis=1)
        if nb_GLO>2:
            A = np.concatenate((A,A_GLO),axis=1)
        if nb_GAL>2:
            A = np.concatenate((A,A_GAL),axis=1)
        
        N =  A.T @ P @ A
        K =  A.T @ P @ B
        dX = np.linalg.inv(N) @ K
        X0 = X0 + dX

        V = B - np.dot(A,dX)
        nParam = len(dX)
        Vsigma0 += [(V.T @ P @V) / (NbSat - nParam)]

        sigma0_2 = Vsigma0[-1].squeeze()
        if NbIter>1:
            if abs(Vsigma0[-1]-Vsigma0[-2])<1e-6:
                break

    SigmaX = sigma0_2 * np.linalg.inv(N)
    X = X0[0].squeeze()
    Y = X0[1].squeeze()
    Z = X0[2].squeeze()
    cdtr = X0[3].squeeze()
    cGGTO=float('NaN')
    cGPGL=float('NaN')
    if nb_GLO>2:
        if nb_GLO>2:
            cGGTO = X0[4]
            if nb_GAL>2:
                cGPGL = X0[5]
        else:
            if nb_GAL>2:
                cGPGL = X0[4]


    return X,Y,Z,cdtr,float(cGGTO),float(cGPGL),sigma0_2,V,SigmaX

def trilatGnssPonderationElev(PosSat,Dobs,X0,sat_index,ElevSat):
    """ Calcul d'une trilatération simple avec un offset
    correspondant à l'erreur d'horloge du récepteur """

    NbSat = PosSat.shape[0]

    """ Extraction des coordonnées des satellites """
    # on reshape systématiquement pour avoir des matrices et non des vecteurs
    Xs = PosSat[:,0].reshape((NbSat,1))
    Ys = PosSat[:,1].reshape((NbSat,1))
    Zs = PosSat[:,2].reshape((NbSat,1))
    Dobs = Dobs.reshape((NbSat,1))
    X0 = X0.reshape((4,1))

    """ Test du nombre de satellites Galileo
    Si moins de 2 satellites Galileo -> suppression des obs Galileo"""

    """ satellites GPS """
    nb_GPS = sum(sat_index==1);

    """ satellites Galileo """
    nb_GAL = sum(sat_index==2);

    """ satellites Glonass """
    nb_GLO = sum(sat_index==3);

    """ nombre total de satellites """
    nb_sat = nb_GPS + nb_GLO + nb_GAL;

    print("GPS : %d\nGLO : %d\nGAL : %d" % (nb_GPS,nb_GLO,nb_GAL))

    indexGLO = np.nan
    indexGAL = np.nan
    if nb_GLO>2:
        X0 = np.concatenate((X0,np.zeros((1,1))),axis=0)
        indexGLO = 4
    if nb_GAL>2:
        X0 = np.concatenate((X0,np.zeros((1,1))),axis=0)
        if indexGLO > 0:
            indexGAL = 5
        else:
            indexGAL = 4

    """ Nombres de colonnes de A :
    3 pour les coordonnées + Nbconst colonnes pour stocker des biais d'horloges récepteur"""

    """ Pondération à 2m """
    sigma = 2
    SigmaB = (sigma / np.sin(ElevSat))**2 * np.eye(NbSat)
    P = np.linalg.inv(SigmaB)

    Vsigma0 = []
    for NbIter in range(15):

        Dcalc = ((X0[0]-Xs)**2 +(X0[1]-Ys)**2 +(X0[2]-Zs)**2)**0.5
        A0 = (X0[0] - Xs) / Dcalc
        A1 = (X0[1] - Ys) / Dcalc
        A2 = (X0[2] - Zs) / Dcalc
        
        B = Dobs - (Dcalc + X0[3])

        A_GPS=np.zeros((NbSat,1))
        A_GLO=np.zeros((NbSat,1))
        A_GAL=np.zeros((NbSat,1))
        
        for i in range(NbSat):
            
            if sat_index[i] == 1:
                A_GPS[i]=1
                
            if sat_index[i] == 2: # Galileo
                A_GPS[i]=1
                A_GAL[i]=1
                try:
                    B[i] -= X0[indexGAL]
                except Exception as err:
                    print(err)
                    
            if sat_index[i] == 3: # Glonass
                A_GPS[i]=1
                A_GLO[i]=1
                try:
                    B[i] -= X0[indexGLO]
                except Exception as err:
                    print(err)

        A = np.concatenate((A0,A1,A2,A_GPS),axis=1)
        if indexGLO > 0:
            A = np.concatenate((A,A_GLO),axis=1)
        if indexGAL > 0:
            A = np.concatenate((A,A_GAL),axis=1)

        N =  A.T @ P @ A
        K =  A.T @ P @ B
        dX = np.linalg.inv(N) @ K
        X0 = X0 + dX

        V = B - np.dot(A,dX)
        nParam = len(dX)
        Vsigma0 += [(V.T @ P @V) / (NbSat - nParam)]
        
        sigma0_2 = Vsigma0[-1].squeeze()
        if NbIter>1:
            if abs(Vsigma0[-1]-Vsigma0[-2])<1e-6:
                break

    SigmaX = sigma0_2 *  np.linalg.inv(N)
    X = X0[0].squeeze()
    Y = X0[1].squeeze()
    Z = X0[2].squeeze()
    cdtr = X0[3].squeeze()
    cGGTO=float('NaN')
    cGPGL=float('NaN')
    
    cGGTO = np.nan
    try:
        cGGTO = float(X0[indexGLO])
    except:
        pass
    
    cGPGL = np.nan
    try:
        cGPGL = float(X0[indexGAL])
    except:
        pass
    


    return X,Y,Z,cdtr,float(cGGTO),float(cGPGL),sigma0_2,V,SigmaX

def TrilatGps(PosSat,Dobs,X0):
    """
    Please do NOT use this function : DEPRECATED
    """
    return trilatGps(PosSat,Dobs,X0)

def TrilatGnss(PosSat,Dobs,X0,sat_index):
    """
    Please do NOT use this function : DEPRECATED
    """
    return trilatGnss(PosSat,Dobs,X0,sat_index)

def TrilatGnssPonderationElev(PosSat,Dobs,X0,sat_index,ElevSat):
    """
    Please do NOT use this function : DEPRECATED
    """
    return trilatGnssPonderationElev(PosSat,Dobs,X0,sat_index,ElevSat)

