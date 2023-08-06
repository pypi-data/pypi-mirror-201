from pySAXS.models.model import Model
from pySAXS.LS.LSsca import Qlogspace
from pySAXS.LS.LSsca import Pcylmulti
import numpy
import scipy.special
import time
# import time
from numba import jit

   
@jit(nopython=True)
def gs(x, A,x0,sigma):
        return A*numpy.exp(-(x - x0)**2 / (2*sigma**2))
@jit(nopython=True)
def convol(sigma,q,I):
          Tc = numpy.zeros(len(q))
          for i in range(len(q)):
              B = gs(q, 1.0, q[i], sigma)
              Tc[i] = Tc[i] + numpy.sum(B * I) / numpy.sum(B)
          return Tc

class ImogoliteSW(Model):
      '''

      class Imogolite SW 
      by AT 09/02/2011
      '''


      def ImogoliteSWFunction(self,q,par):
         
          """
          q array of q (A-1)
          par[0] Concentration en tubes/cm3
          par[1] Rayon interne
          par[2] Epaisseur de la paroi du tube
          par[3] Longueur du tube
          par[4] Nombre d'Atome de Si dans la circonference du tube 
          par[5] Nombre electron par motif
          par[6] Parametre de maille
          par[7] Densite electronique interne
          par[8] Densite electronique externe
          par[9] Distance entre tubes agreges
          par[10] Nombre de tubes isoles
          par[11] Nombre de tube par 2
          par[12] Nombre de tube par 3
          par[13] Nombre de tube par 4
          par[14] FMWH beam
          """
          start = time.time()

          "Definition des rayons"
          r=numpy.zeros(2)          
          r[0]=par[1]
          r[1]=r[0]+par[2]
          
          "Definition des densites electroniques"
          rho=numpy.zeros(3)
          rho[0]=par[7]
          rho[1]=(par[4]*par[5])/(numpy.pi*par[6]*(r[1]*r[1]-r[0]*r[0]))
          rho[2]=par[8]          
          print ('densite electronique paroi =', rho[1])       
          rho=rho*1e24*0.282e-12

          "Definition de la longueur"
          L = par[3]*10

          F2=Pcylmulti(self.q,r,rho,L,par[0])

          a=2.0*(r[0]+par[2])
          b=a+par[9]
          S2T=2.0*scipy.special.j0(self.q*b)+2.0
          S3T=6.0*scipy.special.j0(self.q*b)+3.0
          S4T=10.0*scipy.special.j0(self.q*b)+2.0*scipy.special.j0(self.q*b*numpy.sqrt(3.0))+4.0
          Sp=par[10]+par[11]+par[12]+par[13]
          p1=par[10]/Sp
          p2=par[11]/Sp
          p3=par[12]/Sp
          p4=par[13]/Sp
                    
          I = (p1+p2/2.0*S2T+p3/3*S3T+p4/4*S4T)*F2
          #print(time.time() - start)
          "Convolution par le faisceau"
          sigma=par[14]/2.3548
          '''Tc=numpy.zeros(len(q))
          for i in range(len(q)):
              B=gs(q,1.0,q[i],sigma)
              Tc[i]=Tc[i]+numpy.sum(B*I)/numpy.sum(B)'''
          Tc=convol(sigma,q,I)
          #print(time.time() - start)
          return Tc




      def __init__(self):
          Model.__init__(self)
          self.IntensityFunc=self.ImogoliteSWFunction
          self.q=Qlogspace(0.005,1.0,500)    #q range(x scale)
          self.Arg=[1.0e16,8.0,6.0,200.0,13.0,100.0,4.25,0.334,0.334,1.0,1.0,0.0,0.0,0.0,0.065]         #list of defaults parameters
          self.Format=["%1.3e","%.2f","%.2f","%.f","%.1f","%.1f","%.2f","%.3f","%.3f","%.1f","%.f","%.f","%.f","%.f","%.4f"]      #list of c format
          self.istofit=[True,True,False,False,False,False,False,False,False,False,False,False,False,False,False]    #list of boolean for fitting
          self.name="Specific: Imogolite Single Wall"          #name of the model
          self.Author="PP"
          self.Description = "Imogolite single wall"
          self.Doc=["Tube concencration (/cm3)",\
                  "Internal radius (A) ",\
                  "Wall thickness (A)",\
                  "Tube length (nm)",\
                  "Number of Si atom per ring",\
                  "Number of electron per structural unit",\
                  "Lattice parameter (A)",\
                  "Internal electronic density (e/A3)",\
                  "External electronic density (e/A3)",\
                  "Space between agreted tubes (A)",\
                  "Number of 1 tube",\
                  "Number of 2 tubes",\
                  "Number of 3 tubes",\
                  "Number of 4 tubes",\
                  "FMWH beam (cm)"] #list of description for parameters


# "Essais gofast"
# @jit(nopython=True)
# def gs(x, A,x0,sigma):
#         return A*numpy.exp(-(x - x0)**2 / (2*sigma**2))
    
# #@jit(["float64[:](float64[:],float64,float64,float64,float64,float64,float64,float64)"],nopython=True)
# @jit(nopython=True)
# def goFast(q,p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14):
#         """
#         q array of q (A-1)
#         par[0] Concentration en tubes/cm3
#         par[1] Rayon interne
#         par[2] Epaisseur de la paroi du tube
#         par[3] Longueur du tube
#         par[4] Nombre d'Atome de Si dans la circonference du tube 
#         par[5] Nombre electron par motif
#         par[6] Parametre de maille
#         par[7] Densite electronique interne
#         par[8] Densite electronique externe
#         par[9] Distance entre tubes agreges
#         par[10] Nombre de tubes isoles
#         par[11] Nombre de tube par 2
#         par[12] Nombre de tube par 3
#         par[13] Nombre de tube par 4
#         par[14] FMWH beam 
#         """

#         r=numpy.zeros(2)       
#         r[0]=p1
#         r[1]=r[0]+p2
        
#         rho=numpy.zeros(3)
#         rho[0]=p7
#         rho[1]=(p4*p5)/(numpy.pi*p6*(r[1]*r[1]-r[0]*r[0]))
#         rho[2]=p8        
#         print ('densite electronique paroi =', rho[1])     
#         rho=rho*1e24*0.282e-12
    
#         F2=Pcylmulti(q,r,rho,p3,p0)

#         a=2.0*(r[0]+p2)
#         b=a+p9
#         S2T=2.0*scipy.special.j0(q*b)+2.0
#         S3T=6.0*scipy.special.j0(q*b)+3.0
#         S4T=10.0*scipy.special.j0(q*b)+2.0*scipy.special.j0(q*b*numpy.sqrt(3.0))+4.0
#         Sp=p10+p11+p12+p13
#         p1=p10/Sp
#         p2=p11/Sp
#         p3=p12/Sp
#         p4=p13/Sp
                  
#         I = (p1+p2/2.0*S2T+p3/3*S3T+p4/4*S4T)*F2

#         "Convolution par le faisceau"
#         sigma=p14/2.3548
#         Tc=numpy.zeros(len(q))
#         for i in range(len(q)):
#             B=gs(q,1.0,q[i],sigma)
#             Tc[i]=Tc[i]+numpy.sum(B*I)/numpy.sum(B)
#         return Tc

        
# class ImogoliteSW(Model):      
#       '''
#       class Imogolite SW 
#       by AT 09/02/2011
#       '''
#       def ImogoliteSWFunction(self,q,par): 
#           start=time.time()
#           i=goFast(q,float(par[0]),float(par[1]),float(par[2]),float(par[3]),float(par[4]),float(par[5]),float(par[6]),float(par[7]),
#                    float(par[8]),float(par[9]),float(par[10]),float(par[11]),float(par[12]),float(par[13]),float(par[14]))
#           end = time.time()
#           print("Elapsed  = %s" % (end - start))
#           return i
    
#       def __init__(self):
#            Model.__init__(self)
#            self.IntensityFunc=self.ImogoliteSWFunction
#            self.N=0
#            self.q=Qlogspace(0.005,1.0,500)    #q range(x scale)
#            self.Arg=[5.0e15,9.0,6.0,600.0,16.0,100.0,4.3,0.11,0.334,1.0,1.0,1.0,1.0,1.0,0.065]         #list of defaults parameters
#            self.Format=["%1.3e","%.2f","%.2f","%.f","%.1f","%.1f","%.2f","%.3f","%.3f","%.1f","%.f","%.f","%.f","%.f","%.4f"]      #list of c format
#            self.istofit=[True,True,False,False,True,True,True,False,False,True,True,True,True,True,False]    #list of boolean for fitting
#            self.name="Specific: Imogolite Single Wall"          #name of the model
#            self.Author="Imogo team"
#            self.Description = "Imogolite single wall"
#            self.Doc=["Tube concencration (/cm3)",\
#                   "Internal radius (A) ",\
#                   "Wall thickness (A)",\
#                   "Tube length (A)",\
#                   "Number of Si atom per ring",\
#                   "Number of electron per structural unit",\
#                   "Lattice parameter (A)",\
#                   "Internal electronic density (e/A3)",\
#                   "External electronic density (e/A3)",\
#                   "Space between agreted tubes (A)",\
#                   "Number of 1 tube",\
#                   "Number of 2 tubes",\
#                   "Number of 3 tubes",\
#                   "Number of 4 tubes",\
#                   "FMWH beam (cm)"] #list of description for parameters
#            self.WarningForCalculationTime=False