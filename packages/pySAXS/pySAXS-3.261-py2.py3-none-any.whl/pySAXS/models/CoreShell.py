from pySAXS.models.model import Model
from pySAXS.LS.LSsca import Qlogspace
from pySAXS.LS.LSsca import *
import numpy

from pySAXS.LS.LSsca import getV
from pySAXS.LS.LSsca import F1

class CoreShell(Model):
    '''
    Core Shell Particle
    by OT 10/06/2009
    modified by PP 06/04/2023
    '''
    def CoreShellFunction(self,q,par):
        """
        q array of q            (Å-1)
        par[0] Core radius      (Å)
        par[1] Shell Radius     (Å)
        par[2] SLD of core      (cm-2)
        par[3] SLD of shell     (cm-2)
        par[4] SLD of solvent   (cm-2)
        par[5] Number density   (cm-3)
        par[6] Background       (cm-1)
        """
        return par[6]+par[5]*((getV(par[0])*1e-24*(par[2]-par[3])*F1(q,par[0])+getV(par[1])*1e-24*(par[3]-par[4])*F1(q,par[1]))**2.0)


    def __init__(self):
        Model.__init__(self)
        self.IntensityFunc=self.CoreShellFunction #function
        self.N=0
        self.q=Qlogspace(1.0e-4,2.0,1000.)      #q range(x scale)
        self.Arg=[75.0,100.0,9.42e10,2.26e11,9.42e10,1.0e15,1.0e-4]         #list of defaults parameters
        self.Format=["%f","%f","%1.3e","%1.3e","%1.3e","%1.3e","%1.3e"]      #list of c format
        self.istofit=[True,True,True,False,False,False,False]    #list of boolean for fitting
        self.name="Core Shell Particle"          #name of the model
        self.category="spheres"
        self.Doc=["Core radius (Å)",\
                  "Shell radius (Å)",\
                  "SLD core (cm-2)",\
                  "SLD shell (cm-2)",\
                  "SLD solvent (cm-2)",\
                  "Number density (/cm-3)",\
                  "Background (cm-1)"] #list of description for parameters


'''

class CoreShell(Model):
    
    Core Shell Particle
    by OT 10/06/2009
    
    def CoreShellFunction(self,q,par):
        """
        q array of q (A-1)
        par[0] Outer radius
        par[1] Inner Radius
        par[2] SLD of Shell
        par[3] SLD of Core
        par[4] Number density(cm-3)
        """
        R=[par[0],par[1]]
        rho=[par[2],par[3]]
        return (par[2]**2.)*par[4]*getV(par[0])*getV(par[0])*1e-48*P3(q,R,rho)[0]
            
    
    parameters definition
    Model(5,CoreShell,Qlogspace(1e-4,1.,500.),
    ([100.,75.,2e11,1e10,1.e16]),
    ("Outer Radius (A)","Inner radius (A)","SLD shell (cm-2)","SLD Core (cm-2)","Number density (cm-3)"),
    ("%f","%f","%1.3e","%1.3e","%1.3e"),(True,True,True,False,False)),
    
    from LSsca
    
    def __init__(self):
        Model.__init__(self)
        self.IntensityFunc=self.CoreShellFunction #function
        self.N=0
        self.q=Qlogspace(1e-4,1.,500.)      #q range(x scale)
        self.Arg=[100.,75.,2e11,1e10,1.e16]         #list of defaults parameters
        self.Format=["%f","%f","%1.3e","%1.3e","%1.3e"]      #list of c format
        self.istofit=[True,True,True,False,False]    #list of boolean for fitting
        self.name="Core Shell Particle"          #name of the model
        self.Doc=["Outer Radius (A)"\
             ,"Inner radius (A)","SLD shell (cm-2)",\
             "SLD Core (cm-2)","Number density (cm-3)"] #list of description for parameters
    
'''
