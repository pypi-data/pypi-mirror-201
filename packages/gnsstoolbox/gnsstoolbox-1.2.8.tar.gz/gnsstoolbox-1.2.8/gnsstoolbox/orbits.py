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
from operator import attrgetter
import os.path
from math import cos, sin, tan, atan, sqrt, pi
import numpy as np

import gpsdatetime as gpst
import gnsstoolbox.gnsstools as gnsstools

class nav_element():
    """GNSS nav element class"""
    def __init__(self):
        self.tgps = gpst.gpsdatetime()

    @property
    def OMEGA0(self):
        if 'OMEGA' in self.__dict__:
            return self.OMEGA
        return

    def __str__(self):
        """ print() method """

        st = ''
        Ls = []
        for s in self.__dict__:
            if not re.search('tgps', s):
                Ls.append('%-35s : %s\n' % (s, self.__dict__.get(s)))
            elif re.search('tgps', s):
                st += '%-35s : %s\n' % (s+ ' (gpsdatetime object)', self.__dict__.get(s).st_iso_epoch())
            else:
                st += '%-35s : %s\n' % (s, "")
                
        for s in sorted(Ls):
            st += s
#        print(st)
        return st


class debug():
    """debug class"""
    def __init__(self):
        self.const = ""

    def __str__(self):
        """Impression des attributs de la classe"""
        out = ""
        for s in self.__dict__:
            out += '%-35s : %s\n' % (s, str(self.__dict__.get(s)))
        return out


class Sp3Pos():
    """ Classe contenant une epoque de position SP3"""
    def __init__(self, mjd, X, Y, Z, dte):
        self.mjd = mjd
        self.X = X
        self.Y = Y
        self.Z = Z
        self.dte = dte


class orbit():
    """GNSS nav file class

    Jacques Beilin - ENSG/DPTS - 2015-05-24
    """

    def __init__(self):

        self.debug = debug()
        self.type = ""
        self.verbose = 0
        self.version = ""
        self.todo = "concatenation de fichiers sp3 GRE"
        self.todo += "Dessin 3D d'une orbite"

        self.type = ""
        self.leap_seconds = 0
        self.ion_alpha_gps = np.zeros(4)
        self.ion_beta_gps = np.zeros(4)
        self.ion_gal = np.zeros(4)
        self.delta_utc = np.zeros(4)

        self.currentline = 0
        self.rinexlines = []

        self.NAV_dataG = []
        for i in range(32):
            self.NAV_dataG.append([])
            self.NAV_dataG[i] = []

        self.NAV_dataR = []
        for i in range(32):
            self.NAV_dataR.append([])
            self.NAV_dataR[i] = []

        self.NAV_dataE = []
        for i in range(36):
            self.NAV_dataE.append([])
            self.NAV_dataE[i] = []

        self.sp3G = []
        for i in range(32):
            self.sp3G.append([])

        self.sp3E = []
        for i in range(36):
            self.sp3E.append([])

        self.sp3R = []
        for i in range(32):
            self.sp3R.append([])
            

    def loadSp3(self, filename=""):
        """sp3 ephemeris loading
        Interpolation of these data with calcSatCoordSp3

        Jacques Beilin - ENSG/DPTS - 2014-05-19

        Input :
        - filenames : sp3 filenames in cell array(one file for each constellation) :
            GPS, GLO and GAL supported
        ex : {'sp3_GPS.sp3' 'sp3_GLO.sp3'  'sp3_GAL.sp3'}

        Output :
        - sp3 class fields
            - Version
            - Flag
            - Date
            - Number_of_Epochs
            - Data_Used
            - Coordinate_Sys
            - Orbit_Type
            - Agency
            - wk
            - sow
            - Epoch_Interval
            - mjd
            - Fractional_Day

            - sp3G : list of Sp3Pos objects for GPS satellites
            - sp3R : list of Sp3Pos objects for Glonass satellites
            - sp3E : list of Sp3Pos objects for Galileo satellites
        """

        if re.compile('list').search(type(filename).__name__):
            for sp3file in filename: # file list
                ret = self._loadSp3(sp3file)
        else:
            ret = self._loadSp3(filename) # only one file

        return ret

    def _loadSp3(self, filename=""):
        if filename == "":
            return -1

        if not os.path.isfile(filename):
            print('Unable to find %s' % (filename))
            return -2

        r = re.compile('[ \t\n\r:]+')

        self.type = 'sp3'

        """ loading strings """
        try:
            with open(filename, encoding='utf-8', errors='replace') as F:
                sp3lines = F.readlines()
        except:
            print('Unable to open %s' % (filename))
            return -3

        print("Loading SP3 file %s" % filename)

        """ Format checking """
        if not(re.match("^#c", sp3lines[0]) or re.match("^#d", sp3lines[0])):
            print("file %s : Format not valid !" % (filename))
            return -4

        """ Epoch count """
        nepoch = 0
        for l in sp3lines:
            if re.compile("^\*").search(l):
                nepoch += 1

        for nl in range(22, len(sp3lines)):
            line = sp3lines[nl]
            if re.match("^\*", line):
                strdate = line[1:]
                list_strdate = strdate.split()
                t = gpst.gpsdatetime()
                t.ymdhms_t(float(list_strdate[0]), float(list_strdate[1]), \
                           float(list_strdate[2]), float(list_strdate[3]), \
                           float(list_strdate[4]), float(list_strdate[5]))
                """ determination de l'intervale entre les points """
                mjd = t.mjd
                try:
                    if mjd0:
                        self.interval = round(t - gpst.gpsdatetime(mjd=mjd0))
                        mjd0 = mjd
                except:
                    mjd0 = mjd

            elif re.match("^PG", line):
                list_str = r.split(line)
                try:
                    X = float(list_str[1])
                    Y = float(list_str[2])
                    Z = float(list_str[3])
                    dte = float(list_str[4])
                    PRN = int(list_str[0][2:])

                    if not abs(dte-999999.999999) < 100:
                        id0 = int(PRN-1)
                        self.sp3G[id0].append(Sp3Pos(mjd, X, Y, Z, dte))
                except:
                    pass

            elif re.match("^PR", line):
                list_str = r.split(line)
                try:
                    X = float(list_str[1])
                    Y = float(list_str[2])
                    Z = float(list_str[3])
                    dte = float(list_str[4])
                    PRN = int(list_str[0][2:])

                    if not abs(dte-999999.999999) < 100:
                        id0 = int(PRN-1)
                        self.sp3R[id0].append(Sp3Pos(mjd, X, Y, Z, dte))
                except:
                    pass

            elif re.match("^PE", line):
                list_str = r.split(line)
                try:
                    X = float(list_str[1])
                    Y = float(list_str[2])
                    Z = float(list_str[3])
                    dte = float(list_str[4])
                    PRN = int(list_str[0][2:])

                    if not abs(dte-999999.999999) < 100:
                        id0 = int(PRN-1)
                        self.sp3E[id0].append(Sp3Pos(mjd, X, Y, Z, dte))
                except:
                    pass

        self._sortSp3()

        return 0

    def _sortSp3(self):
        """
        1. sort all sp3G, sp3E, sp3R lists
        2. set first and last epoch
        3. set sat list

        J. Beilin - 2018-06-22

        """
        self.EpochList = []
        for i in range(len(self.sp3G)):
            self.sp3G[i] = sorted(self.sp3G[i], key=lambda s: s.mjd, reverse=False)
            for j in range(len(self.sp3G[i])):
                self.EpochList.append(gpst.gpsdatetime(mjd=self.sp3G[i][j].mjd))

        for i in range(len(self.sp3R)):
            self.sp3R[i] = sorted(self.sp3R[i], key=lambda s: s.mjd, reverse=False)
            for j in range(len(self.sp3R[i])):
                self.EpochList.append(gpst.gpsdatetime(mjd=self.sp3R[i][j].mjd))

        for i in range(len(self.sp3E)):
            self.sp3E[i] = sorted(self.sp3E[i], key=lambda s: s.mjd, reverse=False)
            for j in range(len(self.sp3E[i])):
                self.EpochList.append(gpst.gpsdatetime(mjd=self.sp3E[i][j].mjd))

        """ setting first and last epoch """
        self.t0 = gpst.gpsdatetime()
        self.tLast = gpst.gpsdatetime(yyyy=1980, mon=1, dd=6)
        nepoch = 0
        self.ListSat = []
        for i in range(len(self.sp3G)):
            try:
                if self.sp3G[i][0].mjd < self.t0.mjd:
                    self.t0.mjd_t(self.sp3G[i][0].mjd)
                if self.sp3G[i][-1].mjd > self.tLast.mjd:
                    self.tLast.mjd_t(self.sp3G[i][-1].mjd)
            except:
                pass
            if len(self.sp3G[i]) > 0:
                self.ListSat.append('G%02d' % (i+1))
            if len(self.sp3G[i]) > nepoch:
                nepoch = len(self.sp3G[i])

        for i in range(len(self.sp3R)):
            try:
                if self.sp3R[i][0].mjd < self.t0.mjd:
                    self.t0.mjd_t(self.sp3R[i][0].mjd)
                if self.sp3R[i][-1].mjd > self.tLast.mjd:
                    self.tLast.mjd_t(self.sp3R[i][-1].mjd)
            except:
                pass
            if len(self.sp3R[i]) > 0:
                self.ListSat.append('R%02d' % (i+1))
            if len(self.sp3R[i]) > nepoch:
                nepoch = len(self.sp3R[i])

        for i in range(len(self.sp3E)):
            try:
                if self.sp3E[i][0].mjd < self.t0.mjd:
                    self.t0.mjd_t(self.sp3E[i][0].mjd)
                if self.sp3E[i][-1].mjd > self.tLast.mjd:
                    self.tLast.mjd_t(self.sp3E[i][-1].mjd)
            except:
                pass
            if len(self.sp3E[i]) > 0:
                self.ListSat.append('E%02d' % (i+1))
            if len(self.sp3E[i]) > nepoch:
                nepoch = len(self.sp3E[i])

        self.nepoch = nepoch

        return 0

    def writeSp3(self, Sp3FileName):
        """
        Write a new sp3 file from all sp3G, sp3E, sp3R lists

        J. Beilin - 2018-06-22

        """

        if Sp3FileName == "":
            return -1

        s = ""
        s += "#cP%04d %2d %2d %2d %2d %11.8f    %4d ORBIT IGS14\n" % \
        (self.t0.yyyy, self.t0.mon, self.t0.dd, self.t0.hh, self.t0.min, \
         self.t0.sec, self.nepoch)
        s += "## %4d %15.8f   %12.8f %5d %15.13f\n" % (self.t0.wk, \
        self.t0.wsec, self.interval, np.floor(self.t0.mjd), self.t0.mjd \
        - np.floor(self.t0.mjd))
        s1 = '+   %2d   ' % (len(self.ListSat))
        while len(s1) < 60:
            s1 += self.ListSat.pop(0)
        s += s1+"\n"
        for i in range(4):
            s1 = '+        '
            while len(s1) < 60:
                if len(self.ListSat) > 0:
                    s1 += self.ListSat.pop(0)
                else:
                    s1 += '  0'
            s += s1+"\n"
        for i in range(5):
            s += '++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n'

        s += '%c M  cc GPS ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc\n'
        s += '%c cc cc ccc ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc\n'
        s += '%f  0.0000000  0.000000000  0.00000000000  0.000000000000000\n'
        s += '%f  0.0000000  0.000000000  0.00000000000  0.000000000000000\n'
        s += '%i    0    0    0    0      0      0      0      0         0\n'
        s += '%i    0    0    0    0      0      0      0      0         0\n'
        s += '/* CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC\n'
        s += '/* CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC\n'
        s += '/* CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC\n'
        s += '/* CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC\n'

        t = gpst.gpsdatetime(mjd=self.t0.mjd)
        eps = 1e-3
        while t.mjd < self.tLast.mjd+1e-6:
            s += "*  %4d %2d %2d %2d %2d %11.8f\n" % (t.yyyy, t.mon, t.dd, t.hh, t.min, t.sec)
            for i in range(len(self.sp3G)):
                try:
                    for j in range(len(self.sp3G[i])):
                        if abs(self.sp3G[i][j].mjd-t.mjd) < eps:
                            s += "PG%02d%14.6f%14.6f%14.6f%14.6f\n" % \
                            (i+1, self.sp3G[i][j].X, self.sp3G[i][j].Y, \
                             self.sp3G[i][j].Z, self.sp3G[i][j].dte)
                            break
                except:
                    pass
            for i in range(len(self.sp3R)):
                try:
                    for j in range(len(self.sp3R[i])):
                        if abs(self.sp3R[i][j].mjd-t.mjd) < eps:
                            s += "PR%02d%14.6f%14.6f%14.6f%14.6f\n" % \
                            (i+1, self.sp3G[i][j].X, self.sp3G[i][j].Y, \
                             self.sp3G[i][j].Z, self.sp3G[i][j].dte)
                            break
                except:
                    pass
            for i in range(len(self.sp3E)):
                try:
                    for j in range(len(self.sp3E[i])):
                        if abs(self.sp3E[i][j].mjd-t.mjd) < eps:
                            s += "PE%02d%14.6f%14.6f%14.6f%14.6f\n" % \
                            (i+1, self.sp3G[i][j].X, self.sp3G[i][j].Y, \
                             self.sp3G[i][j].Z, self.sp3G[i][j].dte)
                            break
                except:
                    pass
            t += self.interval

        try:
            with open(Sp3FileName, 'wt') as f:
                f.write(s)
        except:
            print('Unable to write data in %s' % (Sp3FileName))
        return 0

    def getSp3(self, constellation, PRN, **kwargs):
        """ Get epoch number and sp3 data for a specific satellite

        Jacques Beilin - ENSG/DPTS - 2015-05-24

        Input :
            - constellation : 'G' for GPS, 'R' for Glonass and 'E' for Galileo
            - PRN : satellite id

        Output :
            - sp3 : matrix containing : mjd, X (km), Y (km), Z (km), dte (us)
            - nl : epoch number
        """

        #mjd = kwargs.get('mjd', 0)

        if re.search('G', constellation):
            ListSp3 = self.sp3G[PRN-1]
        elif re.search('R', constellation):
            ListSp3 = self.sp3R[PRN-1]
        elif re.search('E', constellation):
            ListSp3 = self.sp3E[PRN-1]
        else:
            nl = 0

        nl = len(ListSp3)
        sp3 = np.zeros((5, nl))
        for i in range(nl):
            sp3[:, i] = np.array([ListSp3[i].mjd, ListSp3[i].X, ListSp3[i].Y, \
                                 ListSp3[i].Z, ListSp3[i].dte])

        return sp3.T, nl

    def loadRinexN(self, filename=""):
        """GPS/Glonass/Galileo navigation RINEX loading

         Jacques Beilin - ENSG/DPTS - 2021-09-11

         Input :
         - filenames : navigation files in a cell array (RINEX v2.11 or RINEX v3.__)

           INFO  :
           Use the function getEphemeris to get the data of navigation files
        """

        if re.compile('list').search(type(filename).__name__):
            for sp3file in filename: # file list
                ret = self._loadRinexN(sp3file)
        else:
            ret = self._loadRinexN(filename) # only one file
            
        return ret


    def _loadRinexN(self, filename=""):
        """GPS/Glonass/Galileo navigation RINEX loading

         Jacques Beilin - ENSG/DPTS - 2015-05-24

         Input :
         - filenames : navigation files in a cell array (RINEX v2.11 or RINEX v3.__)

           INFO  :
           Use the function getEphemeris to get the data of navigation files
        """
        
        

        if filename == "":
            return -1

        if not os.path.isfile(filename):
            print('Unable to find %s' % (filename))
            return -2


        # loading strings
        try:
            with open(filename, encoding='utf-8', errors='replace') as F:
                self.rinexlines = F.readlines()
                self.currentline = 0
#                F.close()
        except:
            print('Unable to open %s' % (filename))
            return -3

        print("Loading RINEX nav file %s" % filename)

        # Format checking
        if not re.search("RINEX VERSION / TYPE", self.rinexlines[0]):
            print("file %s : Format not valid !" % (filename))
            return -4

        self._read_nav_header()

        if self.version >= 3:
            self._read_nav_data_GNSS_300()
        else:
            if self.type == 'N':
                self._read_nav_data_GPS_211()
            if self.type == 'G':
                self._read_nav_data_Glonass_211()
        self.type = "nav"


    def _read_nav_header(self):
        """"""

        for i in range(len(self.rinexlines)):

            s = self.rinexlines[i]
            self.currentline = i # on stocke pour savoir où on en est dans la lecture

            if re.search('RINEX VERSION / TYPE', s):
                self.version = float(s[0:10])
                self.type = s[20]

            if re.search('LEAP SECONDS', s):
                self.leap_seconds = float(s[0:6])

#            if self.version> = 3:
#                print("NAV rinex v3 not supported in current version")

            else:
                if re.search('ION ALPHA', s):
                    for j in range(4):
                        self.ion_alpha_gps[j] = self._nav_str2float(s[2+(j)*12:2+(j+1)*12])

                if re.search('ION BETA', s):
                    for j in range(4):
                        self.ion_beta_gps[j] = self._nav_str2float(s[2+(j)*12:2+(j+1)*12])

                if re.search('DELTA-UTC: A0, A1, T, W', s):
                    self.delta_utc[0] = self._nav_str2float(s[0:22])
                    self.delta_utc[1] = self._nav_str2float(s[22:41])
                    self.delta_utc[2] = self._nav_str2float(s[41:50])
                    self.delta_utc[3] = self._nav_str2float(s[50:59])

            if re.search('END OF HEADER', s):
                return

    def _nav_str2float(self, s):
        """Conversion from RINEX string representation of floats to python float"""
        try:
            x = float(re.sub('[Dd]', 'e', s))
        except:
            x = 0
        return x

    def _read_nav_data_Glonass_211(self):
        """"""

        while 1:
            self.currentline += 1
            if self.currentline > len(self.rinexlines)-1:
                break

            s = self.rinexlines[self.currentline]

            nav = nav_element()

            nav.const = 'R'
            nav.PRN = int(s[0:2])
            nav.tgps.rinex_t(s[2:22])
            nav.mjd = nav.tgps.mjd

            nav.SV_clock_offset = self._nav_str2float(s[22:41])
            nav.SV_relat_freq_offset = self._nav_str2float(s[41:60])
            nav.Message_frame_time = self._nav_str2float(s[60:79])

            self.currentline += 1
            s = self.rinexlines[self.currentline]
            #print(s)
            nav.X = 1e3 * self._nav_str2float(s[3:22])
            nav.X_dot = 1e3 * self._nav_str2float(s[22:41])
            nav.MS_X_acc = 1e3 * self._nav_str2float(s[41:60])
            nav.sv_health = self._nav_str2float(s[60:79])

            self.currentline += 1
            s = self.rinexlines[self.currentline]
            #print(s)
            nav.Y = 1e3 * self._nav_str2float(s[3:22])
            nav.Y_dot = 1e3 * self._nav_str2float(s[22:41])
            nav.MS_Y_acc = 1e3 * self._nav_str2float(s[41:60])
            nav.freq_num = self._nav_str2float(s[60:79])

            self.currentline += 1
            s = self.rinexlines[self.currentline]
            #print(s)
            nav.Z = 1e3 * self._nav_str2float(s[3:22])
            nav.Z_dot = 1e3 * self._nav_str2float(s[22:41])
            nav.MS_Z_acc = 1e3 * self._nav_str2float(s[41:60])
            nav.age_op_inf = self._nav_str2float(s[60:79])

            pos = -1
            for i in range(len(self.NAV_dataR[nav.PRN-1])):
                if abs(nav.mjd-self.NAV_dataR[nav.PRN-1][i].mjd) < 1.0/1440.0:
                    pos = i
                    if self.verbose > 0:
                        print('Ephemeris data already loaded for satellite %s%02d (%.5f ~ %.5f Delta = %.2f s)' % (nav.const, nav.PRN, nav.mjd, self.NAV_dataR[nav.PRN-1][pos].mjd, 86400*(nav.mjd - self.NAV_dataR[nav.PRN-1][pos].mjd)))
                    break

            if pos < 0:
                self.NAV_dataR[nav.PRN-1].append(nav)
            else:
                if self.verbose > 0:
                    print('Ephemeris data already loaded for satellite %s%02d (%.5f ~ %.5f Delta = %.2f s)' % (nav.const, nav.PRN, nav.mjd, self.NAV_dataR[nav.PRN-1][pos].mjd, 86400*(nav.mjd - self.NAV_dataR[nav.PRN-1][pos].mjd)))

        for i in range(32): # sort list
            self.NAV_dataR[i] = sorted(self.NAV_dataR[i], key=attrgetter("mjd"))

        self.rinexlines = []
        self.currentline = 0


    def _read_nav_data_GPS_211(self):
        """"""

        while 1:
            self.currentline += 1
            if self.currentline > len(self.rinexlines)-1:
                break

            s = self.rinexlines[self.currentline]

            nav = nav_element()

            nav.const = 'G'
            nav.PRN = int(s[0:2])
            nav.tgps.rinex_t(s[2:22])
            nav.mjd = nav.tgps.mjd
            nav.TOC = nav.mjd

            nav.alpha0 = self._nav_str2float(s[22:41])
            nav.alpha1 = self._nav_str2float(s[41:60])
            nav.alpha2 = self._nav_str2float(s[60:79])

            self.currentline += 1
            s = self.rinexlines[self.currentline]
            #print(s)
            nav.IODE = self._nav_str2float(s[3:22])
            nav.crs = self._nav_str2float(s[22:41])
            nav.delta_n = self._nav_str2float(s[41:60])
            nav.M0 = self._nav_str2float(s[60:79])

            self.currentline += 1
            s = self.rinexlines[self.currentline]
            #print(s)
            nav.cuc = self._nav_str2float(s[3:22])
            nav.e = self._nav_str2float(s[22:41])
            nav.cus = self._nav_str2float(s[41:60])
            nav.sqrt_a = self._nav_str2float(s[60:79])

            self.currentline += 1
            s = self.rinexlines[self.currentline]
            #print(s)
            nav.TOE = self._nav_str2float(s[3:22])
            nav.cic = self._nav_str2float(s[22:41])
            nav.OMEGA = self._nav_str2float(s[41:60])
            nav.cis = self._nav_str2float(s[60:79])

            self.currentline += 1
            s = self.rinexlines[self.currentline]
            #print(s)
            nav.i0 = self._nav_str2float(s[3:22])
            nav.crc = self._nav_str2float(s[22:41])
            nav.omega = self._nav_str2float(s[41:60])
            nav.OMEGA_DOT = self._nav_str2float(s[60:79])

            self.currentline += 1
            s = self.rinexlines[self.currentline]
            #print(s)
            nav.IDOT = self._nav_str2float(s[3:22])
            nav.code_L2 = self._nav_str2float(s[22:41])
            nav.gps_wk = self._nav_str2float(s[41:60])
            nav.L2_P = self._nav_str2float(s[60:79])

            self.currentline += 1
            s = self.rinexlines[self.currentline]
            #print(s)
            nav.sv_acc = self._nav_str2float(s[3:22])
            nav.sv_health = self._nav_str2float(s[22:41])
            nav.TGD = self._nav_str2float(s[41:60])
            nav.IODC = self._nav_str2float(s[60:79])

            self.currentline += 1
            s = self.rinexlines[self.currentline]
            #print(s)
            nav.transmit_time = self._nav_str2float(s[3:22])
            try:
                nav.fit_interval = self._nav_str2float(s[22:41])
            except:
                nav.fit_interval = 0.0

            pos = -1
            for i in range(len(self.NAV_dataG[nav.PRN-1])):
                if abs(nav.mjd-self.NAV_dataG[nav.PRN-1][i].mjd) < 1/96:
                    pos = i
                    break

            if pos < 0:
                self.NAV_dataG[nav.PRN-1].append(nav)
            else:
                if self.verbose > 0:
                    print('Ephemeris data already loaded for satellite %s%02d (%.5f ~ %.5f Delta = %.2f s)' % (nav.const, nav.PRN, nav.mjd, self.NAV_dataG[nav.PRN-1][pos].mjd, 86400*(nav.mjd - self.NAV_dataG[nav.PRN-1][pos].mjd)))

        for i in range(32): # sort list
            self.NAV_dataG[i] = sorted(self.NAV_dataG[i], key=attrgetter("mjd"))

        self.rinexlines = []
        self.currentline = 0

    def _read_nav_data_GNSS_300(self):
        """"""

        while 1:
            self.currentline += 1
            if self.currentline > len(self.rinexlines)-1:
                break

            s = self.rinexlines[self.currentline]

            nav = nav_element()

            nav.const = s[0:1] # detection de la constellation (les brdc 3.nn peuvent être mixtes)

            if nav.const == 'G':

                nav.PRN = int(s[1:3])
                nav.tgps.rinex_t(s[3:23])
                nav.mjd = nav.tgps.mjd
                nav.TOC = nav.mjd

                nav.alpha0 = self._nav_str2float(s[23:42])
                nav.alpha1 = self._nav_str2float(s[42:61])
                nav.alpha2 = self._nav_str2float(s[61:80])

                self.currentline += 1
                s = self.rinexlines[self.currentline]
                #print(s)
                nav.IODE = self._nav_str2float(s[4:23])
                nav.crs = self._nav_str2float(s[23:42])
                nav.delta_n = self._nav_str2float(s[42:61])
                nav.M0 = self._nav_str2float(s[61:80])

                self.currentline += 1
                s = self.rinexlines[self.currentline]
                #print(s)
                nav.cuc = self._nav_str2float(s[4:23])
                nav.e = self._nav_str2float(s[23:42])
                nav.cus = self._nav_str2float(s[42:61])
                nav.sqrt_a = self._nav_str2float(s[61:80])

                self.currentline += 1
                s = self.rinexlines[self.currentline]
                #print(s)
                nav.TOE = self._nav_str2float(s[4:23])
                nav.cic = self._nav_str2float(s[23:42])
                nav.OMEGA = self._nav_str2float(s[42:61])
                nav.cis = self._nav_str2float(s[61:80])

                self.currentline += 1
                s = self.rinexlines[self.currentline]
                #print(s)
                nav.i0 = self._nav_str2float(s[4:23])
                nav.crc = self._nav_str2float(s[23:42])
                nav.omega = self._nav_str2float(s[42:61])
                nav.OMEGA_DOT = self._nav_str2float(s[61:80])

                self.currentline += 1
                s = self.rinexlines[self.currentline]
                #print(s)
                nav.IDOT = self._nav_str2float(s[4:23])
                nav.code_L2 = self._nav_str2float(s[23:42])
                nav.gps_wk = self._nav_str2float(s[42:61])
                nav.L2_P = self._nav_str2float(s[61:80])

                self.currentline += 1
                s = self.rinexlines[self.currentline]
                #print(s)
                nav.sv_acc = self._nav_str2float(s[4:23])
                nav.sv_health = self._nav_str2float(s[23:42])
                nav.TGD = self._nav_str2float(s[42:61])
                nav.IODC = self._nav_str2float(s[61:80])

                self.currentline += 1
                s = self.rinexlines[self.currentline]
                #print(s)
                nav.transmit_time = self._nav_str2float(s[4:23])
                try:
                    nav.fit_interval = self._nav_str2float(s[23:42])
                except:
                    nav.fit_interval = 0.0

                pos = -1
                for i in range(len(self.NAV_dataG[nav.PRN-1])):
                    if abs(nav.mjd-self.NAV_dataG[nav.PRN-1][i].mjd) < 1/1440:
                        pos = i
                        break

                if pos < 0:
                    self.NAV_dataG[nav.PRN-1].append(nav)
                else:
                    if self.verbose > 0:
                        print('Ephemeris data already loaded for satellite %s%02d (%.5f ~ %.5f Delta = %.2f s)' % (nav.const, nav.PRN, nav.mjd, self.NAV_dataG[nav.PRN-1][pos].mjd, 86400*(nav.mjd - self.NAV_dataG[nav.PRN-1][pos].mjd)))

            if nav.const == 'R':

                nav.PRN = int(s[1:3])
                nav.tgps.rinex_t(s[3:23])
                nav.mjd = nav.tgps.mjd

                nav.SV_clock_offset = self._nav_str2float(s[23:42])
                nav.SV_relat_freq_offset = self._nav_str2float(s[42:61])
                nav.Message_frame_time = self._nav_str2float(s[61:80])

                self.currentline += 1
                s = self.rinexlines[self.currentline]
                #print(s)
                nav.X = 1e3 * self._nav_str2float(s[3:23])
                nav.X_dot = 1e3 * self._nav_str2float(s[23:42])
                nav.MS_X_acc = 1e3 * self._nav_str2float(s[42:61])
                nav.sv_health = self._nav_str2float(s[61:80])

                self.currentline += 1
                s = self.rinexlines[self.currentline]
                #print(s)
                nav.Y = 1e3 * self._nav_str2float(s[3:23])
                nav.Y_dot = 1e3 * self._nav_str2float(s[23:42])
                nav.MS_Y_acc = 1e3 * self._nav_str2float(s[42:61])
                nav.freq_num = self._nav_str2float(s[61:80])

                self.currentline += 1
                s = self.rinexlines[self.currentline]
                #print(s)
                nav.Z = 1e3 * self._nav_str2float(s[3:23])
                nav.Z_dot = 1e3 * self._nav_str2float(s[23:42])
                nav.MS_Z_acc = 1e3 * self._nav_str2float(s[42:61])
                nav.age_op_inf = self._nav_str2float(s[61:80])

                pos = -1
                for i in range(len(self.NAV_dataR[nav.PRN-1])):
                    if abs(nav.mjd-self.NAV_dataR[nav.PRN-1][i].mjd) < 1.0/1440.0:
                        pos = i
                        if self.verbose > 0:
                            print('Ephemeris data already loaded for satellite %s%02d (%.5f ~ %.5f Delta = %.2f s)' % (nav.const, nav.PRN, nav.mjd, self.NAV_dataR[nav.PRN-1][pos].mjd, 86400*(nav.mjd - self.NAV_dataR[nav.PRN-1][pos].mjd)))
                        break

                if pos < 0:
                    self.NAV_dataR[nav.PRN-1].append(nav)
                else:
                    if self.verbose > 0:
                        print('Ephemeris data already loaded for satellite %s%02d (%.5f ~ %.5f Delta = %.2f s)' % (nav.const, nav.PRN, nav.mjd, self.NAV_dataR[nav.PRN-1][pos].mjd, 86400*(nav.mjd - self.NAV_dataR[nav.PRN-1][pos].mjd)))


            if nav.const == 'E':

                nav.PRN = int(s[1:3])
                nav.tgps.rinex_t(s[3:23])
                nav.mjd = nav.tgps.mjd
                nav.TOC = nav.mjd

                nav.alpha0 = self._nav_str2float(s[23:42])
                nav.alpha1 = self._nav_str2float(s[42:61])
                nav.alpha2 = self._nav_str2float(s[61:80])

                self.currentline += 1
                s = self.rinexlines[self.currentline]
                #print(s)
                nav.IODnav = self._nav_str2float(s[4:23])
                nav.crs = self._nav_str2float(s[23:42])
                nav.delta_n = self._nav_str2float(s[42:61])
                nav.M0 = self._nav_str2float(s[61:80])

                self.currentline += 1
                s = self.rinexlines[self.currentline]
                #print(s)
                nav.cuc = self._nav_str2float(s[4:23])
                nav.e = self._nav_str2float(s[23:42])
                nav.cus = self._nav_str2float(s[42:61])
                nav.sqrt_a = self._nav_str2float(s[61:80])

                self.currentline += 1
                s = self.rinexlines[self.currentline]
                #print(s)
                nav.TOE = self._nav_str2float(s[4:23])
                nav.cic = self._nav_str2float(s[23:42])
                nav.OMEGA = self._nav_str2float(s[42:61])
                nav.cis = self._nav_str2float(s[61:80])

                self.currentline += 1
                s = self.rinexlines[self.currentline]
                #print(s)
                nav.i0 = self._nav_str2float(s[4:23])
                nav.crc = self._nav_str2float(s[23:42])
                nav.omega = self._nav_str2float(s[42:61])
                nav.OMEGA_DOT = self._nav_str2float(s[61:80])

                self.currentline += 1
                s = self.rinexlines[self.currentline]
                #print(s)
                nav.IDOT = self._nav_str2float(s[4:23])
                nav.gps_wk = self._nav_str2float(s[42:61])
                nav.gal_wk = nav.gps_wk

                self.currentline += 1
                s = self.rinexlines[self.currentline]
                #print(s)
                nav.SISA = self._nav_str2float(s[4:23])
                nav.sv_health = self._nav_str2float(s[23:42])

                pos = -1
                for i in range(len(self.NAV_dataE[nav.PRN-1])):
                    if abs(nav.mjd-self.NAV_dataE[nav.PRN-1][i].mjd) < 1/1440:
                        pos = i
                        break

                if pos < 0:
                    self.NAV_dataE[nav.PRN-1].append(nav)
                else:
                    if self.verbose > 0:
                        print('Ephemeris data already loaded for satellite %s%02d (%.5f ~ %.5f Delta = %.2f s)' % (nav.const, nav.PRN, nav.mjd, self.NAV_dataE[nav.PRN-1][pos].mjd, 86400*(nav.mjd - self.NAV_dataE[nav.PRN-1][pos].mjd)))


        for i in range(len(self.NAV_dataG)): # sort list
            self.NAV_dataG[i] = sorted(self.NAV_dataG[i], key=attrgetter("mjd"))

        for i in range(len(self.NAV_dataR)): # sort list
            self.NAV_dataR[i] = sorted(self.NAV_dataR[i], key=attrgetter("mjd"))

        for i in range(len(self.NAV_dataE)): # sort list
            self.NAV_dataE[i] = sorted(self.NAV_dataE[i], key=attrgetter("mjd"))

        self.rinexlines = []
        self.currentline = 0


    def getEphemeris(self, const, PRN, mjd):
        """
         Get navigation message for one satellite at mjd (GPS, Glonass and Galileo supported)

         Jacques Beilin - ENSG/DPTS - 2015-05-21

         Input (assuming rinex nav file already loaded) :
         - constellation : 'G' = GPS, 'R' = Glonass, 'E' = Galileo
         - PRN : satellite id
         - mjd : date (modified julian date format)

         Output :
             - Eph structure containing informations

         If no informations are found, no fields are defined in Eph.
         Ex : hasattr(Eph, 'mjd') returns 0 if Eph is empty
         or use try: ...except:... block

         Eph content depends on constellation (GPS, Glonass and Galileo supported)

         Note : getEphemeris returns 0 if health of satellite is not OK (sv_health ~ =  0)

         Examples :

         GPS

         Eph = getEphemeris('G', 1, 56442.0833333)
         Eph =
         {
           PRN =  1
           mjd =  56442.0833333335
           TOC =  56442.0833333335
           alpha0 =  3.15997749567000e-05
           alpha1 =  4.32009983342100e-12
           alpha2 = 0
           const = G
           IODE =  94
           crs =  2.25000000000000
           delta_n =  4.63876465173900e-09
           M0 =  1.81168558621700
           cuc =  2.75671482086200e-07
           e =  0.00189499533735200
           cus =  1.05910003185300e-05
           sqrt_a =  5153.70066070600
           TOE =  352800
           cic =  2.60770320892300e-08
           OMEGA = -1.46537454108600
           cis =  1.37835741043100e-07
           i0 =  0.959848465747100
           crc =  173.687500000000
           omega =  0.255929757187400
           OMEGA_DOT = -8.04104922769100e-09
           IDOT =  3.31799535068200e-10
           code_L2 = 0
           gps_wk =  1742
           L2_P = 0
           sv_acc =  2
           sv_health = 0
           TGD =  8.38190317153900e-09
           IODC =  94
           trans_time =  345600
         }

          GLONASS

         Eph = getEphemeris('R', 1, 56442.0833333)
         Eph =
         {
           PRN =  1
           mjd =  56442.0104166665
           TOC =  56442.0104166665
           SV_clock_offset = -1.72349624335800e-04
           SV_relat_freq_offset = 0
           const = R
           Message_frame_time =  345600
           X =  18585.5019531200
           X_dot =  1.61786460876500
           X_acc = 0
           sv_health = 0
           Y = -12058.0571289100
           Y_dot = -0.623869895935100
           Y_acc =  9.31322574615500e-10
           freq_num =  1
           Z = -12625.5478515600
           Z_dot =  2.97767543792700
           Z_acc = 0
           age_op_inf = 0
         }

          Galileo

         Eph = getEphemeris('E', 11, 56442.0833333)
         Eph =
         {
           PRN =  11
           mjd =  56442
           TOC =  56442
           alpha0 =  9.06531931832400e-04
           alpha1 =  8.25934876047500e-11
           alpha2 = 0
           const = E
           IODnav =  64
           crs = -127
           delta_n =  3.22049128924600e-09
           M0 =  2.45252068075900
           cuc = -5.72949647903400e-06
           e =  3.02415806800100e-04
           cus =  1.07511878013600e-05
           sqrt_a =  5440.61737251300
           TOE =  345600
           cic =  2.42143869400000e-08
           OMEGA = -2.27501476678800
           cis = 0
           i0 =  0.957955133762200
           crc =  109.468750000000
           omega = -0.819738964252500
           OMEGA_DOT = -5.59094717110500e-09
           IDOT = -1.00004165574900e-11
           data_src =  513
           gal_wk =  1742
           SISA = -1
           sv_health =  452
           BGDE5a = -6.51925802230800e-09
           BGDE5b = 0
           trans_time =  346255
         }
        """

        if const == 'G':
            NavData = self.NAV_dataG
            if (PRN < 1 or PRN > 32):
                return
        elif const == 'R':
            NavData = self.NAV_dataR
            if (PRN < 1 or PRN > 32):
                return
        elif const == 'E':
            NavData = self.NAV_dataE
            if (PRN < 1 or PRN > 30):
                return
        else:
            print("Constellation not implemented")

        # recuperation des dates pour le satellite concerné
        dates = np.zeros((len(NavData[PRN-1]), 1))

        if len(dates) == 0: # On sort si pas d'ephemerides pour ce satellite
            return

        for i in range(len(NavData[PRN-1])):
            dates[i] = mjd-NavData[PRN-1][i].mjd
            #print(i, mjd-NavData[PRN-1][i].mjd)

        pos = np.argmin(np.abs(dates))
        dt_min = np.min(np.abs(dates))
        #print(pos, dt_min)

        if dt_min > 1/12: # au minimum on doit avoir un message par preriode de 2h
            return

        #print(NavData[PRN-1][pos].__dict__)
        return NavData[PRN-1][pos]
    
    def calcSatCoord(self, const, PRN, mjd, degree=9):
        """
         Calculates ECEF GPS, Galileo and Glonass satellite coordinates and
         satellite clock error from ephemeris structure or sp3_data

         Jacques Beilin - ENSG/DPTS - 2015-05-24

         Input :
         - const : constellation id ('G' for GPS, 'R' for Glonass and 'E' for Galileo)
         - PRN : satellite id in constellation
         - mjd : modified Julian day
         - degree : degree for Lagrange interpolation (optional)

         Output
         - X, Y, Z : cartesian coordinates :
          - if navigation message used :
                    - WGS84 for GPS
                    - GTRF for Galileo
                    - WGS84 for Glonass (PZ90 to WGS84 in pos_Glonass)
          - else : sp3 coordinate system (IGS08)
         - dte : satellite clock offset
         - debug : debug structure with all results.

         If orbit is not computed, position and dte are set to 0
        """
        
        return self._orb_sat(const, PRN, mjd, degree)

    def _orb_sat(self, const, PRN, mjd, degree=9):
        """
         Calculates ECEF GPS, Galileo and Glonass satellite coordinates and
         satellite clock error from ephemeris structure or sp3_data

         Jacques Beilin - ENSG/DPTS - 2015-05-24

         Input :
         - const : constellation id ('G' for GPS, 'R' for Glonass and 'E' for Galileo)
         - PRN : satellite id in constellation
         - mjd : modified Julian day
         - degree : degree for Lagrange interpolation (optional)

         Output
         - X, Y, Z : cartesian coordinates :
          - if navigation message used :
                    - WGS84 for GPS
                    - GTRF for Galileo
                    - WGS84 for Glonass (PZ90 to WGS84 in pos_Glonass)
          - else : sp3 coordinate system (IGS08)
         - dte : satellite clock offset
         - debug : debug structure with all results.

         If orbit is not computed, position and dte are set to 0
        """
        if self.type == "":
            return 0, 0, 0, 0

        if self.type == "sp3":
            try:
                (X, Y, Z, dte) = self.calcSatCoordSp3(const, PRN, mjd, degree)
            except:
                X, Y, Z, dte = 0, 0, 0, 0
        else:
            if const == "R":
                try:
                    (X, Y, Z, dte, debug, VX, VY, VZ) = self.calcSatCoordGlonassNav(const, PRN, mjd)
                except:
                    X, Y, Z, dte = 0, 0, 0, 0
            elif (const == "G" or const == "E"):
                try:
                    (X, Y, Z, dte) = self.calcSatCoordGPSNav(const, PRN, mjd)
                except:
                    X, Y, Z, dte = 0, 0, 0, 0

        return X, Y, Z, dte
    
    
    def calcSatCoordNav(self, const, PRN, mjd):
        """
        Orbit and satellite clock error calculation from ephemeris
        
        Jacques Beilin 2015-05-22
        
        Input :
         - const : constellation id ( 'G' for GPS and 'E' for Galileo)
         - PRN : satellite id in constellation
         - mjd : modified Julian day in GPS time scale
        
         Output :
         - X, Y, Z : satellite position in cartesian coordinates
         - WGS84 for GPS
         - GTRF for Galileo
         - dte : satellite clock error
        
        self.debug : structure containing intermediate results
        
        Returns X = 0, Y = 0, Z = 0, dte = 0 and debug = cell if Eph.const
        different from 'G' or 'E'
        """
        if const == "R":
            return self.calcSatCoordGlonassNav(const, PRN, mjd)
        elif re.search(const, "GE"):
            return self.calcSatCoordGPSNav(const, PRN, mjd)
        return np.nan, np.nan, np.nan, np.nan


    def calcSatCoordGlonassNav(self, const, PRN, mjd):
        """
        Compute position, velocity and dte of a Glonass satellite from its ephemeris at mjd

        Jacques Beilin 2015-05-28

        Input :
         - const : constellation id ('R' for Glonass)
         - PRN : satellite id in constellation
         - mjd : modified Julian day in UTC time scale

        Output
        - Xs, Ys, Zs : cartesian coordinates in WGS84
        - VXs, VYs, VZs : velocities in WGS84
        - dte : satellite clock offset

        Position, velocity and dte set to 0 if orbit is not computed
        """

        if const != 'R':
            return

        nav = self.getEphemeris(const, PRN, mjd)
        if not hasattr(nav, 'mjd'):
            return np.nan, np.nan, np.nan, np.nan

        tgps = gpst.gpsdatetime()
        tgps.mjd_t(mjd)

        OMEGAe = 7.2921151467e-5 # rad/s
        a = 6378136.0
        mu = 398600440000000.0
        C20 = -1.08263e-3

        h2r = pi/12.0 # hours to radians

        te = gpst.gpsdatetime()
        te.mjd_t(nav.mjd)

        thetaGe = te.GAST * h2r
        debug.thetaGe = thetaGe

        xa = nav.X * cos(thetaGe) - nav.Y * sin(thetaGe)
        ya = nav.X * sin(thetaGe) + nav.Y * cos(thetaGe)
        za = nav.Z

        Vxa = nav.X_dot * cos(thetaGe) - nav.Y_dot * sin(thetaGe) - OMEGAe * ya
        Vya = nav.X_dot * sin(thetaGe) + nav.Y_dot * cos(thetaGe) + OMEGAe * xa
        Vza = nav.Z_dot

        Jxa = nav.MS_X_acc * cos(thetaGe) - nav.MS_Y_acc * sin(thetaGe)
        Jya = nav.MS_X_acc * sin(thetaGe) - nav.MS_Y_acc * cos(thetaGe)
        Jza = nav.MS_Z_acc

        h = 150 # integration step

        # forward or backward integration ?
        T = (mjd - te.mjd) * 86400 # integration duration
        if T < 0:
            h = -h

        Nstep = int(T/h) + 1 # step number (+1 for last iteration)
        debug.Nstep = Nstep
        last_step_duration = (mjd-nav.mjd)*86400 - int(T/h)*h

        #    |-----------------------------|
        # nav.mjd                         mjd
        #
        #     1   2   3   ......   N-1    N
        #
        # 0 to N-1 -> 150
        # N -> last_step_duration

        Y = np.zeros(6).reshape((6, 1))
        K1 = np.zeros(6).reshape((6, 1))
        K2 = np.zeros(6).reshape((6, 1))
        K3 = np.zeros(6).reshape((6, 1))
        K4 = np.zeros(6).reshape((6, 1))

        # Conditions initiales
        Y = np.array([[xa], [ya], [za], [Vxa], [Vya], [Vza]])

        for i in range(Nstep):


            if i == Nstep-1:
                h = last_step_duration
            #print("Step : ", i, " h = ", h)

            # K1
            YK1 = Y

            r = (YK1[0]**2+YK1[1]**2+YK1[2]**2)**0.5
            mu_b = mu / r**2
            xa_b = YK1[0] / r
            ya_b = YK1[1] / r
            za_b = YK1[2] / r
            rho_b = a / r

            K1[0] = YK1[3]
            K1[1] = YK1[4]
            K1[2] = YK1[5]
            K1[3] = -mu_b * xa_b + 3/2 * C20 * mu_b * xa_b * rho_b**2 * (1 - 5 * za_b**2) + Jxa
            K1[4] = -mu_b * ya_b + 3/2 * C20 * mu_b * ya_b * rho_b**2 * (1 - 5 * za_b**2) + Jya
            K1[5] = -mu_b * za_b + 3/2 * C20 * mu_b * za_b * rho_b**2 * (3 - 5 * za_b**2) + Jza

            #print("K1 = ", K1)

            # K2
            YK2 = Y + h/2 * K1

            r = (YK2[0]**2+YK2[1]**2+YK2[2]**2)**0.5
            mu_b = mu / r**2
            xa_b = YK2[0] / r
            ya_b = YK2[1] / r
            za_b = YK2[2] / r
            rho_b = a / r

            K2[0] = YK2[3]
            K2[1] = YK2[4]
            K2[2] = YK2[5]
            K2[3] = -mu_b * xa_b + 3/2 * C20 * mu_b * xa_b * rho_b**2 * (1 - 5 * za_b**2) + Jxa
            K2[4] = -mu_b * ya_b + 3/2 * C20 * mu_b * ya_b * rho_b**2 * (1 - 5 * za_b**2) + Jya
            K2[5] = -mu_b * za_b + 3/2 * C20 * mu_b * za_b * rho_b**2 * (3 - 5 * za_b**2) + Jza

            #print("K2 = ", K2)

            # K3
            YK3 = Y + h/2 * K2

            r = (YK3[0]**2+YK3[1]**2+YK3[2]**2)**0.5
            mu_b = mu / r**2
            xa_b = YK3[0] / r
            ya_b = YK3[1] / r
            za_b = YK3[2] / r
            rho_b = a / r

            K3[0] = YK3[3]
            K3[1] = YK3[4]
            K3[2] = YK3[5]
            K3[3] = -mu_b * xa_b + 3/2 * C20 * mu_b * xa_b * rho_b**2 * (1 - 5 * za_b**2) + Jxa
            K3[4] = -mu_b * ya_b + 3/2 * C20 * mu_b * ya_b * rho_b**2 * (1 - 5 * za_b**2) + Jya
            K3[5] = -mu_b * za_b + 3/2 * C20 * mu_b * za_b * rho_b**2 * (3 - 5 * za_b**2) + Jza

            #print("K3 = ", K3)

            # K4
            YK4 = Y + h * K3

            r = (YK4[0]**2+YK4[1]**2+YK4[2]**2)**0.5
            mu_b = mu / r**2
            xa_b = YK4[0] / r
            ya_b = YK4[1] / r
            za_b = YK4[2] / r
            rho_b = a / r

            K4[0] = YK4[3]
            K4[1] = YK4[4]
            K4[2] = YK4[5]
            K4[3] = -mu_b * xa_b + 3/2 * C20 * mu_b * xa_b * rho_b**2 * (1 - 5 * za_b**2) + Jxa
            K4[4] = -mu_b * ya_b + 3/2 * C20 * mu_b * ya_b * rho_b**2 * (1 - 5 * za_b**2) + Jya
            K4[5] = -mu_b * za_b + 3/2 * C20 * mu_b * za_b * rho_b**2 * (3 - 5 * za_b**2) + Jza

            #print("K4 = ", K4)

            #  Y_{k+1} = Y_k + h/6 * (K1 + 2* K2 + 2*K3 +K4)
            Y = Y + h/6 * (K1 + 2 * K2 + 2 * K3 + K4)

            #print("Y = ", Y)


        X_ECI = Y[0]
        Y_ECI = Y[1]
        Z_ECI = Y[2]
        VX_ECI = Y[3]
        VY_ECI = Y[4]
        VZ_ECI = Y[5]

        #print(X_ECI, Y_ECI, Z_ECI)
        # Transformation to ECEF coordinates (PZ90)

        thetaGeFin = tgps.GAST * h2r
        debug.thetaGeFin = thetaGeFin

        (X_ECEF_PZ90, Y_ECEF_PZ90, Z_ECEF_PZ90) = \
        gnsstools.tool_rotZ(X_ECI, Y_ECI, Z_ECI, -thetaGeFin)
        (VX_ECEF_PZ90, VY_ECEF_PZ90, VZ_ECEF_PZ90) = \
        gnsstools.tool_rotZ(VX_ECI, VY_ECI, VZ_ECI, -thetaGeFin)

        VX_ECEF_PZ90 = VX_ECEF_PZ90 + OMEGAe * Y_ECEF_PZ90
        VY_ECEF_PZ90 = VY_ECEF_PZ90 - OMEGAe * X_ECEF_PZ90

        dte = nav.SV_clock_offset + nav.SV_relat_freq_offset * (mjd - nav.mjd) * 86400

        # Transformation to WGS84
        T = np.array([[-0.36], [0.08], [0.18]])

        X_ECEF_WGS84 = X_ECEF_PZ90 + T[0]
        Y_ECEF_WGS84 = Y_ECEF_PZ90 + T[1]
        Z_ECEF_WGS84 = Z_ECEF_PZ90 + T[2]

        VX_ECEF_WGS84 = VX_ECEF_PZ90
        VY_ECEF_WGS84 = VY_ECEF_PZ90
        VZ_ECEF_WGS84 = VZ_ECEF_PZ90

        return X_ECEF_WGS84[0], Y_ECEF_WGS84[0], Z_ECEF_WGS84[0], dte, VX_ECEF_WGS84[0], VY_ECEF_WGS84[0], VZ_ECEF_WGS84[0], debug
         

    def calcSatCoordGPSNav(self, const, PRN, mjd):
        """
        Orbit and satellite clock error calculation from ephemeris

        Jacques Beilin 2015-05-22

        Input :
         - const : constellation id ( 'G' for GPS and 'E' for Galileo)
         - PRN : satellite id in constellation
         - mjd : modified Julian day in GPS time scale

         Output :
         - X, Y, Z : satellite position in cartesian coordinates
          - WGS84 for GPS
          - GTRF for Galileo
         - dte : satellite clock error

         self.debug : structure containing intermediate results

         Returns X = 0, Y = 0, Z = 0, dte = 0 and debug = cell if Eph.const
         different from 'G' or 'E'
         """


        if (const != 'G' and const != 'E'):
            return

        nav = self.getEphemeris(const, PRN, mjd)
        if not hasattr(nav, 'mjd'):
            return np.nan, np.nan, np.nan, np.nan

        tgps = gpst.gpsdatetime()
        tgps.mjd_t(mjd)

        self.debug.dt0 = 86400 * (mjd - nav.mjd)
        dt0 = self.debug.dt0

        # Mean motion computation
        self.debug.mu = 3.986005e14
        self.debug.a = nav.sqrt_a**2
        self.debug.n0 = sqrt(self.debug.mu/self.debug.a**3)
        self.debug.n = self.debug.n0 + nav.delta_n

        # Mean anomaly computation at t
        self.debug.M = nav.M0 + self.debug.n * dt0

        # Kepler's equation for eccentric anomaly E
        Ek = self.debug.M
        for i in range(10):
            E = self.debug.M + nav.e * sin(Ek)
            if abs(E - Ek) < 1e-12:
                break
            Ek = E
        self.debug.E = E

        # True anomaly computation
        self.debug.v = 2 * atan((tan(E/2))*sqrt((1+nav.e)/(1-nav.e)))

        # Argument of latitude
        self.debug.phi = self.debug.v + nav.omega
        phi = self.debug.phi

        # Argument on latitude correction
        self.debug.dphi = nav.cus * sin(2*self.debug.phi) + nav.cuc * cos(2*self.debug.phi)
        dphi = self.debug.dphi

        #Radius correction
        self.debug.dr = nav.crs * sin(2*phi) + nav.crc * cos(2*phi)
        dr = self.debug.dr

        #Radius
        self.debug.r = self.debug.a * (1 - nav.e * cos(self.debug.E))
        r = self.debug.r

        # Position in orbital plane
        self.debug.xy = np.array([[(r + dr) * cos(phi + dphi)],\
                        [(r + dr) * sin(phi + dphi)],\
                        [0.0]])

        # Position of orbital plane in the space

        # temporal evolution af i and OMEGA
        i = nav.i0 + nav.IDOT * self.debug.dt0
        OMEGA0 = nav.OMEGA
        OMEGA = OMEGA0 + nav.OMEGA_DOT * self.debug.dt0
        debug.OMEGA = OMEGA
        debug.i = i

        # inclination correction
        debug.di = nav.cic * cos(2*phi) + nav.cis * sin(2*phi)
        i = i + debug.di

        # Keplerian elements to ECI cartesian coordinates
        (ix, iy, iz) = gnsstools.tool_rotX(self.debug.xy[0], self.debug.xy[1], self.debug.xy[2], i)
        (X_ECI, Y_ECI, Z_ECI) = gnsstools.tool_rotZ(ix, iy, iz, OMEGA)
        self.debug.X_ECI = np.array([[X_ECI], [Y_ECI], [Z_ECI]])

        # x, y in orbital plane
        # X in celestrian equatorial frame

        wsec = tgps.wsec

        # if mjd<nav.mjd and wk<nav.gps_wk wsec = - offset between mjd and Eph.mjd
        if tgps.mjd < nav.TOC and tgps.wk < nav.gps_wk:
            wsec = wsec - 604800.0

        # if week of Eph < week of tgps, add 86400*7
        if tgps.wk > nav.gps_wk:
            wsec = wsec + 604800.0

        self.debug.OMEGAe = -7.2921151467e-5 * wsec

        (X_ECEF, Y_ECEF, Z_ECEF) = gnsstools.tool_rotZ(self.debug.X_ECI[0][0], \
        self.debug.X_ECI[1][0], self.debug.X_ECI[2][0], self.debug.OMEGAe)
        self.debug.X_ECEF = np.array([[X_ECEF], [Y_ECEF], [Z_ECEF]])

        # Relativist correction computation
        F = -4.442807633E-10
        dt_relat = F * nav.sqrt_a * nav.e * sin(E)
        self.debug.dt_relat = dt_relat

        # Satellite clock error computation
        dte = nav.alpha0 + nav.alpha1 * dt0 + nav.alpha2 * dt0**2 + dt_relat
        self.debug.dte = dte

        return  X_ECEF[0], Y_ECEF[0], Z_ECEF[0], dte

    def calcSatCoordSp3(self, constellation, PRN, mjd, degree=9):
        """
        Position and satellite clock error interpolation with a Lagrange polynomial

        Jacques Beilin - ENSG/DPTS - 2014-05-19

        Input :
        - sp3_data : structure created with function loadSp3.m
        - mjd : Modified Julian Date of interpolation time
        - constellation : 'G' for GPS, 'R' for Glonass and 'E' for Galileo
        - PRN : satellite id
        - degree : Lagrange polynomial degree

        Output :
        - X, Y, Z : position at the given mjd (m)
        - dte : dte at the given mjd (s)

        Position and dte are set to 0 if orbit is not computed

        extrapolation : allowed = 1, forbidden = 0
        WARNING : extrapolation with Lagrange polynomial is not recommended
        """

        # extrapolation : allowed = 1, forbidden = 0
        # WARNING : extrapolation with Lagrange polynomial is not recommended
        extrapolate = 0

        X = np.nan
        Y = np.nan
        Z = np.nan
        dte = np.nan

        verbose = self.verbose

        m2 = (degree + 1) / 2

        if re.search('G', constellation):
            nl = len(self.sp3G[PRN-1])
        elif re.search('R', constellation):
            nl = len(self.sp3R[PRN-1])
        elif re.search('E', constellation):
            nl = len(self.sp3E[PRN-1])
        # check if enougth epochs are available to interpolate a position with a Lagrange polynom
        if degree > nl:
            if verbose:
                print('Satellite %s%02d : not enough epochs to interpolate a position : coordinates and dte set to 0' % (constellation, PRN))
            return X, Y, Z, dte

        (orb, nl) = self.getSp3(constellation, PRN)

        # check presence of mjd into data period
        if extrapolate == 0:
            if (mjd < orb[0, 0] - 1/86400):
                if verbose:
                    print('Satellite %s%02d : mjd is before first epoch of sp3 file (%.8f < %.8f) : coordinates and dte set to 0' % (constellation, PRN, mjd, orb[0, 1]))
                return  X, Y, Z, dte
            if (mjd > orb[int(nl-1), 0]):
                if verbose:
                    print('Satellite %s%02d : mjd is after last epoch of sp3 file (%.8f > %.8f) : coordinates and dte set to 0' % (constellation, PRN, mjd, orb[int(nl-1), 1]))
                return  X, Y, Z, dte

        # seek epoch just before mjd
        try:
            Vpos = np.nonzero(orb[:, 0] > mjd)
            pos = Vpos[0][0]-1
        except:
            return X, Y, Z, dte

        # side effects
        if pos < m2: # near file beginning
            first_index = 0
        elif pos < nl - m2: # normal case : (m + 1)/2 values around mjd
            first_index = pos - m2 + 1
        else:  # near file end
            first_index = nl - degree -1

        last_index = int(first_index + degree)

        # load temporary matrix
        A = orb[int(first_index):int(last_index+1), :]

        # interpolation and output
        (Xs, Ys, Zs, clock) = self._inter_Lagrange(A, mjd)

        X = 1.0e3*Xs
        Y = 1.0e3*Ys
        Z = 1.0e3*Zs
        dte = clock * 1.0e-6

        return X, Y, Z, dte

    def _inter_Lagrange(self, sp3_extract, mjd):
        """ Lagrange interpolation in a matrix of positions and satellite clock errors

            Jacques Beilin - ENSG/DPTS - 2014-05-19

            Input :
                - sp3_extract : matrix extracted from sp3.G/R/E for one satellite (lines : epochs (degree + 1 values), columns : mjd X Y Z clk_error)
                - mjd         : Modified Julian Date of interpolation time

            Output :
                - Xs, Ys, Zs, clock : satellite position and clock error """

        # détermination du degre en fonction de la taille de la matrice fournie

        nl = sp3_extract.shape[0]
        degree = nl-1
        Xs = 0.0
        Ys = 0.0
        Zs = 0.0
        clock = 0.0

        Lj = np.ones(degree)
        for j in range(0, degree):
            for k in range(0, degree):
                if k != j:
                    Lj[j] = Lj[j] * (mjd - sp3_extract[k, 0]) / (sp3_extract[j, 0] - sp3_extract[k, 0])

            Xs = Xs + Lj[j] * sp3_extract[j, 1]
            Ys = Ys + Lj[j] * sp3_extract[j, 2]
            Zs = Zs + Lj[j] * sp3_extract[j, 3]
            clock = clock + Lj[j] * sp3_extract[j, 4]


        return Xs, Ys, Zs, clock
    

    def calcDte(self, const, PRN, mjd):
        """
        Satellite clock error calculation from navigation message.

        Jacques Beilin 2017-12-24

        Input :
         - const : constellation id ( 'G' for GPS and 'E' for Galileo)
         - PRN : satellite id in constellation
         - mjd : modified Julian day in GPS time scale

         Output :
         - dte : satellite clock error

         Usage :
         dte = mybrdc._calc_dte(const, PRN, mjd)

        """
        
        dte = 0.0

        if self.type == 'sp3':
            return

        elif self.type == 'nav':

            nav = self.getEphemeris(const, PRN, mjd)
            if not hasattr(nav, 'mjd'):
                return

            if const == 'G' or const == 'E':
                self.debug.dt0 = 86400 * (mjd - nav.mjd)
                dt0 = self.debug.dt0

                dt_relat = self.calcDtrelatNav(const, PRN, mjd)

                """ Satellite clock error computation """
                dte = nav.alpha0 + nav.alpha1 * dt0 + nav.alpha2 * dt0**2 + dt_relat

            elif const == 'R':
                dte = nav.SV_clock_offset + nav.SV_relat_freq_offset * (mjd - nav.mjd) * 86400

        return dte

    def calcDtrelatNav(self, const, PRN, mjd):
        """
        Relativistic correction calculation from navigation message.

        Jacques Beilin 2017-12-24

        Input :
         - const : constellation id ( 'G' for GPS and 'E' for Galileo)
         - PRN : satellite id in constellation
         - mjd : modified Julian day in GPS time scale

         Output :
         - dt_relat : relativistic correction (s)
             if no dt_relat computed, 0 is returned

         Usage :
         dt_relat = mybrdc.calcDtrelatNav(const, PRN, mjd)

         """
        if const == 'G' or const == 'E':

            nav = self.getEphemeris(const, PRN, mjd)
            if not hasattr(nav, 'mjd'):
                return

            tgps = gpst.gpsdatetime()
            tgps.mjd_t(mjd)

            dt0 = 86400 * (mjd - nav.mjd)

            # Mean motion computation
            mu = 3.986005e14
            a = nav.sqrt_a**2
            n0 = sqrt(mu/a**3)
            n = n0 + nav.delta_n

            # Mean anomaly computation at t
            M = nav.M0 + n * dt0

            # Kepler's equation for eccentric anomaly E
            Ek = M
            for i in range(10):
                E = M + nav.e * sin(Ek)
                if abs(E - Ek) < 1e-12:
                    break
                Ek = E

            F = -4.442807633e-10
            dt_relat = F * nav.e * sqrt(a) * sin(Ek)

        elif const == 'R':

            # dt_relat = -2 r.v/c^2
            c = 299792458.0
            [Xs, Ys, Zs, dte, VXs, VYs, VZs, debug] = self.calcSatCoordGlonassNav(const, PRN, mjd)
            dt_relat = -2*(Xs*VXs+Ys*VYs+Zs*VZs)/(c*c)
            dt_relat = dt_relat.squeeze()

        return dt_relat

