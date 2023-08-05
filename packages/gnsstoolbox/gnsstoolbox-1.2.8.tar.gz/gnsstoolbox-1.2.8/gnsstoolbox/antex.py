# -*- coding: utf-8 -*-
"""
Copyright (C) 2014-2023, Jacques Beilin <jacques.beilin@gmail.com>, Ana-Maria Andrei

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


import os              # pour le systéme d'exploatation 
import re              # pour regular expressions ... fonction search
import numpy as np     # pour fonctions mathématique
import gpsdatetime as gps  # pour le temps GPS


# C'est la définition de la classe antex
class antex():
    
    """ Antenna calibration classe """
    
    """
    Permet de stocker et manipuler toutes les informations des fichiers de données atx.
   
    """
    def __init__(self, filename=""):
        
        """
        Méthode constructeur, initialise l'objet Antex à partir d’un fichier d’antenne de chemin filename
        
        Cette classe contient deux atributs:
            Antennas = objet de type list qui contient toutes les informations des antennes existente dans le fichier atx existent
            Header = objets de type list qui contient toutes les lignes de l'entête du fichier ANTEX
         """
        
        self.Antennas = []    # [] une liste qui peut être modifié
        self.Header = []
#        self.LoadAntex(filename)
        #print( 'Maintenant vous êtes en fonction constructeur __init__ avec l' arguments {}'.format(filename) )
#        try:
#            self.LoadAntex(filename)
#        except:
#            print("Unable to load %s" % (filename))
        self.LoadAntex(filename)



    def LoadAntex(self, filename):
       
        """
        Cette méthode lit un fichier ANTEX et complète la liste d’objets Antenna et l’attribut Header
            o list des objets de type Antenna et
            o list avec toutes les lignes de l'entête du header 
              
        Arguments:
            filename: str, le non du fichier atx
        
            
        Copyright: Ana-Maria Andrei, 2018-11-15
        """
        #print( 'Maintenant, vous êtes dans la function LoadAntex avec l'argument {}'.format(filename) )
        
        # l'argument filename est un string vide
        if (filename == ""): 
            print('Le nom du fichier est vide.')
            return -1

        # est l'argument filename un fichier qui existe dans le chemin  donné
        if not os.path.isfile(filename):
            print ('Dans le path du fichier {} il n y a pas'.format(filename))
            return -2
        
        # Si nous sommes arrivés ici maintenant essayons de lire ce fichier

        # loading strings
        try:
            F = open(filename, 'r')         # Ouvrez le fichier à l'aide de la fonction Open () avec l'attribut Read 'R' (Lire)
            atxlines = F.readlines()        # Lisez chaque ligne du fichier et placez-la dans une liste de chaînes 
            F.close()                       # Fermez le processus de lecture

        except:
            print ('Unable to open %s' % (filename))
            return -3
        
        # Affiche le message ci-dessous
        # Crées un string avec le nom de fichier et et le nombre de caractères dans le nom 
        print("Loading ANTEX file %s %d" % (filename, len(filename))) # 'Loading ANTEX file {}'.format(filename)
 

        """ suppression du header """
        for i in range(len(atxlines)):
            
            # attention! indexul este non-compris
            if re.search("END OF HEADER", atxlines[i]):
                self.Header = atxlines[:i+1] # Ici vous stockez toutes les lignes toutes les lignes liées à l'en-tête de la tête de table
                atxlines = atxlines[i+1:]    # Ici vous stockez toutes les lignes liées au bloc d'antenne (toutes les antennes)
                break
        
        
        # Variable pour stocker la position (index) d'où démarre un bloc d' Antenna 
        imin = 0
        print("header: {}, body: {}".format(len(self.Header), len(atxlines)))
        
        # Pour chaque position dans la liste des lignes de bloc Antenna
        for i in range(len(atxlines)):
            
            # De là commence le bloc d'antenne, le stockage de l'index
            if re.search("START OF ANTENNA", atxlines[i]):
                imin = i
            
            # Ici se termine le bloc Antenna
            if re.search("END OF ANTENNA", atxlines[i]):
#                print( 'AntennaBlock est entre la position {} et {}'.format(imin, i+1) )
                
                # Variable pour stocker la liste des lignes formant le bloc Antenna
                antennaBlock = atxlines[imin:i+1]
#                print(antennaBlock)
                
                # Construire un objet Antenna à l'aide de l'argument de bloc de ligne Antenna
                # L'argument est une liste de string (les lignes dans le fichier ATX qui définissent un bloc Antenna)

                Ant = Antenna(antennaBlock)
#                print(Ant.__dict__)
#                print(Ant)
                
                # Ajouter la variable dans laquelle un objet d'antenne est stocké dans la liste d'antennes
                self.Antennas.append(Ant)
                
    
    def __str__(self):
        
        """
        Fonction standard qui affiche l'objet Antex
    
        """
        s = '#antennas : {}'.format(len(self.Antennas))
        
        return s
   
    def GetReceiverAntenna(self,antennaType=""):
        return self.GetAntenna(antennaType)   
    
    def GetAntenna(self, antennaType=""): # antennaType est de type str (GetAntenna)
        
        """  
        Cette méthode extrait un objet de type Antenna de la liste d’antennes selon son nom
           
        Argument: 
            antennaType: string, le type ou le nom de l'antenne
        
        Output:
            None, un objet de type Antenna ou une liste des objets Antenna 
        
        ATTENTION!: pour l'antenne du satellite, le même nom peut exister plusieurs fois. 
        La différence sera faite par la période de validité (ValidFrom, ValidUntil)
        """
        
        # le type d'antenna n'a pas été spécifié
        if not antennaType:
               return None
           
        # Liste de toutes les antennes qui ont ce nom 
        # pour le même type de satellite il y a plusieurs modèles d'antennes
        # selon le code d'identification satellite et l'intervalle de temps
        # pour les récepteurs, vous n'aurez qu'une seule antenne
        # nous utilisons list comprehension un court chemin en Python pour écrire 
        # plus d'opération en une seule ligne
        
        lst = [ant for ant in self.Antennas if ant.Type == antennaType] 
        
        # l'antena n'existe pas dans le fichier Antex
        if len(lst) == 0:
            return None
        
        # Une antenne a été trouvée
        elif len(lst) == 1:
            return lst[0]
        
        # Plusieurs antennes ont été trouvées
        else:
            return lst



    def AddAntenna(self, antenna): # Ant de classe Antenna (AddAntenna)
        
        """
        Cette méthode ajoute un objet de type Antenna à la liste des antennes dans l'objet Antex

        Arguments: 
            antenna: Antenna, la variable qui fait référence à l'antenne que vous souhaitez ajouter à la liste. 
        
        Output: 
            ATTENTION!: Lorsque nous avons le même type d'antenne, nous devons faire une copie
            (deepcopy) de l'argument de l'antenne pour être sûr que toute modification ultérieure 
            de celui-ci n'est pas reflétée dans l'objet Antex
        """
        
        import copy
        
        self.Antennas.append(copy.deepcopy(antenna)) # Ajouter à la file d'attente de la liste  array méthode
        
        return

        
    def SelectMultipleAntennas(self, antenna_names):
        
        """
        Cette méthode sélectionne plusieurs objets d'antenne dans la liste d'antennes
        de l'Antex correspondant aux noms d'antenne dans l'argument Antenna_names
        
        Argument: 
            antenna_names: list of string, liste des noms des antennes à sélectionner
        
        Output: 
            Liste des objets de type Antenna. 

        Utilise la méthode GetAntenna () pour chaque antenne dans la liste des antennes.
        """
        
        # Initialise un nouvel objet de liste
        lst = []
        
        # Ajouter l'objet type d'antenne à la fin de la liste
        for antenna in antenna_names:
            lst.append(self.GetAntenna(antenna))
        
        return lst
    
    def WriteAntex(self, filename='new_file.atx', writePCV = "ALL"):
    
        """
        Cette méthode écrit toutes les informations qui existent dans l’objet ANTEX 
        dans un nouveau fichier 
        
        Argument : 
            filenames: string, le nom du nouveau fichier (par défaut : New_file.atx)

        Output ext: 
            Nouveau fichier 
        """
        
        print("header: {}, body: {}".format(len(self.Header), len(self.Antennas)))
        
        # ouvrir un fisier avc le nom filename pour écrire (voir l'argument 'w' write)
        with open(filename, 'w') as f:
            
            # header (écrit tete du tabel)
            for item in self.Header:
                f.write("%s" % item)
            
            # Pour chaque antenne en partie
            for antenna in self.Antennas:
                f.write( antenna.WriteAntenna(writePCV) )

# Un objet appelé Antenna
class Antenna():
    
    """
    La classe Antenna est définie pour manipuler le bloc de lignes entre « START OF ANTENNA»
    et « END OF ANTENNA ». Les informations dans le bloc d’antenne sont différentes 
    de bloc à bloc, d’où la nécessité de construire une classe dans laquelle on définit
    les éléments spécifiques pour chaque bloc, comme la description du format ANTEX
    """
    # Constructor a un seul argument 
    # Antennablock est une sous-liste de la liste atxlines.
    # antennaBlock contient toutes les lignes  toate liniile entre START OF ANTENNA et END OF ANTENNA
    
    def __init__(self, antennaBlock):
        
        """
        Cette méthode initialise et construit un objet de type Antenna. 
        
        Argument : antennaBlock: list [string], la liste des lignes afférents au bloc Antenna. 
        Toutes les lignes dans le fichier Antex qui se réfèrent à la même antenne et sont 
        entre « START OF ANTENNA » et « END OF ANTENNA ».
    
        Output:
            Définit et initialise les attributs de Frequencies et Comments plus tous les autres 
            en appelant la méthode ReadAntennaBlock().
-	
        """
        #print('Maintenant, vous créez un objet Antenna à partir d'un bloc de {} lignes'.format(len(antennaBlock)))
        self.Frequencies = {} 
        self.Comments = []
        
        self.ReadAntennaBlock(antennaBlock)
    
    def ReadAntennaBlock(self, antennaBlock=''):
       
        """
        Cette méthode Lit le bloc des lignes du fichier atx entre « START OF ANTENNA » et 
        « END OF ANTENNA ». 
        
        Argument:
            antennaBlock: list of strings
        
        Output:
            Définit les différents attributs de l'objet Antenna en fonction de
            la définition du format Antex, les attributs suivants sont définis:
            type, SATELLITECODECNN, etc.
        """
        #print('Maintenant vous êtes dans la function ReadAntennaBlock {} lignes'.format(len(antennaBlock)))
        
        # boucle pour chaque position dans la liste antennaBlock
        for i in range(len(antennaBlock)):
            
            #chaque élément dans la liste (ligne) est mise dans la variabile AtxLine
            AtxLine = antennaBlock[i]
            #print(AtxLine)
            
            # Définition ANTEX pour étiquette ...
            if re.search('TYPE / SERIAL NO', AtxLine):
                self.Type = AtxLine[:20].strip()                    #A20   A_text string de 20 caracteres
                self.SatelliteCodeCNN = AtxLine[20:40].strip()      #A20
                self.SatelliteCodeCNNN = AtxLine[40:50].strip()     #A10
                self.CosparId = AtxLine[50:60].strip()              #A10
                
            # Définition ANTEX pour la prochaine etiquette...
            if re.search('METH / BY / # / DATE', AtxLine):
                self.CalibrationMethod = AtxLine[:20].strip()           #A20 # strip Suppression des espaces vides du début et de la fin
                self.Agency = AtxLine[20:40].strip()                    #A20
                self.NAntennasCalibrated = int(AtxLine[40:50].strip())   #I6,4X    I_integer, x_space
                self.Date = AtxLine[50:60].strip()                      #A10
            
            # Définition ANTEX pour l'étiquette DAZI
            if re.search('DAZI', AtxLine):
                self.DAzi = float(AtxLine[2:8])                 #2X,F6.1,52X   F_float
            
            # Étiquette suivante
            if re.search('ZEN1 / ZEN2 / DZEN', AtxLine):
                self.Zen1 = float(AtxLine[2:8])                 #2X,3F6.1,40X
                self.Zen2 = float(AtxLine[8:14])
                self.DZen = float(AtxLine[14:20])
            
            if re.search('# OF FREQUENCIES', AtxLine):    
                self.NFrequencies = int(AtxLine[:6])

            if re.search('VALID FROM', AtxLine):       #5I6,F13.7,17X
                t = AtxLine.split()                 # la lista evec eléments nécessaires à la définition de l'heure GPS

                self.ValidFrom = gps.gpsdatetime()
                self.ValidFrom.ymdhms_t(float(t[0]),float(t[1]),float(t[2]),float(t[3]),float(t[4]),float(t[5]))

            if re.search('VALID UNTIL', AtxLine):   #5I6,F13.7,17X
                t = AtxLine.split()
                self.ValidUntil=gps.gpsdatetime()
                self.ValidUntil.ymdhms_t(float(t[0]),float(t[1]),float(t[2]),float(t[3]),float(t[4]),float(t[5]))

            if re.search('SINEX CODE', AtxLine):     #A10,50X
                self.SinexCode = AtxLine[:10].strip()
            
            if re.search('COMMENT', AtxLine):     #60X
                self.Comments.append(AtxLine[:60])                    
            
            # maintenant commence le bloc pour une fréquence AtxLine[:10].strip()
            if re.search('START OF FREQUENCY', AtxLine):      # 3X,A1,I2,54X
                
                key = AtxLine[3:6]
                
                # Stockez la position de ligne dans la variable Imin
                imin = i    # s' actualise
            
            # Ici se termine le bloc pour une fréquence
            if re.search('END OF FREQUENCY', AtxLine):        # 3X,A1,I2,54X
                #print('Frequency block depuis le {} la {}'.format(imin, i+1))

                frequencyBlock = antennaBlock[imin:i+1]
                freq = Frequency(frequencyBlock)
                self.Frequencies[key] = freq
 
    def __str__(self):
        """
        Définit les informations qui seront affichées dans l'objet Antenna.
        
        Output:
            Informations textuelles à l'écran à l'aide de la fonction Print ()
            un string avec le nombre d'objets Frequency dans l'objet Antenna
        """
        
        #print("{:20s} {:20s} {:10s} {:10s} {:20s}".format(self.Type, self.SatelliteCodeCNN, self.SatelliteCodeCNNN, self.CosparId, 'TYPE / SERIAL NO'))
        s = ""
        s += '{:40s}: {}'.format('Antenna type (strict IGS)', self.Type) + "\n"
        s += '{:40s}: {}'.format('Serial number / Satellite code', self.SatelliteCodeCNN) + "\n"
        s += '{:40s}: {}'.format('Satellite code sNNN (optional)', self.SatelliteCodeCNNN) + "\n"
        s += '{:40s}: {}'.format('COSPAR ID (optional)', self.CosparId) + "\n"    
        s += '{:40s}: {}'.format('Calibration method', self.CalibrationMethod) + "\n"
        s += '{:40s}: {}'.format('Agency', self.Agency) + "\n"
        s += '{:40s}: {}'.format('Number of individual antennas calibrated', self.NAntennasCalibrated) + "\n"
        s += '{:40s}: {}'.format('Date', self.Date) + "\n"
        s += '{:40s}: {}'.format('Increment of the azimuth', self.DAzi) + "\n"
        s += '{:40s}: {} {} {}'.format('Zenith / nadir angle', self.Zen1, self.Zen2, self.DZen) + "\n"     
        s += '{:40s}: {}'.format('SINEX code', self.SinexCode if hasattr(self, 'SinexCode') else '') + "\n"
        s += '{:40s}: {}'.format('Start of validity period', self.ValidFrom if hasattr(self, 'ValidFrom') else '') + "\n"
        s += '{:40s}: {}'.format('End of validity period', self.ValidUntil if hasattr(self, 'ValidUntil') else '') + "\n"
        s += '{:40s}: {}'.format('Number of frequency blocks', len(self.Frequencies) if hasattr(self, 'Frequencies') else '') 
        
        return s
 

    

    def ComputeCorrection(self, obs): # Pas défini!
        
        print("Antenna.ComputeCorrection. No implementation!!!")
        
        return Correction # Format pas défini!!




    def RemoveAzimuthPattern(self,): 
        """
        Cette méthode supprime toutes les valeurs des variations qui dépendent de 
        l'azimut pour toutes les fréquences existantes pour l'antenne actuelle. 
        
        Output:
            Modifie l'objet de base, c'est-à-dire supprime toutes 
            les données PCV dépendantes de l'azimut pour toutes les fréquences.
        
        """
        #print("Antenna.RemoveAzimuthPattern")
        
        # Seulement si ceux-ci existent
        if self.DAzi > 0.0:
            # pour chaque fréquence
            for key, data in self.Frequencies.items():
                # Seules les valeurs (toutes les colonnes) liées à la première ligne
                ncols = 1 + int((self.Zen2 - self.Zen1) / self.DZen)
                self.Frequencies[key].PCV = data.PCV[:ncols]
        
        # Après la suppression doit être mis à jour et l'étape de l'azimut, c'est à dire
        # il n y a plus de variations dépendente d' azimut
        self.DAzi = 0.0
        
    
    def PlotAntenna(self,): 
        
        """
        Dessine les variations de PCV pour chaque fréquence en utilisant les coordonnées polaires
        
        Output extern:
            Affiche une figure 2D avec une graphe d'antenne pour
            chaque fréquence de l'objet. 
            Le nombre de graphe = le nombre des fréquences.
        """
        #print("Antenna.PlotAntenna")
        
        # Import librarie pour desiner sous le pdeudonyme plt
        import matplotlib.pyplot as plt
        
        # Quand il n a pas des variations de phase (PCV)
        if self.DAzi == 0.0:
            print('No plot as no PCV for the antenna type {}'.format(self.Type))
            return None
        
        # Nombre de lignes et de colonnes pour organiser vos données plus facilement
        ncols = 1 + int((self.Zen2 - self.Zen1) / self.DZen)
        nrows = 1 + 1 + int((360 - 0) / self.DAzi)
        
        # Coordonnées polaire
        azimuths = np.radians(np.arange(0, 361, self.DAzi))
        zeniths = np.arange(self.Zen1, self.Zen2+self.DZen, self.DZen)
        r, theta = np.meshgrid(zeniths, azimuths)

        # Créer une nouvelle figure avec graphique pour chaque fréquence que nous utilisons coordonnée polaire
        nfig = self.NFrequencies
        fig, axarr = plt.subplots(nfig, 1, figsize=(5,5*nfig), subplot_kw=dict(projection='polar'))

        # Index, frequencyKey, Frequency object
        for i, (key, freqObj) in enumerate(self.Frequencies.items()): 
            
            # Axes de coordonnées
            ax = axarr[i]

            # Zéro sur la direction nord, et la direction dans le sens horaire
            ax.set_theta_zero_location("N")
            ax.set_theta_direction(-1)
            
            # maintenant nous dessinons le grafique
            values = freqObj.PCV.reshape(nrows, ncols) # tine minte ca prima linie contine datele ptr NOAZI
            cs = ax.contourf(theta, r, values[1:,:], cmap=plt.cm.rainbow)  # fara linia NOAZI
            
            # Ajouter une barre de couleur
            fig.colorbar(cs, ax=ax, orientation='vertical')
            #fig.colorbar(im1, cax=cax, orientation='vertical')
            
            # Créer un titre et l'attacher aux axes de coordonnées actuels
            n, e, u = freqObj.PCO
            title = '{} PCV\n{}\nPCO ({})[mm] [North: {:.2f}, East: {:.2f}, Up: {:.2f}]'.format(key, self.Type, key, n, e, u);
            ax.set_title(title)

        # Organiser soigneusement les graphiques dans la figure
        fig.tight_layout()

        return fig
    
    
    def WriteAntenna(self, writePCV = "ALL"):
        
        """
        Cette méthode ecrit un objet Antenna dans un format ANTEX
        Elle a été ajouté pour se répéter pour chaque antenne
 
        Output:
           Un string sur plusieurs lignes.
           (Toutes les lignes nécessaires pour écrire un bloc Antenna)
        """
        
        # mandatory (Lignes obligatoires)
        # Nous mettons toutes les lignes l'une après l'autre dans un seul string
        s = '{:60s}{:20s}\n'.format('', 'START OF ANTENNA') + \
            '{:20s}{:20s}{:10s}{:10s}{:20s}\n'.format(self.Type, self.SatelliteCodeCNN, self.SatelliteCodeCNNN, self.CosparId, 'TYPE / SERIAL NO') + \
            '{:20s}{:20s}{:6d}{:4s}{:10s}{:20s}\n'.format(self.CalibrationMethod, self.Agency, self.NAntennasCalibrated, '', self.Date, 'METH / BY / # / DATE') + \
            '{:2s}{:6.1f}{:52s}{:20s}\n'.format('', self.DAzi, '', 'DAZI') + \
            '{:2s}{:6.1f}{:6.1f}{:6.1f}{:40s}{:20s}\n'.format('', self.Zen1, self.Zen2, self.DZen, '', 'ZEN1 / ZEN2 / DZEN') + \
            '{:6d}{:54s}{:20s}\n'.format(self.NFrequencies, '', '# OF FREQUENCIES')
        
        # optionnel (Lignes facultatives uniquement si elles existent
        if hasattr(self, 'ValidFrom'):
            t = self.ValidFrom; # objet de typ gpsdatetime
            s = s + '{:6d}{:6d}{:6d}{:6d}{:6d}{:13.7f}{:17s}{:20s}\n'.format(t.yyyy, t.mon, t.dd, t.hh, t.min, t.sec, '', 'VALID FROM') 
        if hasattr(self, 'ValidUntil'):
            t = self.ValidUntil;
            s = s + '{:6d}{:6d}{:6d}{:6d}{:6d}{:13.7f}{:17s}{:20s}\n'.format(t.yyyy, t.mon, t.dd, t.hh, t.min, t.sec, '', 'VALID UNTIL') 
        if hasattr(self, 'SinexCode'):
            s = s + '{:10s}{:50s}{:20s}\n'.format(self.SinexCode, '', 'SINEX CODE') 
        if hasattr(self, 'Comments'):
            s = s + ''.join(['{:60s}{:20s}\n'.format(comment, 'COMMENT') for comment in self.Comments])
        
        # PCV        
        ncols = 1 + int((self.Zen2 - self.Zen1) / self.DZen)
        
        # Variations pour chaque fréquence en partie
#        for freq in self.Frequencies:
#            s += freq.WriteFrequency(ncols, self.DAzi)   
        for freq in self.Frequencies.values():
                s = s + freq.WriteFrequency(ncols, self.DAzi, writePCV)   
#        for f in self.Frequencies:
#            print(f.PCO, type(f))
        
        # la dérniere ligne
        s = s + '{:60s}{:20s}\n'.format('', 'END OF ANTENNA')
        
        return '{}'.format(s)
    
"""
    La classe Frequency est définit pour manipuler le bloc de lignes entre « START OF FREQUENCY »
    et « END OF FREQUENCY ». Les informations dans le bloc de fréquence sont 
    différentes de bloc à bloc, d’où la nécessité de construire une classe dans
    laquelle on définit les éléments spécifiques pour chaque bloc, 
    comme la description du format. Le format ANTEX se change.

"""
class Frequency():
    
    # constructorul obiectului are nevoie de un argument frequencyBlock
    # argumentul este o lista de strings (blocul de linii ce defineste o frecventa)
    def __init__(self, frequencyBlock):
        
        """
        Initialise et construit un objet de type Frequency
        
        Argument:
            frequencyBlock: list of strings, la liste des lignes afférents au bloc Frequency . 
            Toutes les lignes dans le fichier Antex qui se réfèrent à la même fréquence 
            et sont entre START OF FREQUENCY et END OF FREQUENCY)
        
        Output:
          Définit et initialise les attributs de PCO et PCV 
          plus tous les ReadFrequencyBlock() correspondants
          
        """
        self.PCO = np.zeros(3)      # un Objet de type np.array avec trois élémentes
        self.PCV = np.array([])

        self.ReadFrequencyBlock(frequencyBlock)
        
    def __str__(self):
        
        s =  '{:8.3f}{:8.3f}{:8.3f}\n'.format(self.PCO[0], self.PCO[1], self.PCO[2])
        return s
        
    # Lire le bloc de lignes qui définit une fréquence  
    def ReadFrequencyBlock(self, frequencyBlock):
        """
        Cette méthode lit un bloc de ligne dans le fichier ANTEX qui se rapporte
        à une fréquence(frequencyBlock
        
        Argument:
            frequencBlock: list of strings
            
        Output:
            Les attributs suivants sont définis : FrequencyKey, PCO, PCV.
        """
        #print('Maintenant vous êtes dans la function ReadFrequencyBlock {} lignes'.format(len(frequencyBlock)))
        
        # pour chaque position dans le bloc de fréquence
        for i in range( len(frequencyBlock)):
            
            # Une ligne de la liste des lignes pour la fréquence correspondant
            AtxLine = frequencyBlock[i]
#            print(i, AtxLine)
            
            # le début du bloc
            if re.search('START OF FREQUENCY', AtxLine):
                self.FrequencyKey = AtxLine[3:6]     # satellite system A1I2 
            
            # le fin du bloc
            elif re.search('END OF FREQUENCY', AtxLine):
                continue  
            
            # PCO phase center offsets 
            # il s'agit de la ligne correspndante des offsets
            elif re.search('NORTH / EAST / UP', AtxLine):       # 3F10.2,30X   
                self.PCO[0] = float(AtxLine[0:10])  #North
                self.PCO[1] = float(AtxLine[10:20])  #East
                self.PCO[2] = float(AtxLine[20:30])    #Up
            
            # PCV phase center variations non-azimuth-dependent pattern
            # c'est le cas pour la ligne qui ne dépend pas de l'azimut,  
            # mais seulement par l'angle zenital # (0... 90) dans le cas du récepteur d'antenne
            # Nadir angle  (0 ... xx) dans le cas de l'antenne satellite
            elif re.search('NOAZI', AtxLine):
                self.ReadNonAzimuthPattern(AtxLine)
                        
            # PCV azimuth-dependent pattern
            # C'est le cas pour les lignes qui contiennent les valeurs des variations de PCV 
            # Azimut dépendant
            else:
                self.ReadAzimuthPattern(AtxLine)

                    
            
    def ReadNonAzimuthPattern(self, atxline): # 3X,A5,mF8.2    M_multiple
        """
        Cette méthode Lit la ligne dans le bloc fréquence qui fait référence aux valeurs 
        (non-)azimuth-dependent pattern
      
        Chaque valeur est mise dans une colonne distincte. 
        Les valeurs sont lues en tant que texte et doivent être converties en nombres réels.
        Le nombre des colonnes dépend de ZEN1, ZEN2, DZen.
        
        ATTENTION! l'index commence à partir de zéro et 
                  toutes les valeurs sont ajoutées dans l’attribut PCV
        
        Argument:
           atxline: string, une ligne dans le bloc de fréquence qui fait référence à  «NOAZI»
            
        Output:
            Actualisation de l’attribut PCV avec les variations dépendant uniquement par l'angle zénithal
        """
        #print('Frequency.ReadNonAzimuthPattern: ', len(atxline.split()))
        values = atxline.split()    # liste de strings, Le premier élément est le texte «Noazi» le reste sont des nombres exprimés en strings
        values = [float(value) for value in values[1:]] # Nous sautons le premier élément et le reste les transforment en nombres float
        
        self.PCV = np.append(self.PCV, values) # on ajout (1+(ZEN2-ZEN1)/DZEN) éléments (colloanes)

    
    def ReadAzimuthPattern(self, atxline):    # F8.1,mF8.2
        """
        Cette méthode lit la ligne dans le bloc de fréquence qui fait référence aux valeurs dépendent de l'azimut.
        Sont lues en tant que texte et doivent être transformées en nombres
        
        Chaque valeur est placée dans une colonne distincte. 
        Aucune colonne ne dépend de ZEN2, ZEN1, DZen.
        Chaque ligne est ajoutée l'une après l'autre et le nombre des lignes dépend du DAzi.
        
        ATTENTION! l'index commence à partir de zéro pour les colonnes et les lignes
        
        Argument:
            atxline: string, une ligne dans le bloc de fréquence qui fait référence à  «NOAZI»
        
        Output:
            -	Met à jour l'attribut PCV en ajoutant des variations dépendant de l’azimut
        
        """
         
        #print('Frequency.ReadAzimuthPattern: ', len(atxline.split()) )
        values = atxline.split()    # liste de strings, le premier élément représente la valeur de l'angle azimutal
        values = [float(value) for value in values[1:]] # Nous sautons le premier élément et le reste les transforment en nombres float
        
        self.PCV = np.append(self.PCV, values) # on ajoute (1+(ZEN2-ZEN1)/DZEN) élementes (colloane) de (1+(360-0)/DAZI) fois (lignes)
        
    
    def WriteFrequency(self, ncols, dazi, writePCV ="ALL"):
     
        """
        Cette méthode ecrit un objet Frequency dans un format ANTEX
        
        Arguments:
            ncol: int, le nombre de colonnes dans PCV
            dazi : float, le pas de l’azimut pour les corrections dépendant du azimut 
                          en permettant de déterminer le nombre de ligne dans le PCV
            writePCV = ["ALL", "PCO", "NOAZI"]
        
        Output:
            Multi-lignes string sur plusieurs lignes
            ( toutes les lignes du bloc de fréquence)
        
        """
        # prémiere ligne 3X,A1,I2,54X
        s = '{:3s}{:3s}{:54s}{:20s}\n'.format('', self.FrequencyKey, '', 'START OF FREQUENCY')
        s = s + '{:10.2f}{:10.2f}{:10.2f}{:30s}{:20s}\n'.format(self.PCO[0], self.PCO[1], self.PCO[2], '', 'NORTH / EAST / UP')
        
        
        if writePCV in ["NOAZI", "ALL"]:
            # Quel genre de variations avons-nous?
            if dazi == 0.0:
                nrows = 1 # seulement non-azimuth depedent variations
            else:
                nrows = 1 + 1 + int((360 - 0) / dazi) # azimuth-dependent variations
            
            # Réorganiser les variations dans une matrice /tableau/Grille
            # PCV sera un objet de type numpy.ndarray
            PCV = self.PCV.reshape(nrows, ncols)
            
            # Il s'agit de la ligne correspondante pour les variations'NOAZI'
            # non-dependent azimuth pattern
            s = s + '{:3s}{:5s}'.format('', 'NOAZI')
            s = s + ''.join(['{:8.2f}'.format(val) for val in PCV[0]]) + '\n'
            
            if writePCV in ["ALL"]: 
                # Nous construisons maintenant toutes les lignes correspondant à chaque 
                # azimuth-dependent pattern
                if nrows > 1:
                    for row, azi in enumerate(np.arange(0,361,dazi)):
                        # nous constrisons un string de string # contruim un string din stringul existent la care adaugam
                        # la valeur de l'azimut écrit sur un champ de 8 caractères
                        # comme le nombre float avec une décimale +
                        # toutes les valeurs des variations pour cet azimut sur 
                        # 8 champs de colonne comme nombres flottants avec deux décimales +
                        # nouveau caractère de ligne
                        s = s + \
                            '{:8.1f}'.format(azi) + \
                            ''.join(['{:8.2f}'.format(val) for val in PCV[row+1]]) + \
                            '\n'

        # Dernière ligne
        s = s + '{:3s}{:3s}{:54s}{:20s}\n'.format('', self.FrequencyKey, '', 'END OF FREQUENCY')
        
        return '{}'.format(s);

        
        
        
        
        

if __name__ == "__main__":
    
    t1 = gps.gpsdatetime()
        

#    f = r'C:\Users\user\Desktop\Master PPMD\Projet informatique\Documentation_initialle\G03b\atx\anamaria.atx'
    f = 'antennes_gnss.atx'
#    f = r'new.atx'
    
#    print(f)
    atx = antex(f)
    
    print(atx)
    
    
    # ========== Tests pour la classe clasa Antex
    
##     test la function GetAntenna()
#    typ = 'ASH700936A_M    NONE'
#    Ant1 = atx.GetAntenna(antennaType=typ)
#    Ant1.PlotAntenna()
#    print(Ant1.__dict__)
#    print(type(Ant1))
#    print('\n')
    
    # test la function SelectMultipleAntennas()
    antenna_names = ['LEIAS10         NONE',
                     'LEIGS08         NONE',
                     'LEIGS08PLUS     NONE',
                     'LEIGS14         NONE',
                     'LEIGS16         NONE',
                     'LEIGS15         NONE']

    listOfAntennas = atx.SelectMultipleAntennas(antenna_names)
#    print(len(listOfAntennas))
#    print(listOfAntennas[-1])
#    print('\n')
##    
##    # test la function AddAntenna()
##    print('Avant:', atx)
##    atx.AddAntenna(Ant1)
##    print('Aprés   :', atx)
##    
    # test la function WriteAntex()
    atx.WriteAntex(filename='antennes_gnss_PCO.atx', writePCV = "NOAZI")
#    
#    
#    
#    # ========== Tests pour la clasa Antenna
#    # vous testez la function __str__()
#    listOfAntennas[-2].__str__()
#    print('\n')
    for ant in atx.Antennas:
        ant.__str__()
#    
#    
#    # test function RemoveAzimuthPattern() 
#    print('Avant:', len(Ant1.Frequencies['G01'].PCV) )
#    Ant1.RemoveAzimuthPattern()
#    print('Aprés  :', len(Ant1.Frequencies['G01'].PCV) )
#    atx.AddAntenna(Ant1)
#    atx.WriteAntex(filename='new_file.atx', listA=listOfAntennas)
#    print(atx)
#    
#    
    # test function PlotAntenna()
#    Ant1.PlotAntenna()
#    listOfAntennas[0].PlotAntenna()

    t2 = gps.gpsdatetime()
    print ('%.3f sec elapsed ' % (t2-t1))