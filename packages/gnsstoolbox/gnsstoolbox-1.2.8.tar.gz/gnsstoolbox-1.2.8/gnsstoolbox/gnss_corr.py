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

import numpy as np
import math

def corr_dtropo_saast(P,T,H,h,zen):
    """[dr]=corr_dtropo_saast(P,T,H,h,zen)
    calculates ZPD from Saastamoinen model
    Jacques Beilin - ENSG - 2014-06-11

    Input :
        - P     : pressure (hPa)
        - T     : temperature (K)
        - H     : humidity (%)
        - h     : ellipsoid height (m)
        - zen   : zenithal angle (rad)

    Output
        - dr    : zenithal tropospheric delay (m)
    Reference : SUBROUTINE TROPOS(Z,HS,T,P,RH,MODEL,DR) from Bernese GPS Software"""

    bcor = np.array([ 1.156, 1.006, 0.874, 0.757, 0.654, 0.563 ])

    if (h>4000.0):
        h=4000.0

    if(h<0.0):
        h=0.0

    p = P * (1.0 - 2.26e-5 * h)**5.225;
    t = T - h * 0.0065;
    rhum = H * np.exp( -6.396e-4 * h);
    if rhum > 100.0 : rhum = 100.0

    # WATER VAPOR PRESSURE
    e = ( rhum / 100.0 ) * np.exp( -37.2465 + 0.213166 * t - 2.56908e-4 * t * t)

    # HEIGHT IN KM
    hl = h / 1000.0
    if (hl < 0.0):
        hl = 0.0

    if (hl > 4.0):
        hl = 4.0

    i = math.floor(hl)

    # REFERENCE HEIGHT FOR LINEAR INTERPOLATION IN TABLE BCOR
    href = i
    B = bcor[i] + (bcor[i+1] - bcor[i]) * (hl - href);

    Delta_tropo = (0.002277 / np.cos(zen)) * (p + (1255.0 / t + 0.05) * e - B * np.tan(zen)**2)
    return Delta_tropo

if __name__ == "__main__":
    print("gnss_corr")

    P = 1013.0
    T = 285.0
    H=50
    h=0
#    zen=np.pi/180.0 * np.array([0,10,20,30,40,50,60,70,80])
    zen = 0 #np.pi / 180 * 45
    dr=corr_dtropo_saast(P,T,H,h,zen)
    print("dr = ",dr)
