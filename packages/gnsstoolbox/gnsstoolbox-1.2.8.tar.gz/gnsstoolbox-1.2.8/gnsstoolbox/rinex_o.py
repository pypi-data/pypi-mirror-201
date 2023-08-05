#!/usr/bin/python
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
from math import ceil, nan
import copy
import os.path

import gpsdatetime as gpst
import gnsstoolbox.gnss_const as const

class rinex_o():
    """RINEX observation class"""

    # delta_t (s) to find an epoch by typestamp
    _deltat = 0.001
    _listConst = ["G", "R", "E", "C", "J", "I", "S"]

    def __init__(self, filename="", onlyMetadata=False):
        self.type = "o"
        self.headers = []
        self.verbose = 0
        self.currentline = 0
        
#        if onlyMetadata:
#            try:
#                self.readMetadata(filename)
#            except Exception as e:
#                print("Unable to load %s\n" % (filename), e)
#        else:
#            try:
#                self.loadRinexO(filename)
#            except Exception as e:
#                print("Unable to load %s\n" % (filename), e)
                
        self.loadRinexO(filename)

    def getCommonEpochs(self, rinex_o_2, mjd, delta=1e-3):
        """
        Get common epochs between 2 receivers at same mjd
        Jacques Beilin - ENSG/DPTS - 2017-01-10

        Input :
        - rinex_o_2 : Second rinex_o object
        - mjd : modified julian date
        - delta : max delta if mjd is not exactly found
                  (optional, if not defined = 1e-3 seconds)

        Output :
        - epoch, epoch2 : epochs from rinex_o and rinex_o_2 objects

        """

        epoch = self.getEpochByMjd(mjd, delta)
        epoch2 = rinex_o_2.getEpochByMjd(mjd, delta)

        return epoch, epoch2

    def getEpochByMjd(self, mjd, *args, **kwargs):
        """
        Get epoch number from mjd
        Jacques Beilin - ENSG/DPTS - 2014-05-20

        Input :
        - mjd : modified julian date
        - delta : max delta if mjd is not exactly found
                  (optional, if not defined = 1e-3 seconds)

        Output :
        - epoch : epoch number corresponding to mjd

        """

        if len(self.headers) == 0:
            return

        _delta = rinex_o._deltat
        for ar in args:
            _delta = ar

        _delta = kwargs.get('delta', _delta)

        for h in range(len(self.headers)):
            for e in range(len(self.headers[h].epochs)):
                if abs((mjd-self.headers[h].epochs[e].tgps.mjd)*86400) < _delta:
                    return self.headers[h].epochs[e]


    def getHeaderByMjd(self, mjd, *args, **kwargs):
        """
        Get header object from mjd
        Jacques Beilin - ENSG/DPTS - 2017-01-10

        Input :
        - mjd : modified julian date
        - delta : max delta if mjd is not exactly found
                  (optional, if not defined = 1e-3 seconds)

        Output :
        - header : header corresponding to mjd
        """

#        return self._get_header_by_mjd(mjd, *args, **kwargs)
#
#    def _get_header_by_mjd(self, mjd, *args, **kwargs):
#        """
#        Get header object from mjd
#        Jacques Beilin - ENSG/DPTS - 2017-01-10
#
#        Input :
#        - mjd : modified julian date
#        - delta : max delta if mjd is not exactly found
#                  (optional, if not defined = 1e-3 seconds)
#
#        Output :s
#        - header : header corresponding to mjd
#        """

        if len(self.headers) == 0:
            return

        _delta = rinex_o._deltat
        for ar in args:
            _delta = ar

        _delta = kwargs.get('delta', _delta)

        for h in range(len(self.headers)):
            for e in range(len(self.headers[h].epochs)):
                if abs((mjd-self.headers[h].epochs[e].tgps.mjd)*86400) < _delta:
                    return self.headers[h]

    def readMetadata(self):
        """
        Jacques Beilin - ENSG - 2021-06-18

        read rinex metadata without reading observations
        RINEX prereqisites :
            - RINEX v2.__ (20150607)
            - GPS, GLONASS and Galileo. Other systems will be ignored.
            - only epoch with code = 0 or 1 will be loaded. Other epochs will be ignored.

        Input
            - filename : RINEX file name
        """        
        if filename == "":
            return -1

        verbose = self.verbose

        if not os.path.isfile(filename):
            print('Unable to find %s' % (filename))
            return -2

        # loading strings
        try:
            with open(filename, encoding='utf-8', errors='replace') as F:
                self.rinexolines = F.readlines()
#                F.close()
        except:
            print('Unable to open %s' % (filename))
            return -3

        print("Loading RINEX file %s" % filename)

        # Format checking
        if not re.search("RINEX VERSION / TYPE", self.rinexolines[0]):
            print("file %s : Format not valid !" % (filename))
            return -4

        # RINEX version number and type
        if re.search("RINEX VERSION / TYPE", self.rinexolines[0]):
            rnx_version = float(self.rinexolines[0][0:9])
            rnx_type = self.rinexolines[0][40]

        if not re.search("[GREM]", rnx_type):
            print("file %s : not a valid rinex observation file !" % (filename))

        if rnx_version <= 2.12:
#            print('Rinex version 2 (%.2f)' % (rnx_version))
            self._readMetadata_2()

        elif rnx_version >= 3.0:
#            print('Rinex version 3 (%.2f)' % (rnx_version))
            self._readMetadata_3()

        return 0
    
    def _readMetadata_2(self):
        print('Read metadata not implemented')
        return 0
    
    def _readMetadata_3(self):
        print('Read metadata not implemented')
        return 0

    def loadRinexO(self, filename="", verbose=0):
        """GPS/Glonass/Galileo observation RINEX loading
        Jacques Beilin - ENSG/DPTS - 2017-01-10

        RINEX prereqisites :
            - RINEX v2.__ (20150607)
            - GPS, GLONASS and Galileo. Other systems will be ignored.
            - only epoch with code = 0 or 1 will be loaded. Other epochs will be ignored.

        Input
            - filename : RINEX file name
            - (epoch_max) : OPTIONAL, number epoch to be loaded"""

        if filename == "":
            return -1

        if not os.path.isfile(filename):
            print('Unable to find %s' % (filename))
            return -2

        # loading strings
        try:
            with open(filename, encoding='utf-8', errors='replace') as F:
                self.rinexolines = F.readlines()
#                F.close()
        except:
            print('Unable to open %s' % (filename))
            return -3

        print("Loading RINEX file %s" % filename)

        # Format checking
        if not re.search("RINEX VERSION / TYPE", self.rinexolines[0]):
            print("file %s : Format not valid !" % (filename))
            return -4

        # RINEX version number and type
        if re.search("RINEX VERSION / TYPE", self.rinexolines[0]):
            rnx_version = float(self.rinexolines[0][0:9])
            rnx_type = self.rinexolines[0][40]

        if not re.search("[GREM]", rnx_type):
            print("file %s : not a valid rinex observation file !" % (filename))

        if rnx_version <= 2.12:
#            print('Rinex version 2 (%.2f)' % (rnx_version))
            self._loadRinexO_2(verbose)

        elif rnx_version >= 3.0:
#            print('Rinex version 3 (%.2f)' % (rnx_version))
            self._loadRinexO_3(verbose)

        return 0


    def _loadRinexO_3(self, verbose=False):
        """GPS/Glonass/Galileo observation RINEX loading
        Jacques Beilin - ENSG/DPTS - 2021-09-03

        RINEX prereqisites :
            - RINEX v3.__
            - GPS, GLONASS and Galileo and...

        Input
            - filename : RINEX file name
            - (epoch_max) : OPTIONAL, number epoch to be loaded"""
        def cutDataLine(s, observables):
            n = len(observables)
            tabline = []
            for i in range(n):
                try:
                    strdata = s[i*16:i*16+14]
                    tabline.append(float(strdata)) 
                except:
#                except Exception as e:
#                    print(s[i*16:i*16+14], e)
                    tabline.append(nan) 
                    
            dictObs = {}
            for key,value in zip(observables,tabline):
                dictObs[key] = value
                    
            return dictObs
 
        verbose = self.verbose
    
        # reading first header
        self.headers.append(header())
        self.currentline = self.headers[0]._read_header_3(self.rinexolines)
        
        while 1:
            
            if self.currentline >= len(self.rinexolines):
                break

            line = self.rinexolines[self.currentline]
            if line[0] == ">":
                
                str_datetime = line[1:28]
                epoch_flag = int(line[31])
                try:
                    sat_number = int(line[32:35])
                except:
                    sat_number = 0
                try:
                    clock_offset = float(line[41:57])
                except:
                    clock_offset = 0.0
                              
#                print(str_datetime, epoch_flag, sat_number)
                
                if epoch_flag <= 1:
                    if verbose > 0:
                        print("reading next epoch (current line : %d)" % (self.currentline))

                    self.headers[-1].epochs.append(epoch(str_datetime)) 
                    self.headers[-1].epochs[-1].clock_offset = clock_offset

                    for nsat in range(sat_number):
                        self.currentline += 1
                        line = self.rinexolines[self.currentline]
                        const = line[0]
                        dataline = line[3:]
                        dictObs = cutDataLine(dataline, self.headers[-1].TYPE_OF_OBSERV[const])
                        
                        S = sat()
                        S.const = const
                        S.PRN = int(line[1:3])
                        S.obs = dictObs
                        
                        self.headers[-1].epochs[-1].satellites.append(S)
                        
                elif epoch_flag in [2]:
                    print('Skipping epoch (flag = 2)')
                        
                elif epoch_flag in [3]:
                    print('Skipping epoch (flag = 3)')
                    self.currentline += sat_number   
                    
                elif epoch_flag in [4]:
                    print('Skipping epoch (flag = 4)')
                    self.currentline += sat_number 
                    
                elif epoch_flag in [5]:
                    print('Skipping epoch (flag = 5)')
                    self.currentline += sat_number 
                    
                elif epoch_flag in [6]:
                    print('Skipping epoch (flag = 6)')
                    self.currentline += sat_number 
                        
                self.currentline += 1
                
            else:
                print('Error on line %d' % self.currentline)
                self.currentline += 1
                
                          
            if self.currentline >= len(self.rinexolines):
                break
            
        self.headers[-1].TIME_OF_LAST_OBS = self.headers[-1].epochs[-1].tgps
        
        interval = int((self.headers[-1].TIME_OF_LAST_OBS - self.headers[-1].TIME_OF_FIRST_OBS) / (len(self.headers[-1].epochs) - 1))
        self.headers[-1].INTERVAL = interval

        return
    

    def _loadRinexO_2(self, verbose=False):
        """GPS/Glonass/Galileo observation RINEX loading
        Jacques Beilin - ENSG/DPTS - 2014-05-20

        RINEX prereqisites :
            - RINEX v2.__

        Input
            - filename : RINEX file name
            - (epoch_max) : OPTIONAL, number epoch to be loaded"""

        # verbose = self.verbose
        
        # reading first header
        self.headers.append(header())
        self.currentline = self.headers[0]._read_header_2(self.rinexolines)

        PreviousEpochFlag = -1
        while 1:

            if self.currentline >= len(self.rinexolines):
                break

            line = self.rinexolines[self.currentline]
            str_datetime = line[0:28]
            epoch_flag = int(line[28])

            if epoch_flag <= 1:
                if verbose > 0:
                    print("reading next epoch (current line : %d)" % (self.currentline))

                self.headers[-1].epochs.append(epoch(str_datetime))

                _NbSat = int(line[29:32])
                _NbLinesHeader = int(ceil(float(_NbSat)/12.0))
                _NbLinesData = _NbSat * self.headers[-1]._NumLinePerEpoch
                _NbLines = _NbLinesHeader + _NbLinesData

                if verbose > 0:
                    print('Currentline : %d\nNbSat : %d\n_NumLinePerEpoch : %d\nNbLinesHeader : %d\nNbLinesData : %d\nNbLines : %d\n' %(self.currentline, _NbSat, self.headers[-1]._NumLinePerEpoch, _NbLinesHeader, _NbLinesData, _NbLines))

                EpochLines = list(self.rinexolines[self.currentline:self.currentline+_NbLines])
                NewLines = self.headers[-1].epochs[-1]._read_epoch_2(EpochLines, \
                                       _NbSat, _NbLinesHeader, _NbLinesData, \
                                       self.headers[-1].TYPE_OF_OBSERV)

                if NewLines:
                    self.currentline += NewLines
                else:
                    print("Error : unexpected end of file")
                    return
                PreviousEpochFlag = epoch_flag
            elif epoch_flag == 2:
                if verbose > 0:
                    print("start of kinematic data (current line index : %d)" % (self.currentline))
                PreviousEpochFlag = epoch_flag
                self.currentline += 1
                line = self.rinexolines[self.currentline]
                # print(">%s<" % line)
                # print(">%s<" % line[29:33])
                NLineHeader = int(line[29:32].rstrip())
                self.currentline += NLineHeader + 1

            elif epoch_flag == 3:
                if verbose > 0:
                    print("new occupation (current line index : %d)" % (self.currentline))
                NLineHeader = int(line[29:32])
                self.headers.append(header())
                # Copie des champs du header précédent
                self.headers[-1].VERSION = copy.copy(self.headers[-2].VERSION)
                self.headers[-1].TYPE = copy.copy(self.headers[-2].TYPE)
                self.headers[-1].PGM = copy.copy(self.headers[-2].PGM)
                self.headers[-1].RUN_BY = copy.copy(self.headers[-2].RUN_BY)
                self.headers[-1].DATE = copy.copy(self.headers[-2].DATE)
                self.headers[-1].OBSERVER = copy.copy(self.headers[-2].OBSERVER)
                self.headers[-1].AGENCY = copy.copy(self.headers[-2].AGENCY)
                self.headers[-1].REC_N = copy.copy(self.headers[-2].REC_N)
                self.headers[-1].REC_TYPE = copy.copy(self.headers[-2].REC_TYPE)
                self.headers[-1].REC_VERS = copy.copy(self.headers[-2].REC_VERS)
                self.headers[-1].ANT_N = copy.copy(self.headers[-2].ANT_N)
                self.headers[-1].ANT_TYPE = copy.copy(self.headers[-2].ANT_TYPE)
                self.headers[-1].X = copy.copy(self.headers[-2].X)
                self.headers[-1].Y = copy.copy(self.headers[-2].Y)
                self.headers[-1].Z = copy.copy(self.headers[-2].Z)
                self.headers[-1].dE = copy.copy(self.headers[-2].dE)
                self.headers[-1].dN = copy.copy(self.headers[-2].dN)
                self.headers[-1].dH = copy.copy(self.headers[-2].dH)
                self.headers[-1].WAVELENGTH_FACT_L1 = copy.copy(self.headers[-2].WAVELENGTH_FACT_L1)
                self.headers[-1].WAVELENGTH_FACT_L2 = copy.copy(self.headers[-2].WAVELENGTH_FACT_L2)
                self.headers[-1].INTERVAL = copy.copy(self.headers[-2].INTERVAL)
                self.headers[-1].TYPE_OF_OBSERV = copy.copy(self.headers[-2].TYPE_OF_OBSERV)


                self.headers[-1]._read_header_2(self.rinexolines, self.currentline, NLineHeader+1)
                for key in self.headers[-1].TYPE_OF_OBSERV:
                    nbObservables = len(self.headers[-1].TYPE_OF_OBSERV[key])
                    break
                self.headers[-1]._NumLinePerEpoch = int(ceil(nbObservables/5.0))
                self.headers[-1].EPOCH_FLAG = 3
                self.currentline += NLineHeader+1
                PreviousEpochFlag = epoch_flag
            elif epoch_flag == 4:
                if verbose > 0:
                    print("header information follows (line %d)" % (self.currentline))
                NLineHeader = int(line[29:32])
                self.headers.append(header())

                # Copie des champs du header précédent
                self.headers[-1].VERSION = copy.copy(self.headers[-2].VERSION)
                self.headers[-1].TYPE = copy.copy(self.headers[-2].TYPE)
                self.headers[-1].PGM = copy.copy(self.headers[-2].PGM)
                self.headers[-1].RUN_BY = copy.copy(self.headers[-2].RUN_BY)
                self.headers[-1].DATE = copy.copy(self.headers[-2].DATE)
                self.headers[-1].OBSERVER = copy.copy(self.headers[-2].OBSERVER)
                self.headers[-1].AGENCY = copy.copy(self.headers[-2].AGENCY)
                self.headers[-1].REC_N = copy.copy(self.headers[-2].REC_N)
                self.headers[-1].REC_TYPE = copy.copy(self.headers[-2].REC_TYPE)
                self.headers[-1].REC_VERS = copy.copy(self.headers[-2].REC_VERS)
                self.headers[-1].ANT_N = copy.copy(self.headers[-2].ANT_N)
                self.headers[-1].ANT_TYPE = copy.copy(self.headers[-2].ANT_TYPE)
                self.headers[-1].X = copy.copy(self.headers[-2].X)
                self.headers[-1].Y = copy.copy(self.headers[-2].Y)
                self.headers[-1].Z = copy.copy(self.headers[-2].Z)
                self.headers[-1].dE = copy.copy(self.headers[-2].dE)
                self.headers[-1].dN = copy.copy(self.headers[-2].dN)
                self.headers[-1].dH = copy.copy(self.headers[-2].dH)
                self.headers[-1].WAVELENGTH_FACT_L1 = copy.copy(self.headers[-2].WAVELENGTH_FACT_L1)
                self.headers[-1].WAVELENGTH_FACT_L2 = copy.copy(self.headers[-2].WAVELENGTH_FACT_L2)
                self.headers[-1].INTERVAL = copy.copy(self.headers[-2].INTERVAL)
                self.headers[-1].TYPE_OF_OBSERV = copy.copy(self.headers[-2].TYPE_OF_OBSERV)
                
#                self.headers[-1]._NumLinePerEpoch = copy.copy(self.headers[-2]._NumLinePerEpoch)
                self.headers[-1]._read_header_2(self.rinexolines, self.currentline, NLineHeader+1)
                for key in self.headers[-1].TYPE_OF_OBSERV:
                    nbObservables = len(self.headers[-1].TYPE_OF_OBSERV[key])
                    break
                self.headers[-1]._NumLinePerEpoch = int(ceil(nbObservables / 5.0))
                self.headers[-1].EPOCH_FLAG = PreviousEpochFlag
                self.currentline += NLineHeader + 1
                PreviousEpochFlag = epoch_flag

            elif epoch_flag == 5:
                if verbose > 0:
                    print("external event")
                NLineToBeSkipped = int(line[29:32])
                self.currentline += NLineToBeSkipped +1
            elif epoch_flag == 6:
                if verbose > 0:
                    print("cycle slip")

        """
        Affectation des dates de début et fin aux headers
        """
        for H in self.headers:
            try:
                H.TIME_OF_FIRST_OBS = copy.copy(H.epochs[0].tgps)
                H.TIME_OF_LAST_OBS = copy.copy(H.epochs[-1].tgps)
            except:
                H.TIME_OF_FIRST_OBS.ymdhms_t(1980, 1, 6, 0, 0, 0)
                H.TIME_OF_LAST_OBS.ymdhms_t(1980, 1, 6, 0, 0, 0)

        """
        Nettoyage des headers sans observations.
        """
        for i in range(len(self.headers)-1, -1, -1):
            if len(self.headers[i].epochs) == 0:
                self.headers.__delitem__(i)

        """
        suppression des constellation non presentes dans headers.TYPE_OF_OBSERV
        """     
        for H in self.headers:
            listConst = []
            for E in H.epochs:
                for S in E.satellites:
                    if not S.const in listConst:
                        listConst.append(S.const)
            listConsttobedeleted = []
            for key in H.TYPE_OF_OBSERV:
                if not key in listConst:
                    listConsttobedeleted.append(key)  
            [H.TYPE_OF_OBSERV.pop(key) for key in listConsttobedeleted]
        
        """
        Recherche des differentes frequences disponibles
        """
        for i in range(len(self.headers)):
            """
            L1:1, L2:2, L5:4... to be continued
            """
            self.headers[i].listFreq = []
            for j in range(len(self.headers[i].TYPE_OF_OBSERV)):
                try:
                    nfreq = int(self.headers[i].TYPE_OF_OBSERV[j][1])
                except Exception as e:
                    nfreq = 0
                if nfreq not in self.headers[i].listFreq:
                    self.headers[i].listFreq.append(nfreq)
            self.headers[i].typeFreq = sum(self.headers[i].listFreq)
            
        self.headers[-1].TIME_OF_LAST_OBS = self.headers[-1].epochs[-1].tgps
        
        interval = int((self.headers[-1].TIME_OF_LAST_OBS - self.headers[-1].TIME_OF_FIRST_OBS) / (len(self.headers[-1].epochs) - 1))
        self.headers[-1].INTERVAL = interval
        
        
    def writeRinex2(self, filename, parameters={"OBSERVABLES":['C1', 'P2', 'L1', 'L2'], "CONST":'GRE'}):
        """
        write Rinex2 file
        Jacques Beilin - ENSG/DPTS - 2020-03-03

        Input :
            - filename
            - parameters : dictionnary

        Output :

        """        
        observables = parameters["OBSERVABLES"]
        s = self.headers[0].writeFirstRinexHeader2(observables)
        
        for header in self.headers:
            for epoch in header.epochs:
                s += epoch.writeRinex2Epoch(parameters)
                
        try:
            with open(filename, "w") as f:
                f.write(s)
        except:
            print("Error : unable to write %s" % filename)
                
    def copyObservable(self, observable1, observable2):
        """
        fill observable2 with observabl1 value
        Jacques Beilin - ENSG/DPTS - 2020-03-03

        Input :
            - observable1 : source observable
            - observable2 : destination observable
        Output :

        """
        for header in self.headers:
            for epoch in header.epochs:
                epoch.copyObservable(observable1, observable2)
        
    
    def fillP2withC2(self):
        """
        fill P2 observable with C2 (L2C) value for GPS data
        Jacques Beilin - ENSG/DPTS - 2020-03-03

        Input :

        Output :

        """
        self.copyObservable("C2", "P2")          
       

    def formatMeasures(self, doppler=False):
        """GPS/Glonass/Galileo observation RINEX Measures format
        M BARBIER - J ORTET - E VIEGAS - ENSG - 2017-07
        """

        rep = []

        # Recherche des objets satellites pour chaque époque
        for ep in self.headers[-1].epochs:
            lst = ep.satellites
            rep.append("{0}{1}{2}{3}".format(ubx.formatdate03(ep.tgps), "%3d" %(0),\
                       "%3d" %(len(lst)), ubx.listSat(lst)))

            # Formatage des données de chaque satellite
            for satl in lst:
                obs = satl.obs
                rep.append("%14.3f  %14.3f  %14.3f  %14.3f  " %(obs["C1"], obs["L1"], obs["D1"], obs["S1"]))

        return rep



class header():
    """Rinex header class"""
    
    _listConst = ["G", "R", "E", "C", "J", "I", "S"]
    
    def __init__(self):
        self.VERSION = 0
        self.EPOCH_FLAG = -1 # permet de différencier les headers correspondants à des observations statiques de ceux correspondant à du cinematique
        self.TYPE = ''
        self.PGM = ''
        self.RUN_BY = ''
        self.DATE = ''
        self.OBSERVER = ''
        self.AGENCY = ''
        self.MARKER_NAME = 'UNKN'
        self.MARKER_NUMBER = ''
        self.REC_N = ''
        self.REC_TYPE = ''
        self.REC_VERS = ''
        self.ANT_N = ''
        self.ANT_TYPE = ''
        self.X = 0.0
        self.Y = 0.0
        self.Z = 0.0
        self.dH = 0.0
        self.dE = 0.0
        self.dN = 0.0
        self.WAVELENGTH_FACTOR = 1.0
        self.WAVELENGTH_FACT_L1 = 1.0
        self.WAVELENGTH_FACT_L2 = 1.0
        
        """
        Rinex observable list
        Major change after release 1.1.1 : change from list to dict to manage Rinex3 
        self.TYPE_OF_OBSERV = {"G" : ['C1C', 'L1C', 'D1C', 'S1C', 'C1W', 'S1W', 'C2W', 'L2W', 'D2W', 'S2W', 'C2L', 'L2L', 'D2L', 'C5Q', 'L5Q', 'D5Q', 'S5Q'],
                               "R" : ['C1C', 'L1C', 'D1C', 'S1C', 'C1P', 'L1P', 'D1P', 'S1P', 'C2P', 'L2P', 'D2P', 'S2P', 'C2C', 'D2C', 'S2C', 'C3Q', 'L3Q', 'D3Q', 'S3Q'],
                               etc...
                               }
        """
        self.TYPE_OF_OBSERV = {}
       
        self.INTERVAL = 0.0
        self.TIME_OF_FIRST_OBS = gpst.gpsdatetime()
        self.TIME_OF_FIRST_OBS.ymdhms_t(1980, 1, 6, 0, 0, 0)
        self.TIME_OF_LAST_OBS = gpst.gpsdatetime()
        self.TIME_OF_LAST_OBS.ymdhms_t(1980, 1, 6, 0, 0, 0)
        """ L1:1, L2:2, L5:4... to be continued """
        self.typeFreq = 0

        self.epochs = []

    def getCommonEpochs(self, rinex_o_2, Nepoch, delta=1e-3):
        """
        Get common epochs between 2 receivers at same mjd
        Jacques Beilin - ENSG/DPTS - 2017-01-10

        Input :
        - rinex_o_2 : Second rinex_o object
        - mjd : modified julian date
        - delta : max delta if mjd is not exactly found
                  (optional, if not defined = 1e-3 seconds)

        Output :
        - epoch, epoch2 : epochs from rinex_o and rinex_o_2 objects

        """
        try:
            epoch = self.epochs[Nepoch]
            if epoch == None:
                return None, None

            t = epoch.tgps
            epoch2 = rinex_o_2.getEpochByMjd(t.mjd, delta)
            return epoch, epoch2
        except:
            return None, None

    def _read_header_3(self, rinexolines, numline=0, maxline=1e7):
        """"""

        end = min(int(numline+maxline), len(rinexolines))
#        print(end)
        
        linesTypeObs = []

        for i in range(numline, end):
            line = rinexolines[i]
#            print(line)

            # RINEX version number and type
            if re.search("RINEX VERSION / TYPE", line[60:]):
                self.VERSION = float(line[0:9])
                self.TYPE = line[40]
                continue

            if re.search("PGM / RUN Boptions[num]()Y / DATE", line[60:]):
                self.PGM = line[0:20].strip()
                self.RUN_BY = line[20:40].strip()
                self.DATE = line[40:60].strip()
                continue

            if re.search('OBSERVER / AGENCY', line[60:]):
                self.OBSERVER = line[0:20].strip()
                self.AGENCY = line[20:60]
                continue

            # Station name
            if re.search('MARKER NAME', line[60:]):
                self.MARKER_NAME = line[0:60].strip()
                continue

            # Station number
            if re.search('MARKER NUMBER', line[60:]):
                self.MARKER_NUMBER = line[0:20].strip()
                continue

            # Receiver number and type
            if re.search('REC # / TYPE / VERS', line[60:]):
                self.REC_N = line[0:20].strip()
                self.REC_TYPE = line[20:40].strip()
                self.REC_VERS = line[40:60].strip()
                continue

            # Antenna typea
            if re.search('ANT # / TYPE', line[60:]):
                self.ANT_N = line[0:20].strip()
                self.ANT_TYPE = line[20:40].strip()
                continue

            # Approximated position
            if re.search('APPROX POSITION XYZ', line[60:]):
                val = line[0:60].split()
                if len(val) > 0:
                    try:
                        self.X = float(val[0])
                    except:
                        self.X = 0
                if len(val) > 1:
                    try:
                        self.Y = float(val[1])
                    except:
                        self.Y = 0
                if len(val) > 2:
                    try:
                        self.Z = float(val[2])
                    except:
                        self.Z = 0
                continue

            # offsets
            if re.search('ANTENNA: DELTA H/E/N', line[60:]):
                val = line[0:60].split()
                if len(val) > 0:
                    try:
                        self.dH = float(val[0])
                    except:
                        self.dH = 0
                if len(val) > 1:
                    try:
                        self.dE = float(val[1])
                    except:
                        self.dE = 0
                if len(val) > 2:
                    try:
                        self.dN = float(val[2])
                    except:
                        self.dN = 0
                continue

            # Antenna type
            if re.search('WAVELENGTH FACT L1/2', line[60:]):
                self.WAVELENGTH_FACT_L1 = float(line[0:6])
                self.WAVELENGTH_FACT_L2 = float(line[6:12])
                continue

            # Interval
            if re.search('INTERVAL', line[60:]):
                try:
                    self.INTERVAL = float(line[0:10])
                except:
                    self.INTERVAL = 0
                    """ todo : calculer l'interval a partuir des données """
                continue

            # Time of first observation
            if re.search('TIME OF FIRST OBS', line[60:]):
                self.TIME_OF_FIRST_OBS.rinex_t(line[0:44])
                continue

            # Time of last observation
            if re.search('TIME OF LAST OBS', line[60:]):
                self.TIME_OF_LAST_OBS.rinex_t(line[0:44])
                continue

            # type of observations
            if re.search('SYS / # / OBS TYPES', line[60:]):
                linesTypeObs.append(line[:60])
                continue

            if re.search('END OF HEADER', line[60:]):
                linesTypeObs2 = []
                for lineTypeObs in linesTypeObs:
                    if not lineTypeObs[0] == " ":
                        linesTypeObs2.append(lineTypeObs)
                    else:
                        linesTypeObs2[-1] = linesTypeObs2[-1][:-1]
                        linesTypeObs2[-1] += lineTypeObs[11:]
                        
                for lineTypeObs in linesTypeObs2:
                    const = lineTypeObs[0]
                    self.TYPE_OF_OBSERV[const] = lineTypeObs[7:].split()     
                    
                """
                A priori inutile en rinex3 mais conserve pour la compatibilite rinex2
                """
                for key in self.TYPE_OF_OBSERV:
                    NbObservable = len(self.TYPE_OF_OBSERV[key])
                    break
                self._NumLinePerEpoch = int(ceil(NbObservable/5.0))
                
                return i+1

        return i+1


    def _read_header_2(self, rinexolines, numline=0, maxline=1e7):
        """"""

        end = min(int(numline+maxline), len(rinexolines))
#        print(end)
        
        TYPE_OF_OBSERV = []

        for i in range(numline, end):
            line = rinexolines[i]
            #print(line)

            # RINEX version number and type
            if re.search("RINEX VERSION / TYPE", line[60:]):
                self.VERSION = float(line[0:9])
                self.TYPE = line[40]
                continue

            if re.search("PGM / RUN Boptions[num]()Y / DATE", line[60:]):
                self.PGM = line[0:20].strip()
                self.RUN_BY = line[20:40].strip()
                self.DATE = line[40:60].strip()
                continue

            if re.search('OBSERVER / AGENCY', line[60:]):
                self.OBSERVER = line[0:20].strip()
                self.AGENCY = line[20:60]
                continue

            # Station name
            if re.search('MARKER NAME', line[60:]):
                self.MARKER_NAME = line[0:60].strip()
                continue

            # Station number
            if re.search('MARKER NUMBER', line[60:]):
                self.MARKER_NUMBER = line[0:20].strip()
                continue

            # Receiver number and type
            if re.search('REC # / TYPE / VERS', line[60:]):
                self.REC_N = line[0:20].strip()
                self.REC_TYPE = line[20:40].strip()
                self.REC_VERS = line[40:60].strip()
                continue

            # Antenna typea
            if re.search('ANT # / TYPE', line[60:]):
                self.ANT_N = line[0:20].strip()
                self.ANT_TYPE = line[20:40].strip()
                continue

            # Approximated position
            if re.search('APPROX POSITION XYZ', line[60:]):
                val = line[0:60].split()
                if len(val) > 0:
                    try:
                        self.X = float(val[0])
                    except:
                        self.X = 0
                if len(val) > 1:
                    try:
                        self.Y = float(val[1])
                    except:
                        self.Y = 0
                if len(val) > 2:
                    try:
                        self.Z = float(val[2])
                    except:
                        self.Z = 0
                continue

            # offsets
            if re.search('ANTENNA: DELTA H/E/N', line[60:]):
                val = line[0:60].split()
                if len(val) > 0:
                    try:
                        self.dH = float(val[0])
                    except:
                        self.dH = 0
                if len(val) > 1:
                    try:
                        self.dE = float(val[1])
                    except:
                        self.dE = 0
                if len(val) > 2:
                    try:
                        self.dN = float(val[2])
                    except:
                        self.dN = 0
                continue

            # Antenna type
            if re.search('WAVELENGTH FACT L1/2', line[60:]):
                self.WAVELENGTH_FACT_L1 = float(line[0:6])
                self.WAVELENGTH_FACT_L2 = float(line[6:12])
                continue

            # Interval
            if re.search('INTERVAL', line[60:]):
                try:
                    self.INTERVAL = float(line[0:10])
                except:
                    self.INTERVAL = 0
                    """ todo : calculer l'interval a partuir des données """
                continue

            # Time of first observation
            if re.search('TIME OF FIRST OBS', line[60:]):
                self.TIME_OF_FIRST_OBS.rinex_t(line[0:44])
                continue

            # Time of last observation
            if re.search('TIME OF LAST OBS', line[60:]):
                self.TIME_OF_LAST_OBS.rinex_t(line[0:44])
                continue

            # type of observations
            if re.search('# / TYPES OF OBSERV', line[60:]):
                ListTypeObs = line[10:60].split()
                for j in range(len(ListTypeObs)):
                    TYPE_OF_OBSERV.append(ListTypeObs[j])
                    
            self._NumLinePerEpoch = int(ceil(float(len(self.TYPE_OF_OBSERV))/5.0))

            if re.search('END OF HEADER', line[60:]):
                for const1 in self._listConst:
                    self.TYPE_OF_OBSERV[const1] = TYPE_OF_OBSERV
                    
                for key in self.TYPE_OF_OBSERV:
                    NbObservable = len(self.TYPE_OF_OBSERV[key])
                    break
                self._NumLinePerEpoch = int(ceil(NbObservable/5.0))
                return i+1

        return i+1


    def _read_header_urw(self, rinexolines, numline=0, maxline=1e6):
        """"""

        end = min(numline+maxline, len(rinexolines))
        #print(end)

        for i in range(numline, end):
            line = rinexolines[i]
            #print(line)

            # U version number and type
            if re.search("RINEX VERSION / TYPE", line[60:]):
                self.VERSION = float(line[0:9])
                self.TYPE = line[40]
                continue

            if re.search("PGM / RUN Boptions[num]()Y / DATE", line[60:]):
                self.PGM = line[0:20].rstrip()
                self.RUN_BY = line[20:40].rstrip()
                self.DATE = line[40:60].rstrip()
                continue

            if re.search('OBSERVER / AGENCY', line[60:]):
                self.OBSERVER = line[0:20].rstrip()
                self.AGENCY = line[20:60]
                continue

            # Station name
            if re.search('MARKER NAME', line[60:]):
                self.MARKER_NAME = line[0:60].rstrip()
                continue

            # Station number
            if re.search('MARKER NUMBER', line[60:]):
                self.MARKER_NUMBER = line[0:20].rstrip()
                continue

            # Receiver number and type
            if re.search('REC # / TYPE / VERS', line[60:]):
                self.REC_N = line[0:20].rstrip()
                self.REC_TYPE = line[20:40].rstrip()
                self.REC_VERS = line[40:60].rstrip()
                continue

            # Antenna typea
            if re.search('ANT # / TYPE', line[60:]):
                self.ANT_N = line[0:20].rstrip()
                self.ANT_TYPE = line[20:40].rstrip()
                continue

            # Approximated position
            if re.search('APPROX POSITION XYZ', line[60:]):
                val = line[0:60].split()
                self.X = float(val[0])
                self.Y = float(val[1])
                self.Z = float(val[2])
                continue

            # offsets
            if re.search('ANTENNA: DELTA H/E/N', line[60:]):
                val = line[0:60].split()
                self.dH = float(val[0])
                self.dE = float(val[1])
                self.dN = float(val[2])
                continue

            # Antenna type
            if re.search('WAVELENGTH FACT L1/2', line[60:]):
                self.WAVELENGTH_FACT_L1 = float(line[0:6])
                self.WAVELENGTH_FACT_L2 = float(line[6:12])
                continue

            # Interval
            if re.search('INTERVAL', line[60:]):
                self.INTERVAL = float(line[0:10])
                continue

            # Time of first observation
            if re.search('TIME OF FIRST OBS', line[60:]):
                self.TIME_OF_FIRST_OBS.rinex_t(line[0:44])
                continue

            # Time of last observation
            if re.search('TIME OF LAST OBS', line[60:]):
                self.TIME_OF_LAST_OBS.rinex_t(line[0:44])
                continue

            # type of observations
            if re.search('# / TYPES OF OBSERV', line[60:]):
                ListTypeObs = line[10:60].split()
                for j in range(len(ListTypeObs)):
                    self.TYPE_OF_OBSERV.append(ListTypeObs[j])

            self._NumLinePerEpoch = int(ceil(float(len(self.TYPE_OF_OBSERV))/5.0))

            if re.search('END OF HEADER', line[60:]):
                return i+1

        return i+1


    def print_header(self):
        print(self)

    def print(self):
        """ print fucntion """
        print(self)

    def __str__(self):

        s = ''
        s += "VERSION : %s\n" % (self.VERSION)
        s += "TYPE : %s\n" % (self.TYPE)
        s += "PGM : %s\n" % (self.PGM)
        s += "RUN BY : %s\n" % (self.RUN_BY)
        s += "DATE : %s\n" % (self.DATE)
        s += "OBSERVER : %s\n" % (self.OBSERVER)
        s += "AGENCY : %s\n" % (self.AGENCY)
#        s += "EPOCH_FLAG : %d\n" % (self.EPOCH_FLAG)
        s += "MARKER NAME : %s\n" % (self.MARKER_NAME)
        s += "MARKER NUMBER : %s\n" % (self.MARKER_NUMBER)
        s += "REC N : %s\n" % (self.REC_N)
        s += "REC TYPE : %s\n" % (self.REC_TYPE)
        s += "REC VERS : %s\n" % (self.REC_VERS)
        s += "ANT N : %s\n" % (self.ANT_N)
        s += "ANT TYPE : %s\n" % (self.ANT_TYPE)
        s += "X  : %14.4f  Y : %14.4f  Z : %14.4f\n" % (self.X, self.Y, self.Z)
        s += "dE : %14.4f dN : %14.4f dH : %14.4f\n" % (self.dE, self.dN, self.dH)
        s += "WAVELENGTH FACTOR L1 : %.1f L2 : %.1f\n" % (self.WAVELENGTH_FACT_L1, self.WAVELENGTH_FACT_L2)
        s += "INTERVAL : %.3f\n" % (self.INTERVAL)
        s += "TIME OF FIRST OBS : %s\n" % (self.TIME_OF_FIRST_OBS.st_iso_epoch())
        s += "TIME OF LAST OBS  : %s\n" % (self.TIME_OF_LAST_OBS.st_iso_epoch())

        for const1 in self.TYPE_OF_OBSERV:
            str = ''
            for i in range(len(self.TYPE_OF_OBSERV[const1])):
                str += self.TYPE_OF_OBSERV[const1][i]+' '
            s += "TYPE_OF_OBSERV %s (%d) : %s\n" % (const1, len(self.TYPE_OF_OBSERV[const1]), str)
     
        s += "EPOCH NUMBER : %d\n" % (len(self.epochs))
        s += "LINES per EPOCH : %d\n" % (self._NumLinePerEpoch)
        return s
    
    def writeFirstRinexHeader2(self, observables=['C1', 'P2', 'L1', 'L2']):
        
        s = ""
        s += "%9.2f%11s%-20s%-20s%s\n" % (self.VERSION, "", "OBSERVATION DATA", self.TYPE, "RINEX VERSION / TYPE")
        s += "%-20s%-20s%-20s%s\n" % (self.PGM, self.RUN_BY, self.DATE, "PGM / RUN BY / DATE") 
        s += "%-20s%-40s%s\n" % (self.OBSERVER, self.AGENCY, "OBSERVER / AGENCY")
        s += "%-60s%s\n" % (self.MARKER_NAME, "MARKER NAME") 
        s += "%-20s%40s%s\n" % (self.MARKER_NUMBER, "", "MARKER NUMBER")
        s += "%-20s%-20s%-20s%s\n" % (self.REC_N, self.REC_TYPE, self.REC_VERS, "REC # / TYPE / VERS")
        s += "%-20s%-20s%-20s%s\n" % (self.ANT_N, self.ANT_TYPE, "", "ANT # / TYPE")
        s += "%14.4f%14.4f%14.4f%18s%s\n" % (self.X, self.Y, self.Z, "", "APPROX POSITION XYZ")
        s += "%14.4f%14.4f%14.4f%18s%s\n" % (self.dH, self.dE, self.dN, "", "ANTENNA: DELTA H/E/N")
        s += "%6d%6d%48s%s\n" % (self.WAVELENGTH_FACT_L1, self.WAVELENGTH_FACT_L2, " ", "WAVELENGTH FACT L1/2")
        
        nObservables = len(observables)
        s += "%6d" % nObservables
        s2 = ""
        for o in observables:
            s2 += "    %2s" % o
        s2 += " " * 400
        s += "%-54s# / TYPES OF OBSERV\n" % s2[:54]
        if nObservables > 9:
            s += "      %-54s# / TYPES OF OBSERV\n" % s2[54:108]
        if nObservables > 18:
            s += "      %-54s# / TYPES OF OBSERV\n" % s2[108:162]
            
        s += "%10.3f%50sINTERVAL\n" % (self.INTERVAL, " ") 
        s += "%6d%6d%6d%6d%6d%13.7f     GPS         %s" % (self.TIME_OF_FIRST_OBS.yyyy,
               self.TIME_OF_FIRST_OBS.mon,
               self.TIME_OF_FIRST_OBS.dd,
               self.TIME_OF_FIRST_OBS.hh,
               self.TIME_OF_FIRST_OBS.min,
               self.TIME_OF_FIRST_OBS.sec,
               "TIME OF FIRST OBS\n")
        s += "%60s%s\n" % (" ", "END OF HEADER")
        
        return s

class epoch():
    """Rinex epoch class"""
    def __init__(self, str_datetime=""):
        """
        str_datetime : chaine de temps au format d'une entete d'un bloc de donnees rinex
        ex :  "17  7  3 10 43  0.0000000"
        """
        self.tgps = gpst.gpsdatetime()
        self.clock_offset = 0.0
        self.satellites = []

        if str_datetime != "":
            self.tgps.rinex_t(str_datetime)

    def _read_epoch_2(self, lines, NbSat, NbLinesHeader, NbLinesData, TypeOfObservable):
        """"""
        for key in TypeOfObservable:
            NnObservable = len(TypeOfObservable[key])
            # Rinex2 : all constallations have same obs types
            TypeOfObservable = TypeOfObservable[key]
            break

        NbLinesPerSat = int(ceil(float(NnObservable)/5.0))
        nMax = len(lines) - NbLinesHeader
#        print(TypeOfObservable, NnObservable, NbLinesPerSat, nMax, len(lines) , NbLinesHeader)


        # create satellite list
        str = ""
        for n in range(NbLinesHeader):
            str += lines[n][32:68]

        ListSat = []
        for n in range(NbSat):
            ListSat.append(str[n*3:n*3+3])

        # splitting lines between header and data
        ListHeader = []
        for n in range(NbLinesHeader):
            ListHeader.append(lines.pop(0))

        for n in range(NbSat):
#            print("Satellite #%d" % n)
            line = ''
            for k in range(NbLinesPerSat):
                if n*NbLinesPerSat+k >= nMax: # jbl 20170314 : cas ou le fichier est trop court
                    try:
                        print("Reading error at %s" %(self.tgps.st_rinex_epoch()))
                    except:
                        print("Reading error at %s" %(self.tgps.st_iso_epoch(2)))
                    return None

                linek = lines[n*NbLinesPerSat+k]
                linek = linek[:-1]
                line += linek+" "*(80-len(linek))

            self.satellites.append(sat())
            self.satellites[-1].setPRN(ListSat[n])

            for k in range(NnObservable):
                strobs = line[16*k:16*k+14]
                try:
                    floatobs = float(strobs)
                    self.satellites[-1].obs[TypeOfObservable[k]] = floatobs
                except:
                    floatobs = nan

            """ Calcul de P3 et P4 """
            if 'C1' in self.satellites[-1].obs and 'P2' in self.satellites[-1].obs:
                try:

                    C1 = self.satellites[-1].obs["C1"]
                    P2 = self.satellites[-1].obs["P2"]
                    P3 = const.k_L3 * (const.f1_2 * C1 - const.f2_2 * P2)
                    P4 = C1 - P2
                    self.satellites[-1].obs["P3"] = P3
                    self.satellites[-1].obs["P4"] = P4
                except:
                    print(self.satellites[-1].obs)

            """ Calcul de L3 et L4 """
            if 'L1' in self.satellites[-1].obs and 'L2' in self.satellites[-1].obs:
                try:
                    L1 = self.satellites[-1].obs["L1"]
                    L2 = self.satellites[-1].obs["L2"]
                    L3 = const.k_L3 * (const.f1_2 * L1 * const.lambda1 \
                                       - const.f2_2 * L2 * const.lambda2)
                    L4 = L1 * const.lambda1 - L2 * const.lambda2
                    self.satellites[-1].obs["L3"] = L3
                    self.satellites[-1].obs["L4"] = L4
                except:
                    print(self.satellites[-1].obs)

        return NbLinesHeader+NbLinesData
    
    def getSat(self, const, prn):
        """
        get satellite object from current epoch 
        None if satellite not present
        """
        try:
            for S in self.satellites:
                if S.PRN == prn and S.const == const:
                    return S
        except:
            pass
        return None
    
    def getObs(self, obsName, const, prn):
        """
        get get obesrvation from satellite object from current epoch 
        None if satellite/observation not present
        """
        try:
            S = self.getSat(const, prn)               
            return S.getObs(obsName)
        except:
            return nan

    def __str__(self):
        s = ''
        s += self.tgps.st_iso_epoch() +  "\n"
        for sat in self.satellites:
            s += sat.__str__() + "\n"
        return s
    
    def copyObservable(self, observable1, observable2):
        """
        fill observable2 with observabl1 value
        Jacques Beilin - ENSG/DPTS - 2020-03-03

        Input :
            - observable1 : source observable
            - observable2 : destination observable
        Output :

        """
        for sat in self.satellites:
            sat.copyObservable(observable1, observable2)    
    
    def writeRinex2Epoch(self, parameters={"OBSERVABLES":['C1', 'P2', 'L1', 'L2'], "CONST":'GRE'}):
        
        observables = parameters["OBSERVABLES"]
        const = parameters["CONST"]
        
        s = " %2d %2d %2d %2d %2d%11.7f  %1d" % (self.tgps.yy, self.tgps.mon, self.tgps.dd, self.tgps.hh, self.tgps.min, self.tgps.sec, 0)
        nSat = 0
        s2 = ""
        for sat in self.satellites:
            if re.search(sat.const, const):
                s2 += "%1s%02d" % (sat.const, sat.PRN)
                nSat += 1
        s2 += " " * 300        
        
        s += "%3d" % nSat 
        s += "%36s\n" % s2[:36]
        if nSat > 12:
            s += "%32s%36s\n" % (" ", s2[36:72])
        if nSat > 24:
            s += "%32s%36s\n" % (" ", s2[72:])
        for sat in self.satellites:
            s2 = ""
            if re.search(sat.const, const):
                for observable in observables:
                    try:
                        s2 += "%14.3f  " % sat.obs[observable]
                    except:
                        s2 += "%14s  " % " "
                s2 += " " * 400                  
                s += "%80s\n" % s2[:80]
                if len(observables) > 5:
                    s += "%80s\n" % s2[80:160]
                if len(observables) > 10:
                    s += "%80s\n" % s2[160:240]
                if len(observables) > 15:
                    s += "%80s\n" % s2[240:320]
                    
        return s

class sat():
    """GNSS observation for a specific PRN"""
    def __init__(self):
        self.type = "o"
        self.const = ''
        self.PRN = 0

        self.obs = dict()

    @property
    def prn(self):
        return "%1s%02d"  % (self.const, self.PRN)
    
    @property
    def C1(self):
        """
        quick way to get C/A code
        """
        try:
            for key in self.obs:
                if re.search("^C1", key):        
                    obs = self.obs[key]
                    return obs
        except:
            return nan  
    
    def getObs(self, obsName):
        """
        get get observation from satellite object 
        None if observation not present
        """
        try:
            for key in self.obs:
                if re.search("^" + obsName, key):        
                    return self.obs[key]
        except:
            return nan

    @prn.setter
    def prn(self, sprn):
        self.PRN = int(sprn[1:])
        self.const = sprn[0]

    def setPRN(self, str_PRN):
        self.PRN = int(str_PRN[1:])
        self.const = str_PRN[0]

    def print(self):
        print(self)

    def __str__(self):
        s = ''

        s += "%-16s : %s\n" % ("const", self.const)
        s += "%-16s : %s\n" % ("PRN", self.PRN)
        s += "%-16s :\n" % ("Observables")
        for observable in self.obs:
            s += "   %-13s : %.3f\n" % (observable, self.obs[observable])

        return s
    
    def copyObservable(self, observable1, observable2):
        """
        fill observable2 with observable1 value
        Jacques Beilin - ENSG/DPTS - 2020-03-03

        Input :
            - observable1 : source observable
            - observable2 : destination observable
        Output :

        """
        try:
            if observable1 in self.obs and (observable2 not in self.obs):
                self.obs[observable2] = self.obs[observable1]
        except:
            pass

