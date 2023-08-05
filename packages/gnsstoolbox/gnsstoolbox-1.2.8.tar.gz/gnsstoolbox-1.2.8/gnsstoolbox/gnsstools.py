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
import gnsstoolbox.gnss_const as const


def toolCartGeoGRS80(X,Y,Z):
    """function [lon,lat,h] = tool_cartgeo_GRS80(X,Y,Z)
    Cartesian to geographic coordinates transformation
    Jacques BEILIN - DPTS - 2014-06-10

    Input :
    - X, Y, Z : cartesian coordinates (m) or vector of coordinates

    Output :
    - lon : vector of longitude (rad)
    - lat : vector of latitude (rad)
    - h : vector of heights (m)


    Function call :
    [lamb,phi,h] = tool_cartgeo_GRS80_2([4201575.762;4201575.762],[189856.033;189856.033],[4779066.058;4779066.058])"""

    # IAG GRS80 constants
    a = 6378137.0
    f = 1/298.257222101
    e2 = 2 * f - f**2

    rxy = np.sqrt(X**2 + Y**2)
    r = np.sqrt( X**2 + Y**2 + Z**2)
    
    if r < const.Rmin:
        return 0.0, 0.0, 0.0
    
    mu = np.arctan((Z / rxy) * ((1 - f) + a * e2 / r))

    num = Z * (1 - f) + e2 * a * (np.sin(mu))**3;
    denum = (1 - f) * (rxy - a * e2 * (np.cos(mu))**3);
    lat = np.arctan(num / denum);

    lon = 2 * np.arctan(Y / (X + rxy));

    w = (1 - e2 * np.sin(lat)**2)**0.5;
    h = rxy * np.cos(lat) + Z * np.sin(lat) - a * w;
    
    try:
        lon = float(lon)
        lat = float(lat)
        h = float(h)
    except:
        pass

    return lon,lat,h

def toolGeoCartGRS80(lon,lat,h):
    """[X,Y,Z] = tool_geocart_GRS80(lon,lat,h)
    Geographic to cartesian coordinates transformation
    Jacques BEILIN - 2014-06-10

    Input :
    - lon : longitude (rad)
    - lat : latitude (rad)
    - h : height (m)
    Output :
    - X, Y, Z : cartesian coordinates (m)

    Function call :
        [X,Y,Z] = tool_geocart_GRS80(2.351412386,48.502786872,160.519)"""

    # IAG GRS80 constants
    a = 6378137.0
    f = 1/298.257222101
    e2 = 2 * f - f**2

    # angles in rad
    N = a / np.sqrt(1.0 - e2 * (np.sin(lat))**2);
    X = (N + h) * (np.cos(lon)) * (np.cos(lat));
    Y = (N + h) * (np.sin(lon)) * (np.cos(lat));
    Z=(N * (1 - e2) + h) * (np.sin(lat));
    
    try:
        X = float(X)
        Y = float(Y)
        Z = float(Z)
    except:
        pass
    
    return X,Y,Z

def toolCartLocGRS80(X0,Y0,Z0,X,Y,Z):
    """function [E,N,U]=  tool_cartloc_GRS80(X0,Y0,Z0,X,Y,Z)
    Coordinate transformation from cartesian coordinates to local coordinates
    Jacques BEILIN - ENSG/DPTS - 2021-09-09

    Input :
    - X0, Y0, Z0 : cartesian coordinates of frame origin (m)
    - X, Y, Z : cartesian coordinates (m)

    Output :
    - E, N, U : Easting, Northing, Up in m"""

    # Geographic coordinates computation
    [lon,lat,h] = tool_cartgeo_GRS80(X0,Y0,Z0);

    # Local coordinates transformation
    R = matCart2Local(lon,lat)
    
    try:
        (nl,nc) = X.shape
        Xl = []
        Yl = []
        Zl = []
        for l in range(nl):
            Vloc = np.array([[X[l,0]-X0],[Y[l,0]-Y0],[Z[l,0]-Z0]])
            XYZl = np.dot(R, Vloc)
            Xl.append(XYZl[0,0])
            Yl.append(XYZl[1,0])
            Zl.append(XYZl[2,0])
            
        if nl == 1:
            Xl = float(Xl)
            Yl = float(Yl)
            Zl = float(Zl) 
    except:
        Vloc = np.array([[X-X0],[Y-Y0],[Z-Z0]])
        XYZl = np.dot(R, Vloc)
        Xl = float(XYZl[0])
        Yl = float(XYZl[1])
        Zl = float(XYZl[2])
       
    return Xl, Yl, Zl

def matCart2Local(lon,lat):
    """
    R = MatCart2Local(lon,lat)
    matrix from cartesian to local coordinates
    Jacques Beilin - 20171214

    Input :
    lon, lat : logitude, latitude (rad)

    Output :
    R : rotation matrix

    """
    lon  = float(lon)
    lat = float(lat)
    R = np.array([[ -np.sin(lon),np.cos(lon),0.0],
            [-np.sin(lat)*np.cos(lon),-np.sin(lat)*np.sin(lon),np.cos(lat)],
            [np.cos(lat)*np.cos(lon),np.cos(lat)*np.sin(lon),np.sin(lat)]])


    return R

def toolAzEle(X,Y,Z,Xs,Ys,Zs):
    """
    [az,ele] = toolAzEle(X,Y,Z,Xs,Ys,Zs)
    Azimuth, elevation calculation
    Jacques BEILIN - ENSG/PEGMMT - 2022-01-06

    Input :
        X,Y,Z : station coordinates
        Xs,Ys,Zs : satellite coordinates vectors (1 sat = 1 line)

    Output
        az : satellite azimuths vector (rad)
        ele : satellite elevation vector (rad)
    """
    az, ele, h = toolAzEleH(X,Y,Z,Xs,Ys,Zs)
    return az, ele

def toolAzEleH(X,Y,Z,Xs,Ys,Zs):
    """
    [az,ele,h] = toolAzEleH(X,Y,Z,Xs,Ys,Zs)
    Azimuth, elevation and height calculation
    Jacques BEILIN - ENSG/DPTS - 2014-06-10

    Input :
        X,Y,Z : station coordinates
        Xs,Ys,Zs : satellite coordinates vectors (1 sat = 1 line)

    Output
        az : satellite azimuths vector (rad)
        ele : satellite elevation vector (rad)
        h : receiver ellipsoidal height (m)"""

    if re.compile('float').search(type(Xs).__name__): # detection du type : float ou nparray
        npts=1
    else:
        npts=Xs.size

    # Geographic coordinates computation
    [lon,lat,h] = toolCartGeoGRS80(X,Y,Z);

    [X1,Y1,Z1] = toolGeoCartGRS80(lon,lat,0);

    # Local coordinates transformation
    R = matCart2Local(lon,lat)

    az = np.zeros((npts,));
    ele = np.zeros((npts,));

    for i in range(npts):

        if  not re.compile('float').search(type(Xs).__name__):
            XS = float(Xs[i]);YS = float(Ys[i]);ZS = float(Zs[i])
        else:
            XS = Xs
            YS = Ys
            ZS = Zs

        VDX = np.array( [ [XS-X1] , [YS-Y1] , [ZS-Z1] ] )
        XYZl = np.dot(R,VDX)
        D =(XYZl[0]**2 + XYZl[1]**2 + XYZl[2]**2)**0.5;
        Dh =(XYZl[0]**2+XYZl[1]**2)**0.5;

        # elevation
        E = np.arcsin(XYZl[2]/D)

        # azimuth
        A = 2.0 * np.arctan(XYZl[0]/(XYZl[1]+Dh));
        if A < 0 :    A = A + 2.0 * np.pi

        az[i] = A
        ele[i] = E

        # debug
#        print 'Az = %6.2f , E = %6.2f ' % (A *180.0/pi,E *180.0/pi)

    return az,ele,h

def toolRotX(X,Y,Z,alpha):
    """[Xr,Yr,Zr] = toolRotX(X,Y,Z,alpha)
    Rotation around X-axis
    Jacques BEILIN - ENSG/DPTS - 2014-06-10

    Input
    - X,Y,Z : cartesian coordinates (m)
    - alpha : rotation angle (rad)

    Output
    - X,Y,Z : cartesian coordinates (m)"""

    R=np.array([[1.0,0.0,0.0],[0.0,np.cos(alpha),-np.sin(alpha)],[0.0,np.sin(alpha),np.cos(alpha)]])
    B=np.dot(R,np.array([X,Y,Z]))
    return B[0],B[1],B[2]

def toolRotY(X,Y,Z,alpha):
    """[Xr,Yr,Zr] = toolRotY(X,Y,Z,alpha)
    Rotation around Y-axis
    Jacques BEILIN - ENSG/DPTS - 2014-06-10

    Input
    - X,Y,Z : cartesian coordinates (m)
    - alpha : rotation angle (rad)

    Output
    - X,Y,Z : cartesian coordinates (m)"""

    R=np.array([[np.cos(alpha),0.0,np.sin(alpha)],[0.0,1.0,0.0],[-np.sin(alpha),1.0,np.cos(alpha)]])
    B=np.dot(R,np.array([X,Y,Z]))
    return B[0],B[1],B[2]

def toolRotZ(X,Y,Z,alpha):
    """[Xr,Yr,Zr] = toolRotZ(X,Y,Z,alpha)
    Rotation around Z-axis
    Jacques BEILIN - ENSG/DPTS - 2014-06-10

    Input
    - X,Y,Z : cartesian coordinates (m)
    - alpha : rotation angle (rad)

    Output
    - X,Y,Z : cartesian coordinates (m)"""

    R=np.array([[np.cos(alpha),- np.sin(alpha),0],[np.sin(alpha),np.cos(alpha),0],[0,0,1]])
    B=np.dot(R,np.array([X,Y,Z]))
    return B[0],B[1],B[2]

def tool_cartgeo_GRS80(X,Y,Z):
    """
    Please do NOT use this function : DEPRECATED
    """
    return toolCartGeoGRS80(X,Y,Z)

def tool_geocart_GRS80(lon,lat,h):
    """
    Please do NOT use this function : DEPRECATED
    """
    return toolGeoCartGRS80(lon,lat,h)

def tool_cartloc_GRS80(X0,Y0,Z0,X,Y,Z):
    """
    Please do NOT use this function : DEPRECATED
    """
    return toolCartLocGRS80(X0,Y0,Z0,X,Y,Z)

def tool_az_ele_h(X,Y,Z,Xs,Ys,Zs):
    """
    Please do NOT use this function : DEPRECATED
    """
    return toolAzEleH(X,Y,Z,Xs,Ys,Zs)

def MatCart2Local(lon,lat):
    """
    Please do NOT use this function : DEPRECATED
    """
    return matCart2Local(lon,lat)

def tool_rotX(X,Y,Z,alpha):
    """
    Please do NOT use this function : DEPRECATED
    """
    return toolRotX(X,Y,Z,alpha)

def tool_rotY(X,Y,Z,alpha):
    """
    Please do NOT use this function : DEPRECATED
    """
    return toolRotY(X,Y,Z,alpha)

def tool_rotZ(X,Y,Z,alpha):
    """
    Please do NOT use this function : DEPRECATED
    """
    return toolRotZ(X,Y,Z,alpha)

    
def test():
    X=4201598.572; Y=189881.734; Z=4779084.978
    Xs=25336662.486; Ys=8253239.166; Zs=2714781.655

    [Az,Ele,h]=toolAzEleH(X,Y,Z,Xs,Ys,Zs)


    Xs=np.array([[25336662.486],[25336662.486]])
    Ys=np.array([[8253239.166],[8253239.166]])
    Zs=np.array([[2714781.655],[2714781.655]])


    [Az,Ele,h]=toolAzEleH(X,Y,Z,Xs,Ys,Zs)
    print( "Az = ",Az)
    print( "Ele = ",Ele)
    print( "h = ",h)


    (x,y,z) = toolCartLocGRS80(X,Y,Z,Xs,Ys,Zs)
    print(x,y,z)

    X=25336662.486
    Y=8253239.166
    Z=2714781.655

    alpha = 1.0
    [Xr,Yr,Zr] = toolRotX(X,Y,Z,alpha)
    print( Xr,Yr,Zr)
    [Xr,Yr,Zr] = toolRotY(X,Y,Z,alpha)
    print( Xr,Yr,Zr)
    [Xr,Yr,Zr] = toolRotZ(X,Y,Z,alpha)
    print( Xr,Yr,Zr)
    
# if __name__ == "__main__":
#     test()
    
